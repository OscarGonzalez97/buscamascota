from django import forms
from app.constants import REPORT_TYPE, SPECIE, SEX
from app.models import Report, ReportImage, PetAdoptionModel
from django.utils.safestring import mark_safe

REPORT_TYPE_ALL = (('','Todos'),) + REPORT_TYPE
SPECIE_ALL = (('','Todas'),) + SPECIE

class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = ('report_type', 
        'title',
        'description',
        'picture',
        'name',
        'phone',
        'specie',
        'age',
        'sex',
        'ubication_resume', 
        'country', 
        'postal_code',
        'city',
        'address',
        'last_time_seen',
        'latitude',
        'longitude',
        'accept_terms',
        )
        labels = {
            'report_type': mark_safe('<b>Tipo de reporte * </b>'),
            'title': mark_safe('<b>Título de reporte *</b>'),
            'description': mark_safe('<b>Descripción de reporte *</b>'),
            'picture': mark_safe('<b>Foto *</b>'),
            'name': mark_safe('<b>Nombre de contacto </b>'),
            'phone': mark_safe('<b>Teléfono de contacto </b>'),
            'specie': mark_safe('<b>Especie *</b>'),
            'age': mark_safe('<b>Edad aproximada</b>'),
            'sex': mark_safe('<b>Sexo</b>'),
            'ubication_resume': mark_safe('<b>Resumen de ubicación *</b>'),
            'last_time_seen': mark_safe('<b>Última vez visto * </b>'),
            'accept_terms': mark_safe('Acepto los <a href="../terminos/">T&eacute;rminos de uso</a> *')
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
                    "placeholder": ("Ejemplo: Encontré un perro blanco con collar, creo que es una mezcla de caniche, parece asustado y no pude retenerlo."),
                }
            ),
            'picture': forms.FileInput(
                attrs={
                    "class": "form-control file-field",
                    "lang": "es",
                }
            ),
            'name': forms.TextInput(
                    attrs={
                    "class": "form-control",
                    "placeholder": ("Ejemplo: Juan Irala"),
                    }
            ),
            'phone': forms.TextInput(
                attrs={
                    "class":"form-control",
                    "type":"tel",
                    "placeholder": ("Ejemplo: +595990123456"),
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
                "placeholder": ("Ejemplo: Árboles, Paso de la Patria, Hipódromo, Asuncion, Región Oriental, 1906, Paraguay"),
                }
            ), 
            'country': forms.HiddenInput(), 
            'postal_code': forms.HiddenInput(),
            'city':forms.HiddenInput(),
            'address': forms.HiddenInput(),
            'last_time_seen': forms.DateInput(format=('%d/%m/%Y'), 
                attrs={'class':'form-control', 'placeholder':'Select a date', 'type':'date'}
            ),
            'latitude': forms.HiddenInput(),
            'longitude': forms.HiddenInput(),
            'accept_terms': forms.CheckboxInput(
                attrs={
                    'onclick': "enableSubmit();"
                }
            ),
        }
        help_texts  = {
            'report_type' : mark_safe("<small><ul><li><b>Perdido</b>: Si perdiste o alguien perdió su mascota y quieres reportarla como perdida.</li><li><b>Avistado</b>: Si viste una mascota que parecía perdida, pero no pudiste retenerla.</li><li><b>Retenido</b>: Si encontraste una mascota y pudiste retenerla o sabes de alguien que la tiene retenida.</li><li><b>Otro</b>: Otro tipo de reporte.</li></ul></small>"),
            'picture': mark_safe("<br><small>Se necesita una imagen de la mascota para evitar confusiones y que sea más sencillo reconocerla</small>")
        }
        # error_messages = {
        
        # }

class ReportSucessForm(forms.ModelForm):
    datauri = forms.CharField(widget=forms.HiddenInput())
    class Meta:
        model = ReportImage
        fields = ('picture', 'report_id')
        widgets = {'picture': forms.HiddenInput(),
                   'report_id': forms.HiddenInput(),
        }


class FilterForm(forms.Form):
    report_type = forms.ChoiceField(widget = forms.Select(attrs={'class': 'custom-select my-1 mr-sm-2'}), choices=REPORT_TYPE_ALL, required=False)
    date_from = forms.CharField(widget = forms.DateInput(format=('%d/%m/%Y'), attrs={'class':'form-control my-1 mr-sm-2', 'placeholder':'Seleccione una fecha', 'type':'date'}), required=False)
    date_to = forms.CharField(widget = forms.DateInput(format=('%d/%m/%Y'), attrs={'class':'form-control my-1 mr-sm-2', 'placeholder':'Seleccione una fecha', 'type':'date'}), required=False)
    specie = forms.ChoiceField(widget = forms.Select(attrs={'class': 'custom-select my-1 mr-sm-2'}), choices=SPECIE_ALL, required=False)
    country = forms.CharField(widget = forms.TextInput(attrs={'class': 'form-control my-1 mr-sm-2'}), required=False)
    city = forms.CharField(widget = forms.TextInput(attrs={'class': 'form-control my-1 mr-sm-2'}), required=False)


class PetAdoptionModelForm(forms.ModelForm):
    class Meta:
        model = PetAdoptionModel
        fields = ['name', 'description', 'specie', 'age', 'sex', 'city', 'country', 'phone', 'picture']


class PetFilterAdoptionModelForm(forms.Form):
    specie = forms.ChoiceField(widget = forms.Select(), choices=SPECIE_ALL, required=False)
    country = forms.CharField(widget = forms.TextInput(), required=False)
    city = forms.CharField(widget = forms.TextInput(), required=False)
    state = forms.CharField(widget = forms.TextInput(), required=False)
    sex = forms.ChoiceField(widget = forms.Select(),choices=SEX, required=False)
    