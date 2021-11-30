import socket, threading, ast

import modules.block       as block
import modules.transaction as tx


class Nodo:

  def __init__(self, name:str, port:int, neighbours: list[dict()]) -> None:

    self.name             = name
    self.port             = port
    self.neighbours       = neighbours # [{ n.name: n.port }]
    self.sock             = socket.socket()
    self.txsPropagadas    = []
    self.blocksPropagados = []
    self.mempool          = []
    self.netListenerT     = threading.Thread(name=self.name+"-netListener", target=self.netListener)
    self.minerT           = threading.Thread(name=self.name+"-miner", target=self.miner)

    """ COMO ENVIAR MSJ ENTRE NODOS """
    self.sock.bind((socket.gethostname(), 5100))
    self.netListenerT.start()
    self.minerT.start()


  def netListener(self):

    print("netListener started...")

    # Presentarse

    self.sock.listen(5)

    while True:
      c, addr = self.sock.accept()
      
      msg = c.recv(2048)
      t   = ast.literal_eval(msg.decode())
      print(t)


      # if msg == 'Transacción Nueva' | 'Transacción'
        # if tx in self.txsPropagadas: continue
        # else:
          # if self.__validateTx(tx):
            # self.mempool.append(tx)
            # self.__propagar('Transacción', tx)
            # self.sock.send(b'Si')
            # self.__writeLog("Transaccion {tx} recibida y validada {time}")
          # else:
            # self.sock.send(b'No')
            # self.__writeLog("Transaccion {tx} recibida y rechazada {time}")
      # else: # Se asume msg == 'Bloque'
        # if b in self.blocksPropagados: continue
        # else:
          # if self.__validateBlock(b):
            # abort miner
            # encadenar
            # self.__propagar('Bloque', b)
            # self.__writeLog("Bloauqe {b} recibido y validado {time}")
          # else:
            # self.sock.send(b'No')
            # self.__writeLog("Bloque {b} recibido y rechazado {time}")


      c.send(b'Thank you for connecting client')
      c.close()


  def __validateTx(self, t) -> bool:
    pass


  def __validateBlock(self, b) -> bool:
    pass


  def __propagar(self, msg: str):

    # for neighbour in self.neighbours:
      # s = socket.socket()
      # s.bind((socket.gethostname(), neighbour.port))
      # s.send(msg, neighbour)
      # s.close()
    pass


  def __writeLog(self, msg: str):
    pass


  def miner(self, abort: bool = False) -> block.Block:

    print("Miner started...")

    while not abort:

      # for tx in self.mempool:
        # block.add(tx)
      
      # calcular hash (merkle root)
      # enviar bloque a self.netListener
      pass

    # abort
      # vaciar bloque
      # self.miner()
