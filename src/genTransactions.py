import random, socket, pickle


import config.variables    as vars
import modules.identity    as id
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
    if (utxo.outputs[sender.address][0] == False) & (sum(inputs) < satoshis):
      utxo.outputs[sender.address] = (True, utxo.outputs[sender.address][1])
      inputs.add(utxo.outputs[sender.address][1])
  
  if sum(inputs) < satoshis:
    users.remove(sender)
    __genTran(users)

  new_tx = tx.Transaction(sender, receiver, satoshis, inputs)
  new_tx.outputs.update(new_tx.change())
  sender.utxos.add(new_tx)
  receiver.utxos.add(new_tx)
  
  return new_tx


def __sendTran(t: tx.Transaction, nodes: list[id.Nodo]) -> None:
  
  s = socket.socket()
  nodo = random.choice(nodes)

  s.connect((socket.gethostname(), nodo.port))

  d = pickle.dumps(t)
  # print("\n\nlen data client: ", len(d))
  # print("\n\nTx:", t)
  s.send(d)

  # print("data recev from node: ", s.recv(1024))
  s.close()
