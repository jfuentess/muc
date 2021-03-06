import re
import urllib2
import sys
import os

opener = urllib2.build_opener()
opener.addheaders = [('User-agent', 'Mozilla/5.0')]
HTMLcode = opener.open(sys.argv[1])

for line in HTMLcode:
	if re.search("\<a href=", line): # Redirige los link para que puedan ser capturados por reader.php
		link = re.search("href=\"(.*?)\"",line).group(1)
		es_wiki = "http://es.wikipedia.org"
		line = re.sub("href=\"(.*?)\"","href=\"http://" + sys.argv[2] + ":" + sys.argv[3] + sys.argv[4] + "?url=" + es_wiki + link + "\"",line)

	expressions = [] #Almacenara temporalmente las verbalizaciones resultantes en cada linea
	alts = [] #Almacenara temporalmente el contenido de las etiquetas alt de cada linea
	if re.search("\<img class=\"tex\"", line): #Filtra las lineas que contengan expresiones matematicas
		for latex in re.finditer("alt=\"(.*?)\"", line): #Itera por cada expresion matematica que aparezca en la linea
			output = ""
			try:
				mathtex = re.sub("alt=","",latex.group(0)) # Elimina la aparicion de "alt="

				mathtex = re.sub("\\\\textstyle","",mathtex) # Elimina \\textstyle
				mathtex = re.sub("\"","",mathtex) # Elimina las apariciones de ". \,"
				mathtex = re.sub("\\\, \.","",mathtex) # Elimina "\, .", en ocasiones van al final de las expresiones  
				mathtex = re.sub("\.\\\,","",mathtex) # Elimina ".\,", en ocasiones van al final de las expresiones  
				mathtex = re.sub("\. \\\,","",mathtex) # Elimina " . \,", en ocasiones van al final de las expresiones  
				mathtex = re.sub("\\\,","",mathtex) # Elimina las apariciones de "\,"
				mathtex = re.sub("\\\!","",mathtex) # Elimina las apariciones de "\!"
				mathtex = re.sub("\\\ "," ",mathtex) # Elimina las apariciones de "\ "
				mathtex = re.sub("(\.\s)$","",mathtex) # Elimina las apariciones de ". " al final de las expresiones
				mathtex = re.sub("(\.)$","",mathtex) # Elimina las apariciones de "." al final de las expresiones
				mathtex = re.sub("\\\iff","\\\Leftrightarrow",mathtex) # Reemplaza \iff por \Leftrightarrow (\iff se interpretaba como una multiplicacion)
				mathtex = re.sub("&lt;","<",mathtex) # Reemplaza &lt; por <
				mathtex = re.sub("&gt;",">",mathtex) # Reemplaza &gt; por >
				mathtex = re.sub("~","",mathtex) # Elimina ~
				mathtex = re.sub("\\\\ne ","\\\\neq ",mathtex) # Reemplaza \ne por \neq 
				mathtex = re.sub("\\\\\{","",mathtex) # Elimina \{ 
				mathtex = re.sub("\\\\\}","",mathtex) # Elimina \}
				mathtex = re.sub("\\\\empty","\\\\emptyset",mathtex) # Reemplaza \empty por \emptyset 
				mathtex = re.sub("\\\\emptysetset","\\\\emptyset",mathtex) # Reemplaza \emptysetset por \emptyset
				mathtex = re.sub("\\\\scriptstyle","",mathtex) # Elimina \scriptstyle
				mathtex = re.sub("\\\\tfrac\{", "\\\\frac{",mathtex) # Reemplaza \tfrac por \frac
				valores = re.findall("\\\\math(.*?){(.*?)}", mathtex) # Elimina las ocurrencias de \mathbf, \mathbb, \mathcal

				for valor in valores:
					mathtex = re.sub("\\\\math(.*?){(.*?)}", " " + valor[1], mathtex, 1)
					
				valores = re.findall("\\\\textrm{(.*?)}", mathtex) # Elimina las ocurrencias de \textrm

				for valor in valores:
					mathtex = re.sub("\\\\textrm{(.*?)}", " " + valor, mathtex, 1)

				decimal = re.search(",[0-9]", mathtex) # Reemplaza "," por "." en los numeros decimales y no en los vectores
				
				try:
					mathtex = re.sub(",[0-9]", "."+re.sub(",","",decimal.group(0)), mathtex)
				except:
					pass

								
				special_symbol = "\\\\assumeSymbol{f}{function} \\\\assumeSymbol{f_n}{function} \\\\assumeSymbol{F}{function} \\\\assumeSymbol{g}{function} \\\\assumeSymbol{i}{imaginaryNumber} \\\\assumeSymbol{\pi}{constantPi} \\\\assumeSymbol{\gamma}{eulerGamma} \\\\setUpConversionOption{doContentMathML}{true} " #Macros para ser interpretados por snuggleTex
				mathtex = "\"" + special_symbol + "\$ " + mathtex + " \$\"" #Entrada a SnuggleTex
				mathml = os.popen("export LANG=en_US.UTF-8; java -cp .:snuggletex-upconversion-1.2.2.jar:snuggletex-core-1.2.2.jar:saxon9-dom-9.1.0.8.jar:saxon9-9.1.0.8.jar LatextoMathml " + mathtex, "r").read() # Ejecucion SnuggleTex
				if len(mathml) > 0: #Obtiene el Content-MathML de la salida de SnuggleTex
					line_mathml = re.split(r"\n",mathml)

					content = False
					input_mathml = ""

					for tag in line_mathml:
						if re.search("/annotation-xml",tag):
							content = False

						if content: 
							input_mathml += tag

						if re.search("MathML-Content\"",tag):
							content = True
							
					input_mathml = re.sub("\"","\\\"",input_mathml) # reemplaza " por \"
					input_mathml = re.sub(">(\s)+",">",input_mathml)

					output = os.popen("python generador/module1.py \"" + input_mathml + "\"", "r").read() #salida de la Verbalizacion
					if len(output) == 0:					
						output = "No se puede generar texto"

				else:
					output = "No se puede generar texto"
					
#				print "<font color=\"#ff0000\">"
#				print "Verbalizaci&oacute;n: " + output + "<br/>"
#				print "</font>"

				expressions.append(output) # Agrega una Verbalizacion
				alts.append(latex.group(1)) # Agrega el contenido de la etiqueta alt que fue verbalizado

			except:
				pass

		cont = 0
		new_line = ""
		for m in re.split("<img",line): # Inserta la verbalizacion en una etiqueta "verb"
			if re.search("alt=\"(.*?)\"", m):
				if re.search("\\\\g(.*?)", alts[cont]): # Solo para el caso que aparezca una keyword de latex que comience con "\g"
					sustitution = re.sub('alt="(.*?)"', 'verb="' + expressions[cont] + '"',m)
					sustitution = 'alt="' + alts[cont] + '"'+ sustitution
				else:	
					sustitution = re.sub('alt="(.*?)"', 'alt="'+alts[cont]+'" verb="' + expressions[cont] + '"',m)
				new_line = new_line + "<font color=\"#ff0000\"><b> [" + expressions[cont] + "] </b></font><img " + sustitution # Rearma la linea con las verbalizacione incluidas
				cont = cont +1

			else:
				if re.search("class=\"tex\"", m):
					new_line = new_line + m # Rearma la linea con las verbalizacione incluidas
				else:
					new_line = new_line + m

		line = new_line

	print line

