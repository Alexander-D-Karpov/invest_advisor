from django.contrib import admin

from invest_advisor.chat.models import BuildingModel, Technopark, TechnoparkSubmission

admin.site.register(Technopark)
admin.site.register(TechnoparkSubmission)
admin.site.register(BuildingModel)
