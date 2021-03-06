# Generated by Django 2.1.4 on 2019-06-07 05:38

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('buenosaires', '0003_auto_20190606_2343'),
    ]

    operations = [
        migrations.AddField(
            model_name='producto_proveedor',
            name='marca',
            field=models.CharField(blank=True, default='Desconocida', max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='producto_proveedor',
            name='peso',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='orden',
            name='fecha_emision',
            field=models.DateField(default=datetime.datetime(2019, 6, 7, 5, 38, 34, 476256, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='solicitud',
            name='fecha_emision',
            field=models.DateTimeField(default=datetime.datetime(2019, 6, 7, 5, 38, 34, 475259, tzinfo=utc)),
        ),
    ]
