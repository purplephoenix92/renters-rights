# Generated by Django 2.2.4 on 2019-08-29 01:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("units", "0009_unit_landlord_name")]

    operations = [
        migrations.AlterField(
            model_name="unitimage",
            name="image_type",
            field=models.CharField(
                choices=[("D", "Document"), ("P", "Move In Picture"), ("P", "Move Out Picture")], default="D", max_length=3
            ),
        )
    ]
