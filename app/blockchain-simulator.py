from genIdentities import genIdentities
from genTransactions import genTransactions


def blockchain_simulator():
  genIdentities(i, n)
  genNetFile(n, m)
  genTransConfigFile()
  genBlockConfigFile()
  genTransactions(f, d)


def genNetFile(nodos, pares):

  with open("../data/netFile.txt", "w") as outfile:

    outfile.write(nodos+'\n')
    n = 0
    nodo
    while n < nodos:
      outfile.write(nodo[n].name+' '+nodo[n].port+'\n')
      n += 1

    outfile.write(pares+'\n')
    m = 0
    nodo1
    nodo2
    while m < pares:
      outfile.write(nodo1[m].name+m+' '+nodo2[m].name+m+'\n')
      m += 1


def genTransConfigFile():

  with open("../data/transConfigFile.txt", "w") as outfile:
    """ 
    - frecuencia (# transacciones/min)
    - #InMax
    - #InMin
    - #OutMax
    - #OutMin
    """
    pass


def genBlockConfigFile():

  with open("../data/blockConfigFile.txt", "w") as outfile:
    """ 
    - TamMaxBloque: 512           # en bytes
    - TiempoPromedioCreacionBloque: 1 # en minutos
    - DificultadInicial: 1000
    """
    pass
