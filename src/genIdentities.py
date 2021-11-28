import bitcoin as btc
from typing import Tuple

import modules.identity    as id
import modules.transaction as tx


def genIdentities(identities: int, nodos: int) -> Tuple[list[id.User], list[id.Nodo]]:
  
  users = []
  nodes = []

  for x in range(identities):
    privKey, publKey = __genKeys()
    name = "user" + str(x)
    mail = name + "@gmail.com"
    address = btc.pubkey_to_address(publKey)
    i = id.User(name, mail, privKey, publKey, address)
    i.utxos.add(tx.Transaction(i, i))
    users.append(i)

  nPort = 5000
  for x in range(nodos):
    privKey, publKey = __genKeys()
    nodo = "nodo" + str(x)
    address = btc.pubkey_to_address(publKey)
    newPort = nPort + x
    nPort = newPort
    i = id.Nodo(nodo, privKey, publKey, address, newPort)
    nodes.append(i)

  return (users, nodes)


def __genKeys() -> Tuple[str, str]:
  privKey = btc.random_key()
  publKey = btc.privkey_to_pubkey(privKey)

  return (privKey, publKey)
