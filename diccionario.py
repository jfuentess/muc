import sys
import os
import csv

#guarda las plantillas de las operaciones
#indexadas por su nombre (de tag)
oper = {}

#para los asteriscos (n-arios) de las plantillas
nario = {}

#Para realizar el unescaping HTML (transforma a unicode)
chtml = {'aacute':u'\xe1', 'eacute':u'\xe9', 'iacute':u'\xed', 'oacute':u'\xf3', 'uacute':u'\xfa', 'ntilde':u'\xf1', 'auml':u'\xe4', 'euml':u'\xeb', 'iuml':u'\xef', 'ouml':u'\xf6', 'uuml':u'\xfc'}

#genera el diccionario de operaciones
def generar_operaciones():
    input = csv.reader(open('operaciones.csv','rb'))
    for t in input:
        oper[t[0]] = t[1]

#genera el diccionario de n-arios
def generar_nario():
    input = csv.reader(open('nario.csv','rb'))
    for t in input:
        nario[t[0]] = t[1]

