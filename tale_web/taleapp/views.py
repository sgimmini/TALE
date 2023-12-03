from django.http import HttpResponse
from django.shortcuts import render
from .forms import CalculationForm, UploadFileForm
from tale_web.settings import MEDIA_ROOT


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

def index(request):
    return HttpResponse("Hello, this is a minimal Django server!")
