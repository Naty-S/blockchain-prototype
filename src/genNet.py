import random
import re

import modules.identity as id


def genNetwork(nodes: list[id.Node], pairs: int) -> list[dict[str,int]]:

  net = []
  totalPairs = 0
  
  while totalPairs < pairs:
    for n in nodes:
      auxNodes = nodes.copy()
      auxNodes.remove(n)
      neighbour = random.choice(auxNodes)
      net.append({ n.name : neighbour.port })
      totalPairs += 1
  
  return net
