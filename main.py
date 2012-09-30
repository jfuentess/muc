# -*- coding: utf-8 -*-
import re
import urllib2
import sys
import os
import StringIO
import xml.etree.cElementTree as cElementTree
from types import *

import verbalizador

#Inicio de renombre de funciones
verbalizar = verbalizador.verbalizar 
#Fin de renombre de funciones

buscartodo = re.findall

#lista de tuplas (código content MathML,dirección de la imagen que la representa)
formula = []

#e.r. para buscar el codigo en content MathML y su correspondiente imagen
erm = "<img class=\"math\" alt=\"<math>(.*?)</math>\" src=\"(.*?)\""


def main():
    i = int(0)
    opener = urllib2.build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/15.0')]
    HTMLcode = opener.open(sys.argv[1]) #introducir dirección web que tenga el código en MathML

    #Inicio de extraer la codificación de la fórmula en MathML
    for line in HTMLcode:
        formula.extend(buscartodo(erm,line))
    #Fin de extraer la codificación de la fórmula en MathML

    verbalizador.diccionario.generar_operaciones() #Genera diccionario de operaciones
    verbalizador.diccionario.generar_nario() #Genera diccionario de n-arios
    verbalizador.diccionario.generar_param() #Genera diccionario de parametros especiales

    for el in formula: #verbaliza todas los codigos encontrados en la pagina web
        frase = verbalizar(cElementTree.iterparse(StringIO.StringIO(el[0]), events=("start", "end")))
        print frase[1]

main()
