import hashlib

class Block():
	# atributos del bloque
	def __init__ (self, transactions, previousHash):
		self.hash = hashlib.sha256()
		self.previousHash = previousHash
		self.nonce = 0
		self.transactions = transactions
	# funcion que consigue el nonce (mina)
	def mineB(self, difficulty):		
		self.hash.update(str(self).encode())
		while int(self.hash.hexdigest(), 16) > 2**(256 - (difficulty/100)):
			self.hash = hashlib.sha256()
			self.nonce += 1		
			self.hash.update(str(self).encode())

	def __str__(self):
		return "{}{}{}".format(self.previousHash.hexdigest(), self.transactions, self.nonce )



