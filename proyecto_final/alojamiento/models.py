from django.db import models

# Create your models here.

class Usuario(models.Model):
    nombre = models.CharField(max_length=32, default="")
    titulo_personal = models.CharField(max_length=32, default="")
    size_letra = models.CharField(max_length=32, default="")
    color_fondo = models.CharField(max_length=32, default="")

class Hotel(models.Model):
    nombre = models.CharField(max_length=32, default="")
    email = models.URLField(max_length=32, default="")
    phone = models.CharField(max_length=32, default="")
    body = models.TextField(default="")
    web = models.URLField(max_length=32, default="")
    direccion = models.CharField(max_length=32, default="")
    zipcode = models.CharField(max_length=32, default="")
    pais = models.CharField(max_length=32, default="")
    latitud = models.CharField(max_length=32, default="")
    longitud = models.CharField(max_length=32, default="")
    cuidad = models.CharField(max_length=32, default="")
    categoria = models.CharField(max_length=32, default="")
    subcategoria = models.CharField(max_length=32, default="")
    imagenes = models.TextField(default="")
    num_comentarios = models.IntegerField(default=0)

class Comentario(models.Model):
    id_hotel = models.IntegerField(default=0)
    comentario = models.TextField(default="")

class HotelSeleccionado(models.Model):
    usuario = models.CharField(max_length=32, default="")
    id_hotel = models.IntegerField(default=0)
    fecha_seleccion = models.CharField(max_length=32, default="")  
