import re

operations = {"divide": "$VAR$ dividido por $VAR$", "power": "$VAR$ elevado a $VAR$", "root_default": "raiz cuadrada de $VAR$", "root" : " $DEGREE$ raiz de $VAR$", "tendsto": "$VAR$ tiende a $VAR$", "sum": "sumatoria $BVAR$ $RANGE$ de $VAR$ $DOMAIN$", "in": "$VAR$ pertenece a $VAR$", "int": "integral $RANGE$ de $VAR$ $BVAR$", "cartesianproduct": "$VAR$ *", "leq": "$VAR$ *", "cos": "coseno de $VAR$", "sin": "seno de $VAR$", "log_default": "logaritmo de $VAR$","log": "logaritmo en base $VAR$ de $VAR$", "ln": "logaritmo natural de $VAR$", "outerproduct": "producto tensorial entre $VAR$ y $VAR$", "limit": "limite de $VAR$ $RANGE$ $DOMAIN$ ", "approx": "$VAR$ es aproximadamente $VAR$", "forall": "para todo $BVAR$ $RANGE$, $VAR$", "compose": "$VAR$ *", "equivalent": "$VAR$ es equivalente a $VAR$", "geq": "$VAR$ *", "eq": "$VAR$ es igual a $VAR$", 
"diff": " $DEGREE$ derivada de $VAR$ $BVAR$", 

"factorial": "factorial de $VAR$", "not" : "no $VAR$", "abs" : "valor absoluto de $VAR$", "minus_default": "menos $VAR$", "minus": "$VAR$ menos $VAR$", "plus": "$VAR$ *", "times": "$VAR$ *", "function": "$FUNCTION$ de $VAR$ *",
"and": "$VAR$ *", "lt": "$VAR$ *", "gt": "$VAR$ *", "neq": "$VAR$ no es igual a $VAR$",
 "or": "$VAR$ *", "union": "$VAR$ *", "intersect": "$VAR$ *", "setdiff": "$VAR$ menos $VAR$", "factorof": "$VAR$ factor de $VAR$", "tan": "tangente de $VAR$", "sec": "secante de $VAR$", "csc": "cosecante de $VAR$", "cot": "cotangente de $VAR$", "sinh": "seno hiperbolico de $VAR$", "cosh": "coseno hiperbolico de $VAR$", "tanh": "tangente hiperbolica de $VAR$", "sech": "secante hiperbolica de $VAR$", "csch": "cosecante hiperbolica de $VAR$", "coth": "cotangente hiperbolica de $VAR$", "arcsin": "arcoseno de $VAR$", "arccos":"arcocoseno de $VAR$", "arctan": "arcotangente de $VAR$", "arcsec": "arcosecante de $VAR$", "arccsc": "arcocosencante de $VAR$", "arccot": "arcocotangente de $VAR$", "arcsinh": "arcoseno hiperbolico de $VAR$", "arccosh": "arcocoseno hiperbolico de $VAR$", "arctanh": "arcotangente hiperbolica de $VAR$", "arcsech": "arcosecante hiperbolica de $VAR$", "arccsch": "arcocosecante hiperbolica de $VAR$", "arccoth": "arcocotangente hiperbolica de $VAR$", "exp": "exponencial de $VAR$", "determinant": "determinante de $VAR$", "gcd": "maximo comun divisor entre $VAR$ *", "lcm": "minimo comun multiplo entre $VAR$ *", "max": "maximo entre $VAR$ *", "min": "minimo entre $VAR$ *", "subset": "$VAR$ *", "prsubset": "$VAR$ *", "set": "conjunto $VAR$ *", "vector": "vector $VAR$ *", "list": "lista $VAR$ *", "notin": "$VAR$ no pertenece a $VAR$",
 "inverse": "inversa de $VAR$"
 }

replace_nary = {"plus": "m&aacute;s $VAR$ *", "times": "por $VAR$ *", "leq": "menor o igual que $VAR$ *", "and": "y $VAR$ *",
"cartesianproduct": "cruz $VAR$ *", "geq": "mayor o igual que $VAR$ *", "compose": "compuesta $VAR$ *", "lt": "menor que $VAR$ *", "gt": "mayor que $VAR$ *", "or": "o $VAR$ *", "union": "union $VAR$ *", "intersect": "interseccion $VAR$ *", "gcd": "coma $VAR$ *", "lcm": "coma $VAR$ *", "max": "coma $VAR$ *", "min": "coma $VAR$ *", "vector": "coma $VAR$ *", "subset": "subconjunto de $VAR$ *", "prsubset": "subconjunto propio de $VAR$ *", "set": "coma $VAR$ *", "vector": "coma $VAR$ *", "list": "coma $VAR$ *", "function": "coma $VAR$ *"
}

#Sirve para transcribir tags especiales (las operaciones trigonometricas en este caso no se aplican como funciones, si no como tags especiales
special = {"cos": "coseno", "sin": "seno", "infinity": "infinito", "eulergamma": "gama", "pi": "pi", "emptyset": "conjunto vacio", "false": "falso", "true": "Verdadero", "integers": "enteros", "reals": "reales", "rationals": "racionales", "naturalnumbers": "numeros naturales", "complexes": "complejos", "primes": "primos", "exponentiale": "exponencial", "tan": "tangente", "sec": "secante", "csc": "cosecante", "cot": "cotangente", "sinh": "seno hiperbolico", "cosh": "coseno hiperbolico", "tanh": "tangente hiperbolica", "sech": "secante hiperbolica", "csch": "cosecante hiperbolica", "coth": "cotangente hiperbolica", "arcsin": "arcoseno", "arccos":"arcocoseno", "arctan": "arcotangente", "arcsec": "arcosecante", "arccsc": "arcocosencante", "arccot": "arcocotangente", "arcsinh": "arcoseno hiperbolico", "arccosh": "arcocoseno hiperbolico", "arctanh": "arcotangente hiperbolica", "arcsech": "arcosecante hiperbolica", "arccsch": "arcocosecante hiperbolica", "arccoth": "arcocotangente hiperbolica", "imaginaryi": "i"
}

#Falta generalizar para los operadores n-arios
def generate(pila):
	operator = ""
	output = ""

	operator = pila.pop()

	#operations unary and binary
	if operator == "root" and len(pila) == 1:
		operator = "root_default"
	if operator == "log" and len(pila) == 1:
		operator = "log_default"
	if operator == "minus" and len(pila) == 1:
		operator = "minus_default"

	try:
		output = operations[operator] #template
	except:
		output = operations['function'] # template general function
	        output = re.sub('\$FUNCTION\$',operator, output, 1)

	range = ""
	bvar = ""
	domain = ""
	degree = ""
	
	limit = False #Sirve para indicar que comenzo un limite. Si despues viene lowlimit, entonces se traduce distinto
	
	while len(pila) > 0:
		element = pila.pop()

		try:
			element = special[element]
		except:
			pass
		
		if operator == "limit":
			limit = True
		
		if element == "bvar":
			tmp = pila.pop()
			bvar += "$PREP$ " + tmp #la preposicion PREP varia segun el operador(sum, diff, int o forall)
			continue #Pasa a la siguiente iteracion

		if element == "uplimit":
			tmp = pila.pop()
			range += " hasta " + tmp
			continue

		if element == "lowlimit":
			tmp = pila.pop()
			if limit != True:
				range += "desde " + tmp
			else:
				range += ", cuando $BVAR$ tiende a " + tmp #Indica que se esta usando bajo el ambito de un limite
			continue

		if element == "condition":
			tmp = pila.pop()
			if limit != True:
				domain += "con " + tmp
			else:
				domain += ", cuando " + tmp #Indica que se esta usando bajo el ambito de un limite
			continue
		if element == "domainofapplication":
			tmp = pila.pop()
			range += "sobre " + tmp
			continue

		if element == "degree":
			tmp = pila.pop()
			degree += tmp
			continue

		if element == "interval":
			tmp1 = pila.pop()
			tmp2 = pila.pop()
			range += "desde " + tmp1 + " hasta " + tmp2
			continue
		if element == "times": #Para el caso de x^{*}
			element = "asterisco"
			
		output = re.sub('\$RANGE\$', range, output, 1)
		output = re.sub('\$DOMAIN\$', domain, output, 1)
		output = re.sub('\$DEGREE\$', degree, output, 1)

		if domain == "": 
			output = re.sub('\$BVAR\$', bvar, output, 1)
		else:
			output = re.sub('\$BVAR\$', "", output, 1)
		
		output = re.sub('\$VAR\$', element, output, 1)

		# Reemplaza $PREP$ por la preposicion correspondiente (para el uso de "bvar")
		if operator == "sum":
			output = re.sub('\$PREP\$', "con", output, 1)
		elif operator == "forall":
			output = re.sub('\$PREP\$', "", output, 1)
		elif operator == "int" or operator == "diff":
			output = re.sub('\$PREP\$', "respecto a", output, 1)
		else:
			output = re.sub('\$PREP\$', "", output, 1)

		try:
		        if len(pila) == 0:
        		        output = re.sub('\*',"", output, 1)
        		else:
        			try:
	                		output = re.sub('\*',replace_nary[operator], output, 1)
	                	except: # Si no es un operador conocido se toma como una funcion
	                		output = re.sub('\*',replace_nary["function"], output, 1)
		except:
			pass
			
			
	output = " (pausa) " + output + " (pausa) "

	return output



