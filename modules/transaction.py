import hashlib

import modules.identity as id


class Transaction:

  def __init__(self, sender: id.User, receiver: id.User, satoshis: int, inputs: list) -> None:
    
    tx            = sender.address.encode() + receiver.address.encode()
    self.txId     = hashlib.sha1(hashlib.sha1(tx).hexdigest().encode()).hexdigest()
    self.inputs   = inputs
    self.outputs  = [TxOutput(satoshis, receiver.address, 0).__dict__]

    # TODO: posiblemente inutil
    self.sender   = sender.address # la encripta con su pub key
    self.receiver = receiver.address


class TxInput(Transaction):

  def __init__(self, prevTxId: str, prevTxOutIndex: int, address: str) -> None:
    self.prevTxId       = prevTxId
    self.prevTxOutIndex = prevTxOutIndex
    self.address        = address
    self.scriptSig      = "" # TODO


class TxOutput(Transaction):

  def __init__(self, value: float, address: str, index: int) -> None:
    self.value        = value # TODO: encriptar?
    self.address      = address
    self.index        = index
    self.spent        = False
    self.scriptPubKey = "" # TODO
