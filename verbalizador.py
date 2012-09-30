import StringIO
import sys
import re
import xml.etree.cElementTree as cElementTree
import diccionario
from types import *

#Inicio de renombre de funciones y variables
oper = diccionario.oper
nario = diccionario.nario
chtml = diccionario.chtml
param = diccionario.param
#Fin de renombre de funciones y variables

#Realiza el unescape HTML
def unescapeHtml(c):
    tmp = []
    tmp = re.findall("&(.*?);",c)
    for a in tmp:
        c = re.sub('&'+a+';', chtml[a], c, 1)
    return c


#Verifica si un tag se encuentra indexado en el diccionario o no
def definido(tag):
    try:
        oper[tag]
        return True
    except:
        return False

def esParam(tag):
    try:
        param[tag]
        return True
    except:
        return False


def gen_len_nat(stack):

    op = stack.pop()
    #Workaround para la raiz cuadrada, log en base 10
    if op[1:] == "root" and len(stack) == 2:
        op = "%root_default"
    if op[1:] == "minus" and len(stack) == 2:
        op = "%minus_default"
    #Fin de workaround

    output = oper[op[1:]]#buscar plantilla adecuada al operador

    element = stack.pop()
    p = []

    while element != '$':
        #Inicio de reemplazo de parametros especiales (ej:Logaritmo (en base x)? de ...)
        if element[0] == '-':
            p = re.findall("-(.*?):(.*?);",element)
            if len(p) != 0:
                fra = re.sub('\$VAR\$', p[0][1] , param[p[0][0]], 1)
                output = re.sub('\$FRA\$', fra, output, 1)

        elif esParam(op[1:]+"_default"):
            output = re.sub('\$FRA\$', param[op[1:]+"_default"], output, 1)
            output = re.sub('\$VAR\$', element, output, 1)
        #Fin de reemplazo de parametros especiales

        #Reemplaza la primera variable que encuentre con el elemento correspondiente
        #Fin reemplazar las variables
        else:
            output = re.sub('\$VAR\$', element, output, 1)
            output = re.sub('\$DEGREE\$', element, output, 1)
            if len(stack) != 1:
                try:
                    output = re.sub('\*',nario[op[1:]], output, 1)
                except: # Si no es un operador conocido se toma como una funcion
                    output = re.sub('\*',nario["function"], output, 1)
            
        element = stack.pop()

    output = re.sub('\*',"", output, 1)
    output = "<p> " + output + "</p>"

    return output


#recibe codigo en MathML con el cual genera el stack necesario
def verbalizar(mathml):

    stack = ['$'] # Pila
    tmp = ['$'] # Pila auxiliar

    for action, el in mathml:
        if action == "start":
            if el.tag == "apply":
                stack.append("start")

            elif el.tag == "ci":
                stack.append("@"+el.text) #Apila el nombre de un identificador

            elif el.tag == "cn":
                stack.append("#"+el.text) #Apila un numero

            elif definido(el.tag): #Apila el nombre de un operador
                stack.append("%"+el.tag)
            #Para apilar el nombre de un parametro de funcion.
            else:
                stack.append("-"+el.tag)

        else: #tag de cierre implica generar lenguaje natural

            if el.tag == "apply":
                element = stack.pop()
                while element != '$':    
                    if element == "start":
                        stack.append(gen_len_nat(tmp))
                        tmp = ['$']
                        break
                    else:
                        tmp.append(element)
                    element = stack.pop()

            #Si es un tag de cierre de parametro entonces se le antecede
            #un "-" al parametro para elegir la plantilla adecuada en el
            #caso de que se requiera una default o no
            elif esParam(el.tag):
		p = el.tag
                p = "-"+p+":"+stack.pop()+";"
                element = stack.pop()
                stack.append(p)

    stack[1] = unescapeHtml(stack[1])
    return stack

