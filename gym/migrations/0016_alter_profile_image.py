# Generated by Django 5.0 on 2024-01-05 17:42

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("gym", "0015_profile"),
    ]

    operations = [
        migrations.AlterField(
            model_name="profile",
            name="image",
            field=models.ImageField(default="default.jpg", upload_to="images"),
        ),
    ]
