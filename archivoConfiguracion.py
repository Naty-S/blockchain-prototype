import random


# Lee el archivo configuracion del generador de transacciones
# y retorna la frecuencia y un numero de entrada y uno de salida
# entre los minimos y maximos

def archivoConfigT (arch):				 

	archivoConfig = open(arch,'r')
	parametrosIniciales = archivoConfig.readlines()
	frecuencia = int(parametrosIniciales[0].split(';')[1])
	numEntradasMin = int(parametrosIniciales[1].split(';')[1])
	numEntradasMax = int(parametrosIniciales[2].split(';')[1])
	numSalidasMin  = int(parametrosIniciales[3].split(';')[1])
	numSalidasMax  = int(parametrosIniciales[4].split(';')[1])

	numeroEntradas = random.randint(numEntradasMin, numEntradasMax)
	numeroSalidas  = random.randint(numSalidasMin, numSalidasMax)

	return frecuencia, numeroEntradas, numeroSalidas


# Lee el archivo configuracion del nodo y retorna sus el tamaño maximo
# del bloque, el tiempo promedio de creacion del bloque y la dificultad inicial

def archivoConfigN (arch):

	archivoConfig = open(arch,'r')
	variables = archivoConfig.readlines()
	tamanioMaxBloque = int(variables[0].split(':')[1])
	tiempoPromedioCreacionBloque = int(variables[1].split(':')[1])
	dificultadInicial = int(variables[2].split(':')[1])

	return tamanioMaxBloque, tiempoPromedioCreacionBloque, dificultadInicial







