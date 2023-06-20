import json
import sys
import urllib
from io import BytesIO
from urllib.parse import urlencode
from rest_framework.pagination import PageNumberPagination

from django.contrib import messages
from django.core.paginator import Paginator
from django.core.serializers.json import DjangoJSONEncoder
from django.http import JsonResponse
from django.shortcuts import render, redirect
from PIL import Image
from rest_framework.response import Response
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework import generics
from rest_framework.generics import ListAPIView
from app.forms import ReportForm, ReportSucessForm, FilterForm
from app.models import Report, ReportImage, PetAdoptionModel
from app.serializers import ReportSerializer, AdoptDetailSerializer, PetAdoptionSerializer
from app.utils import tweet, post_instagram_facebook
from rest_framework.generics import RetrieveAPIView
from rest_framework.response import Response
from .models import Report

from .serializers import ReportSerializer, ReportImageSerializer
import datetime

from .pagination import CustomPagination
from rest_framework.views import APIView


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

    reports = __getReports(report_type, specie, country,
                           city, date_from, date_to)

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
                messages.error(
                    request, "Es necesario una ubicación, por favor marque un punto en el mapa")
        else:
            messages.error(
                request, "Por favor verifique los datos del formulario")
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
            path_reports = 'media/animals/' + str(report_id) + '.png'
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
        url = "buscamascota.org/reporte/" + str(report_id)

        # if reportImageExist and ('pp_tweet' in request.session):
        #     reportImage = ReportImage.objects.get(report_id=report_id)
        #     # publish at Twitter
        #     tweet(report.report_type, report.country,
        #           report.title, reportImage.picture, url)
        #     # publish at Instagram & Facebook
        #     # post_instagram_facebook(report.report_type, report.country, report.title, reportImage.picture, url)
        #     del request.session['pp_tweet']

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
            reportImageDownloadable = report.picture.url
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
            url = "buscamascota.org/reporte/" + str(report_id)
            text = "Conoces esta mascota? Echa un vistazo! " + url
            mydict = {'text': text}
            text = urlencode(mydict)

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


# API


def filter_reports(report_type, specie, country, city, date_from, date_to):
    query = {'allowed': True}
    this_year = datetime.date.today().year

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
    elif date_from == '' and date_to == '':  # Si no pasa datos de fecha, traer del ultimo año
        query['created_at__year'] = this_year
    elif date_to != '':
        query['last_time_seen__lte'] = date_to
    elif date_from != '':
        query['last_time_seen__gte'] = date_from

    report_objs = Report.objects.filter(**query).order_by('last_time_seen')

    return report_objs


class ReportListAPIView(APIView):

    def get(self, request, format=None):
        this_year = datetime.date.today().year
        paginator = CustomPagination()
        reports = Report.objects.filter(created_at__year=this_year)
        result_page = paginator.paginate_queryset(reports, request)
        serializer = ReportSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request, format=None):
        form = FilterForm(request.POST)
        # if 'search' in request.POST:
        if form.is_valid():
            report_type = form.cleaned_data['report_type']
            specie = form.cleaned_data['specie']
            country = form.cleaned_data['country']
            city = form.cleaned_data['city']
            date_from = form.cleaned_data['date_from']
            date_to = form.cleaned_data['date_to']

        paginator = CustomPagination()
        reports = filter_reports(
            report_type, specie, country, city, date_from, date_to)

        result_page = paginator.paginate_queryset(reports, request)
        serializer = ReportSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)


def report_list(request):
    reports = Report.objects.all()
    serializer = ReportSerializer(reports, many=True)
    return JsonResponse({"Reportes": serializer.data}, safe=False)


@api_view(['GET'])
def adopt(request, adopt_id):
    try:
        adoption = PetAdoptionModel.objects.get(id=adopt_id)
        serializer = AdoptDetailSerializer(adoption)
        return JsonResponse(serializer.data)
    except PetAdoptionModel.DoesNotExist:
        return JsonResponse({'error': 'La adopción no existe.'}, status=404)


# def publicar(request):  # Vista para guardar una adopción
#     if request.method == 'POST':
#         form = PetAdoptionModelForm(request.POST, request.FILES)
#         if form.is_valid():
#             instance = form.save(commit=False)
#             adopt_id = str(instance.id)
#             request.session['pp_publish'] = True
#             return redirect('success', adopt_id=adopt_id)
#         else:
#             messages.error(request, 'Por favor, verifique los datos del formulario')
#     else:
#         form = PetAdoptionModelForm()
#
#     context = {'form': form}
#
#     return render(request, 'adoptar.html', context)
#


class PetAdoptionPagination(PageNumberPagination):
    page_size = 10  # Number of pet adoptions per page
    page_size_query_param = 'page_size'
    max_page_size = 100


class ReportGetAPIView(RetrieveAPIView):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class PetAdoptionListAPIView(ListAPIView):
    def get(self, request, format=None):
        paginator = PetAdoptionPagination()
        pet_adoptions = PetAdoptionModel.objects.all()
        result_page = paginator.paginate_queryset(pet_adoptions, request)
        serializer = PetAdoptionSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request, format=None):
        form = FilterForm(request.POST)  # Assuming you have a form for filtering
        if form.is_valid():
            specie = form.cleaned_data['specie']
            country = form.cleaned_data['country']
            city = form.cleaned_data['city']
            # Add more filter fields as per your requirements

            # Apply filters to the queryset
            queryset = self.get_queryset()
            if specie:
                queryset = queryset.filter(specie=specie)
            if country:
                queryset = queryset.filter(country=country)
            if city:
                queryset = queryset.filter(city=city)
            # Apply more filters based on the form fields

            # Paginate the filtered queryset
            paginator = self.pagination_class()
            page = paginator.paginate_queryset(queryset, request)
            serializer = self.serializer_class(page, many=True)
            return paginator.get_paginated_response(serializer.data)

        return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)
