from django.shortcuts import render, redirect
from django.http import HttpResponse
from app.constants import REPORT_TYPE, SPECIE
from app.forms import ReportForm
from django.contrib import messages

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
            instance = form.save(commit=False)
            instance.who_sent = request.META['REMOTE_ADDR']
            instance.save()
            messages.success(request, "Reporte creado con éxito!")
            #publish at Twitter
            #publish at Facebook
            #publish at Instagram
            #create PDF
        else:
            try:
                if not form.cleaned_data['latitude'] or not form.cleaned_data['longitude']:
                    print(form.cleaned_data)

            except e:
                print(e)
                messages.error(request, "Es necesario una ubicación, por favor marque un punto en el mapa")
            

    else:
        form = ReportForm()
        
    context = {'form': form}

    return render(request, 'publicar.html', context)