# Generated by Django 2.2.5 on 2019-10-03 01:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("units", "0010_auto_20190829_0159")]

    operations = [
        migrations.AddField(
            model_name="unit",
            name="landlord_email",
            field=models.EmailField(blank=True, max_length=254, verbose_name="Landlord Email"),
        ),
        migrations.AlterField(
            model_name="unitimage",
            name="image_type",
            field=models.CharField(
                choices=[("D", "Document"), ("MIP", "Move In Picture"), ("MOP", "Move Out Picture")], default="D", max_length=3
            ),
        ),
    ]