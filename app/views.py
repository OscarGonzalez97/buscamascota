from django.shortcuts import render
from django.http import HttpResponse
from app.constants import REPORT_TYPE, SPECIE
from app.forms import ReportForm

def index(request):
    return render(request,'index.html')

def colaborate(request):
    return render(request,'colaborar.html')

def terms(request):
    return render(request,'terminos.html')

def map(request):
    context={
        'report_type':REPORT_TYPE,
        'specie': SPECIE
    }
    return render(request,'map.html', context)

def publish(request):
    msg = ''
    registration_error = -1
    created = False
    form = ReportForm(request.POST or None)
    
    #if request.method == "POST":

    context = {
        'form': form,
        'messages': msg,
    }
    return render(request,'publicar.html', context)