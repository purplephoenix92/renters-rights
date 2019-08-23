# Generated by Django 2.2.3 on 2019-08-20 22:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("documents", "0002_auto_20190815_0033")]

    operations = [
        migrations.AlterField(
            model_name="documenttemplate",
            name="body",
            field=models.TextField(
                help_text="Template to be rendered using Django template engine. The template will receive a User object named user, a Unit object named unit, and any fields that are related to this template."
            ),
        )
    ]