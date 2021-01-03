from django.contrib import admin
from app.models import Report

class ReportAdmin(admin.ModelAdmin):
    search_fields = ['id']

admin.site.register(Report, ReportAdmin)