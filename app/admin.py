from django.contrib import admin
from app.models import Report
from app.models import PetAdoptionModel
class ReportAdmin(admin.ModelAdmin):
    search_fields = ['id']

admin.site.register(Report, ReportAdmin)

class PetAdmin(admin.ModelAdmin):
    search_fields = ['id']

admin.site.register(PetAdoptionModel, PetAdmin)

   