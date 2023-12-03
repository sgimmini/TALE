from django.http import HttpResponse
from django.shortcuts import render
from .forms import CalculationForm


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

def index(request):
    return HttpResponse("Hello, this is a minimal Django server!")
