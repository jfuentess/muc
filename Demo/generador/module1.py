import StringIO
import sys
import re
import xml.etree.cElementTree as cElementTree
from types import *

import module2

def extract_mathml(file_mathml):

	# file_mathml is the file containing the mathml code
	f = open(file_mathml, "r")

	output = ""

	# reads the file file_mathml
	for line in f.readlines():
		output += line

	f.close()

	return output


def parsing(mathml_code):

	# parsing the MathML code
	output = cElementTree.iterparse(StringIO.StringIO(mathml_code), events=("start", "end"))

	return output


	
def generate(context):

	# identifies start and end contexts
	counter = 0

	# Data stack
	stack = []
	tmp = []

	for action, elem in context:
#		print stack
		if action == "start" and elem.tag == "apply":
		        counter = counter + 1
			stack.append("start")

		elif action == "end" and elem.tag == "apply":
		        counter = counter - 1
			while len(stack) > 0:
				element = stack.pop()
			
				if element == "start":
					string = module2.generate(tmp)
					stack.append(string)
					tmp = []
					break
				else:
					tmp.append(element)
								
		elif action == "end" and elem.tag == "set": #Detecta conjuntos (no van incluidos dentro del tag "apply")
			while len(stack) > 0:
				element = stack.pop()
				tmp.append(element)
				if element == "set":
					string = module2.generate(tmp)
					stack.append(string)
					tmp = []
					break

		elif action == "end" and elem.tag == "vector": #Detecta vectores (no van incluidos dentro del tag "apply")
			while len(stack) > 0:
				element = stack.pop()
				tmp.append(element)
				if element == "vector":
					string = module2.generate(tmp)
					stack.append(string)
					tmp = []
					break

		elif action == "end" and elem.tag == "list": #Detecta vectores (no van incluidos dentro del tag "apply")
			while len(stack) > 0:
				element = stack.pop()
				tmp.append(element)
				if element == "list":
					string = module2.generate(tmp)
					stack.append(string)
					tmp = []
					break

		elif action == "end"and elem.tag == "msub":
			subindex = stack.pop()
			base = stack.pop()
			stack.append("(pausa) " + base + " sub " + subindex +" (pausa)")
			

		elif action != "end":
			if elem.tag == "ci" or elem.tag == "cn" or elem.tag == "mi" or elem.tag == "mn":
				if elem.text != None:
					stack.append(elem.text)
			elif elem.tag != "logbase" and elem.tag != "fn" and elem.tag != "msub":
				stack.append(elem.tag)

	return stack


def replace_greek(stack):
	greek_letter = {"alpha": "alfa", "beta": "beta", "gamma": "gama", "delta": "delta", "epsilon": "epsilon", "straightepsilon": "epsilon", "zeta": "zeta", "eta": "eta", "theta": "teta", "iota": "iota", "kappa": "kapa", "lambda": "lambda", "mu": "mu", "nu": "nu", "xi": "xi", "rho": "ro", "sigma": "sigma", "tau": "tau", "upsilon": "upsilon", "phi": "fi", "chi": "chi", "psi": "si", "omega": "omega", "Gamma": "gama mayuscula", "Delta": "delta mayuscula", "Theta": "teta mayuscula", "Lambda": "lambda mayuscula", "Xi": "xi mayuscula", "Pi": "pi mayuscula", "Sigma": "sigma mayuscula", "Upsilon": "upsilon mayuscula", "Phi": "fi mayuscula", "Psi": "si mayuscula", "Omega": "omega mayuscula", "varepsilon": "epsilon", "vartheta": "teta", "varpi": "pi", "varrho": "ro", "varsigma": "sigma", "straightphi": "fi", "varphi": "fi", "pi": "pi"}

	letters = re.findall("#(.*?);",stack)
	for letter in letters:
		stack = re.sub("#(.*?);", greek_letter[letter], stack,1)
	
	return stack

	
def delete_pause(stack):
	output = re.sub("(\(pausa\)\s*)+","(pausa) ", stack) #eliminates repeated pauses

	return output

	
def main():

#	mathml = extract_mathml(sys.argv[1])

	mathml = sys.argv[1]

	# Data stack
	stack = []

	mathml = re.sub("&","#",mathml)# Replace & by #
	
	context = parsing(mathml)

	stack = generate(context)
	stack = stack.pop()
	
	if re.search("#",stack): # Detecta si existen letras griegas en la verbalizacion
		stack = replace_greek(stack)

	stack = delete_pause(stack)
	
	print stack
	
main()
