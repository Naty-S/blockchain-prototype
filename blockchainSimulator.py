
import src.genIdenti   as genIds
import src.genTransac  as genTxs
import src.genNet      as genNet
import src.nodo        as nodo

def blockchainSimulator(i: int = 5, n: int = 3, m: int = 4, d: str = "") -> None:
  
  (users, nodes) = genIds.genIdentities(i, n)
  net = genNet.genNetwork(list(nodes.values()), m)
  nodo.nodo("nodo0", "", nodes, net)
  nodo.nodo("nodo1", "", nodes, net)
  nodo.nodo("nodo2", "", nodes, net)
  genTxs.genTransactions(users, list(nodes.values()), "./output/logs/")
