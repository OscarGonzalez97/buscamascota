from django.shortcuts import render, redirect
from django.http import HttpResponse
from app.constants import REPORT_TYPE, SPECIE
from app.forms import ReportForm, ReportSucessForm
from app.utils import tweet
from app.models import BlackList, Report, ReportImage
from django.contrib import messages
import sys


def index(request):
    return render(request,'index.html')

def colaborate(request):
    return render(request,'colaborar.html')

def terms(request):
    return render(request,'terminos.html')

def license(request):
    return render(request,'licencia.html')

def map(request):
    context={
        'report_type':REPORT_TYPE,
        'specie': SPECIE
    }
    return render(request,'map.html', context)

def publish(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = ReportForm(request.POST, request.FILES)
        # check whether it's valid:
        if form.is_valid():
            if form.cleaned_data['latitude'] and form.cleaned_data['longitude']:
                instance = form.save(commit=False)
                instance.who_sent = request.META['REMOTE_ADDR']
                #check if the ip exists in Blacklist table           
                if not BlackList.objects.filter(ip=instance.who_sent).exists():
                    instance.save()
                    report_id = str(instance.id)
                    #redirect to another view where is the report id
                    return redirect('success', report_id=report_id)
                else:
                   messages.error(request, "La IP se encuentra baneada debido a una publicación realizada. Póngase en contacto con el administrador del sitio.")
            else:
                messages.error(request, "Es necesario una ubicación, por favor marque un punto en el mapa")
        else:
            messages.error(request, "Por favor verifique los datos del formulario")
    else:
        form = ReportForm()
        
    context = {'form': form}

    return render(request, 'publicar.html', context)

def success(request, report_id):
    report_type = age = 0

    specie = image = description =  last_time_seen = ubication_resume = name = phone = sex = url = ''

    reportImageExist = ReportImage.objects.filter(report_id=report_id).exists()

    form = ReportSucessForm()

    
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = ReportSucessForm(request.POST, request.FILE)
        # check whether it's valid:
        if form.is_valid():
            form.save()
            reportImageExist = True
            print('I save the report image!')

        
    try:
        report = Report.objects.get(id=report_id, allowed=True)

        if report.specie == 'otro':
            specie = 'animal'
        else:
            specie = report.specie
        
        report_type = report.report_type
        image = report.picture.url
        description = report.description
        age = report.age
        last_time_seen = report.last_time_seen
        ubication_resume = report.ubication_resume
        name = report.name
        phone = report.phone
        sex = report.sex
        url = "buscamascota.org/reporte/" + str(report_id)

        if reportImageExist:
            reportImage = ReportImage.objects.get(report_id=report_id)
            #publish at Twitter
            tweet(report.report_type, report.country, report.title, reportImage.picture.url, url)
            #publish at Facebook

            #publish at Instagram
        
    except:
        print("Oops!", sys.exc_info()[0], "occurred.")
        messages.error(request, "Error al recuperar reporte! Inténtelo más tarde o póngase en contacto con el administrador del sitio.")

    context={
        'report_id': report_id,
        'report_type': report_type,
        'specie': specie,
        'image': image,
        'description': description,
        'age': age,
        'last_time_seen': last_time_seen,
        'ubication_resume': ubication_resume,
        'name': name,
        'phone': phone,
        'sex': sex,
        'url': url,
        'form': form,
        'reportImageExist': reportImageExist
    }

    return render(request, 'exito.html', context)