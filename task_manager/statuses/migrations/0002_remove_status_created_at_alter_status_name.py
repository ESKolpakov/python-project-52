# Generated by Django 5.2 on 2025-04-11 17:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("statuses", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="status",
            name="created_at",
        ),
        migrations.AlterField(
            model_name="status",
            name="name",
            field=models.CharField(max_length=100),
        ),
    ]
