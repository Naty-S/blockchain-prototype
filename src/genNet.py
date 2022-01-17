#!/usr/bin/env python3
import random
from typing import Tuple, List, Dict

import modules.identity as id


def genNetwork(nodes: Dict[str,id.Node], pairs: int) -> List[Tuple[str,int]]:

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
