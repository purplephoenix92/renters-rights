# Generated by Django 2.2.5 on 2019-10-03 01:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("noauth", "0001_initial")]

    operations = [
        migrations.AlterField(model_name="authcode", name="next_page", field=models.TextField(default="/", editable=False))
    ]