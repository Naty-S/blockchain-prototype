import ast, pymerkle, queue, socket, threading, time, pdb

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

    self.__socket.bind((socket.gethostname(), self.__port))
    self.__netListenerT.start()
    self.__minerT.start()


  def __netListener(self) -> None:

    # TODO: Presentarse a sus vecinos

    self.__socket.listen(5)

    while True:
      c, addr = self.__socket.accept()
      msg     = ast.literal_eval(c.recv(2048).decode())
      request = msg[0]
      ackSi   = request.encode() + b" ACK: " + self.__name.encode() + b": Si"
      ackNo   = request.encode() + b" ACK: " + self.__name.encode() + b": No"
      print(f"\n\n\t\trequest : {request}\n\n")

      if (request == "Transaccion Nueva") | (request == "Transaccion"):
        tx = msg[1]
        if tx in self.__spreadTxs:
          print("tx in self.__spreadTxs...")
          continue

        txId = tx["txId"]
        if self.__validateTx(tx):
          self.__mempool.put(tx, True)
          self.__spread("Transaccion", tx)
          self.__spreadTxs.append(tx)
          self.__writeLog("Transaccion >"+txId+"< recibida y aceptada: ["+time.asctime()+"]\n")
          c.send(ackSi)
          c.close()
        else:
          self.__writeLog("Transaccion <"+txId+"> recibida y rechazada: ["+time.asctime()+"]\n")
          c.send(ackNo)
          c.close()
      else: # Se asume request == 'Bloque'
        b = msg[1]
        if b in self.__spreadBlocks:
          print("tx in self.__spreadBlocks...")
          continue

        if self.__validateBlock(b):
          print("aborting minig...")
          self.__minerAbort.set()
          self.__updateMempool(b)
          self.__chain(b)
          self.__spread("Bloque", b)
          self.__spreadBlocks.append(b)
          self.__writeLog("Bloque >"+str(b["bId"])+"< recibido y aceptado: ["+time.asctime()+"]\n")
          c.send(ackSi)
          c.close()
        else:
          self.__writeLog("Bloque <"+str(b["bId"])+"> recibido y rechazado: ["+time.asctime()+"]\n")
          c.send(ackNo)
          c.close()
      
      # Verify if miner mined a block
      if self.__minedBlock.qsize() != 0:
        print("block mined...")
        b = self.__minedBlock.get(True)
        self.__spread("Bloque", b)
        self.__spreadBlocks.append(b)
        self.__writeLog("Bloque >"+str(b["bId"])+"< minado y propagado: ["+time.asctime()+"]")

      # if ctrl + c : SystemExit()/ sys.exit()
      # threading.Event()


  def __validateTx(self, tx: dict) -> bool:

    print("validateTx...")

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

    print("validateBlock...")

    txsMerkle = pymerkle.MerkleTree()
    for tx in b["transactions"]: txsMerkle.update(tx["txId"])

    try:
      b["prevBlock"] == self.__blockchain[-1].bId
      txsMerkle.rootHash.decode() == b["merkleRoot"]
      int(b["bId"],16) < 2**(256-(vars.DIFFICULTY)/100) # Hash got correct pow
      return True
    except:
      return False


  def __chain(self, b: dict) -> None:

    bBlock = block.Block(b["bId"], b["prevBlock"], b["merkleRoot"], b["transactions"])
    bBlock.timestamp = b["timestamp"]
    self.__blockchain.add(bBlock)


  def __spread(self, request: str, info: dict) -> None:

    msg = str((request, info)).encode()

    for neighbour in self.__neighbours:
      print("spread...")
      s = socket.socket()
      s.bind((socket.gethostname(), neighbour))
      s.send(msg)
      s.close()


  # Filter mempool with transaction not in the winner block
  def __updateMempool(self, winner: dict) -> None:

    print("updateMempool...")
    txsNotInWinner = [ tx for tx in self.__mempool.queue if tx not in winner["transactions"] ]
    self.__mempool = queue.Queue()
    for tx in txsNotInWinner: self.__mempool.put(tx)


  def __miner(self) -> None:

    while True:
      print("mining...")
      newBlock   = block.Block("-1", self.__blockchain[-1].bId, "-1", [])
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
        self.__mempool.put(tx, True)
      

  def __writeLog(self, msg: str) -> None:

    with open(self.__logFile, "a+") as logFile: logFile.write(msg)
