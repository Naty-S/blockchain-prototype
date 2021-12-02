


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
