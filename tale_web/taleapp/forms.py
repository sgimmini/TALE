import os
from django import forms
from django.core.files.storage import FileSystemStorage
from .models import UploadFile

from tale_web.settings import MEDIA_ROOT

UPLOAD_STORAGE = FileSystemStorage(location=os.path.join(MEDIA_ROOT, 'uploads'))


class CalculationForm(forms.Form):
    number1 = forms.IntegerField(label='Number 1')
    number2 = forms.IntegerField(label='Number 2')

class UploadFileForm(forms.ModelForm):
    class Meta:
        model = UploadFile
        fields = ['file']
        widgets = {'file': forms.FileInput(attrs={'accept': '.txt'})}

    def clean_file(self):
        uploaded_file = self.cleaned_data['file']
        if not uploaded_file.name.endswith('.txt'):
            raise forms.ValidationError('Only .txt files are allowed.')
        return uploaded_file