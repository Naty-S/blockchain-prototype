import random

import config.variables as vars
import modules.identity as id
import modules.transaction as tx


def genTransactions(users: list[id.User], nodes: list[id.Nodo], dir: str) -> None:

  while True:
    t = __genTran(users)
    __sendTran(t, nodes)
  

def __genTran(users: list[id.User]) -> tx.Transaction:

  sender   = random.choice(users)
  receiver = random.choice(users)
  satoshis = random.randint(1, 10000000) * random.random() + 1

  while sender == receiver:
    receiver = random.choice(users)

  inputs = set()
  for utxo in sender.utxos:
    print("utxo: ", utxo)
    if (utxo.outputs[sender.address][0] == False) & (sum(inputs) < satoshis):
      utxo.outputs[sender.address] = (True, utxo.outputs[sender.address][1])
      print("utxo: ", utxo)
      inputs.add(utxo.outputs[sender.address][1])
  
  print("inputs: ", inputs)

  if sum(inputs) < satoshis:
    users.remove(sender)
    __genTran(users)

  new_tx = tx.Transaction(sender, receiver, satoshis, inputs)
  new_tx.outputs.update(new_tx.change())
  sender.utxos.add(new_tx)
  receiver.utxos.add(new_tx)
  print("new_tx: ", new_tx)
  
  return new_tx


def __sendTran(t: tx.Transaction, nodes: list[id.Nodo]) -> None:
  pass
