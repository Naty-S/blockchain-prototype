import random, socket


import config.variables    as vars
import modules.identity    as id
import modules.transaction as tx


def genTransactions(users: list[id.User], nodes: list[id.Nodo], dir: str) -> None:

  # while True:
  for x in range(6):
    nodo     = random.choice(nodes)
    sender   = random.choice(users)
    receiver = random.choice(users)
    s        = socket.socket()
    
    # s.connect((socket.gethostname(), 5100))
    # print("\tserver connected...\n")
    
    if sender == receiver:
      print("\tsender==receiver...\n")
      continue
    
    satoshis = random.randint(1, 10000000) * random.random() + 1
    t        = __genTran(sender, receiver, satoshis)
    ack      = __sendTran(t, s)
    # print(ack)

    # if ack == "Si":
    #   # TODO: marcar utxo como gastado
    #   pass
    
    s.close()

def __genTran(sender: id.User, receiver: id.User, satoshis: int) -> tx.Transaction:

  print("\tgenerating tx...\n")
  inputs       = []
  total_amount = 0
  for utxo in sender.utxos:
    print("\tchecking utxos...\n",utxo)
    for out in utxo.outputs:
      print("\tchecking outputs...\n",out)
      if out["address"] != sender.address:
        print("\tout.address != sender.address...\n")
        continue

      print("\n\tutxo txId:\n\t\t", utxo.txId)
      for i in utxo.inputs:
        print("\n\tinputs prevTxId:\n\t\t", i["prevTxId"])
        print("\n\tinputs prevTxOutIndex:\n\t\t", i["prevTxOutIndex"])
        print("\n\tinputs address:\n\t\t", i["address"])
      print("\n\tout value:\n\t\t", out["value"])
      print("\n\tout index:\n\t\t", out["index"])
      print("\n\tout address:\n\t\t", out["address"])
      print("\n\tout spent:\n\t\t", out["spent"])
      print("\n")

      if (out["spent"] == False) & (total_amount < satoshis):
        out["spent"] = True # Se asume que la red acepta la transaccion
        input     = tx.TxInput(utxo.txId, out["index"], sender.address).__dict__
        inputs.append(input)
        total_amount += out["value"]
      print("\nadding input...\n")
  
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


def __sendTran(t: tx.Transaction, s: socket.socket) -> str:
  
  print("\nsending tx...\n")
  txDict = t.__dict__ # si cambia la ref, la vuelve un dict
  msg = str({"Nueva Transaccion" : txDict}).encode()
  print("\nmsg...\n", msg)
  # s.send(msg)

  # new_var = s.recv(512).decode()
  # print("data recev from node: ", new_var)
  return ""
