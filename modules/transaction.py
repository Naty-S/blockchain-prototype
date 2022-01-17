#!/usr/bin/env python3
import hashlib
from typing import List

import modules.identity as id


class Transaction:

  def __init__(self, sender: id.User, receiver: id.User, satoshis: int, inputs: List[dict]) -> None:
    
    tx              = sender.address.encode() + receiver.address.encode()
    self.txId       = hashlib.sha256(hashlib.sha256(tx).hexdigest().encode()).hexdigest()
    self.inputs     = inputs
    self.outputs    = [TxOutput(satoshis, receiver.address, 0).__dict__]
    # TODO: To verify P2SH
    self.senderKey   = sender.publKey
    self.receiverKey = receiver.publKey


class TxInput(Transaction):

  def __init__(self, prevTxId: str, prevTxOutIndex: int, value:int, address: str) -> None:
    self.prevTxId       = prevTxId
    self.prevTxOutIndex = prevTxOutIndex
    self.address        = address
    self.value          = value
    self.scriptSig      = "" # TODO


class TxOutput(Transaction):

  def __init__(self, value: float, address: str, index: int) -> None:
    self.value        = value
    self.address      = address
    self.index        = index
    self.spent        = False
    self.scriptPubKey = "" # TODO
