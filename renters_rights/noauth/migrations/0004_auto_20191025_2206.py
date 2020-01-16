# Generated by Django 2.2.6 on 2019-10-25 22:06

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("noauth", "0003_authcode_previous_emails")]

    operations = [
        migrations.RemoveField(model_name="authcode", name="previous_emails"),
        migrations.AddField(
            model_name="user",
            name="previous_emails",
            field=django.contrib.postgres.fields.ArrayField(
                base_field=models.EmailField(max_length=254), default=[], size=None
            ),
        ),
    ]