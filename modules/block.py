#!/usr/bin/env python3
import hashlib
from typing import List

import config.variables    as vars


class Block:

  def __init__(self, prevBlock: str, merkleRoot: str, transactions: List[str]) -> None:

    self.size         = 0
    self.nonce        = 0
    self.merkleRoot   = merkleRoot
    self.prevBlock    = prevBlock
    self.transactions = transactions
    self.timestamp    = ""
    header   = str(self.prevBlock) + str(self.merkleRoot) + str(self.nonce) + self.timestamp + str(self.transactions)
    self.bId = hashlib.sha256(hashlib.sha256(header.encode()).hexdigest().encode()).hexdigest()
    self.height       = -1 # TODO position in the chain, pueden tener la misma altura al competir(forks)


  def calcHash(self):
    
    header   = str(self.prevBlock) + str(self.merkleRoot) + str(self.nonce) + self.timestamp + str(self.transactions)
    self.bId = hashlib.sha256(hashlib.sha256(header.encode()).hexdigest().encode()).hexdigest()
    

  # Proof of Work
  def pow(self):

    while int(self.bId, 16) > 2**(256 - (vars.INIT_DIFFICULTY / 100)):
      self.nonce += 1
      self.calcHash()
