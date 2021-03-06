#!/usr/bin/env python3
from typing import Tuple, List, Dict

import modules.blockchain as bc
import modules.identity   as id
import modules.node       as node


def nodo(name: str, nodes: Dict[str,id.Node], net: List[Tuple[str,int]], logDir: str, bc: bc.Blockchain) -> None:
  
  nodo       = nodes[name]
  neighbours = [ c for c in net if c.__contains__(nodo.name) ]
  node.Node(nodo, neighbours, logDir, bc)
