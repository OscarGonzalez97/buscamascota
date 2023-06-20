from rest_framework import serializers
from .models import Report, ReportImage

from .models import Report


class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = '__all__'
class ReportImageSerializer(serializers.ModelSerializer):
    picture = serializers.ImageField(write_only=True)

    class Meta:
        model = ReportImage
        fields = ['picture', 'report_id', 'created_at']
