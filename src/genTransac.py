import random, socket, time, os


import config.variables    as vars
import modules.identity    as id
import modules.transaction as tx


def genTransactions(users: list[id.User], nodes: list[id.Node], logDir: str) -> None:

  logFile = logDir + "genTransac.log"

  # Clear last sesion
  with open(logFile, "w+") as file:
    file.write(f"[{time.asctime()}]: Starting to generate transacctions...")

  x = 0
  # while True:
  while x < 9:
    print(f"\ntx: {x}...")
    node     = random.choice(nodes)
    sender   = random.choice(users)
    receiver = random.choice(users)
    
    if sender == receiver: continue
    
    satoshis = random.randint(1, 10000000) * random.random() + 1
    t        = __genTx(sender, receiver, satoshis)
    print(f"sending tx: {t.txId}...")
    __sendTx(t, node)

    msg = "Transaccion Nueva <"+str(t.txId)+"> enviada: ["+time.asctime()+"]\n"
    with open(logFile, "a") as file:
      file.write(msg)

    time.sleep(60 / vars.FREQUENCY)
    x += 1
  
  print("finish gen txs")


def __genTx(sender: id.User, receiver: id.User, satoshis: int) -> tx.Transaction:

  inputs       = []
  total_amount = 0
  for utxo in sender.utxos:
    print(f"checking utxo: {utxo.txId}, from: {sender.address}...")

    for out in utxo.outputs:
      print(f"checking out: {out}...")

      # Checks if the output is from the sender
      if out["address"] != sender.address: continue

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
  
  print(f"adding tx to receiver: {receiver.address}...")
  receiver.utxos.append(new_tx)
    
  return new_tx


def __sendTx(t: tx.Transaction, node: id.Node) -> None:
  
  s      = socket.socket()
  txDict = t.__dict__
  msg    = str(("Transaccion Nueva", txDict)).encode()

  s.connect((b'localhost', node.port))
  print(f"conected to {node.port}...")
  s.send(msg)
  print(f"msg sended to: {node.name}...")

  print(f"waiting ack...")
  ack = s.recv(512).decode()
  print(f"\tgen txs got: {ack}...")

  # if ack[-1] == 'i':
  #   # TODO: marcar t como gastada
  #   pass
  
  s.close()
