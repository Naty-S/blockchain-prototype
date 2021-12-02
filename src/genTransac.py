import random, socket, time, pdb, os


import config.variables    as vars
import modules.identity    as id
import modules.transaction as tx


def genTransactions(users: list[id.User], nodes: list[id.Node], logDir: str) -> None:

  logFile = logDir + "genTransac.log"

  x = 0
  # while True:
  while x < 5:
    print(f"tx: {x}...")
    node     = random.choice(nodes)
    sender   = random.choice(users)
    receiver = random.choice(users)
    
    if sender == receiver:
      print("\tsender == receiver...\n")
      continue
    
    satoshis = random.randint(1, 10000000) * random.random() + 1
    t        = __genTran(sender, receiver, satoshis)
    print("sending tx...")
    __sendTran(t, node)

    msg = "Transaccion Nueva <"+str(t.txId)+"> enviada: ["+time.asctime()+"]\n"
    with open(logFile, "a+") as file:
      file.write(msg)

    x += 1
  
  print("finish gen txs")


def __genTran(sender: id.User, receiver: id.User, satoshis: int) -> tx.Transaction:

  inputs       = []
  total_amount = 0
  for utxo in sender.utxos:
    print("checking utxos...")
    for out in utxo.outputs:
      print("checking out...")
      # Checks if the output is from the sender
      if out["address"] != sender.address:
        print("\tout[address] != sender.address...\n")
        continue

      if (out["spent"] == False) & (total_amount < satoshis):
        print("creating input...")
        out["spent"] = True # Se asume que la red acepta la transaccion
        input        = tx.TxInput(utxo.txId, out["index"], out["value"], sender.address).__dict__
        inputs.append(input)
        total_amount += out["value"]
  
  if total_amount < satoshis:
    print("\ttotal_amount < satoshis...\n")
    # yield

  print("creating tx...")
  new_tx = tx.Transaction(sender, receiver, satoshis, inputs)
  
  if total_amount > satoshis:
    print("creating change...")
    change = tx.TxOutput(total_amount - satoshis, sender.address, len(new_tx.outputs) + 1).__dict__
    new_tx.outputs.append(change)
    sender.utxos.append(new_tx)
  
  print("adding tx to receiver...")
  receiver.utxos.append(new_tx)
    
  return new_tx


def __sendTran(t: tx.Transaction, node: id.Node) -> None:
  
  s      = socket.socket()
  print("socket created...")
  txDict = t.__dict__
  msg    = str(("Transaccion Nueva", txDict)).encode()

  s.connect((socket.gethostname(), node.port))
  print(f"conected to {node.port}...")
  s.send(msg)
  print(f"msg sended ...")

  print(f"waiting ack ...")
  # pdb.set_trace()
  ack = s.recv(512).decode()
  print(f"\n\n\t\tack : {ack}\n\n")

  # if ack == "Si":
  #   # TODO: marcar t como gastada
  #   pass
  
  s.close()
