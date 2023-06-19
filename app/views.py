import json
import sys
import urllib
from io import BytesIO
from urllib.parse import urlencode

from django.contrib import messages
from django.core.paginator import Paginator
from django.core.serializers.json import DjangoJSONEncoder
from django.http import JsonResponse
from django.shortcuts import render, redirect
from PIL import Image
from app.forms import ReportForm, ReportSucessForm, FilterForm
from app.models import Report, ReportImage
from app.utils import tweet, post_instagram_facebook
from app.serializers import ReportSerializer

def index(request):
    return render(request, 'index.html')


def __getReports(report_type, specie, country, city, date_from, date_to):
    query = {'allowed': True}

    if report_type != '':
        query['report_type'] = report_type

    if specie != '':
        query['specie'] = specie

    if country != '':
        query['country__icontains'] = country

    if city != '':
        query['city__icontains'] = city

    if date_from != '' and date_to != '':
        query['last_time_seen__range'] = (date_from, date_to)
    elif date_to != '':
        query['last_time_seen__lte'] = date_to
    elif date_from != '':
        query['last_time_seen__gte'] = date_from

    report_objs = Report.objects.filter(**query).order_by('last_time_seen')
    reports = []

    for report_obj in report_objs:
        reports.append(
            {'id': report_obj.id,
             'report_type': report_obj.report_type,
             'title': report_obj.title,
             'description': report_obj.description,
             'name': report_obj.name,
             'phone': report_obj.phone,
             'specie': report_obj.specie,
             'age': report_obj.age,
             'sex': report_obj.sex,
             'ubication_resume': report_obj.ubication_resume,
             'latitude': report_obj.latitude,
             'longitude': report_obj.longitude,
             'last_time_seen': report_obj.last_time_seen,
             'picture': report_obj.picture.url,
             'country': report_obj.country,
             'city': report_obj.city})
    return reports


def colaborate(request):
    return render(request, 'colaborar.html')


def terms(request):
    return render(request, 'terminos.html')


def license(request):
    return render(request, 'licencia.html')


def map(request):
    report_type = specie = country = city = date_from = date_to = ''
    if request.method == 'POST':
        form = FilterForm(request.POST)
        # if 'search' in request.POST:
        if form.is_valid():
            report_type = form.cleaned_data['report_type']
            specie = form.cleaned_data['specie']
            country = form.cleaned_data['country']
            city = form.cleaned_data['city']
            date_from = form.cleaned_data['date_from']
            date_to = form.cleaned_data['date_to']
    else:
        form = FilterForm()

    reports = __getReports(report_type, specie, country, city, date_from, date_to)

    paginator = Paginator(reports, 15)  # Show 15 reports per page.

    page_number = request.GET.get('page')

    if page_number == 0:
        page_number = 1

    page_obj = paginator.get_page(page_number)

    context = {
        'reports': json.dumps(reports, cls=DjangoJSONEncoder),
        'page_obj': page_obj,
        'form': form,
    }

    return render(request, 'map.html', context)


def publish(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = ReportForm(request.POST, request.FILES)
        # check whether it's valid:
        if form.is_valid():
            if form.cleaned_data['latitude'] and form.cleaned_data['longitude']:
                instance = form.save(commit=False)
                instance.save()
                report_id = str(instance.id)
                request.session['pp_publish'] = True
                request.session['pp_tweet'] = True
                # redirect to another view where is the report id
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

    specie = image = description = last_time_seen = ubication_resume = name = phone = sex = url = ''

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
            im = Image.open(BytesIO(response.file.read()))
            path_reports = 'media/reports/report' + str(report_id) + '.png'
            im.save(path_reports, quality=50)
            instance.picture = path_reports
            instance.save()
            reportImageExist = True
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
        url = "127.0.0.1:8000/reporte/" + str(report_id)

        if reportImageExist and ('pp_tweet' in request.session):
            reportImage = ReportImage.objects.get(report_id=report_id)
            # publish at Twitter
            tweet(report.report_type, report.country, report.title, reportImage.picture, url)
            # publish at Instagram & Facebook
            # post_instagram_facebook(report.report_type, report.country, report.title, reportImage.picture, url)
            del request.session['pp_tweet']

    except:
        print("Oops!", sys.exc_info()[0], "occurred.")
        messages.error(request,
                       "Error al recuperar reporte! Inténtelo más tarde o póngase en contacto con el administrador del sitio.")

    context = {
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
    if reportImageExist:
        return render(request, 'exito.html', context)
    else:
        return render(request, 'exito-escritorio.html', context)


def report(request, report_id):
    report_type = age = 0

    specie = image = description = last_time_seen = ubication_resume = name = phone = sex = created_at = reportImageDownloadable = latitude = longitude = url = text = ''

    # report_id was created
    reportExist = Report.objects.filter(id=report_id).exists()

    # This is the image of the report generated in the success view
    reportImageExist = ReportImage.objects.filter(report_id=report_id).exists()

    if reportExist:
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
            created_at = report.created_at
            latitude = report.latitude
            longitude = report.longitude
            url = "127.0.0.1:8000/reporte/" + str(report_id)
            text = "Conoces esta mascota? Echa un vistazo! " + url
            mydict = {'text': text}
            text = urlencode(mydict)

        except:
            print("Oops!", sys.exc_info()[0], "occurred.")
            messages.error(request,
                           "Error al recuperar reporte! Inténtelo más tarde o póngase en contacto con el administrador del sitio.")

        try:
            reportImage = ReportImage.objects.get(report_id=report_id)
            path_reports = '/media/animals/' + str(reportImage) + '.png'
            print("Path reports: ", path_reports)
            reportImageDownloadable = path_reports
        except:
            messages.error(request, "La imagen del reporte no existe!")

        context = {
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
            'reportExist': reportExist,
            'created_at': created_at,
            'reportImageDownloadable': reportImageDownloadable,
            'latitude': latitude,
            'longitude': longitude,
            'url': url,
            'text': text,
        }
        return render(request, 'reporte.html', context)
    else:
        return render(request, '404.html')
    

def report_list(request):
    reports = Report.objects.all()
    paginator = Paginator(reports, 15)  # Show 15 reports per page.

    page_number = request.GET.get('page')

    if page_number == 0:
        page_number = 1

    page_obj = paginator.get_page(page_number)
    serializer = ReportSerializer(page_obj, many=True)
    return JsonResponse(serializer.data, safe=False)

def __getReportFilter(report_type, specie, country, city, date_from, date_to):
    query = {'allowed': True}

    if report_type != '':
        query['report_type'] = report_type

    if specie != '':
        query['specie'] = specie

    if country != '':
        query['country__icontains'] = country

    if city != '':
        query['city__icontains'] = city

    if date_from != '' and date_to != '':
        query['last_time_seen__range'] = (date_from, date_to)
    elif date_to != '':
        query['last_time_seen__lte'] = date_to
    elif date_from != '':
        query['last_time_seen__gte'] = date_from

    report_objs = Report.objects.filter(**query).order_by('last_time_seen')
    return(report_objs)
