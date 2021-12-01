
import genIdenti        as genIds
import genTransac       as genTxs
import genNet

def blockchainSimulator(i: int = 5, n: int = 3, m: int = 0, d: str = "") -> None:
  
  (users, nodes) = genIds.genIdentities(i, n)
  net = genNet.genNetwork(n, m)
  genTxs.genTransactions(users, list(nodes), "./output/logs/")
