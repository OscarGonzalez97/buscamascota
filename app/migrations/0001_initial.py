# Generated by Django 3.1 on 2020-09-29 04:45

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BlackList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip', models.GenericIPAddressField()),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
            ],
        ),
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('report_type', models.CharField(choices=[('perdido', 'Perdido'), ('avistamiento', 'Avistamiento'), ('retenido', 'Retenido'), ('otro', 'Otro')], default='', max_length=12)),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField(max_length=2000)),
                ('picture', models.ImageField(upload_to='animals')),
                ('name', models.CharField(blank=True, max_length=50, null=True)),
                ('phone', models.CharField(blank=True, max_length=30, null=True)),
                ('specie', models.CharField(choices=[('perro', 'Perro'), ('gato', 'Gato'), ('otro', 'Otro')], default='', max_length=6)),
                ('age', models.PositiveIntegerField(blank=True, null=True)),
                ('sex', models.CharField(choices=[('macho', 'Macho'), ('hembra', 'Hembra'), ('desconocido', 'Desconocido')], default='', max_length=12)),
                ('ubication_resume', models.TextField(max_length=1000)),
                ('country', models.CharField(blank=True, max_length=100, null=True)),
                ('postal_code', models.CharField(blank=True, max_length=50, null=True)),
                ('city', models.CharField(blank=True, max_length=100, null=True)),
                ('address', models.CharField(blank=True, max_length=300, null=True)),
                ('latitude', models.FloatField()),
                ('longitude', models.FloatField()),
                ('report_state', models.BooleanField(db_index=True, default=False)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('edited_at', models.DateTimeField(blank=True, null=True)),
                ('last_time_seen', models.DateField()),
                ('accept_terms', models.BooleanField(default=False)),
                ('who_sent', models.GenericIPAddressField(blank=True, null=True)),
            ],
        ),
    ]
