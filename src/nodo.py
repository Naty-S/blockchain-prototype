
import modules.identity as id
import modules.node     as node


def nodo(name: str, dir: str, nodes: dict(str,id.Node), net: list[dict(str,int)]) -> None:
  
  nodo       = nodes[name]
  neighbours = [ c[nodo.name] for c in net if c.__contains__(nodo.name) ]
  node.Node(nodo.name, nodo.port, neighbours)
