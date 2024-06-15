from celery import shared_task
from dadata import Dadata
from django.conf import settings

from invest_advisor.users.models import Company, User


@shared_task
def retrieve_company_info(user_id):
    user = User.objects.get(id=user_id)
    if len(user.tax_number) not in [10, 12]:
        print("Tax number must be 10 or 12 digits")
        return
    try:
        int(user.tax_number)
    except ValueError:
        print("Tax number must be a number")
        return
    if Company.objects.filter(tax_number=user.tax_number).exists():
        user.company_info = (
            Company.objects.filter(tax_number=user.tax_number).first().data
        )
        user.save()
    else:
        with Dadata(settings.DADATA_API_KEY, settings.DADATA_SECRET_KEY) as dadata:
            result = dadata.find_by_id("party", user.tax_number)
            if result:
                company = Company(tax_number=user.tax_number, data=result)
                company.save()
                user.company_info = result
                user.save()
            else:
                company = Company(tax_number=user.tax_number, data={})
                company.save()
                print("Company not found")
                return
