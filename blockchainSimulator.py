import sys

import config.variables    as vars
import modules.node        as node
import src.genIdentities   as genIds
import src.genTransactions as genTxs


def blockchainSimulator(i: int = 5, n: int = 3, m: int = 0, d: str = "") -> None:
  
  (users, nodes) = genIds.genIdentities(i, n)
  # genNetFile(n, m)
  # init nodes, serian(pueden) threads?
  genTxs.genTransactions(users, nodes, "") # hacerlo thread?


def genNetFile(nodos: int, pares: int) -> None:

  # with open(vars.NET_FILE, "w") as outfile:

  #   outfile.write(nodos+'\n')
  #   n = 0
  #   node
  #   while n < nodos:
  #     outfile.write(node[n].name+' '+node[n].port+'\n')
  #     n += 1

  #   outfile.write(pares+'\n')
  #   m = 0
  #   nodo1
  #   nodo2
  #   while m < pares:
  #     outfile.write(nodo1[m].name+m+' '+nodo2[m].name+m+'\n')
  #     m += 1
  pass


