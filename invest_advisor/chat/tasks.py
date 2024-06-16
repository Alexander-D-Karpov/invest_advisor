import json
from ast import literal_eval
from contextlib import contextmanager

import requests
from celery import shared_task
from django.conf import settings
from django.core.cache import cache

from invest_advisor.chat.api.serializers import (
    TechnoparkSubmissionSerializer,
    BuildingSubmissionSerializer,
    TechnoparkTableDataSerializer,
    BuildingTableDataSerializer,
)
from invest_advisor.chat.models import (
    TechnoparkSubmission,
    BuildingSubmission,
    Chat,
    ChatMessage,
    Technopark,
    BuildingModel,
)
from invest_advisor.chat.services import (
    filter_technoparks,
    filter_buildings,
    generate_report_file,
)


@contextmanager
def redis_lock(lock_id, timeout=60):
    """Attempt to acquire a lock by the given ID and hold it for the timeout duration."""
    status = cache.add(lock_id, "true", timeout)
    try:
        yield status
    finally:
        if status:
            cache.delete(lock_id)


def send_technopark(submission: TechnoparkSubmission):
    data = {
        "user_data": (
            json.dumps(submission.user.company_info)
            if submission.user and submission.user.company_info
            else ""
        ),
        "names": [x.name for x in filter_technoparks(submission)],
        "uuid": str(submission.id),
        "additional_filters": json.dumps(
            TechnoparkSubmissionSerializer(submission).data
        ),
    }
    r = requests.post(settings.ML_HOST + "/conversation", json=data, timeout=60)
    if r.status_code != 200:
        raise Exception(f"Failed to send data to ML: {r.text}")
    data = r.json()
    submission.ml_data = data
    submission.save()
    try:
        c = Chat.objects.get(id=submission.id)
    except Chat.DoesNotExist:
        c = Chat.objects.create(
            type="technopark",
            id=submission.id,
            name=submission.name,
            user=submission.user,
        )
    try:
        places = data["places"]
        technoparks = Technopark.objects.filter(name__in=places)
    except Exception as e:
        print(f"Failed to get technoparks: {e}")
        technoparks = []
    try:
        ChatMessage.objects.create(
            chat=c,
            from_user=False,
            text=data["messages"][0]["text"],
            data=TechnoparkTableDataSerializer(technoparks, many=True).data,
        )
    except Exception as e:
        print(f"Failed to create chat message: {e}")


def send_building(submission: BuildingSubmission):
    data = {
        "user_data": (
            json.dumps(submission.user.company_info)
            if submission.user and submission.user.company_info
            else ""
        ),
        "names": [x.name for x in filter_buildings(submission)],
        "uuid": str(submission.id),
        "additional_filters": json.dumps(BuildingSubmissionSerializer(submission).data),
    }
    r = requests.post(settings.ML_HOST + "/conversation", json=data, timeout=60)
    if r.status_code != 200:
        raise Exception(f"Failed to send data to ML: {r.text}")
    data = r.json()
    submission.ml_data = data
    submission.save()
    try:
        c = Chat.objects.get(id=submission.id)
    except Chat.DoesNotExist:
        c = Chat.objects.create(
            type="building",
            id=submission.id,
            name=submission.name,
            user=submission.user,
        )
    try:
        places = data["places"]
        buildings = BuildingModel.objects.filter(name__in=places)
    except Exception as e:
        print(f"Failed to get buildings: {e}")
        buildings = []

    try:
        ChatMessage.objects.create(
            chat=c,
            from_user=False,
            text=data["messages"][0]["text"],
            data=BuildingTableDataSerializer(buildings, many=True).data,
        )
    except Exception as e:
        print(f"Failed to create chat message: {e}")


def send_message(message: ChatMessage):
    data = {
        "message": message.text,
    }
    r = requests.post(
        settings.ML_HOST + "/conversation/" + str(message.chat.id),
        json=data,
        timeout=60,
    )
    if r.status_code != 200:
        raise Exception(f"Failed to send data to ML: {r.text}")
    data = r.json()
    print(data)
    try:
        ChatMessage.objects.create(
            chat=message.chat,
            from_user=False,
            text=data["messages"][-1]["text"],
        )
    except Exception as e:
        print(f"Failed to create chat message: {e}")


def generate_place_report(chat, place):
    user_data = chat.user.company_info if chat.user and chat.user.company_info else ""
    data = {
        "user_data": json.dumps(user_data),
        "place_name": place,
    }
    r = requests.post(
        settings.ML_HOST + "/places/advice_and_support", json=data, timeout=60
    )
    if r.status_code != 200:
        raise Exception(f"Failed to send data to ML: {r.text}")
    data = r.json()
    generate_report(chat.id, data["advice"], data["support"], place)
    return


def generate_chat_name(submission, chat):
    data = {
        "place_names": submission.ml_data["places"],
    }
    r = requests.post(settings.ML_HOST + "/generate_name", json=data, timeout=60)
    if r.status_code != 200:
        raise Exception(f"Failed to send data to ML: {r.text}")
    name = literal_eval(r.text).strip('"').replace("\\n", "").strip()
    chat.name = name
    chat.save()
    submission.name = name
    submission.save()


def generate_report(chat_id, advise, support, place):
    chat = Chat.objects.get(id=chat_id)
    message = ChatMessage.objects.create(chat=chat, from_user=False, text=place)
    generate_report_file(message, support, advise)


@shared_task(bind=True, ignore_result=True)
def send_data_to_ml(self, type: str, obj_id, extra_data: dict = None):
    lock_id = "ml_lock"
    with redis_lock(lock_id, timeout=60) as acquired:
        if acquired:
            print(f"Lock acquired. Executing task {type}, {self.request.id}")
            if type == "technopark":
                submission = TechnoparkSubmission.objects.get(id=obj_id)
                send_technopark(submission)
                send_data_to_ml.apply_async(
                    kwargs={"type": "name", "obj_id": submission.id}, countdown=1
                )
            elif type == "building":
                submission = BuildingSubmission.objects.get(id=obj_id)
                send_building(submission)
                send_data_to_ml.apply_async(
                    kwargs={"type": "name", "obj_id": submission.id}, countdown=1
                )
            elif type == "message":
                message = ChatMessage.objects.get(id=obj_id)
                send_message(message)
            elif type == "file":
                chat = Chat.objects.get(id=obj_id)
                place = extra_data["name"]
                generate_place_report(chat, place)
            elif type == "name":
                chat = Chat.objects.get(id=obj_id)
                if chat.type == "technopark":
                    submission = TechnoparkSubmission.objects.get(id=obj_id)
                elif chat.type == "building":
                    submission = BuildingSubmission.objects.get(id=obj_id)
                generate_chat_name(submission, chat)
            print(f"Task {type}, {self.request.id} executed.")
        else:
            print(f"Task {type} skipped, lock not acquired.")
