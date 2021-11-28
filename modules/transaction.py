import hashlib

import modules.identity as id


class Transaction:

  def __init__(self, sender: id.User, receiver: id.User, satoshis: int = 10000000, inputs = set()) -> None:
    
    tx            = sender.address.encode() + receiver.address.encode()
    self.txId     = hashlib.sha256(hashlib.sha256(tx).hexdigest().encode()).hexdigest()
    self.sender   = sender
    self.receiver = receiver
    self.satoshis = satoshis
    self.inputs   = inputs
    self.outputs  = { self.receiver.address : (False, satoshis) }
    self.fee      = -1 # TODO: por definir
  

  def __str__(self) -> str:
    return "\n\nTransaccion: " + self.txId + \
           "\n\tEntradas: \n\t\t" + str(self.inputs) + \
           "\n\tSalidas: \n\t\t" + str(self.outputs) + "\n\n"

  
  def change(self) -> dict():

    inputs = sum(self.inputs)
    if inputs > self.satoshis:
      return { self.sender.address : (False, inputs - self.satoshis) }

    return {}
  