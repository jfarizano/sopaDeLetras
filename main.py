from random import *
from math import *

def main(list):

	letras = "ABCDEFGHIJKLMNÑOPQRSTUVWXYZ"
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

	for i in range(0, len(tablero)):
		if tablero[i] == "":
			tablero[i] = choice(letras)
	imprimirTablero(tablero)

def crearTablero(list):

	rt = palabraMasLarga(list)
	tablero = [""]*rt**2
	return tablero

def imprimirTablero(tablero):

	rt = int(sqrt(len(tablero)))
	filas = []
	for i in range(0, rt):
		filas += [tablero[i * rt: (i * rt) + rt]]
	for fila in filas:
		print(fila)

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

main(["TESTING", "HOLA", "PRUEBA"])
