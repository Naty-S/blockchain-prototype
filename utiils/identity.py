import json


class Identity:

  def __init__(self, name, privKey, publKey, address) -> None:
    identity = {
      name : {
        "privKey" : privKey,
        "publKey" : publKey,
        "address" : address
      }
    }
    with open("identities.json", "w") as outfile:
      outfile.write(identity)
  
  def update(key, new_data):
    with open("identities.json",'r+') as file:
      file_data = json.load(file)
      file_data[key].append(new_data)
      # Sets file's current position at offset.
      file.seek(0)
      json.dump(file_data, file, indent = 2)


class User(Identity):

  def __init__(self, name, mail, privKey, publKey, address) -> None:
    super().__init__(name, privKey, publKey, address)
    new_data = {
      "mail" : mail,
      "utxoIns" : [],
      "utxoOuts" : []
    }
    super().update(self.name, new_data)


class Nodo(Identity):

  def __init__(self, name, privKey, publKey, address, port) -> None:
    super().__init__(name, privKey, publKey, address)
    self.port = port
    new_data = {
      "port" : port
    }
    super().update(self.name, new_data)
