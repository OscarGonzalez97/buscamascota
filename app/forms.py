from django import forms
from app.constants import REPORT_TYPE, SPECIE, SEX
from app.models import Report
from django.utils.translation import gettext_lazy as _

# REPORT_TYPE_EMPTY = [('','Indique el tipo de reporte')] + list(SPECIE)
# SPECIE_EMPTY = [('','Indique especie')] + list(SPECIE)
# SEX_EMPTY = [('','Sexo del animal')] + list(SEX)

class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = ('report_type', 
        'title',
        'description',
        'specie',
        'age',
        'sex',
        'ubication_resume', 
        'country', 
        'postal_code',
        'city',
        'adress',
        'last_time_seen'
        )
        labels = {
            'report_type': _('Tipo de reporte *'),
            'title': _('Título de reporte *'),
            'description': _('Descripción de reporte *'),
            'specie': _('Especie *'),
            'age': _('Edad aproximada'),
            'sex': _('Sexo'),
            'ubication_resume': _('Ubicación'), 
            'country': _('País'), 
            'postal_code': _('Código postal'),
            'city': _('Ciudad'),
            'adress': _('Dirección'),
            'last_time_seen': _('Última vez visto')
        }
        widgets = {
            'report_type': forms.Select(attrs={'class': 'form-control'}),
            'title': forms.TextInput(
                    attrs={
                    "class": "form-control",
                    "placeholder": ("Ejemplo: Perro con collar encontrado barrio San Vicente"),
                    }
            ),
            'description': forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4,
                    "placeholder": ("Encontre un perro blanco con collar, creo que es una mezcla de caniche, parece asustado y no pude retenerlo."),
                }
            ),
            'specie': forms.Select(
                attrs={
                    "class": "form-control"
                }
            ),
            'age': forms.NumberInput(
                attrs={
                    "class": "form-control"
                }
            ),
            'sex': forms.Select(
                attrs={
                    "class": "form-control"
                }
            ),
            'ubication_resume': forms.TextInput(
                    attrs={
                    "class": "form-control",
                    "placeholder": ("Ejemplo: Perro con collar encontrado barrio San Vicente"),
                    }
            ), 
            'country': forms.TextInput(
                    attrs={
                    "class": "form-control disabled",
                    "placeholder": ("Ejemplo: Perro con collar encontrado barrio San Vicente"),
                    }
            ), 
            'postal_code': forms.TextInput(
                    attrs={
                    "class": "form-control disabled",
                    "placeholder": ("Ejemplo: Perro con collar encontrado barrio San Vicente"),
                    }
            ),
            'city': forms.TextInput(
                    attrs={
                    "class": "form-control disabled",
                    "placeholder": ("Ejemplo: Perro con collar encontrado barrio San Vicente"),
                    }
            ),
            'adress': forms.TextInput(
                    attrs={
                    "class": "form-control disabled",
                    "disabled" : True
                    }
            ),
            'last_time_seen': forms.DateInput(format=('%d/%m/%Y'), 
                attrs={'class':'form-control', 'placeholder':'Select a date', 'type':'date'}),
        }
        