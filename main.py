import sys
from random import *
from math import *

# Representación de datos
"""
Representamos una sopa de letras de tamaño nxn mediante una lista de tamaño n², donde cada elemento representa
una letra de la misma.
Por ejemplo, el tablero: A B C
						 D E F
						 G H I
es de tamaño 3x3, por lo tanto tiene 9 elementos y está representado por la lista:
["A", "B", "C", "D", "E", "F", "G", "H", "I"]
"""
def main(lista, tablero = []):

	modo = 0

	if len(sys.argv) > 1 and sys.argv[1] in ["1","2","3"]:
		modo = sys.argv[1]
	else:
		mensajeBienvenida = """Bienvenido, ingrese un número para elegir la opción deseada:
		1 - Crear sopa de letras a partir de una lista de palabras
		2 - Buscar la posición de las palabras de una lista en una sopa de letras dada 
		3 - Salir del programa
		"""

		print(mensajeBienvenida)

	while modo not in ["1","2","3"]:
		if modo != 0:
			print("Opción inválida, ingrese un número válido")
			modo = str(input("Modo deseado: "))
		else:
			modo = str(input("Modo deseado: "))

	if modo == "1":
		imprimirTablero(crearSopa(lista))
	elif modo == "2":
		buscarPalabras(lista, tablero)
	elif modo == "3":
		exit()

# Código opción 1

"""
Crea una sopa de letras en base a una lista de strings
"""
def crearSopa(lista):

	direcciones = ["hori1", "hori2", "vert1", "vert2", "diag"]
	tablero = crearTablero(lista)
	listaPalabras = sorted(lista, key=len, reverse=True)

	for palabra in listaPalabras:
		disponibles = []
		intentos = 0

		while disponibles == [] and intentos <= 10:
			direccion = choice(direcciones)
			disponibles = lugaresDisponibles(tablero, palabra, direccion)
			intentos += 1
		if intentos > 10:
			print("No se pudo insertar: ", palabra)
		else:
			pos = choice(disponibles)
			if direccion != "diag":
				if direccion[-1] == "1":
					colocarPalabra(tablero, palabra, direccion, pos)
				else:
					palabra = palabra[::-1]
					colocarPalabra(tablero, palabra, direccion, pos)
			else:
				colocarPalabra(tablero, palabra, direccion, pos)
	
	rellenarTablero(tablero)
	return rellenarTablero(tablero)

"""
Crea un tablero vacio del tamaño necesario en base a una lista de palabras
"""
def crearTablero(lista):

	tamaño = palabraMasLarga(lista) + randint(2,7)
	tablero = [""]*tamaño**2
	return tablero

"""
Imprime la sopa de letras en una forma placentera de leer para el usuario
"""
def imprimirTablero(tablero):

	raiz = int(sqrt(len(tablero)))
	filas = []
	tableroStr = []

	# Convierte la lista plana en lista de filas (matriz)
	for i in range(0, raiz):
		filas += [tablero[i * raiz: (i * raiz) + raiz]]
	# Convierte las filas en string (ahora el tablero es lista de strings)
	for i in range(0, len(filas)):
		tableroStr += [' '.join(filas[i])]
	# Imprime cada fila como string
	for str in tableroStr:
		print(str)

"""
Rellena los espacios vacios de una sopa de letras con letras al azar
"""
def rellenarTablero(tablero):

	letras = "ABCDEFGHIJKLMNÑOPQRSTUVWXYZ"

	for i in range(0, len(tablero)):
		if tablero[i] == "":
			tablero[i] = choice(letras)
	return tablero

"""
Devuelve un entero con el largo del string de mayor longitud de una lista
"""
def palabraMasLarga(lista):
	max = 0
	for palabra in lista:
		if len(palabra) > max:
			max = len(palabra)
	return max

"""
Devuelve una lista de los posibles lugares donde una palabra se puede insertar, dada una direccion.
"""
def lugaresDisponibles(tablero, palabra, direccion):

	raiz = int(sqrt(len(tablero)))
	length = len(palabra)
	pos = []

	if direccion == "diag":
		for i in range(0, len(tablero)):
			final = i + (length-1)*(raiz+1)
			if tablero[i:final+1:raiz+1] == [""]*length and diagValida(tablero, palabra, i):
				pos += [i]
	elif direccion[:4] == "veraiz":
		for i in range(0, (raiz-length+1)*raiz):
			if i == 0:
				ultima = raiz * length-1
				columna = tablero[i:ultima:raiz]
				if columna == [""]*length:
					pos += [i]
			else:
				ultima = (raiz * length-1) + i
				columna = tablero[i:ultima:raiz]
				if columna == [""]*length:
					pos += [i]
	elif direccion[:4] == "hori":
		filas = []
		for i in range(0, raiz):
			filas += [tablero[i * raiz: (i * raiz) + raiz]]
		for i in range(0, raiz):
			for j in range(0, raiz-length+1):
				if filas[i][j:j + length] == [""] * length:
					pos += [(i*raiz)+j]
	return pos

"""
Devuelve un booleano que indica si una palabra dada entra en la diagonal de la casilla del tablero dado
"""
def diagValida(tablero, palabra, casilla):
	raiz = int(sqrt(len(tablero)))
	length = len(palabra)
	filas = []
	listaNum = [n for n in range(0, raiz**2)]

	for i in range(0, raiz):
		filas += [listaNum[i * raiz: (i * raiz) + raiz]]
	for j in range(0, raiz):
		for k in range(0, raiz):
			if casilla == filas[j][k] and k <= (raiz-length):
				return True

"""
Inserta la palabra en el tablero en la direccion y posicion dados
"""
def colocarPalabra(tablero, palabra, direccion, pos):

	raiz = int(sqrt(len(tablero)))
	length = len(palabra)
	contador = 0

	if direccion == "diag":
		for i in range(0, length):
			tablero[pos + (raiz+1)*i] = palabra[contador]
			contador += 1
	elif direccion[:4] == "vert":
		for i in range(0, length):
			tablero[pos + raiz*i] = palabra[contador]
			contador += 1
	elif direccion[:4] == "hori":
		for i in range(0, length):
			tablero[pos+i] = palabra[contador]
			contador += 1

# Código opción 2:

"""
Busca una lista de palabras en la sopa, devuelve una lista con cada palabra encontrada, su posicion y direccion
"""
def buscarPalabras(palabras, tablero):

	direcciones = ["hori1", "hori2", "vert1", "vert2", "diag"]
	encuentros = []

	for palabra in palabras:
		length = len(palabra)
		raiz = int(sqrt(len(tablero)))
		for i in range(0, len(tablero)):
			if ''.join(tablero[i:i+length]) in [palabra, palabra[::-1]]:
				encuentros += [{'palabra': palabra, 'dir': 'horizontal' , 'pos': i}]
			elif ''.join(tablero[i::raiz][:length]) in [palabra, palabra[::-1]]:
				encuentros += [{'palabra': palabra, 'dir': 'vertical' , 'pos': i}]
			elif ''.join(tablero[i::1+raiz][:length]) in [palabra, palabra[::-1]]:
				encuentros += [{'palabra': palabra, 'dir': 'diag' , 'pos': i}]
	[print(encuentro) for encuentro in encuentros]
	return encuentros
"""
Inicializa el programa con unos valores predefinidos para pruebas
"""
def start():
	palabrasPrueba = []
	
	#tableroPrueba = ['Y', 'L', 'G', 'A', 'W', 'O', 'J', 'G', 'A', 'N', 'S', 'I', 'P', 'Z', 'O', 'B', 'I', 'A', 'R', 'C', 'D', 'C', 'E', 'T', 'C', 'Z', 'X', 'E', 'R', 'U', 'S', 'M', 'T', 'Z', 'S', 'A', 'R', 'E', 'A', 'L', 'O', 'H', 'B', 'P', 'T', 'J', 'D', 'G', 'M']
	
	with open("palabras", "r") as palabras:
		for palabra in palabras.readlines():
			palabrasPrueba += [palabra.strip()]
		palabras.close()
	tableroPrueba = crearSopa(palabrasPrueba)
	main(palabrasPrueba, tableroPrueba)

start()
