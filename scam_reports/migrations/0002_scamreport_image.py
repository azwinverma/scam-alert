# Generated by Django 5.1.4 on 2025-01-10 04:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scam_reports', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='scamreport',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='scam_images/'),
        ),
    ]
