import random

import modules.identity as id
import genIdenti        as genIds
import genTransac       as genTxs


def blockchainSimulator(i: int = 5, n: int = 3, m: int = 0, d: str = "") -> None:
  
  (users, nodes) = genIds.genIdentities(i, n)
  net = genNetwork(n, m)
  genTxs.genTransactions(users, list(nodes), "./output/logs/")


def genNetwork(nodes: list[id.Node], pairs: int) -> list[dict(str,int)]:

  net = []
  totalPairs = 0
  
  while totalPairs < pairs:
    for n in nodes:
      auxNodes = nodes.copy()
      neighbour = random.choice(auxNodes.remove(n))
      net.append({ n.name : neighbour.port })
      totalPairs += 1

