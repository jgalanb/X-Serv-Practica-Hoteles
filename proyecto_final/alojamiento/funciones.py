from django import forms

class LoginUsuario(forms.Form):
    username = forms.CharField(max_length=15,
                        widget=forms.TextInput(attrs={'size': '6'}))
    password = forms.CharField(max_length=15,
                        widget=forms.PasswordInput(attrs={'size': '6'}))

elecciones_categoria = (
    ('Seleccione una categoria', 'Seleccione una categoria'),
    ('Hoteles', 'Hoteles'),
    ('Apartahoteles', 'Apartahoteles'),
    ('Hostales', 'Hostales'),
    ('Albergues', 'Albergues'),
    ('Residencias universitarias', 'Residencias universitarias'),
)

elecciones_estrellas = (
    ('Seleccione el numero de estrellas', 'Seleccione el numero de estrellas'),
    ('1 estrellas', '1 estrellas'),
    ('2 estrellas', '2 estrellas'),
    ('3 estrellas', '3 estrellas'),
    ('4 estrellas', '4 estrellas'),
    ('5 estrellas', '5 estrellas'),
    ('5 estrellas Gran Lujo', '5 estrellas Gran Lujo'),
    ('1 llave', '1 llave'),
    ('2 llaves', '2 llaves'),
    ('3 llaves', '3 llaves'),
    ('4 llaves', '4 llaves'),
)

elecciones_color = (
    ('Seleccione un color', 'Seleccione un color'),
    ('default','Por defecto'),
    ('rojo', 'Rojo'),
    ('naranja', 'Naranja'),
    ('amarillo', 'Amarillo'),
    ('verde', 'Verde'),
    ('azul', 'Azul'),
    ('gris', 'Gris'),
)

elecciones_size = (
    ('Seleccione un size de letra', 'Seleccione un size de letra'),
    ('1.2em', 'Mediana'),
    ('2em', 'Grande'),
    ('3em', 'Extra grande'),
)

eleccion_idioma = (
    ('Seleccione un idioma', 'Seleccione un idioma'),
    ('en', 'Ingles'),
    ('fr', 'Frances'),
)

class FiltroCategorias(forms.Form):
    Categoria = forms.ChoiceField(choices=elecciones_categoria)

class FiltroEstrellas(forms.Form):
    SubCategoria = forms.ChoiceField(choices=elecciones_estrellas)

class FiltroIdioma(forms.Form):
    Idioma = forms.ChoiceField(choices=eleccion_idioma)

class PerfilUsuario(forms.Form):
    Titulo_personal = forms.CharField(max_length=100,
                             widget=forms.TextInput(attrs={'size': '10'}))
    Color_fondo = forms.ChoiceField(choices=elecciones_color)
    Size_letra = forms.ChoiceField(choices=elecciones_size)

class ComentarioUsuario(forms.Form):
    Comentario = forms.CharField(max_length=1024,
                             widget=forms.TextInput(attrs={'size': '10'}))

def filtrar_hoteles():
    form = '\n\t<FORM action="/alojamientos" name="FiltroCategorias" '
    form += 'method="POST" accept-charset="UTF-8">\n\t\t<fieldset>\t'
    form += '<legend>Filtrar alojamientos</legend>'
    form += '<input type="hidden" name="tipo" value="filtrar" />'
    form += FiltroCategorias().as_p()
    form += FiltroEstrellas().as_p()
    form += '\n\t\t\t<input type="submit" value="Filtrar">\n\t\t</fieldset>'
    form += '\n\t</form><br>'
    return form

def filtrar_idiomas(id_hotel):
    form = '\n\t<FORM action="/alojamientos' + str(id_hotel) + '" name='
    form += '"FiltrarIdioma" method="POST" accept-charset="UTF-8">\n\t\t<fieldset>\t'
    form += '<legend>Seleccion de idioma</legend>'
    form += '<input type="hidden" name="tipo" value="Idioma" />'
    form += FiltroIdioma().as_p()
    form += '\n\t\t\t<input type="submit" value="Aceptar">\n\t\t</fieldset>'
    form += '\n\t</form><br>'
    return form

def CambiarPerfilUsuario(nombre_usuario):
    form = '\n\t<FORM action="/' + nombre_usuario + '" name="PerfilUsuario" '
    form += 'method="POST" accept-charset="UTF-8">\n\t\t<fieldset>\t'
    form += '<legend>Cambiar mi perfil</legend>'
    form += '<input type="hidden" name="tipo" value="PerfilUsuario" />'
    form += PerfilUsuario().as_p()
    form += '\n\t\t\t<input type="submit" value="Confirmar">\n\t\t</fieldset>'
    form += '\n\t</form><br>'
    return form

def Comentar(nombre_usuario, id_hotel):
    form = '\n\t<FORM action="/alojamientos' + str(id_hotel) + '" name='
    form += '"ComentarioUsuario" method="POST" accept-charset="UTF-8">\n\t\t'
    form += '<input type="hidden" name="tipo" value="Comentario" />'
    form += '<textarea name="Comentario" rows="10" cols="50" '
    form += 'placeholder="Introduce tu comentario..."></textarea><br/>'
    form += '\n\t\t<input type="submit" value="Enviar comentario">\n\t</form><br>'
    return form

def Seleccionar(nombre_usuario, id_hotel):
    form = '\n\t<FORM action="/' + nombre_usuario + '" name='
    form += '"Seleccionar" method="POST" accept-charset="UTF-8">\n\t\t'
    form += '<input type="hidden" name="tipo" value="Seleccion" />'
    form += '<input type="hidden" name="idHotel" value="' + str(id_hotel) + '" />'
    form += '\n\t\t<input type="submit" value="Me gusta este alojamiento!">\n\t</form><br>'
    return form

def ActualizarBase():
    form = '\n\t<FORM action="/" name='
    form += '"Actualizar" method="POST" accept-charset="UTF-8">\n\t\t'
    form += '<input type="hidden" name="tipo" value="Actualizar" />'
    form += '\n\t\t<input type="submit" value="Cargar/Actualizar alojamientos!">\n\t</form><br>'
    return form
