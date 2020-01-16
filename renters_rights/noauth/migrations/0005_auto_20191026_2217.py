# Generated by Django 2.2.6 on 2019-10-26 22:17

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("noauth", "0004_auto_20191025_2206")]

    operations = [
        migrations.AddField(
            model_name="user", name="pending_code", field=models.CharField(blank=True, editable=False, max_length=20, null=True)
        ),
        migrations.AddField(
            model_name="user", name="pending_code_timestamp", field=models.DateTimeField(blank=True, editable=False, null=True)
        ),
        migrations.AddField(
            model_name="user", name="pending_new_email", field=models.EmailField(blank=True, max_length=254, null=True)
        ),
        migrations.AlterField(
            model_name="user",
            name="previous_emails",
            field=django.contrib.postgres.fields.ArrayField(
                base_field=models.EmailField(max_length=254), default=list, size=None
            ),
        ),
    ]