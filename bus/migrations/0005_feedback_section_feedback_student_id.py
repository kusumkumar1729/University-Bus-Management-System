# Generated by Django 5.1.2 on 2024-10-28 19:53

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("bus", "0004_remove_feedback_condition_feedback_buscondition_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="feedback",
            name="section",
            field=models.CharField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="feedback",
            name="student_id",
            field=models.CharField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]