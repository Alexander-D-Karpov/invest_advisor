import json
from contextlib import contextmanager

import requests
from celery import shared_task
from django.conf import settings
from django.core.cache import cache

from invest_advisor.chat.api.serializers import (
    TechnoparkSubmissionSerializer,
    BuildingSubmissionSerializer,
)
from invest_advisor.chat.models import (
    TechnoparkSubmission,
    BuildingSubmission,
    Chat,
    ChatMessage,
)
from invest_advisor.chat.services import filter_technoparks, filter_buildings


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
        "additional_filters": json.dumps(TechnoparkSubmissionSerializer(submission).data),
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
        ChatMessage.objects.create(
            chat=c,
            from_user=False,
            text=data["messages"][0]["text"],
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
        ChatMessage.objects.create(
            chat=c,
            from_user=False,
            text=data["messages"][0]["text"],
        )
    except Exception as e:
        print(f"Failed to create chat message: {e}")


def send_message(message: ChatMessage):
    data = {
        "message": message.text,
    }
    r = requests.post(settings.ML_HOST + "/conversation/" + str(message.chat.id), json=data, timeout=60)
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


@shared_task(bind=True, ignore_result=True)
def send_data_to_ml(self, type: str, obj_id, extra_data: dict = None):
    lock_id = "ml_lock"
    with redis_lock(lock_id, timeout=60) as acquired:
        if acquired:
            print(f"Lock acquired. Executing task {type}, {self.request.id}")
            if type == "technopark":
                submission = TechnoparkSubmission.objects.get(id=obj_id)
                send_technopark(submission)
            elif type == "building":
                submission = BuildingSubmission.objects.get(id=obj_id)
                send_building(submission)
            elif type == "message":
                message = ChatMessage.objects.get(id=obj_id)
                send_message(message)
            print(f"Task {type}, {self.request.id} executed.")
        else:
            print(f"Task {type} skipped, lock not acquired.")
