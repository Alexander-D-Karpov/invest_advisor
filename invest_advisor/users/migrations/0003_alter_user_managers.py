# Generated by Django 4.2.13 on 2024-06-15 09:06

from django.db import migrations
import invest_advisor.users.models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0002_company_user_city_user_company_info_user_country_and_more"),
    ]

    operations = [
        migrations.AlterModelManagers(
            name="user",
            managers=[
                ("objects", invest_advisor.users.models.UserManager()),
            ],
        ),
    ]
