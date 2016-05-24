# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Comentario',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('id_hotel', models.IntegerField(default=0)),
                ('comentario', models.TextField(default=b'')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Hotel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(default=b'', max_length=32)),
                ('email', models.URLField(default=b'', max_length=32)),
                ('phone', models.CharField(default=b'', max_length=32)),
                ('body', models.TextField(default=b'')),
                ('web', models.URLField(default=b'', max_length=32)),
                ('direccion', models.CharField(default=b'', max_length=32)),
                ('zipcode', models.CharField(default=b'', max_length=32)),
                ('pais', models.CharField(default=b'', max_length=32)),
                ('latitud', models.CharField(default=b'', max_length=32)),
                ('longitud', models.CharField(default=b'', max_length=32)),
                ('cuidad', models.CharField(default=b'', max_length=32)),
                ('categoria', models.CharField(default=b'', max_length=32)),
                ('subcategoria', models.CharField(default=b'', max_length=32)),
                ('imagenes', models.TextField(default=b'')),
                ('num_comentarios', models.IntegerField(default=0)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(default=b'', max_length=32)),
                ('titulo_personal', models.CharField(default=b'', max_length=32)),
                ('size_letra', models.CharField(default=b'', max_length=32)),
                ('color_fondo', models.CharField(default=b'', max_length=32)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
