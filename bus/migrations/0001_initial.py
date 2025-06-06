# Generated by Django 5.1.2 on 2024-10-25 23:12

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="BusApplication",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("full_name", models.CharField(max_length=100)),
                ("student_id", models.CharField(max_length=20)),
                ("contact_number", models.CharField(max_length=15)),
                ("email", models.EmailField(max_length=254)),
                ("route", models.CharField(max_length=50)),
                ("bus_stop", models.CharField(max_length=100)),
                ("section", models.CharField(max_length=100)),
                ("created_at", models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name="BusInfo",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100)),
                ("routes", models.TextField()),
                ("morning_start_time", models.TimeField()),
                ("college_start_time", models.TimeField()),
                ("description", models.TextField(blank=True, null=True)),
                ("image", models.ImageField(blank=True, null=True, upload_to="media")),
            ],
        ),
        migrations.CreateModel(
            name="BusVacancy",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("bus_name", models.CharField(max_length=100)),
                ("total_seats", models.IntegerField(default=50)),
                ("occupied_seats", models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name="Note",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("image", models.ImageField(blank=True, null=True, upload_to="media")),
                ("note", models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name="Payment",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("student", models.CharField(max_length=20)),
                ("amount", models.DecimalField(decimal_places=2, max_digits=10)),
                ("transaction_id", models.CharField(max_length=100, unique=True)),
                ("status", models.CharField(max_length=20)),
                ("payment_method", models.CharField(max_length=50)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name="Student",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("student_id", models.CharField(max_length=20, unique=True)),
                ("full_name", models.CharField(max_length=100)),
                ("course", models.CharField(max_length=100)),
                ("year", models.IntegerField()),
                ("image", models.ImageField(blank=True, null=True, upload_to="media")),
                (
                    "first_year_fee",
                    models.DecimalField(decimal_places=2, default=35000, max_digits=10),
                ),
                (
                    "second_year_fee",
                    models.DecimalField(decimal_places=2, default=35000, max_digits=10),
                ),
                (
                    "third_year_fee",
                    models.DecimalField(decimal_places=2, default=35000, max_digits=10),
                ),
                (
                    "fourth_year_fee",
                    models.DecimalField(decimal_places=2, default=35000, max_digits=10),
                ),
                (
                    "paid_amount_first_year",
                    models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
                ),
                (
                    "paid_amount_second_year",
                    models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
                ),
                (
                    "paid_amount_third_year",
                    models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
                ),
                (
                    "paid_amount_fourth_year",
                    models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
                ),
            ],
        ),
        migrations.CreateModel(
            name="StudentLogin",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("password", models.CharField(default="webcap", max_length=50)),
                (
                    "student",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE, to="bus.student"
                    ),
                ),
            ],
        ),
    ]
