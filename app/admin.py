from django.contrib import admin
from app.models import Report
from app.models import PetAdoptionModel


class ReportAdmin(admin.ModelAdmin):
    search_fields = ['id']
    list_display = ('id', 'report_type' , 'city' ,'country', 'allowed')

admin.site.register(Report, ReportAdmin)

class PetAdmin(admin.ModelAdmin):
    search_fields = ['id']
    list_display = ('id', 'name','specie' , 'city','state' ,'country', 'phone', 'allowed')

admin.site.register(PetAdoptionModel, PetAdmin)

