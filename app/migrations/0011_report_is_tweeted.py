# Generated by Django 3.2 on 2023-06-22 15:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0010_auto_20230619_1647'),
    ]

    operations = [
        migrations.AddField(
            model_name='report',
            name='is_tweeted',
            field=models.BooleanField(default=False),
        ),
    ]