
import modules.block       as block
import modules.transaction as tx


class Blockchain:
  
  def __init__(self) -> None:
    self.__chain = []
    self.__genGensisBlock()


  def __genGensisBlock(self) -> None:

    self.__chain.append(block.Block("-1", "-1", "-1", []))


  def getChain(self) -> list: return self.__chain


  def add(self, b: block.Block) -> None: self.__chain.append(b)


  def blockExplorer(self) -> block.Block:
    pass


  def txExplorer(self) -> tx.Transaction:
    pass
