# Generated by Django 3.0.6 on 2022-07-27 12:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('INSERTION', '0008_remove_cosmic_measurement_path_file_ur_in_server'),
    ]

    operations = [
        migrations.AddField(
            model_name='cosmic_measurement',
            name='PATH_FILE_UR_IN_SERVER',
            field=models.FileField(blank=True, default=None, null=True, upload_to='media'),
        ),
    ]
