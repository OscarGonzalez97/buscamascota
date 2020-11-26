from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from app.constants import REPORT_TYPE, SPECIE
from app.forms import ReportForm, ReportSucessForm
from app.utils import tweet, post_instagram_facebook
from app.models import BlackList, Report, ReportImage
from django.contrib import messages
from django.core.serializers.json import DjangoJSONEncoder
import sys
import urllib
import json
from django.core.paginator import Paginator

def index(request):
    reports = __getReports()
    context = { 'reports': json.dumps(reports, cls=DjangoJSONEncoder) }
    return render(request,'index.html', context)

def __getReports():
    query = {'allowed': True}

    report_objs = Report.objects.filter(**query)
    reports = []

    for report_obj in report_objs:
        reports.append(
        {'id' : report_obj.id,
        'report_type' : report_obj.report_type,
        'title' : report_obj.title,
        'description' : report_obj.description,
        'name' : report_obj.name,
        'phone' : report_obj.phone,
        'specie' : report_obj.specie,
        'age' : report_obj.age, 
        'sex' : report_obj.sex, 
        'ubication_resume' : report_obj.ubication_resume, 
        'latitude' : report_obj.latitude, 
        'longitude' : report_obj.longitude, 
        'last_time_seen' : report_obj.last_time_seen,
        'picture':report_obj.picture.url,
        'country':report_obj.country,
        'city':report_obj.city})
    return reports

def colaborate(request):
    return render(request,'colaborar.html')

def terms(request):
    return render(request,'terminos.html')

def license(request):
    return render(request,'licencia.html')

def map(request):

    reports = __getReports()

    paginator = Paginator(reports, 15) # Show 25 reports per page.
    
    page_number = request.GET.get('page')   

    if (page_number == 0):
        page_number=1
    
    page_obj = paginator.get_page(page_number)

    context={
        'report_type':REPORT_TYPE,
        'specie': SPECIE,
        'reports': json.dumps(reports, cls=DjangoJSONEncoder),
        'page_obj': page_obj,
    }
    
    response = render(request,'map.html', context)
    
    return response

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
                instance.save()
                report_id = str(instance.id)
                request.session['pp_publish'] = True
                #redirect to another view where is the report id
                return redirect('success', report_id=report_id)
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

    
    if request.method == 'POST' and ('pp_publish' in request.session):
        # create a form instance and populate it with data from the request:
        form = ReportSucessForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            instance = form.save(commit=False)
            data = form.cleaned_data['datauri']
            response = urllib.request.urlopen(data)
            path_reports = 'media/reports/report'+ str(report_id)+ '.png'
            with open(path_reports, 'wb') as f:
                f.write(response.file.read())
            instance.picture = path_reports
            instance.save()
            reportImageExist = True
            print('I save the report image!')
            del request.session['pp_publish']

        
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
            # tweet(report.report_type, report.country, report.title, reportImage.picture, url)
            #publish at Instagram & Facebook
            # post_instagram_facebook(report.report_type, report.country, report.title, reportImage.picture, url)
        
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

    