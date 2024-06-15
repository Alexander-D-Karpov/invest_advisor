from django.db.models.signals import post_save
from django.dispatch import receiver

from invest_advisor.users.models import User
from invest_advisor.users.tasks import retrieve_company_info


@receiver(post_save, sender=User)
def user_post_save(sender, instance, created, **kwargs):
    if created:
        retrieve_company_info.apply_async(kwargs={"user_id": instance.id}, countdown=5)
