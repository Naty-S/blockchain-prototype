import random
from typing import Tuple

import modules.identity as id


def genNetwork(nodes: dict[str,id.Node], pairs: int) -> list[Tuple[str,int]]:

  nodesL     = list(nodes.values())
  net        = []
  totalPairs = 0
  
  while totalPairs < pairs:
    for n in nodesL:
      auxNodes = nodesL.copy()
      auxNodes.remove(n)
      neighbour = random.choice(auxNodes)
      net.append( (n.name, neighbour.port) )
      totalPairs += 1
  
  return net
