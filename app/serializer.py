from rest_framework import serializers

from app.models import Report, PetAdoptionModel


class ReportSerializer(serializers.ModelSerializer):  #Endpoint de listar reportes
    class Meta:
        model = Report
        fields = "__all__"


class AdoptDetailSerializer(serializers.ModelSerializer):  #Endpoint para detalle de adopciones
    class Meta:
        model = PetAdoptionModel
        fields = ['title', 'name', 'description', 'specie', 'age', 'sex', 'city', 'country', 'phone', 'picture']
