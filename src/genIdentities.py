import bitcoin as btc

import utils.identity as ident


def genIdentities(identities: int, nodos: int) -> list[ident.Identity]:
  
  idents = list[ident.Identity]

  for x in range(identities):
    privKey, publKey = __genKeys()
    name = "user" + str(x)
    mail = name + "@gmail.com"
    address = btc.pubkey_to_address(publKey)
    utxo = {
      "ins" : {},
      "outs" : {}
    }
    i = ident.User(name, mail, privKey, publKey, address, utxo)
    idents.append(i)

  for x in range(nodos):
    privKey, publKey = __genKeys()
    nodo = "nodo" + str(x)
    address = btc.pubkey_to_address(publKey)
    port = -1 # TODO: por definir
    i = ident.Nodo(nodo, privKey, publKey, address, port)
    idents.append(i)
  

  return idents


def __genKeys() -> str:
  privKey = btc.random_key()
  publKey = btc.privkey_to_pubkey(privKey)

  return privKey, publKey
