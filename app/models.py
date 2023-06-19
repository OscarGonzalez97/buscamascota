from django.db import models
from app.constants import REPORT_TYPE, SPECIE, SEX
from django.utils import timezone
from django_resized import ResizedImageField


class Report(models.Model):
    report_type = models.CharField(max_length=12, choices=REPORT_TYPE, default='')
    title = models.CharField(max_length=200)
    description = models.TextField(max_length=2000)
    picture = ResizedImageField(size=[600, 600], quality=100, crop=['middle', 'center'], upload_to='animals')
    name = models.CharField(max_length=50, null=True, blank=True)
    phone = models.CharField(max_length=30, null=True, blank=True)
    specie = models.CharField(max_length=6, choices=SPECIE, default='')
    age = models.PositiveIntegerField(null=True, blank=True)
    sex = models.CharField(max_length=12, choices=SEX, default='')
    ubication_resume = models.TextField(max_length=1000)
    country = models.CharField(max_length=100, null=True, blank=True)
    postal_code = models.CharField(max_length=50, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    address = models.CharField(max_length=300, null=True, blank=True)
    latitude = models.FloatField(blank=True)
    longitude = models.FloatField(blank=True)
    report_state = models.BooleanField(default=False, db_index=True)
    created_at = models.DateTimeField(editable=False, default=timezone.now)
    edited_at = models.DateTimeField(null=True, blank=True)
    last_time_seen = models.DateField()
    accept_terms = models.BooleanField(default=False)
    allowed = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        # On save, update timestamps
        if not self.id:
            self.created_at = timezone.now()
            self.report_state = False
            self.allowed = True
        self.edited_at = timezone.now()
        return super(Report, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.id)


class PetAdoptionModel(models.Model):
    title = models.CharField(max_length=100)
    name = models.CharField(max_length=100,null=True, blank=True)
    description = models.TextField()
    specie = models.CharField(max_length=6, choices=SPECIE)
    age = models.PositiveIntegerField(null=True, blank=True)
    sex = models.CharField(max_length=12, choices=SEX)
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100,)
    phone = models.CharField(max_length=30, null=True,blank=True)
    picture = models.ImageField(upload_to='pet_pictures/')
    allowed = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.specie} - {self.id}"


class ReportImage(models.Model):
    picture = models.CharField(blank=True, max_length=300)
    report_id = models.ForeignKey(Report, on_delete=models.CASCADE, blank=True)
    created_at = models.DateTimeField(editable=False, default=timezone.now)
    