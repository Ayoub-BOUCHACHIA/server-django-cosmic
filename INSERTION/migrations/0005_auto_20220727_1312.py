# Generated by Django 3.0.6 on 2022-07-27 12:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('INSERTION', '0004_auto_20220727_1311'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cosmic_measurement',
            name='PATH_FILE_UR_IN_SERVER',
            field=models.FileField(null=True, upload_to='media'),
        ),
    ]
