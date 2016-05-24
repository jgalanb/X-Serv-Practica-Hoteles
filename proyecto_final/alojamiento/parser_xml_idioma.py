#!/usr/bin/python
# -*- coding: utf-8 -*-

#
# Simple XML parser for the RSS channel from BarraPunto
# Jesus M. Gonzalez-Barahona
# jgb @ gsyc.es
# TSAI and SAT subjects (Universidad Rey Juan Carlos)
# September 2009
#
# Just prints the news (and urls) in BarraPunto.com,
#  after reading the corresponding RSS channel.

from xml.sax.handler import ContentHandler
from xml.sax import make_parser
import sys

class myContentHandler(ContentHandler):

    def __init__ (self):
        self.inItem = False
        self.inContent = False
        self.inCategoria = False
        self.inSubCategoria = False
        self.theContent = ""
        self.lista_hoteles = []
        self.dict_hotel = {'name': "", 'web': "", "address": "",
                            'categoria': "", 'subcategoria': "",
                            'url': "", 'email': "", 'phone': "",
                            'body': "", 'zipcode': "",
                            'country': "", 'latitude': "",
                            'longitude': "", 'subAdministrativeArea': ""}


    def startElement (self, name, attrs):
        if name in ['name', 'web', 'address','url', 'email', 'phone', 'body',
                    'zipcode', 'country', 'latitude', 'longitude',
                    'subAdministrativeArea']:
              self.inItem = True
              self.inContent = True

        if name == 'item':
            if attrs.get('name') == "Categoria":
                self.inItem = True
                self.inContent = True
                self.inCategoria = True
            if attrs.get('name') == "SubCategoria":
                self.inItem = True
                self.inContent = True
                self.inSubCategoria = True

    def endElement (self, name):
        if name in ['name', 'web', 'address', 'email', 'phone', 'body',
                    'zipcode', 'country', 'latitude', 'longitude',
                    'subAdministrativeArea']:
            self.dict_hotel[name] = self.theContent
            self.inItem = False
            self.inContent = False
            self.theContent = ""

        if name in ['item']:
            if self.inCategoria:
                self.dict_hotel['categoria'] = self.theContent
                self.inItem = False
                self.inContent = False
                self.inCategoria = False
                self.theContent = ""
            if self.inSubCategoria:
                self.dict_hotel['subcategoria'] = self.theContent
                self.inItem = False
                self.inContent = False
                self.inSubCategoria = False
                self.theContent = ""

        if name in ['url']:
            try:
                self.dict_hotel[name].append(self.theContent)
                self.inItem = False
                self.inContent = False
                self.theContent = ""
            except AttributeError:
                self.dict_hotel[name] = [self.theContent]
                self.inItem = False
                self.inContent = False
                self.theContent = ""

        if name == "service":
            self.lista_hoteles.append(self.dict_hotel)
            self.dict_hotel = {'name': "", 'web': "", "address": "",
                                'categoria': "", 'subcategoria': "",
                                'url': "", 'email': "", 'phone': "",
                                'body': "", 'zipcode': "",
                                'country': "", 'latitude': "",
                                'longitude': "", 'subAdministrativeArea': ""}

    def characters (self, chars):
        if self.inContent:
            self.theContent = self.theContent + chars

# --- Main prog


def get_info_hoteles_idioma(idioma):

    # Load parser and driver

    theParser = make_parser()
    theHandler = myContentHandler()
    theParser.setContentHandler(theHandler)

    # Ready, set, go!
    if idioma == "en":
        xmlURL = "http://cursosweb.github.io/etc/alojamientos_en.xml"
    elif idioma == "fr":
        xmlURL = "http://cursosweb.github.io/etc/alojamientos_fr.xml"
    theParser.parse(xmlURL)
    return theHandler.lista_hoteles
