import ast, pymerkle, queue, socket, threading, time, pdb
from typing import Tuple

import modules.block       as block
import modules.blockchain  as bc
import config.variables    as vars


class Node:

  def __init__(self, name: str, port: int, neighbours: list[int], logDir: str, bc: bc.Blockchain) -> None:

    self.__name         = name
    self.__port         = port
    self.__logFile      = logDir + self.__name + ".log"
    self.__neighbours   = neighbours # [port]
    self.__socket       = socket.socket()
    self.__spreadTxs    = []  # [dict]
    self.__spreadBlocks = []  # [dict]
    self.__orphanBlocks = []  # [dict] TODO: forks
    self.__mempool      = queue.Queue()  # [tx.__dict__]
    self.__minedBlock   = queue.Queue(1) # Block.__dict__
    self.__blockchain   = bc  # Blockchain
    self.__netListenerT = threading.Thread(name=self.__name+"-netListener", target=self.__netListener)
    self.__minerT       = threading.Thread(name=self.__name+"-miner", target=self.__miner)
    self.__minerAbort   = threading.Event()

    self.__socket.bind((b'localhost', self.__port))
    self.__netListenerT.start()
    self.__minerT.start()


  def __netListener(self) -> None:

    # TODO: Presentarse a sus vecinos

    self.__socket.listen(5)

    while True:
      c, addr = self.__socket.accept()
      msg     = ast.literal_eval(c.recv(8192).decode())
      request = msg[0]
      ackSi   = request.encode() + b" ACK: " + self.__name.encode() + b": Si"
      ackNo   = request.encode() + b" ACK: " + self.__name.encode() + b": No"
      print(f"request : {request}")

      if (request == "Transaccion Nueva") | (request == "Transaccion"):
        tx = msg[1]
        if tx in self.__spreadTxs: continue

        txId = tx["txId"]
        if self.__validateTx(tx):
          self.__mempool.put(tx)
          self.__spread("Transaccion", tx)
          self.__writeLog("Transaccion >"+txId+"< recibida y aceptada: ["+time.asctime()+"]\n")
          self.__spreadTxs.append(tx)
          c.send(ackSi)
          c.close()
        else:
          self.__writeLog("Transaccion <"+txId+"> recibida y rechazada: ["+time.asctime()+"]\n")
          c.send(ackNo)
          c.close()
      else: # Se asume request == 'Bloque'
        b = msg[1]
        if b in self.__spreadBlocks: continue

        if self.__validateBlock(b):
          print(f"aborting minig...")
          self.__minerAbort.set()
          self.__updateMempool(b)
          self.__chain(b)
          self.__spread("Bloque", b)
          self.__writeLog("Bloque >"+str(b["bId"])+"< recibido y aceptado: ["+time.asctime()+"]\n")
          self.__spreadBlocks.append(b)
          c.send(ackSi)
          c.close()
        else:
          self.__writeLog("Bloque <"+str(b["bId"])+"> recibido y rechazado: ["+time.asctime()+"]\n")
          c.send(ackNo)
          c.close()
      
      # Verify if miner mined a block
      if self.__minedBlock.qsize() != 0:
        print(f"block mined: {self.__name}...")
        b = self.__minedBlock.get(True)
        self.__spread("Bloque", b)
        self.__writeLog("Bloque >"+str(b["bId"])+"< minado y propagado: ["+time.asctime()+"]")
        self.__spreadBlocks.append(b)
        self.__minerAbort.clear() # Reset to false

      # if ctrl + c : SystemExit()/ sys.exit()
      # threading.Event()


  def __validateTx(self, tx: dict) -> bool:

    print(f"validateTx {tx['txId']}...")

    try:
      tx["inputs"]
      tx["outputs"]
    except:
      return False
    else:
      # TODO: verificar scripts P2SH
      # TODO: inputsScripts  = [ i["scriptSig"] for i in tx["inputs"] ]
      # TODO: outsScripts = [ o["scriptPubKey"] for o in tx["outputs"] ]

      inputsValues = [ i["value"] for i in tx["inputs"] ]
      outsValues   = [ o["value"] for o in tx["outputs"] ]
      outsSpent    = [ o["spent"] for o in tx["outputs"] ]

      try:
        sum(outsValues) < sum(inputsValues)
        not any(outsSpent)
      except:
        return False
      else:
        return True
    

  def __validateBlock(self, b: dict) -> bool:

    print(f"validateBlock {b['bId']}...")

    txsMerkle = pymerkle.MerkleTree()
    for tx in b["transactions"]: txsMerkle.update(tx["txId"])

    try:
      b["prevBlock"] == self.__blockchain.getChain()[-1].bId
      txsMerkle.rootHash.decode() == b["merkleRoot"]
      int(b["bId"], 16) < 2**(256 - (vars.DIFFICULTY / 100)) # Hash got correct pow
      return True
    except:
      return False


  def __chain(self, b: dict) -> None:

    bBlock = block.Block(b["prevBlock"], b["merkleRoot"], b["transactions"])
    bBlock.bId = b["bId"]
    bBlock.timestamp = b["timestamp"]
    self.__blockchain.add(bBlock)


  def __spread(self, request: str, info: dict) -> None:

    msg = str((request, info)).encode()

    for neighbour in self.__neighbours:
      print(f"{self.__name} spread: {list(info.items())[0]} to {neighbour}...")
      s = socket.socket()
      s.connect((b'localhost', neighbour))
      s.send(msg)
      print(f"\t{self.__name} got ack : {s.recv(512).decode()}")
      s.close()


  # Filter mempool with transaction not in the winner block
  def __updateMempool(self, winner: dict) -> None:

    print(f"updateMempool {self.__mempool.queue}...")

    txsNotInWinner = [ tx for tx in self.__mempool.queue if tx not in winner["transactions"] ]
    self.__mempool = queue.Queue()
    for tx in txsNotInWinner: self.__mempool.put(tx)

    print(f"mempool updated {self.__mempool.queue}...")


  def __miner(self) -> None:

    while True:

      print(f"{self.__name} mining...")
      
      newBlock   = block.Block(self.__blockchain.getChain()[-1].bId, "-1", [])
      merkleTree = pymerkle.MerkleTree()

      # Ask if have to abort mining
      while not self.__minerAbort.is_set():

        tx   = self.__mempool.get(True)
        txId = tx["txId"]
        newBlock.transactions.append(tx)
        newBlock.size += len(txId) # Length of the tx id
        merkleTree.update(txId.encode())
        self.__mempool.task_done()

        # Full block
        if newBlock.size == 512:
          newBlock.timestamp  = time.asctime()
          newBlock.merkleRoot = merkleTree.rootHash.decode()
          newBlock.pow()
          self.__minedBlock.put(newBlock.__dict__, True)

      # Reset to false
      self.__minerAbort.clear()
      
      # Return transacctions to mempool
      for tx in newBlock.transactions:
        self.__mempool.put(tx)
      
      

  def __writeLog(self, msg: str) -> None:

    with open(self.__logFile, "a+") as logFile: logFile.write(msg)
