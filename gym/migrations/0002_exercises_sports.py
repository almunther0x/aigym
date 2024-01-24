# Generated by Django 5.0 on 2023-12-29 19:28

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("gym", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Exercises",
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
                ("date", models.DateField(max_length=100)),
                ("counts", models.CharField(max_length=255)),
                ("time", models.TimeField()),
            ],
        ),
        migrations.CreateModel(
            name="Sports",
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
                ("video", models.TextField()),
                ("title", models.TextField()),
                ("about", models.TextField()),
                ("link", models.TextField()),
            ],
        ),
    ]
