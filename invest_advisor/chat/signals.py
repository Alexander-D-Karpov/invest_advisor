from django.db.models.signals import post_save
from django.dispatch import receiver

from invest_advisor.chat.models import BuildingSubmission, Chat, TechnoparkSubmission


@receiver(post_save, sender=TechnoparkSubmission)
@receiver(post_save, sender=BuildingSubmission)
def create_chat_submission(sender, instance, created, **kwargs):
    if created:
        Chat.objects.create(
            type="technopark" if sender is TechnoparkSubmission else "building",
            id=instance.id,
            name=instance.name,
            user=instance.user,
        )
