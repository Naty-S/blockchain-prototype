
from identity import User, Nodo


def genIdentities(identities, nodos):
  x = 0
  while x < identities:
    privKey, publKey = __genKeys()
    name = "user" + x
    mail = name + "@gmail.com"
    address
    User(name, mail, privKey, publKey, address)
    x += 1

  x = 0
  while x < nodos:
    privKey, publKey = __genKeys()
    nodo = "nodo" + x
    address
    port
    Nodo(nodo, privKey, publKey, address, port)
    x += 1


def __genKeys():
  pass
