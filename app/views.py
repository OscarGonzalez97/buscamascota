from django.shortcuts import render
from django.http import HttpResponse
from app.constants import REPORT_TYPE, SPECIE

# Create your views here.
def index(request):
    return render(request,'index.html')

def colaborate(request):
    return render(request,'colaborar.html')

def map(request):
    context={
        'report_type':REPORT_TYPE,
        'specie': SPECIE
    }
    return render(request,'map.html', context)

def publish(request):
    return render(request,'publicar.html')