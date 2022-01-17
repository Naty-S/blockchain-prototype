#!/usr/bin/env python3
import modules.block       as block


class Blockchain:
  
  def __init__(self) -> None:
    self.__chain = []
    self.__genGensisBlock()


  def __genGensisBlock(self) -> None:

    self.__chain.append(block.Block("-1", "-1", []))


  def getChain(self) -> list:
    
    return self.__chain


  def add(self, b: block.Block) -> None:
    
    self.__chain.append(b)


  def blockExplorer(self, flag: str, value: str) -> None:
    
    # get from hash
    if flag == '-h':
      found = False
      for i in range(len(self.__chain)):
        if value == self.__chain[i].bId:
          print(f"Bloque {value}:\n{self.__chain[i]}")
          found = True

      if not found: print(f"Bloque {value} no encontrado")

    # get from height
    elif flag == '-a':
      if -1 < int(value) < len(self.__chain):
        print(f"Bloque de altura {value}:\n{self.__chain[value]}")
      else:
        print(f"Altura {value} invalida")
    else:
      print("Solo se permite buscar por altura (-a) o(exclusivo) hash (-h)")


  def txExplorer(self, flag: str, hash: str) -> None:
    
    if flag == "-h":
      found = False
      for b in self.__chain:
        for tx in b.transactions:
          if hash == tx["txId"]:
            print(f"Transaccion {hash}:\n{tx}")
            found = True

      if not found: print(f"Transaccion {hash} no encontrada")
    else:
      print("Solo se permite buscar hash (-h)")
