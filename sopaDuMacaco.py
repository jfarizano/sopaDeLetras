from math import *
from random import *

def lugaresDisponibles(tablero, palabra, dir):
    length = len(palabra)
    size = int(sqrt(len(tablero)))
    pos = []
    if dir == "vert":
        for i in range(0, len(tablero)):
            if i == 0:
                ultima = size * length-1
                columna = tablero[i:ultima:size]
                if columna == [""]*length:
                    pos += [i]
            else:
                ultima = (size * length-1) + i
                columna = tablero[i:ultima:size]
                if columna == [""]*length:
                    pos += [i]
        return pos
    if dir == "horiz":
        filas = []
        for i in range(0, size):
            filas += [tablero[i*size: (i*size)+size]]
        for i in range(0, size):
            for j in range(0, size-length):
                if filas[i][j:j+length] == [""]*length:
                    pos += [(i*size)+j]
        return pos



def test():
    size = 5
    tablero = [""] * (size**2)
    tablero[0] = "A"
    tablero[3] = "A"
    tablero[15] = "A"
    tablero[24] = "A"

    lugares = lugaresDisponibles(tablero, "AAAA", "horiz")
    print(lugares)

test()

