from django.db import models
from app.constants import REPORT_TYPE, SPECIE, SEX
from django.utils import timezone

class Report(models.Model):
    report_type = models.CharField(max_length=12, choices=REPORT_TYPE, default='')
    title = models.CharField(max_length=200)
    description = models.TextField(max_length=2000)
    picture = models.ImageField(upload_to='animals')
    name = models.CharField(max_length=50, null=True, blank=True)
    phone = models.CharField(max_length=30, null=True, blank=True)
    specie = models.CharField(max_length=6, choices=SPECIE, default='')
    age = models.PositiveIntegerField (null=True,blank=True)
    sex = models.CharField(max_length=12, choices=SEX, default='')
    ubication_resume = models.TextField(max_length=1000)
    country = models.CharField(max_length=100, null=True, blank=True)
    postal_code = models.CharField(max_length=50, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    address = models.CharField(max_length=300, null=True, blank=True)
    latitude = models.FloatField()
    longitude = models.FloatField()
    report_state = models.BooleanField(default=False, db_index=True)
    created_at = models.DateTimeField(editable=False, default=timezone.now)
    edited_at = models.DateTimeField(null=True, blank=True)
    last_time_seen = models.DateField()
    accept_terms = models.BooleanField(default=False)
    who_sent = models.GenericIPAddressField(null=True, blank=True)
    
    def save(self, *args, **kwargs):
        # On save, update timestamps
        if not self.id:
            self.created_at = timezone.now()
            self.report_state = False
        self.edited_at = timezone.now()
        return super(Report, self).save(*args, **kwargs)

class BlackList(models.Model):
    ip = models.GenericIPAddressField()
    created_at = models.DateTimeField(editable=False, default=timezone.now)