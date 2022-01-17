#!/usr/bin/env python3
import bitcoin as btc
from typing import Tuple, List, Dict

import modules.identity    as id
import modules.transaction as tx


def genIdenti(identities: int, nodos: int) -> Tuple[List[id.User], Dict[str,id.Node]]:
  
  users = []
  nodes = {}

  for x in range(identities):
    
    privKey, publKey = __genKeys()
    name             = "user" + str(x)
    mail             = name + "@gmail.com"
    address          = btc.pubkey_to_address(publKey)
    coinbase         = tx.TxInput("0", 0, 10000000, address).__dict__
    user             = id.User(name, mail, privKey, publKey, address)
    
    user.utxos.append(tx.Transaction(user, user, 10000000, [coinbase]))
    users.append(user)

  newPort = 5000
  for x in range(nodos):
    
    privKey, publKey = __genKeys()
    name             = "nodo" + str(x)
    address          = btc.pubkey_to_address(publKey)
    node             = id.Node(name, privKey, publKey, address, newPort)
    newPort          += 1
    
    nodes.update({name : node})

  return (users, nodes)


def __genKeys() -> Tuple[str, str]:
  
  privKey = btc.random_key()
  publKey = btc.privkey_to_pubkey(privKey)

  return (privKey, publKey)
