import random
from typing import Tuple

import modules.identity as id


def genNetwork(nodes: list[id.Node], pairs: int) -> list[Tuple[str,int]]:

  net = []
  totalPairs = 0
  
  while totalPairs < pairs:
    for n in nodes:
      auxNodes = nodes.copy()
      auxNodes.remove(n)
      neighbour = random.choice(auxNodes)
      net.append( (n.name, neighbour.port) )
      totalPairs += 1
  
  return net
