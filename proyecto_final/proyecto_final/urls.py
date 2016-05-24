from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'myproject.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^login$', 'django.contrib.auth.views.login'),
    url(r'^logout$', 'alojamiento.views.salir_cuenta'),
    url(r'^images/(.*)$','django.views.static.serve',
        {'document_root': 'templates/dreamy/images/'}),
    url(r'^(style-default.css)$', 'django.views.static.serve',
        {'document_root': 'templates/dreamy/'}),
    url(r'^(style-rojo.css)$', 'django.views.static.serve',
        {'document_root': 'templates/dreamy/'}),
    url(r'^(style-azul.css)$', 'django.views.static.serve',
        {'document_root': 'templates/dreamy/'}),
    url(r'^(style-verde.css)$', 'django.views.static.serve',
        {'document_root': 'templates/dreamy/'}),
    url(r'^(style-gris.css)$', 'django.views.static.serve',
        {'document_root': 'templates/dreamy/'}),
    url(r'^(style-amarillo.css)$', 'django.views.static.serve',
        {'document_root': 'templates/dreamy/'}),
    url(r'^(style-naranja.css)$', 'django.views.static.serve',
        {'document_root': 'templates/dreamy/'}),
    url(r'^accounts/profile/$', 'alojamiento.views.acceder_cuenta'),
    url(r'^/?$', 'alojamiento.views.pag_principal'),
    url(r'^/?alojamientos$', 'alojamiento.views.pag_alojamientos'),
    url(r'^alojamientos(\d+)$', 'alojamiento.views.pag_alojamiento'),
    url(r'^/?about$', 'alojamiento.views.pag_about'),
    url(r'^/?(.*)/xml$', 'alojamiento.views.pag_usuario_xml'),
    url(r'^/?(.*)$', 'alojamiento.views.pag_usuario'),

)
