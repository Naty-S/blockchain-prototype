
import hashlib

import config.variables    as vars


class Block:

  def __init__(self, bId: str, prevBlock: str, merkleRoot: str, transactions: list[str]) -> None:

    self.bId          = bId # block header hash
    self.size         = 0
    self.nonce        = 0
    self.merkleRoot   = merkleRoot
    self.prevBlock    = prevBlock
    self.transactions = transactions
    self.timestamp    = ""
    self.height       = -1 # TODO position in the chain, pueden tener la misma altura al competir(forks)


  def __calcHash(self):
    
    self.bId = hashlib.sha256(hashlib.sha256(str(self.__dict__)).hexdigest().encode()).hexdigest()

  def pow(self):

    while int(self.bId.hexdigest(), 16) > 2**(256 - (vars.DIFFICULTY/100)):
      self.nonce += 1
      self.__calcHash()
