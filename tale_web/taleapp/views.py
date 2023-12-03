import os
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .forms import CalculationForm, UploadFileForm
from tale_web.settings import MEDIA_ROOT
import zipfile
from .models import UploadFile

def front_page(request):
    return render(request, 'front_page.html')

def calculation_view(request):
    if request.method == 'POST':
        form = CalculationForm(request.POST)
        if form.is_valid():
            number1 = form.cleaned_data['number1']
            number2 = form.cleaned_data['number2']
            result = number1 + number2
            return render(request, 'calculation.html', {'form': form, 'result': result})

    else:
        form = CalculationForm()
    return render(request, 'calculation.html', {'form': form})

def upload_file_view(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            # Save the uploaded file instance to the database
            uploaded_file = form.save()
            return render(request, 'upload_success.html')  # Redirect to success page or any other action
    else:
        form = UploadFileForm()
    return render(request, 'upload_file.html', {'form': form})

def download_selected_files(request):
    if request.method == 'POST':
        selected_files_ids = request.POST.getlist('selected_files')
        selected_files = UploadFile.objects.filter(id__in=selected_files_ids)

        # Create a ZIP archive with the selected files
        zip_file_path = os.path.join(MEDIA_ROOT, 'zips', 'ouput.zip')  # Define the path for the ZIP file

        with zipfile.ZipFile(zip_file_path, 'w') as zipf:
            for file in selected_files:
                file_path = os.path.join(MEDIA_ROOT, 'uploads', str(file.file))
                zipf.write(file_path, arcname=os.path.basename(file.file.name))

        # Prepare the ZIP file for download
        with open(zip_file_path, 'rb') as zip_file:
            response = HttpResponse(zip_file.read(), content_type='application/zip')
            response['Content-Disposition'] = 'attachment; filename="selected_files.zip"'

        return response
    return render(request, 'download_page.html', {'files': UploadFile.objects.all()})

def index(request):
    return HttpResponse("Hello, this is a minimal Django server!")
