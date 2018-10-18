import sys
from random import *
from math import *
from pathlib import Path

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

# Funciones principales

def main():
	"""
	main: File File -> File
	Dados los archivos de textos que representan la lista de palabras y una sopa de letras, inicia el programa

	"""
	listaPalabras = []

	# Si no existen alguno de los archivos, crea uno vacío
	for archivo in ["tablero.txt", "palabras.txt"]:
		if not Path(archivo).is_file():
			open(archivo, "w").close()

	# Lee el archivo con las palabras (palabras.txt), y crea una lista de palabras con las mismas dadas
	with open("palabras.txt", "r") as palabrasArchivo:
		for palabra in palabrasArchivo.readlines():
			listaPalabras += [palabra.upper().strip()]

	# Lee el archivo con el tablero (tablero.txt), y crea una lista con cada caracter alfanumérico
	with open("tablero.txt", "r") as tableroArchivo:
		tablero = [char for char in tableroArchivo.read().split() if len(char) == 1]

	# Llama a la función para elegir el modo
	sopaDeLetras(listaPalabras, tablero)

def sopaDeLetras(listaPalabras, tablero):
	"""
	sopaDeLetras: List(String) List(String) -> String
	Dada una lista de palabras o una lista de palabras y una lista que representa un tablero,
	da a elegir al usuario si quiere crear una sopa de letras con la lista de palabras dadas o buscar la posición de
	las palabras dadas en el tablero dado.
	"""

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
		if listaPalabras == []:
			print("Error: archivo palabras.txt vacío")
		else:
			tablero = tableroAString(crearSopa(listaPalabras))

			# Escribe el tablero al archivo tablero.txt
			with open("tablero.txt", "w") as tableroArchivo:
				tableroArchivo.write(tablero)

			print("\nTablero creado, revise el archivo tablero.txt que se encuentra en el directorio del programa")
	elif modo == "2":
		if listaPalabras == [] or tablero == []:
			print("Error: archivo palabras.txt y/o tablero.txt vacío/s")
		else:
			return buscarPalabras(listaPalabras, tablero)
	elif modo == "3":
		exit()

# Código opción 1

def crearSopa(lista):
	"""
	crearSopa: List(String) -> List(String)
	Dada una lista de palabras. devuelve una sopa de letras con todas las palabras de la misma
	"""

	direcciones = ["hori1", "hori2", "vert1", "vert2", "diag"]
	tablero = crearSopaVacia(lista)

	# Ordena la lista por longitud de palabra, en orden descendiente
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
	return rellenarTablero(tablero)

def crearSopaVacia(lista):
	"""
	crearSopaVacia: List(String) -> List(String)
	Dada una lista de palabras, devuelve una lista de tamaño n² que representa el tablero de la sopa de letras, donde
	n es la longitud de la palabras más larga de la lista dada más un entero en el rango [2,6]
	"""

	tamaño = max(ceil(sqrt(sumaLongitudesPalabras(lista))), palabraMasLarga(lista)) + randint(2,7)
	tablero = [""]*tamaño**2
	return tablero

def palabraMasLarga(lista):
	"""
	palabraMasLarga: List(String) -> Int
	Dada una lista de strings, devuelve la longitud del string más largo
	"""

	max = 0
	for palabra in lista:
		if len(palabra) > max:
			max = len(palabra)
	return max

def tableroAString(tablero):
	"""
	tableroAString: List(String) -> List(String)
	Dado el tablero, lo convierte a un string
	"""

	raiz = int(sqrt(len(tablero)))
	filas = []
	tableroFilasStr = []
	tableroStr = ""

	# Convierte la lista plana en lista de filas (matriz)
	for i in range(0, raiz):
		filas += [tablero[i * raiz: (i * raiz) + raiz]]
	# Convierte las lista en una nueva lista donde cada elemento es un string que representa la fila
	for i in range(0, len(filas)):
		tableroFilasStr += [' '.join(filas[i])]
	# Convierte la lista de filas en un tablero representado por un string
	for i in range(0, len(tableroFilasStr)):
		tableroStr = tableroStr + tableroFilasStr[i] + "\n"

	return tableroStr

def rellenarTablero(tablero):
	"""
	rellenarTablero: List(String) -> List(String)
	Dado un tablero, rellena todas las posiciones vacías con una letra del alfabeto al azar
	"""

	letras = "ABCDEFGHIJKLMNÑOPQRSTUVWXYZ"

	for i in range(0, len(tablero)):
		if tablero[i] == "":
			tablero[i] = choice(letras)
	return tablero

def sumaLongitudesPalabras(lista):
	"""
	sumaLongitudesPalabras: List(String) -> Int
	Dada una lista de palabras, devuelve la suma de la longitud de todas las palabras en la misma.
	"""

	suma = 0

	for palabra in lista:
		suma += len(palabra)
	return suma

def lugaresDisponibles(tablero, palabra, direccion):
	"""
	lugaresDisponibles: List(String) String String -> List(Int)
	Dado el tablero, la palabra a colocar y la dirección en que se desea colocar, devuelve las posiciones iniciales
	posibles donde la palabra se puede colocar en esa dirección en el tablero
	"""

	raiz = int(sqrt(len(tablero)))
	length = len(palabra)
	pos = []

	if direccion == "diag":
		for i in range(0, len(tablero)):
			final = (length-1)*(raiz+1) + i +1
			diagonal = tablero[i:final:raiz+1]
			if diagonalDisponible(palabra, diagonal) and diagValida(tablero, palabra, i):
				pos += [i]
	elif direccion[:4] == "vert":
		for i in range(0, (raiz-length+1)*raiz):
			ultima = (raiz * length-1) + i
			columna = tablero[i:ultima:raiz]
			if len(columna) == len(palabra):
				if columnaDisponible(palabra, columna, direccion):
					pos += [i]
	elif direccion[:4] == "hori":
		filas = []
		# Convierte la lista plana en lista de filas (matriz)
		for i in range(0, raiz):
			filas += [tablero[i * raiz: (i * raiz) + raiz]]
		# Secciona las filas en sublistas de tamaño igual a la longitud de la palabra
		for i in range(0, raiz):
			for j in range(0, raiz-length+1):
				fila = filas[i][j:j + length]
				if filaDisponible(palabra, fila, direccion):
					pos += [(i*raiz)+j]
	return pos

def filaDisponible(palabra, fila, direccion):
	"""
	filaDisponible: List(String) String List(String) String -> Boolean
	Dada la palabra a colocar y la fila en que se desea colocar, devuelve True si es posible colocarla en la dirección
	y sentido dado, en caso contrario devuelve False
	"""

	contador = 0

	# Convierte el string a lista de strings
	if direccion[-1] == "1":
		letras = [letra for letra in palabra]
	else:
		letras = [letra for letra in palabra[::-1]]

	# Devuelve False si el espacio para un caracter está ocupado por un string distinto de vacío y distinto de la letra que irá en ese espacio
	for i in range(0, len(letras)):
		if fila[i] not in ["",letras[contador]]:
			return False
		contador += 1
	return True


def columnaDisponible(palabra, columna, direccion):
	"""
	columnaDisponible: List(String) String List(String) String -> Boolean
	Dada la palabra a colocar y la columna en que se desea colocar, devuelve True si es posible colocarla en la dirección
	y sentido dado, en caso contrario devuelve False
	"""

	contador = 0

	# Convierte el string a lista de strings
	if direccion[-1] == "1":
		letras = [letra for letra in palabra]
	else:
		letras = [letra for letra in palabra[::-1]]
	
	# Devuelve False si el espacio para un caracter está ocupado por un string distinto de vacío y distinto de la letra que irá en ese espacio
	for i in range(0, len(letras)):
		if columna[i] not in ["",letras[contador]]:
			return False
		contador += 1
	return True
	
def diagonalDisponible(palabra, diagonal):
	"""
	diagonalDisponible: List(String) String List(String) String -> Boolean
	Dada la palabra a colocar y la diagonal en que se desea colocar, devuelve True si es posible colocarla en la dirección
	y sentido dado, en caso contrario devuelve False
	"""

	letras = [letra for letra in palabra]
	contador = 0

	if len(diagonal) == len(letras):
		for i in range(0, len(letras)):
			if diagonal[i] != "" and diagonal[i] != letras[contador]:
				return False
			contador += 1
		return True
	else:
		return False

def diagValida(tablero, palabra, pos):
	"""
	diagValida: List(String) String Int -> Boolean
	Dado el tablero, una palabra y un número que representa una posición del tablero, devuelve True si la palabra se
	puede colocar en la diagonal de esa casilla, en caso contrario devuelve False
	"""

	raiz = int(sqrt(len(tablero)))
	length = len(palabra)
	filas = []
	listaNum = [n for n in range(0, raiz**2)]

	for i in range(0, raiz):
		filas += [listaNum[i * raiz: (i * raiz) + raiz]]
	for j in range(0, raiz):
		for k in range(0, raiz):
			if pos == filas[j][k] and k <= (raiz-length):
				return True

def colocarPalabra(tablero, palabra, direccion, pos):
	"""
	colocarPalabra: List(String) String String Int -> List(String)
	Dado el tabalero, una palabra, una dirección y una casilla, modifica el tablero con la palabra colocada en la
	dirección y posición dada.
	"""

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

def buscarPalabras(palabras, tablero):
	"""
	buscarPalabras: List(String) List(String) -> List(Dictionary(String String String String String Int))
	Dada una lista de palabras y una sopa de letras, devuelve una lista de diccionarios, que representan la posición
	y la dirección en que se encuentran esas palabras.
	"""
	
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
				encuentros += [{'palabra': palabra, 'dir': 'diagonal' , 'pos': i}]

	# Imprime las posiciones de cada palabra de forma legible
	for encuentro in encuentros:
		coordenadas = obtenerCoordenada(tablero, encuentro['pos'])
		fila = str(coordenadas[0])
		columna = str(coordenadas[1])
		print("La palabra " + encuentro['palabra'] + " se encuentra en la fila " + fila + " y columna " + columna + " de forma " + encuentro['dir'])

def obtenerCoordenada(tablero, pos):
	"""
	obtenerCoordenadas: List(String) Int -> Int Int
	Dada una sopa de letras representada mediante una lista plana y una posición en esa lista, devuelve las coordenadas x e y de
	esa posición si la lista fuera una matriz
	"""

	tamaño = len(tablero)
	raiz = int(sqrt(len(tablero)))
	listaNum = []
	filas = []
	coordenadas = []

	for i in range(0, tamaño):
		listaNum += [i]
	for i in range(0, raiz):
			filas += [listaNum[i * raiz: (i * raiz) + raiz]]
	for i in range(0, raiz):
		for j in range(0, raiz):
			if filas[i][j] == pos:
				coordenadas += [i] + [j]
				return coordenadas
		
# Llamada para iniciar el programa
main()
