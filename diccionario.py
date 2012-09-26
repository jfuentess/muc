import sys
import os
import csv

#guarda las plantillas de las operaciones
#indexadas por su nombre (de tag)
oper = {}

#para los asteriscos (n-arios) de las plantillas
nario = {}

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

