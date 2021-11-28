import socket, pickle


class Nodo:

  def __init__(self) -> None:
    self.netListener # thread
    self.miner # thread


def netListener():
  s = socket.socket()
  # host = "nodo1" # ident.Node.name
  # s.bind((host.name, host.port))
  s.bind((socket.gethostname(), nodo.port))
  s.listen(5)

  data = []
  while True:
    c, addr = s.accept()
    print('Got connection from address: ', addr)
    
    # bufsize = c.getsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF)
    # print("client bufsize: ",c.__sizeof__)
    packet = c.recv(65536)
    # print("packet len: ", len(packet))
    # if not packet: break
    
    # data.append(packet)
    # v = b''.join(data)
    # data_arr = pickle.loads(packet)
    # print("Data recv from client: ", data_arr)

    c.send(b'Thank you for connecting client')
    c.close()

