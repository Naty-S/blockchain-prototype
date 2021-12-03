import os

import modules.blockchain  as blockchain
import src.genIdenti       as genIds
import src.genTransac      as genTxs
import src.genNet          as genNet
import src.nodo            as nodo


def blockchainSimulator(i: int = 5, n: int = 3, m: int = 4, outDir: str = "./output/logs/") -> None:
  
  if not os.path.exists(outDir):
    os.makedirs(outDir)
  
  (users, nodes) = genIds.genIdenti(i, n)
  net = genNet.genNetwork(nodes, m)
  bc = blockchain.Blockchain()
  nodo.nodo("nodo0", nodes, net, outDir, bc)
  nodo.nodo("nodo1", nodes, net, outDir, bc)
  nodo.nodo("nodo2", nodes, net, outDir, bc)
  genTxs.genTransac(users, nodes, outDir)
  print(f"Blockchain:\n{[b.bId for b in bc.getChain()]}")
  print(f"Block height = 3: {bc.blockExplorer('-a', 3)}")


blockchainSimulator()
