from random import *
from math import *

def main(list, tablero = []):

	mensajeBienvenida = """Bienvenido, ingrese un número para elegir la opción deseada:
	1 - Crear sopa de letras a partir de una lista de palabras
	2 - Buscar la posición de las palabras de una lista en una sopa de letras dada 
	3 - Salir del programa
	"""

	print(mensajeBienvenida)
	modo = 0

	while modo != "1" and modo != "2" and modo != "3":
		if modo != 0:
			print("Opción inválida, ingrese un número válido")
			modo = str(input("Modo deseado: "))
		else:
			modo = str(input("Modo deseado: "))

	if modo == "1":
		crearSopa(list)
	elif modo == "2":
		buscarPalabras(list, tablero)
	else:
		exit()

# Código opción 1

def crearSopa(list):

	direcciones = ["hori1", "hori2", "vert1", "vert2", "diag"]
	tablero = crearTablero(list)
	listaPalabras = sorted(list, key=len, reverse=True)

	for palabra in listaPalabras:
		disponibles = []
		while disponibles == []:
			direccion = choice(direcciones)
			disponibles = lugaresDisponibles(tablero, palabra, direccion)
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
	print("\n")
	imprimirTablero(tablero)

def crearTablero(list):

	rt = palabraMasLarga(list)
	tablero = [""]*rt**2
	return tablero

def imprimirTablero(tablero):

	rt = int(sqrt(len(tablero)))
	filas = []
	tableroStr = []

	# Convierte la lista plana en lista de filas (matriz)
	for i in range(0, rt):
		filas += [tablero[i * rt: (i * rt) + rt]]
	# Convierte las filas en string (ahora el tablero es lista de strings)
	for i in range(0, len(filas)):
		tableroStr += [listaAString(filas[i])]
	# Imprime cada fila como string
	for str in tableroStr:
		print(str)

def listaAString(list):
	str = ""
	for i in range(0, len(list)):
		str = str + list[i] + " "

	return str

def rellenarTablero(tablero):

	letras = "ABCDEFGHIJKLMNÑOPQRSTUVWXYZ"

	for i in range(0, len(tablero)):
		if tablero[i] == "":
			tablero[i] = choice(letras)

def palabraMasLarga(list):

	max = 0
	for palabra in list:
		if len(palabra) > max:
			max = len(palabra)
	return max

def lugaresDisponibles(tablero, palabra, direccion):

	rt = int(sqrt(len(tablero)))
	length = len(palabra)
	pos = []

	if direccion == "diag":
		for i in range(0, len(tablero)):
			final = i + (length-1)*(rt+1)
			if tablero[i:final+1:rt+1] == [""]*length and diagValida(tablero, palabra, i):
				pos += [i]
	elif direccion[:4] == "vert":
		for i in range(0, (rt-length+1)*rt):
			if i == 0:
				ultima = rt * length-1
				columna = tablero[i:ultima:rt]
				if columna == [""]*length:
					pos += [i]
			else:
				ultima = (rt * length-1) + i
				columna = tablero[i:ultima:rt]
				if columna == [""]*length:
					pos += [i]
	elif direccion[:4] == "hori":
		filas = []
		for i in range(0, rt):
			filas += [tablero[i * rt: (i * rt) + rt]]
		for i in range(0, rt):
			for j in range(0, rt-length+1):
				if filas[i][j:j + length] == [""] * length:
					pos += [(i*rt)+j]
	return pos

def diagValida(tablero, palabra, casilla):

	rt = int(sqrt(len(tablero)))
	length = len(palabra)
	filas = []
	listaNum = [n for n in range(0, rt**2)]

	for i in range(0, rt):
		filas += [listaNum[i * rt: (i * rt) + rt]]
	for j in range(0, rt):
		for k in range(0, rt):
			if casilla == filas[j][k] and k <= (rt-length):
				return True

def colocarPalabra(tablero, palabra, direccion, pos):

	rt = int(sqrt(len(tablero)))
	length = len(palabra)
	contador = 0

	if direccion == "diag":
		for i in range(0, length):
			tablero[pos + (rt+1)*i] = palabra[contador]
			contador += 1
	elif direccion[:4] == "vert":
		for i in range(0, length):
			tablero[pos + rt*i] = palabra[contador]
			contador += 1
	elif direccion[:4] == "hori":
		for i in range(0, length):
			tablero[pos+i] = palabra[contador]
			contador += 1

# Código opción 2:

def buscarPalabras(list, tablero):
	print(list)
	imprimirTablero(tablero)

#crearSopa(["TESTING", "HOLA", "PRUEBA", "WIRZT", "CASA", "BARCO"])
#crearSopa(["TESTING", "HOLA", "PRUEBA", "WIRZT", "CASA", "BARCO", "DIAGONAL", "TELE", "PUÑO", "GANCHO"])
tableroPrueba = ['Y', 'L', 'G', 'A', 'W', 'O', 'J', 'G', 'A', 'N', 'S', 'I', 'P', 'Z', 'O', 'B', 'I', 'A', 'R', 'C', 'D', 'C', 'E', 'T', 'C', 'Z', 'X', 'E', 'R', 'U', 'S', 'M', 'T', 'Z', 'S', 'A', 'R', 'E', 'A', 'L', 'O', 'H', 'B', 'P', 'T', 'J', 'D', 'G', 'M']
main(["TESTING", "HOLA", "PRUEBA", "WIRZT", "CASA", "BARCO"], tableroPrueba)
#imprimirTablero(tableroPrueba)
