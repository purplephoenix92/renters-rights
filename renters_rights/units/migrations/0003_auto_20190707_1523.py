# Generated by Django 2.2.3 on 2019-07-07 15:23

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("units", "0002_auto_20190707_0228"),
    ]

    operations = [
        migrations.RemoveField(model_name="unit", name="deleted_at"),
        migrations.AddField(
            model_name="unitimage",
            name="owner",
            field=models.ForeignKey(
                default=4,
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
            ),
            preserve_default=False,
        ),
    ]
