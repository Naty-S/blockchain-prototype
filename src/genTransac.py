import random, socket, time


import config.variables    as vars
import modules.identity    as id
import modules.transaction as tx


def genTransac(users: list[id.User], nodes: dict[str,id.Node], logDir: str) -> None:

  nodesL  = list(nodes.values())
  logFile = logDir + "genTransac.log"

  # Clear last sesion
  with open(logFile, "w+") as file:
    file.write(f"[{time.asctime()}]: Starting to generate transactions...\n")

  x = 0
  while True:
    __writeLog(logFile, f"[{time.asctime()}]: Generating transaction: {x}...\n")
    sender   = random.choice(users)
    receiver = random.choice(users)
    
    if sender == receiver:
      continue
    
    satoshis = random.randint(1, 10000000) * random.random() + 1
    t        = __genTx(sender, receiver, satoshis, logFile)
    
    __writeLog(logFile, f"[{time.asctime()}]: Sending transaction: {t.txId}...\n")
    __sendTx(t, random.choice(nodesL), logFile)

    time.sleep(60 / vars.FREQUENCY)
    x += 1


def __genTx(sender: id.User, receiver: id.User, satoshis: int, logFile: str) -> tx.Transaction:

  __writeLog(logFile, f"[{time.asctime()}]: Sending: {satoshis} from {sender.address} to {receiver.address}...\n")

  inputs       = []
  totalAmount = 0
  
  for utxo in sender.utxos:
    __writeLog(logFile, f"[{time.asctime()}]: Checking utxo: {utxo.txId}...\n")

    for out in utxo.outputs:
      __writeLog(logFile, f"[{time.asctime()}]: Checking output: {out}...\n")

      # Checks if the output is from the sender
      if out["address"] != sender.address:
        continue

      if (out["spent"] == False) & (totalAmount < satoshis):
        
        out["spent"] = True # Assumes transaction acepted
        input        = tx.TxInput(utxo.txId, out["index"], out["value"], sender.address).__dict__
        # TODO: Sign input
        __writeLog(logFile, f"[{time.asctime()}]: Input created: {input}...\n")
        inputs.append(input)
        totalAmount += out["value"]
  
    # if total_amount < satoshis:
    # TODO
    #   total_amount = 0
    #   newSatoshis = (random.randint(1, 1000000) * random.random() + 1)
    #   __genTx(sender, sender, newSatoshis, logFile)

  new_tx = tx.Transaction(sender, receiver, satoshis, inputs)
  __writeLog(logFile, f"[{time.asctime()}]: Transaction created...\n")
  # TODO: Sign output
  
  if totalAmount > satoshis:
    
    change = tx.TxOutput(totalAmount - satoshis, sender.address, len(new_tx.outputs) + 1).__dict__
    new_tx.outputs.append(change)
    sender.utxos.append(new_tx)

    __writeLog(logFile, f"[{time.asctime()}]: Change created...\n")
  
  receiver.utxos.append(new_tx)
    
  return new_tx


def __sendTx(t: tx.Transaction, node: id.Node, logFile: str) -> None:
  
  s      = socket.socket()
  txDict = t.__dict__
  msg    = str(("Transaccion Nueva", txDict)).encode()

  s.connect((b'localhost', node.port))
  __writeLog(logFile, f"[{time.asctime()}]: Connected: {node.port}...\n")
  
  s.send(msg) # TODO: Encrypt
  __writeLog(logFile, f"[{time.asctime()}]: Request send: {node.name}...\n")

  __writeLog(logFile, f"[{time.asctime()}]: Waiting ack...\n")
  ack = s.recv(512).decode()
  __writeLog(logFile, f"[{time.asctime()}]: Got ack: {ack}...\n")

  # if ack[-1] == 'i':
  #   # TODO: marcar t como gastada
  #   pass
  
  s.close()


def __writeLog(logFile: str, msg: str) -> None:

  with open(logFile, "a") as file:
    file.write(msg)
