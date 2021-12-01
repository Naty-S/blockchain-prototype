import random, socket


import config.variables    as vars
import modules.identity    as id
import modules.transaction as tx


def genTransactions(users: list[id.User], nodes: list[id.Node], dir: str) -> None:

  # while True:
  for x in range(10):
    node     = random.choice(nodes)
    sender   = random.choice(users)
    receiver = random.choice(users)
    
    if sender == receiver: continue
    
    satoshis = random.randint(1, 10000000) * random.random() + 1
    t        = __genTran(sender, receiver, satoshis)
    __sendTran(t, node)


def __genTran(sender: id.User, receiver: id.User, satoshis: int) -> tx.Transaction:

  inputs       = []
  total_amount = 0
  for utxo in sender.utxos:
    for out in utxo.outputs:
      if out["address"] != sender.address: continue

      if (out["spent"] == False) & (total_amount < satoshis):
        out["spent"] = True # Se asume que la red acepta la transaccion
        input     = tx.TxInput(utxo.txId, out["index"], sender.address).__dict__
        inputs.append(input)
        total_amount += out["value"]
  
  if total_amount < satoshis:
    print("\ttotal_amount < satoshis...\n")
    # yield

  new_tx = tx.Transaction(sender, receiver, satoshis, inputs)
  
  if total_amount > satoshis:
    change = tx.TxOutput(total_amount - satoshis, sender.address, len(new_tx.outputs) + 1).__dict__
    new_tx.outputs.append(change)
    sender.utxos.append(new_tx)
  
  receiver.utxos.append(new_tx)
    
  return new_tx


def __sendTran(t: tx.Transaction, node: id.Node) -> None:
  
  s      = socket.socket()
  txDict = t.__dict__
  msg    = str({"Nueva Transaccion" : txDict}).encode()

  s.connect((socket.gethostname(), node.port))
  s.send(msg)

  ack = s.recv(512).decode()
  # print("data recv from node: ", node.name, ", port: ", node.port, ". ACK: ", ack)

  # if ack == "Si":
  #   # TODO: marcar t como gastada
  #   pass
  
  s.close()
