from tale.tale import runPipeline, runEntityExtraction
import os
from django.http import HttpResponse, JsonResponse
import json
from django.shortcuts import render
from .forms import CalculationForm, UploadFileForm
from tale_web.settings import MEDIA_ROOT
import zipfile
from .models import UploadFile


OUTPUT_DIR = os.path.join(MEDIA_ROOT, 'outputs')
# Create a ZIP archive with the selected files
ZIP_FILE_PATH = os.path.join(MEDIA_ROOT, 'zips', 'ouput.zip')  # Define the path for the ZIP file


def front_page(request):
    return render(request, 'front_page.html')

def serve_dynamic_image(request, output_folder, image_name):
    # Construct the path to the image based on the output_folder provided
    image_path = os.path.join(OUTPUT_DIR, output_folder, image_name)

    try:
        with open(image_path, 'rb') as img_file:
            return HttpResponse(img_file.read(), content_type='image/png')  # Adjust content_type based on your image type
    except FileNotFoundError:
        # Handle case when image is not found
        return HttpResponse('Image not found', status=404)

def render_html_file(request, output_folder):
    if request.method == 'POST':
        # Perform the logic to retrieve the HTML file based on output_folder from the POST request or any other method
        html_file_path = os.path.join(OUTPUT_DIR, output_folder, 'output.html') 
        with open(html_file_path, 'r') as html_file:
            file_content = html_file.read()
        return HttpResponse(file_content, content_type='text/html')
    else:
        return HttpResponse("Invalid request")

def display_output(request):
    # get all the folders in the output directory
    folders = [folder for folder in os.listdir(OUTPUT_DIR) if os.path.isdir(os.path.join(OUTPUT_DIR, folder))]
    context = {'folders': folders}
    return render(request, 'display_outputs.html', context)

def show_list_of_files2process(request):
    # Shows a list of uploaded files
    uploaded_files = UploadFile.objects.all()
    context = {'uploaded_files': uploaded_files}
    return render(request, 'file_process.html', context)


def getContext(request, file_id):
    # Retrieve the selected file based on file_id
    selected_file = UploadFile.objects.get(id=file_id)
    
    # run the entity extraction pipeline on uploaded file
    runEntityExtraction(selected_file.file.path)
    
    return render(request, 'file_process.html')  # Display a success page or redirect elsewhere

def process_file(request, file_id):
    # Retrieve the selected file based on file_id
    selected_file = UploadFile.objects.get(id=file_id)

    # Assuming the script takes the input file and generates an output file
    input_file_path = selected_file.file.path  # Path to the selected input file
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # run the tale pipeline on uploaded file     
    runPipeline(input_file_path)

    return render(request, 'processing_success.html')  # Display a success page or redirect elsewhere


def download_all_outputs(request):

    # Create a ZIP file containing all files in the output directory
    with zipfile.ZipFile(ZIP_FILE_PATH, 'w') as zipf:
        for root, dirs, files in os.walk(OUTPUT_DIR):
            for file in files:
                file_path = os.path.join(root, file)
                zipf.write(file_path, arcname=os.path.relpath(file_path, OUTPUT_DIR))

    # Prepare the ZIP file for download
    with open(ZIP_FILE_PATH, 'rb') as zip_file:
        response = HttpResponse(zip_file.read(), content_type='application/zip')
        response['Content-Disposition'] = 'attachment; filename="all_outputs.zip"'

    # Delete the temporary ZIP file after generating the response
    os.remove(ZIP_FILE_PATH)

    return response


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



        with zipfile.ZipFile(ZIP_FILE_PATH, 'w') as zipf:
            for file in selected_files:
                file_path = os.path.join(MEDIA_ROOT, 'uploads', str(file.file))
                zipf.write(file_path, arcname=os.path.basename(file.file.name))

        # Prepare the ZIP file for download
        with open(ZIP_FILE_PATH, 'rb') as zip_file:
            response = HttpResponse(zip_file.read(), content_type='application/zip')
            response['Content-Disposition'] = 'attachment; filename="selected_files.zip"'
        os.remove(ZIP_FILE_PATH)

        return response
    return render(request, 'download_page.html', {'files': UploadFile.objects.all()})

def edit_context(request):
    
    return render(request, 'edit_context.html')


def json_data_view(request):
    """Return the context.json file as a JSON response
    """
    with open(os.path.join("media", "uploads", "context.json")) as json_file:
        data = json.load(json_file)
    return JsonResponse(data)


def index(request):
    return HttpResponse("Hello, this is a minimal Django server!")