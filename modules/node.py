import ast, pymerkle, queue, socket, threading, time, pdb
from typing import Tuple

import modules.block       as block
import modules.blockchain  as bc
import config.variables    as vars


class Node:

  def __init__(self, name: str, port: int, neighbours: list[int], logDir: str, blockchain: bc.Blockchain) -> None:

    self.__name         = name
    self.__port         = port
    self.__logFile      = logDir + self.__name + ".log"
    # [int]: Neighbours ports
    self.__neighbours   = neighbours
    # [dict]: Transactions already spread
    self.__spreadTxs    = []  
    # [dict]: Blocks already spread
    self.__spreadBlocks = []  
    # [tx.__dict__]
    self.__mempool      = queue.Queue(-1)
    # Block.__dict__
    self.__minedBlock   = queue.Queue(1)
    # Shared blockchain
    self.__blockchain   = blockchain
    # TODO: List used whe forks occurs
    self.__myBlockchain = []
    # [dict] TODO
    self.__orphanBlocks = []
    self.__socket       = socket.socket()
    self.__netListenerT = threading.Thread(name=self.__name+"-netListener", target=self.__netListener)
    self.__minerT       = threading.Thread(name=self.__name+"-miner", target=self.__miner)
    self.__minerAbort   = threading.Event()

    # Clear last sesion
    with open(self.__logFile, "w+") as file:
      file.write(f"[{time.asctime()}]: Starting Node: {self.__name}...")

    self.__socket.bind((b'localhost', self.__port))
    self.__netListenerT.start()
    self.__minerT.start()


  def __netListener(self) -> None:

    # TODO: Presentarse a sus vecinos

    self.__socket.listen(5)

    while True:
      connex  = self.__socket.accept()[0]
      msg     = ast.literal_eval(connex.recv(8192).decode())
      request = msg[0]
      ackSi   = request.encode() + b"ACK: " + self.__name.encode() + b": Si"
      ackNo   = request.encode() + b"ACK: " + self.__name.encode() + b": No"
      print(f"{self.__name}: Got request : {request}...")

      if (request == "Transaccion Nueva") | (request == "Transaccion"):
        
        tx = msg[1]
        
        if tx in self.__spreadTxs:
          continue

        txId = tx["txId"]
        if self.__validateTx(tx):

          print(f"{self.__name}: Adding {txId} to mempool...")
          self.__mempool.put(tx, True)
          
          self.__spread("Transaccion", tx)
          self.__writeLog("Transaccion >"+txId+"< recibida y aceptada: ["+time.asctime()+"]\n")
          self.__spreadTxs.append(tx)
          connex.send(ackSi)
          connex.close()
        else:
          print(f"{self.__name}: Transaction {txId} rejected...")

          self.__writeLog("Transaccion <"+txId+"> recibida y rechazada: ["+time.asctime()+"]\n")
          connex.send(ackNo)
          connex.close()
      else: # Se asume request == 'Bloque'
        b = msg[1]
        
        if b in self.__spreadBlocks:
          continue

        if self.__validateBlock(b):
          print(f"{self.__name}: Aborting minig...")
          self.__minerAbort.set()
          self.__updateMempool(b)
          self.__chain(b)
          self.__spread("Bloque", b)
          self.__writeLog("Bloque >"+b["bId"]+"< recibido y aceptado: ["+time.asctime()+"]\n")
          self.__spreadBlocks.append(b)
          connex.send(ackSi)
          connex.close()
        else:
          print(f"{self.__name}: Block {b['bId']} rejected...")

          self.__writeLog("Bloque <"+b["bId"]+"> recibido y rechazado: ["+time.asctime()+"]\n")
          connex.send(ackNo)
          connex.close()
      
      # Verify if miner mined a block
      if self.__minedBlock.qsize() != 0:
        
        b = self.__minedBlock.get(True)
        print(f"{self.__name}: Block mined: {b['bId']}...")
        self.__spread("Bloque", b)
        self.__writeLog("Bloque >"+b["bId"]+"< minado y propagado: ["+time.asctime()+"]")
        self.__spreadBlocks.append(b)
        # Miner can start again
        self.__minerAbort.clear()


  def __validateTx(self, tx: dict) -> bool:

    print(f"{self.__name}: Validating Tx: {tx['txId']}...")

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

    print(f"{self.__name}: Validating Block: {b['bId']}...")

    txsMerkle = pymerkle.MerkleTree()
    for tx in b["transactions"]:
      txsMerkle.update(tx["txId"])

    try:
      b["prevBlock"] == self.__blockchain.getChain()[-1].bId
      txsMerkle.rootHash.decode() == b["merkleRoot"]
      # Verify Proof of Work
      int(b["bId"], 16) < 2**(256 - (vars.DIFFICULTY / 100))
      return True
    except:
      return False


  def __chain(self, b: dict) -> None:

    print(f"{self.__name}: Adding block to blockchain: {b['bId']}...")

    bBlock           = block.Block(b["prevBlock"], b["merkleRoot"], b["transactions"])
    bBlock.bId       = b["bId"]
    bBlock.timestamp = b["timestamp"]
    self.__blockchain.add(bBlock)


  def __spread(self, request: str, info: dict) -> None:

    print(f"{self.__name}: Spreading...")
    msg = str((request, info)).encode()

    for neighbour in self.__neighbours:
      
      print(f"{self.__name}: Sending to {neighbour}: {list(info.items())[0]}...")
      
      s = socket.socket()
      s.connect((b'localhost', neighbour))
      s.send(msg)
      print(f"\t{self.__name}: Got ack : {s.recv(512).decode()}")
      s.close()


  # Filter mempool with transaction not in the winner block
  def __updateMempool(self, winner: dict) -> None:

    print(f"{self.__name}: Updating mempool: {self.__mempool.queue}...")

    txsNotInWinner = [ tx for tx in self.__mempool.queue if tx not in winner["transactions"] ]
    self.__mempool = queue.Queue()
    for tx in txsNotInWinner: self.__mempool.put(tx, True)

    print(f"{self.__name}: mempool updated {self.__mempool.queue}...")


  def __miner(self) -> None:

    while True:

      print(f"{self.__name}: Started mining...")
      
      newBlock   = block.Block(self.__blockchain.getChain()[-1].bId, "-1", [])
      merkleTree = pymerkle.MerkleTree()

      # Ask if have to abort mining
      while not self.__minerAbort.is_set():

        print(f"{self.__name}: Checking txs in mempool...")

        tx   = self.__mempool.get(True)
        txId = tx["txId"]
        print(f"{self.__name}: Adding tx {txId} to new block...")
        newBlock.transactions.append(tx)
        newBlock.size += len(txId) # Length of the tx id
        print(f"{self.__name}: Adding tx {txId} to merkle tree...")
        merkleTree.update(txId.encode())
        self.__mempool.task_done()

        # Full block
        if newBlock.size == 512:
  
          newBlock.timestamp  = time.asctime()
          newBlock.merkleRoot = merkleTree.rootHash.decode()
          print(f"{self.__name}: Proof of work...")
          newBlock.pow()
          self.__minedBlock.put(newBlock.__dict__, True)

      # Reset to false, restart mining
      print(f"{self.__name}: Restarting mining...")
      self.__minerAbort.clear()
      
      # Return transacctions to mempool
      print(f"{self.__name}: Returning transaccionts to mempool...")
      for tx in newBlock.transactions:
        self.__mempool.put(tx, True)
      

  def __writeLog(self, msg: str) -> None:

    print(f"{self.__name}: Writing in log file...")
    with open(self.__logFile, "a") as logFile: logFile.write(msg)
