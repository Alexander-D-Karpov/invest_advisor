# Generated by Django 4.2.13 on 2024-06-16 11:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("chat", "0013_chatmessage_file"),
    ]

    operations = [
        migrations.AddField(
            model_name="chatmessage",
            name="data",
            field=models.JSONField(blank=True, null=True, verbose_name="Данные"),
        ),
    ]
