import ast, pymerkle, socket, threading, time
from typing import Tuple

import config.variables    as vars
import modules.block       as block
import modules.blockchain  as bc
import modules.identity    as id


class Node:

  def __init__(self, node: id.Node, neighbours: list[Tuple[str,int]], logDir: str, blockchain: bc.Blockchain) -> None:

    self.__name         = node.name
    self.__port         = node.port
    self.__privKey      = node.privKey
    self.__publKey      = node.publKey
    self.__logFile      = logDir + self.__name + ".log"
    # [(str,int)]: Neighbours ports
    self.__neighbours   = neighbours
    # [dict]: Transactions already spread
    self.__spreadTxs    = []  
    # [dict]: Blocks already spread
    self.__spreadBlocks = []  
    # [tx.__dict__]
    self.__mempool      = []
    # Block.__dict__
    self.__minedBlock   = []
    # Shared blockchain
    self.__blockchain   = blockchain
    # TODO: List used when forks occurs
    self.__myBlockchain = []
    # [dict] TODO
    self.__orphanBlocks = []
    self.__socket       = socket.socket()
    self.__netListenerT = threading.Thread(name=self.__name+"-netListener", target=self.__netListener)
    self.__minerT       = threading.Thread(name=self.__name+"-miner", target=self.__miner)
    self.__minerAbort   = threading.Event()

    # Clear last sesion
    with open(self.__logFile, "w+") as file:
      file.write(f"[{time.asctime()}]: Starting Node: {self.__name}...\n")

    self.__socket.bind((b'localhost', self.__port))
    self.__netListenerT.start()
    self.__minerT.start()


  def __netListener(self) -> None:

    # TODO: Introduce to neighbours

    self.__socket.listen(5)

    while True:
      connex  = self.__socket.accept()[0]
      msg     = ast.literal_eval(connex.recv(8192).decode())
      request = msg[0]
      ackSi   = f"{request} ACK: {self.__name} : Si".encode()
      ackNo   = f"{request} ACK: {self.__name} : No".encode()
      self.__writeLog(f"[{time.asctime()}]: Got request: {request}...\n")

      if (request == "Transaccion Nueva") | (request == "Transaccion"):
        
        tx   = msg[1]
        txId = tx["txId"]
        self.__writeLog(f"[{time.asctime()}]: Transaction received: {txId}...\n")

        # Check if already spreaded
        if tx in self.__spreadTxs:
          continue

        if self.__validateTx(tx):
          self.__writeLog(f"[{time.asctime()}]: Transaction accepted: {txId}...\n")
          self.__writeLog(f"[{time.asctime()}]: Adding transaction to mempool: {txId}...\n")
          self.__mempool.append(tx)
          self.__writeLog(f"[{time.asctime()}]: Transaction added to mempool: {txId}...\n")          
          self.__spread("Transaccion", tx)
          self.__spreadTxs.append(tx)
          connex.send(ackSi) # TODO: Encrypt
          connex.close()
        else:
          self.__writeLog(f"[{time.asctime()}]: Transaction rejected: {txId}..\n.")
          connex.send(ackNo) # TODO: Encrypt
          connex.close()
      elif request == "Bloque":
        b = msg[1]
        bId = b["bId"]
        self.__writeLog(f"[{time.asctime()}]: Block received: {bId}...\n")

        # Check if already spreaded
        if b in self.__spreadBlocks:
          continue

        if self.__validateBlock(b):
          self.__writeLog(f"[{time.asctime()}]: Block accepted: {bId}...\n")
          self.__writeLog(f"[{time.asctime()}]: Aborting mining...\n")
          self.__minerAbort.set()
          self.__updateMempool(b)
          self.__chain(b)
          self.__spread("Bloque", b)
          self.__spreadBlocks.append(b)
          connex.send(ackSi) # TODO: Encrypt
          connex.close()
        else:
          self.__writeLog(f"[{time.asctime()}]: Block rejected: {bId}...\n")
          connex.send(ackNo) # TODO: Encrypt
          connex.close()
      else: # request == "Presentacion"
        pass # TODO
      
      # Verify if miner mined a block
      if len(self.__minedBlock) != 0:
        b = self.__minedBlock.pop()
        self.__writeLog(f"[{time.asctime()}]: Block mined: {b['bId']}...\n")
        self.__spread("Bloque", b)
        self.__spreadBlocks.append(b)
        # Miner can start again
        self.__minerAbort.clear()


  def __validateTx(self, tx: dict) -> bool:

    self.__writeLog(f"[{time.asctime()}]: Validating Transaction: {tx['txId']}...\n")

    try:
      tx["inputs"]
      tx["outputs"]
    except:
      return False
    else:
      # TODO: Verify scripts P2SH
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


  def __checkScript(self, script) -> bool:

    # TODO
    pass
    

  def __validateBlock(self, b: dict) -> bool:

    self.__writeLog(f"[{time.asctime()}]: Validating Block: {b['bId']}...\n")

    txsMerkle = pymerkle.MerkleTree()
    for tx in b["transactions"]:
      txsMerkle.update(tx["txId"])

    try:
      b["prevBlock"] == self.__blockchain.getChain()[-1].bId
      txsMerkle.rootHash.decode() == b["merkleRoot"]
      # Verify Proof of Work
      int(b["bId"], 16) < 2**(256 - (vars.INIT_DIFFICULTY / 100))
      return True
    except:
      return False


  def __chain(self, b: dict) -> None:

    self.__writeLog(f"[{time.asctime()}]: Adding block to blockchain: {b['bId']}...\n")

    bBlock           = block.Block(b["prevBlock"], b["merkleRoot"], b["transactions"])
    bBlock.bId       = b["bId"]
    bBlock.timestamp = b["timestamp"]
    self.__blockchain.add(bBlock)


  def __spread(self, request: str, info: dict) -> None:

    self.__writeLog(f"[{time.asctime()}]: Spreading...\n")
    msg = str((request, info)).encode()

    for neighbour in self.__neighbours:
      
      self.__writeLog(f"[{time.asctime()}]: Sending to {neighbour}: {info}...\n")
      
      s = socket.socket()
      s.connect((b'localhost', neighbour))
      s.send(msg) # TODO: Encrypt
      # BUG: Infinit loop/wait
      # self.__writeLog(f"[{time.asctime()}]: Waiting ack...\n")
      # self.__writeLog(f"[{time.asctime()}]: Got ack: {s.recv(512).decode()}...\n")
      s.close()


  # Filter mempool with transaction not in the winner block
  def __updateMempool(self, winner: dict) -> None:

    self.__writeLog(f"[{time.asctime()}]: Updating mempool: {self.__mempool}...\n")

    txsNotInWinner = [ tx for tx in self.__mempool if tx not in winner["transactions"] ]
    self.__mempool = []

    for tx in txsNotInWinner:
      self.__mempool.append(tx)

    self.__writeLog(f"[{time.asctime()}]: Mempool updated: {self.__mempool}...\n")


  def __miner(self) -> None:

    while True:

      self.__writeLog(f"[{time.asctime()}]: Mining started...\n")
      
      newBlock   = block.Block(self.__blockchain.getChain()[-1].bId, "-1", [])
      merkleTree = pymerkle.MerkleTree()

      # Ask if have to abort mining
      while not self.__minerAbort.is_set():

        if len(self.__mempool) != 0:

          self.__writeLog(f"[{time.asctime()}]: Checking transactions in mempool...\n")
  
          tx   = self.__mempool.pop()
          txId = tx["txId"]

          self.__writeLog(f"[{time.asctime()}]: Adding transaction to new block: {txId}...\n")
          newBlock.transactions.append(tx)
          newBlock.size += len(txId)
          
          self.__writeLog(f"[{time.asctime()}]: Adding transaction to merkle tree: {txId}...\n")
          merkleTree.update(txId.encode())

          # Full block
          if (newBlock.size == vars.BLOCK_MAX_SIZE):
    
            newBlock.timestamp  = time.asctime()
            newBlock.merkleRoot = merkleTree.rootHash.decode()
            self.__writeLog(f"[{time.asctime()}]: Executing Proof of work...\n")
            newBlock.pow()
            newBlock.timestamp  = time.asctime()
            self.__minedBlock.append(newBlock.__dict__)

      # Reset to false, restart mining
      self.__writeLog(f"[{time.asctime()}]: Restarting mining...\n")
      self.__minerAbort.clear()
      
      # Return transacctions to mempool
      self.__writeLog(f"[{time.asctime()}]: Returning transactions to mempool...\n")
      for tx in newBlock.transactions:
        self.__mempool.append(tx)
      

  def __writeLog(self, msg: str) -> None:

    with open(self.__logFile, "a") as logFile:
      logFile.write(msg)
