# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('alojamiento', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='HotelSeleccionado',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('usuario', models.CharField(default=b'', max_length=32)),
                ('id_hotel', models.IntegerField(default=0)),
                ('fecha_seleccion', models.CharField(default=b'', max_length=32)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
