# Generated by Django 4.2.7 on 2023-12-06 16:04

import django.core.files.storage
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('taleapp', '0003_alter_uploadfile_file'),
    ]

    operations = [
        migrations.AlterField(
            model_name='uploadfile',
            name='file',
            field=models.FileField(storage=django.core.files.storage.FileSystemStorage(location='C:\\Users\\fraul\\Documents\\GitHub\\TALE\\tale\\tale_web\\media\\uploads'), upload_to=''),
        ),
    ]
