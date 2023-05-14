# Generated by Django 4.2 on 2023-05-09 14:26

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ("bms", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="book",
            name="id",
            field=models.UUIDField(
                default=uuid.UUID("6e1825ab-a2ca-4855-b8d3-929f3146cf4c"),
                primary_key=True,
                serialize=False,
            ),
        ),
        migrations.AlterField(
            model_name="book",
            name="payload",
            field=models.FileField(blank=True, upload_to="books/"),
        ),
    ]
