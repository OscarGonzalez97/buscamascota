from django import forms
from app.constants import REPORT_TYPE, SPECIE, SEX

REPORT_TYPE_EMPTY = [('','Indique el tipo de reporte')] + list(SPECIE)
SPECIE_EMPTY = [('','Indique especie')] + list(SPECIE)
SEX_EMPTY = [('','Sexo del animal')] + list(SEX)

