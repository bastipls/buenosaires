# Generated by Django 2.1.4 on 2019-06-10 00:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('buenosaires', '0006_auto_20190607_2357'),
    ]

    operations = [
        migrations.AddField(
            model_name='solicitud',
            name='estado',
            field=models.CharField(blank=True, choices=[('Sin revisar', 'Sin revisar'), ('Aprobada', 'Aporbada'), ('Rechazada', 'Rechazada')], default='Sin revisar', max_length=20, null=True),
        ),
    ]
