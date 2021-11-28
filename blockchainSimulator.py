import sys

import config.variables as vars
import src.genIdentities    as genIds
import src.genTransactions  as genTxs


def blockchainSimulator(i: int, n: int, m: int, d: str) -> None:
  
  print("start")
  (users, nodes) = genIds.genIdentities(i, n)
  print("users: ", users)
  print("nodes: ", nodes)
  # genNetFile(n, m)
  # genTransConfigFile()
  # genBlockConfigFile()
  genTxs.genTransactions(users, nodes, "")


def genNetFile(nodos: int, pares: int) -> None:

  # with open(vars.NET_FILE, "w") as outfile:

  #   outfile.write(nodos+'\n')
  #   n = 0
  #   nodo
  #   while n < nodos:
  #     outfile.write(nodo[n].name+' '+nodo[n].port+'\n')
  #     n += 1

  #   outfile.write(pares+'\n')
  #   m = 0
  #   nodo1
  #   nodo2
  #   while m < pares:
  #     outfile.write(nodo1[m].name+m+' '+nodo2[m].name+m+'\n')
  #     m += 1
  pass


def genTransConfigFile() -> None:

  with open(vars.TRANSACTION_COFIG_FILE, "w") as outfile:
    """ 
    - frecuencia (# transacciones/min)
    - #InMax
    - #InMin
    - #OutMax
    - #OutMin
    """
    pass


def genBlockConfigFile() -> None:

  with open(vars.BLOCK_COFIG_FILE, "w") as outfile:
    """ 
    - TamMaxBloque: 512           # en bytes
    - TiempoPromedioCreacionBloque: 1 # en minutos
    - DificultadInicial: 1000
    """
    pass
