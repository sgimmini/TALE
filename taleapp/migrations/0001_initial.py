# Generated by Django 4.2.7 on 2023-12-03 17:39

import django.core.files.storage
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UploadFile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(storage=django.core.files.storage.FileSystemStorage(location='/Users/levinkobelke/TALE/tale_web/media/uploads'), upload_to='uploads')),
            ],
        ),
    ]
