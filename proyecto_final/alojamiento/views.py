from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.contrib.auth import logout
from parser_xml import get_info_hoteles
from parser_xml_idioma import get_info_hoteles_idioma
from models import Hotel, Usuario, Comentario, HotelSeleccionado
from django.contrib.auth.models import User
from funciones import LoginUsuario
from django.views.decorators.csrf import csrf_exempt
import math
from django.template.loader import get_template
from django.template import Context
from funciones import filtrar_hoteles, CambiarPerfilUsuario, Comentar, filtrar_idiomas, Seleccionar, ActualizarBase
from django.shortcuts import render
from datetime import datetime

# Create your views here.

def cargar_usuarios():
    usuarios = Usuario.objects.all()
    if len(usuarios) == 0:
        usuarios = User.objects.all()
        respuesta = "Cargado en la base de datos!"
        for usuario in usuarios:
            nombre_usuario = usuario.username
            new_user = Usuario(nombre=nombre_usuario)
            new_user.save()
    else:
        respuesta = "Estan cargados usuarios en la base de datos!"

    return respuesta

def cargar_alojamientos():
    info_hoteles = get_info_hoteles()
    resp = "Todos los datos se han almacenado en la base de datos!"
    for hotel in info_hoteles:
        datos_hotel = hotel
        nombre_hotel = datos_hotel['name']
        web_hotel = datos_hotel['web']
        direccion_hotel = datos_hotel['address']
        categoria_hotel = datos_hotel['categoria']
        subcategoria_hotel = datos_hotel['subcategoria']
        imagenes_hotel = datos_hotel['url']
        email_hotel = datos_hotel['email']
        phone_hotel = datos_hotel['phone']
        body_hotel = datos_hotel['body']
        zipcode_hotel = datos_hotel['zipcode']
        pais_hotel = datos_hotel['country']
        latitud_hotel = datos_hotel['latitude']
        longitud_hotel = datos_hotel['longitude']
        cuidad_hotel = datos_hotel['subAdministrativeArea']
        new_hotel = Hotel(nombre=nombre_hotel,
                            email=email_hotel,
                            phone=phone_hotel,
                            body=body_hotel,
                            web=web_hotel,
                            direccion=direccion_hotel,
                            zipcode=zipcode_hotel,
                            pais=pais_hotel,
                            latitud=latitud_hotel,
                            longitud=longitud_hotel,
                            cuidad=cuidad_hotel,
                            categoria=categoria_hotel,
                            subcategoria=subcategoria_hotel,
                            imagenes=imagenes_hotel)
        new_hotel.save()

    return resp

def obtener_menu(tipo):
    if tipo != "pag principal":
        menu = '<li><a href="/">Inicio</a></li>' +\
                '<li><a href="/alojamientos">Alojamientos</a></li>' +\
                '<li><a href="/about">About</a></li>'
    else:
        menu = '<li><a href="/alojamientos">Alojamientos</a></li>' +\
                '<li><a href="/about">About</a></li>'

    return menu

def lista_alojamientos_comentados():
    alojamientos = Hotel.objects.all()
    rango = list(reversed(range(20)))
    respuesta = ""
    max_hoteles = 1
    for num in rango:
        alojamientos = Hotel.objects.filter(num_comentarios=num)
        if len(alojamientos) != 0 and num != 0:
            for alojamiento in alojamientos:
                if max_hoteles <= 10:
                    try:
                        hotel = Hotel.objects.get(nombre=alojamiento.nombre)
                        identificador = hotel.id
                        img_presentacion = hotel.imagenes
                        try:
                            img_presentacion = img_presentacion.split("',")[0]
                            img_presentacion = img_presentacion.split("u'")[1]
                        except IndexError:
                            img_presentacion = ""
                        pagina_hotel = "http://localhost:8000/alojamientos" + str(identificador)
                    except Hotel.DoesNotExist:
                        respuesta = "El modelo Hotel no existe!"

                    respuesta += "<p><a href='" + alojamiento.web + "'>" + alojamiento.nombre + \
                            "</a><br/>" +\
                            "Direccion: " + alojamiento.direccion + "<br/>" + \
                            "<a href='" + pagina_hotel + "'>Mas informacion</a>" + "<br/>"
                    if img_presentacion == "":
                        respuesta += "<h4><font color='red'>No hay imagen disponible</font></h4>" + "<hr>"
                    else:
                        respuesta += '<img src="' + img_presentacion + '"width="200" height="150" border="2">' + \
                            '<hr>'

                    max_hoteles = max_hoteles + 1

                else:
                    break

    return respuesta

def mostrar_alojamientos(alojamientos):
    resp = ""
    for alojamiento in alojamientos:
        try:
            identificador = Hotel.objects.get(nombre=alojamiento.nombre)
            identificador = identificador.id
            pagina_hotel = "http://localhost:8000/alojamientos" + str(identificador)
        except Hotel.DoesNotExist:
            http_Error = "El modelo Hotel no existe!"

        resp += "<p>" + alojamiento.nombre + "<br/>" +\
                "Categoria: " + alojamiento.categoria + "<br/>" +\
                "Subcategoria: " + alojamiento.subcategoria + "<br/>" +\
                "<a href='" + pagina_hotel + "'>Mas informacion</a>" + "</p>" + '<hr>'

    return resp

def paginas_personales():
    enlaces = "Enlaces a paginas personales de los usuarios:<hr><br/>"
    usuarios = Usuario.objects.all()
    if len(usuarios) == 0:
        cargar_usuarios()

    for usuario in usuarios:
        titulo = usuario.titulo_personal
        pag_user = "http://localhost:8000/" + usuario.nombre
        if titulo == "":
            enlaces += "Usuario: " + usuario.nombre + "<br/><a href='" + pag_user + "'> Pagina de " + \
                        usuario.nombre + "</a><br/>"
        else:
            enlaces += "Usuario: " + usuario.nombre + "<br/><a href='" + pag_user + "'>" + \
                        usuario.titulo_personal + "</a><br/>"
    return enlaces

# Vista de paginas!

@csrf_exempt
def pag_principal(request):
    titulo = "Pagina principal del sitio web!"
    http_Resp = ActualizarBase()
    metodo = request.method
    if metodo == "POST" and request.POST.get("tipo") == "Actualizar":
        http_Resp += cargar_alojamientos()
        return HttpResponseRedirect("/")
    else:
        http_Resp += lista_alojamientos_comentados()

    tipo = "pag principal"
    menu = obtener_menu(tipo)
    enlaces = paginas_personales()
    autenticado = request.user.is_authenticated()
    if autenticado == True:
        user = Usuario.objects.get(nombre=request.user.username)
        color = user.color_fondo
    else:
        color = 'default'

    return render(request, 'dreamy/index.html', {"contenido": http_Resp,
                    "menu": menu, "titulo": titulo,
                    "enlaces_personales": enlaces,
                    'autenticado': request.user.is_authenticated(),
                    'usuario': request.user.username,
                    'form': LoginUsuario(),
                    'color': color})

@csrf_exempt
def pag_alojamientos(request):
    titulo = "Pagina de todos los alojamientos"
    formulario = filtrar_hoteles()
    metodo = request.method
    if metodo == "GET":
        alojamientos = Hotel.objects.all()
        respuesta = mostrar_alojamientos(alojamientos)

    elif metodo == "POST":
        categoria = request.POST.get("Categoria")
        subcategoria = request.POST.get("SubCategoria")
        if categoria == "Seleccione una categoria" and subcategoria == "Seleccione el numero de estrellas":
            respuesta = "<h4><p><font color='red'>Error, introduce alguna categoria o numero de estrellas antes de filtrar!</font></p></h4>"
        elif categoria == "Seleccione una categoria" and subcategoria != "Seleccione el numero de estrellas":
            respuesta = "<h4><p>Aplicar filtro solamente por subcategoria.</p></h4>"
            alojamientos = Hotel.objects.filter(subcategoria=subcategoria)
            if len(alojamientos) == 0:
                respuesta +="<h4><font color='red'>Lo sentimos, no se han encontrado resultados a su busqueda!</font></h4>"
            else:
                respuesta += mostrar_alojamientos(alojamientos)

        elif categoria != "Seleccione una categoria" and subcategoria == "Seleccione el numero de estrellas":
            respuesta = "<h4><p>Aplicar filtro solamente por la categoria de los alojamientos.</p></h4>"
            alojamientos = Hotel.objects.filter(categoria=categoria)
            if len(alojamientos) == 0:
                respuesta +="<h4><font color='red'>Lo sentimos, no se han encontrado resultados a su busqueda!</font></h4>"
            else:
                respuesta += mostrar_alojamientos(alojamientos)

        elif categoria != "Seleccione una categoria" and subcategoria != "Seleccione el numero de estrellas":
            respuesta = "<h4><p>Aplicar filtro por categoria y subcategoria.</p></h4>"
            alojamientos = Hotel.objects.filter(categoria=categoria, subcategoria=subcategoria)
            if len(alojamientos) == 0:
                respuesta +="<h4><font color='red'>Lo sentimos, no se han encontrado resultados a su busqueda!</font></h4>"
            else:
                respuesta += mostrar_alojamientos(alojamientos)

    http_Resp = formulario + respuesta
    tipo = "pag NO principal"
    menu = obtener_menu(tipo)
    enlaces = ""
    autenticado = request.user.is_authenticated()
    if autenticado == True:
        user = Usuario.objects.get(nombre=request.user.username)
        color = user.color_fondo
    else:
        color = 'default'

    return render(request, 'dreamy/index.html', {"contenido": http_Resp,
                    "menu": menu, "titulo": titulo,
                    "enlaces_personales": enlaces,
                    'autenticado': request.user.is_authenticated(),
                    'usuario': request.user.username,
                    'form': LoginUsuario(),
                    'color': color})

def info_otro_idioma(idioma, hotel_idioma):
    info_hoteles = get_info_hoteles_idioma(idioma)
    for hotel in info_hoteles:
        datos_hotel = hotel
        nombre_hotel = datos_hotel['name']
        if nombre_hotel == hotel_idioma:
            web_hotel = datos_hotel['web']
            direccion_hotel = datos_hotel['address']
            categoria_hotel = datos_hotel['categoria']
            subcategoria_hotel = datos_hotel['subcategoria']
            imagenes_hotel = datos_hotel['url']
            email_hotel = datos_hotel['email']
            phone_hotel = datos_hotel['phone']
            body_hotel = datos_hotel['body']
            zipcode_hotel = datos_hotel['zipcode']
            pais_hotel = datos_hotel['country']
            latitud_hotel = datos_hotel['latitude']
            longitud_hotel = datos_hotel['longitude']
            cuidad_hotel = datos_hotel['subAdministrativeArea']
            respuesta = "<p><h3><font color='blue'>Basic Data</font></h3></p>"
            respuesta += "<p>Email: " + email_hotel + "</p>"
            respuesta += "<p>Phone: " + phone_hotel + "</p>"
            respuesta += "<p>Web: <a href='" + web_hotel + "'>" + nombre_hotel + "</a></p>"
            respuesta += "<p><h4>" + body_hotel + "</h4></p>"
            respuesta += "<p><h3><font color='blue'>Geo Data</font></h3></p>"
            respuesta += "<p>Address: " + direccion_hotel + "</p>"
            respuesta += "<p>Zipcode: " + zipcode_hotel + "</p>"
            respuesta += "<p>Country: " + pais_hotel + "</p>"
            respuesta += "<p>SubAdministrativeArea: " + cuidad_hotel + "</p>"
            respuesta += "<p>Latitude: " + latitud_hotel + "</p>"
            respuesta += "<p>Longitude: " + longitud_hotel + "</p>"
            respuesta += "<p><h3><font color='blue'>Hotel Images</font></h3></p>"
            imagenes = str(imagenes_hotel)
            try:
                imagen_1 = imagenes.split("http://")[1].split("'")[0]
                imagen_1 = "http://" + imagen_1
                respuesta += '<p><img src="' + imagen_1 + '"width="400" height="200" border="2"></p>'
                imagen_2 = imagenes.split("http://")[2].split("'")[0]
                imagen_2 = "http://" + imagen_2
                respuesta += '<p><img src="' + imagen_2 + '"width="400" height="200" border="2"></p>'
                imagen_3 = imagenes.split("http://")[3].split("'")[0]
                imagen_3 = "http://" + imagen_3
                respuesta += '<p><img src="' + imagen_3 + '"width="400" height="200" border="2"></p>'
                imagen_4 = imagenes.split("http://")[4].split("'")[0]
                imagen_4 = "http://" + imagen_4
                respuesta += '<p><img src="' + imagen_4 + '"width="400" height="200" border="2"></p>'
                imagen_5 = imagenes.split("http://")[5].split("'")[0]
                imagen_5 = "http://" + imagen_5
                respuesta += '<p><img src="' + imagen_5 + '"width="400" height="200" border="2"></p>'
            except IndexError:
                pass
            break
        else:
            respuesta = "<h4><font color='red'>Lo sentimos, el alojamiento " +\
                        "buscado no se encuentra en el idioma seleccionado!</font></h4>"

    return respuesta

@csrf_exempt
def pag_alojamiento(request, identificador):
    hotel = Hotel.objects.get(id=int(identificador))
    titulo = hotel.nombre
    http_Resp = ""
    info_ingles = ""
    info_frances = ""
    autenticado = request.user.is_authenticated()
    if autenticado == True:
        http_Resp += Seleccionar(request.user.username, hotel.id)
        http_Resp += filtrar_idiomas(hotel.id)
        metodo = request.method
        if metodo == "POST" and request.POST.get("tipo") == "Idioma":
            idioma = request.POST.get("Idioma")
            if idioma == "en":
                info_ingles += info_otro_idioma(idioma, hotel.nombre)
            elif idioma == "fr":
                info_frances += info_otro_idioma(idioma, hotel.nombre)

    http_Resp += "<p><h3><font color='blue'>Datos generales</font></h3></p>"
    http_Resp += "<p>Email: " + hotel.email + "</p>"
    http_Resp += "<p>Telefono: " + hotel.phone + "</p>"
    http_Resp += "<p>Pagina hotel: <a href='" + hotel.web + "'>" + hotel.nombre + "</a></p>"
    http_Resp += "<p><h4>" + hotel.body + "</h4></p>"
    http_Resp += "<p><h3><font color='blue'>Datos de localizacion</font></h3></p>"
    http_Resp += "<p>Dirrecion: " + hotel.direccion + "</p>"
    http_Resp += "<p>Codigo postal: " + hotel.zipcode + "</p>"
    http_Resp += "<p>Pais: " + hotel.pais + "</p>"
    http_Resp += "<p>Cuidad: " + hotel.cuidad + "</p>"
    http_Resp += "<p>Latitud: " + hotel.latitud + "</p>"
    http_Resp += "<p>Longitud: " + hotel.longitud + "</p>"
    http_Resp += "<p><h3><font color='blue'>Imagenes hotel</font></h3></p>"
    imagenes = hotel.imagenes
    try:
        imagen_1 = imagenes.split("http://")[1].split("'")[0]
        imagen_1 = "http://" + imagen_1
        http_Resp += '<p><img src="' + imagen_1 + '"width="400" height="200" border="2"></p>'
        imagen_2 = imagenes.split("http://")[2].split("'")[0]
        imagen_2 = "http://" + imagen_2
        http_Resp += '<p><img src="' + imagen_2 + '"width="400" height="200" border="2"></p>'
        imagen_3 = imagenes.split("http://")[3].split("'")[0]
        imagen_3 = "http://" + imagen_3
        http_Resp += '<p><img src="' + imagen_3 + '"width="400" height="200" border="2"></p>'
        imagen_4 = imagenes.split("http://")[4].split("'")[0]
        imagen_4 = "http://" + imagen_4
        http_Resp += '<p><img src="' + imagen_4 + '"width="400" height="200" border="2"></p>'
        imagen_5 = imagenes.split("http://")[5].split("'")[0]
        imagen_5 = "http://" + imagen_5
        http_Resp += '<p><img src="' + imagen_5 + '"width="400" height="200" border="2"></p>'
    except IndexError:
        pass

    http_Resp += "<p><h3><font color='blue'>Comentarios:</font></h3></p>"
    comentarios = Comentario.objects.filter(id_hotel=hotel.id)
    if len(comentarios) == 0:
        http_Resp += "<p>Para este hotel no hay comentarios disponibles.</p>"
    else:
        for comentario in comentarios:
            http_Resp += "<li>" + comentario.comentario

    autenticado = request.user.is_authenticated()
    if autenticado == True:
        user = Usuario.objects.get(nombre=request.user.username)
        color = user.color_fondo
        http_Resp += "<p><h3><font color='blue'>Introducir un comentario:</font></h3></p>"
        http_Resp += Comentar(request.user.username, hotel.id)
        metodo = request.method
        if metodo == "POST" and request.POST.get("tipo") == "Comentario":
            comentario = request.POST.get("Comentario")
            new_comentario = Comentario(id_hotel=hotel.id, comentario=comentario)
            new_comentario.save()
            hotel.num_comentarios = hotel.num_comentarios + 1
            hotel.save()
            return HttpResponseRedirect("/alojamientos" + str(hotel.id))
    else:
        http_Resp += "<h4><font color='red'>No puedes comentar si no estas registado!</font></h4>"
        color = 'default'

    if info_ingles != "":
        contenido = info_ingles
    elif info_frances != "":
        contenido = info_frances
    else:
        contenido = http_Resp

    tipo = "pag NO principal"
    menu = obtener_menu(tipo)
    enlaces = ""
    return render(request, 'dreamy/index.html', {"contenido": contenido,
                    "menu": menu, "titulo": titulo,
                    "enlaces_personales": enlaces,
                    'autenticado': request.user.is_authenticated(),
                    'usuario': request.user.username,
                    'form': LoginUsuario(),
                    'color': color})

def mostrar_hoteles_seleccionados(usuario, indice):
    respuesta = ""
    alojamientos = HotelSeleccionado.objects.filter(usuario=usuario)
    if len(alojamientos) == 0:
        respuesta += "El usuario " + usuario + " no tiene alojamientos seleccionados!"
        contador = 0
    else:
        for alojamiento in alojamientos[indice:indice+10]:
            idHotel = alojamiento.id_hotel
            hotel = Hotel.objects.get(id=idHotel)
            identificador = hotel.id
            img_presentacion = hotel.imagenes
            try:
                img_presentacion = img_presentacion.split("',")[0]
                img_presentacion = img_presentacion.split("u'")[1]
            except IndexError:
                img_presentacion = ""

            pagina_hotel = "http://localhost:8000/alojamientos" + str(identificador)
            respuesta += "<p><a href='" + hotel.web + "'>" + hotel.nombre + \
                            "</a><br/>" +\
                            "Direccion: " + hotel.direccion + "<br/>" + \
                            "<a href='" + pagina_hotel + "'>Mas informacion</a>" + "<br/>" + \
                            "Seleccionado el dia: " + alojamiento.fecha_seleccion + "<br/>"
            if img_presentacion == "":
                respuesta += "<h4><font color='red'>No hay imagen disponible</font></h4>" + "<hr>"
            else:
                respuesta += '<img src="' + img_presentacion + '"width="200" height="150" border="2">' + \
                    '<hr>'

        contador = 0
        for alojamiento in alojamientos:
            contador = contador + 1

    return respuesta, contador

@csrf_exempt
def pag_usuario(request, usuario):
    try:
        offset = int(request.GET.get('offset'))
    except TypeError:
        offset = 0

    indice = int(offset)*10
    titulo = "Pagina personal de " + usuario
    http_Resp = ""
    pag_xml = "http://localhost:8000/" + usuario + "/xml"
    http_Resp += "<p><a href='" + pag_xml + "'>Mi canal XML</a></p>"
    autenticado = request.user.is_authenticated()
    if autenticado == True:
        user = Usuario.objects.get(nombre=request.user.username)
        color = user.color_fondo
        http_Resp += CambiarPerfilUsuario(request.user.username)
        metodo = request.method
        if metodo == "POST":
            if request.POST.get("tipo") == "PerfilUsuario":
                titulo_personal = request.POST.get("Titulo_personal")
                if titulo_personal != "":
                    http_Resp += "<h4>Has cambiado el titulo personal!</h4><br/>"
                    modificar_user = Usuario.objects.get(nombre=request.user.username)
                    modificar_user.titulo_personal = titulo_personal
                    modificar_user.save()

                color_usuario = request.POST.get("Color_fondo")
                if color_usuario != "Seleccione un color":
                    modificar_user = Usuario.objects.get(nombre=request.user.username)
                    modificar_user.color_fondo = color_usuario
                    modificar_user.save()
                    return HttpResponseRedirect("/" + request.user.username)
            elif request.POST.get("tipo") == "Seleccion":
                idHotel = request.POST.get("idHotel")
                fecha = str(datetime.now())
                new_seleccion = HotelSeleccionado(usuario=request.user.username,
                                                    id_hotel=idHotel,
                                                    fecha_seleccion=fecha)
                new_seleccion.save()
                return HttpResponseRedirect("/" + request.user.username)
    else:
        color = 'default'

    http_Resp += "<p><h3><font color='blue'>Mi seleccion de alojamientos en Madrid:</font></h3></p>"
    respuesta, contador = mostrar_hoteles_seleccionados(usuario, indice)
    http_Resp += respuesta
    for n in range (0, int(math.ceil(float(contador)/10.0))):
        http_Resp += "<a href='" + str(usuario) + "?offset=" + str(n) + "'>" + str(n+1) + " " + "</a>"

    tipo = "pag NO principal"
    menu = obtener_menu(tipo)
    enlaces = ""
    return render(request, 'dreamy/index.html', {"contenido": http_Resp,
                    "menu": menu, "titulo": titulo,
                    "enlaces_personales": enlaces,
                    'autenticado': request.user.is_authenticated(),
                    'usuario': request.user.username,
                    'form': LoginUsuario(),
                    'color': color})

def obtener_XML_usuario(usuario):
    hoteles_seleccionados = HotelSeleccionado.objects.filter(usuario=usuario)
    respuesta = '<?xml version="1.0" encoding="UTF-8"?>\n'
    respuesta += '<serviceList>Alojamientos seleccionados por \n\t' + usuario
    for hotel_seleccionado in hoteles_seleccionados:
        id_hotel = hotel_seleccionado.id_hotel
        hotel = Hotel.objects.get(id=id_hotel)
        nombre_hotel = hotel.nombre
        direccion_hotel = hotel.direccion
        web_hotel = hotel.web
        fecha_seleccion = hotel_seleccionado.fecha_seleccion
        img_presentacion = hotel.imagenes
        try:
            img_presentacion = img_presentacion.split("',")[0].split("u'")[1]
        except IndexError:
            img_presentacion = ""
        respuesta += '<Alojamiento>'
        respuesta += '\t<nombre><![CDATA[ '
        respuesta += nombre_hotel
        respuesta += '\t ]]></nombre>'
        respuesta += '\t<direccion>'
        respuesta += direccion_hotel
        respuesta += '\t</direccion>'
        respuesta += '\t<web>'
        respuesta += web_hotel
        respuesta += '\t</web>'
        respuesta += '\t<fecha_seleccion>'
        respuesta += fecha_seleccion
        respuesta += '\t</fecha_seleccion>'
        respuesta += '\t<url_img>'
        respuesta += img_presentacion
        respuesta += '\t</url_img>'
        respuesta += '</Alojamiento>'

    respuesta += '</serviceList>\n'

    return respuesta

@csrf_exempt
def pag_usuario_xml(request, usuario):
    try:
        user = Usuario.objects.get(nombre=usuario)
        http_Resp = obtener_XML_usuario(usuario)
    except Usuario.DoesNotExist:
        http_Resp = "<h4><font color='red'>Error! El usuario indicado no existe!</font></h4>"

    return HttpResponse(http_Resp, content_type="text/xml")

@csrf_exempt
def pag_about(request):
    titulo = "Pagina about del sitio web!"
    http_Resp = "<p>Practica realizada por Jesus Galan Barba. <br/></p>"
    http_Resp += "Se trata de un sitio web donde ver informacion sobre distintos " +\
                    "hoteles en la Comunidad de Madrid, poder seleccionarlos, " +\
                    "comentar sobre ellos, acceder a paginas de los usuarios del " +\
                    "sitio web, etc. Solamente es necesario tener una cuenta y " +\
                    "navegar por la aplicacion. Os esperamos!"
    tipo = "pag NO principal"
    menu = obtener_menu(tipo)
    enlaces = ""
    autenticado = request.user.is_authenticated()
    if autenticado == True:
        user = Usuario.objects.get(nombre=request.user.username)
        color = user.color_fondo
    else:
        color = 'default'
    return render(request, 'dreamy/index.html', {"contenido": http_Resp,
                    "menu": menu, "titulo": titulo,
                    "enlaces_personales": enlaces,
                    'autenticado': request.user.is_authenticated(),
                    'usuario': request.user.username,
                    'form': LoginUsuario(),
                    'color': color})

@csrf_exempt
def acceder_cuenta(request):
    return HttpResponseRedirect("/" + request.user.username)

@csrf_exempt
def salir_cuenta(request):
    logout(request)
    return HttpResponseRedirect("/")
