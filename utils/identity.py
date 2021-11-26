

class Identity:

  def __init__(self, name: str, privKey: str, publKey: str, address: str) -> None:
    self.name = name
    self.privKey = privKey
    self.publKey = publKey
    self.address = address


class User(Identity):

  def __init__(self, name: str, mail: str, privKey: str, publKey: str, address: str, utxo) -> None:
    super().__init__(name, privKey, publKey, address)
    self.mail = mail
    self.utxo = utxo
    

class Nodo(Identity):

  def __init__(self, name: str, privKey: str, publKey: str, address: str, port: int) -> None:
    super().__init__(name, privKey, publKey, address)
    self.port = port