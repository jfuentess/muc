import StringIO
import sys
import re
import xml.etree.cElementTree as cElementTree
import diccionario
from types import *

#Inicio de renombre de funciones y variables
oper = diccionario.oper
nario = diccionario.nario 
#Fin de renombre de funciones y variables

#Verifica si un tag se encuentra indexado en el diccionario o no
def definido(tag):
    try:
        oper[tag]
        return True
    except:
        return False


def gen_len_nat(stack):

    op = stack.pop()

    #Workaround para la raiz cuadrada, log en base 10
    if op == "root" and len(stack) == 2:
        op = "root_default"
    if op == "log" and len(stack) == 2:
        op = "log_default"
    if op == "minus" and len(stack) == 2:
        op = "minus_default"
    #Fin de workaround

    output = oper[op]
    element = stack.pop()

    while element != '$':
        #Esto es un workaround, porque el algoritmo no toma en cuenta los parametros de las funciones
        output = re.sub('\$VAR\$', element, output, 1)
        output = re.sub('\$DEGREE\$', element, output, 1)
        #Fin de workaround
        if len(stack) != 1:
            try:
                output = re.sub('\*',nario[op], output, 1)
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

            elif el.tag == "ci" or el.tag == "cn":
                stack.append(el.text) #Apila un numero o el nombre de una variable

            elif definido(el.tag): #verifica que sea funcion u operador
            #else:
                stack.append(el.tag)

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

                    
    return stack

