import os, subprocess, threading

import config.variables    as vars
import modules.blockchain  as blockchain
import modules.block       as block
import src.genIdenti       as genIds
import src.genTransac      as genTxs
import src.genNet          as genNet
import src.nodo            as nodo

def blockchainSimulator(i: int = 5, n: int = 1, m: int = 0, outDir: str = "./output/logs/") -> None:
  
  if not os.path.exists(outDir): os.makedirs(outDir)
  
  (users, nodes) = genIds.genIdentities(i, n)
  net = genNet.genNetwork(list(nodes.values()), m)

  # for x in range(n):
  #   name = 'nodo'+str(x)
  #   cmd = f"cd 'c:/Users/User/USB/blockchain-prototype'; nodo.nodo({name}, '', {nodes}, {net}, outDir)"
  #   subprocess.run(["cmd.exe", "/c", "start", f"{cmd}"])
  bc = blockchain.Blockchain()
  nodo.nodo("nodo0", nodes, net, outDir, bc)
  # nodo.nodo("nodo1", nodes, net, outDir, genesis)
  # nodo.nodo("nodo2", nodes, net, outDir, genesis)
  # blockchain.Blockchain(vars.DIFFICULTY, list(nodes.values())) # Creates genesis block and spread to network
  # print(f"threads: {threading.enumerate()}")
  genTxs.genTransactions(users, list(nodes.values()), outDir)


blockchainSimulator()
