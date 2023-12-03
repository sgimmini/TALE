from django.db import models
from django.core.files.storage import FileSystemStorage
from tale_web.settings import MEDIA_ROOT
import os
# Create your models here.


UPLOAD_STORAGE = FileSystemStorage(location=os.path.join(MEDIA_ROOT, 'uploads'))

class UploadFile(models.Model):
    file = models.FileField(storage=UPLOAD_STORAGE, upload_to='')
    class Meta:
        app_label = 'taleapp'