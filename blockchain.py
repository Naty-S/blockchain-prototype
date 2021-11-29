import hashlib
from block import Block

class Blockchain():
	def __init__(self, difficulty):
		self.difficulty = difficulty
		self.chain = []
		self.transactions = []
		self.genesisBlock()

		# crea el bloque genesis
	def genesisBlock(self):
		hash = hashlib.sha256()
		hash.update('0'.encode())
		genesis = Block('genesis', hash)
		genesis.mineB((self.difficulty/100))
		self.chain.append(genesis)

		# valida que el hash del bloque enviado es igual al que se crea
		# valida que el hash supero la dificultad preestablecidad de minado
		# valida que el hash que recibe del bloque anterior es en efecto el prevHash
	def validation(self, block):	
		hash = hashlib.sha256() 
		hash.update(str(block).encode())
		return block.hash.hexdigest() == hash.hexdigest() and int(block.hash.hexdigest(),16) < 2**(256-(self.difficulty)/100) and block.previousHash == self.chain[-1].hash
		
		# agrega una transaccion al mempool
	def addTransaccion(self, transaction):
		self.transactions.append(transaction)

		# agrega un bloque a la cadena luego de validarlo 
	def addToBlockchain(self, block):
		if self.validation(block) == True:
			self.chain.append(block)

		# agrega transacciones al bloque luego de conseguir el nonce
	def addToBlock(self):
		if len(self.transactions) > 0:
			transaction = self.transactions.pop(0)
			newBlock = Block(transaction, self.chain[-1].hash)
			newBlock.mineB(self.difficulty)
			self.addToBlockchain(newBlock)
			print('\n\n====================')
			print('Hash:\t\t', newBlock.hash.hexdigest())
			print('previousHash:\t\t', newBlock.previousHash.hexdigest())
			print('Nonce:\t\t', newBlock.nonce)
			print('Transaction:\t\t', newBlock.transactions)
			
		# funcion que consigue el nonce (mina, PoW)
	def mineB(self, difficulty):		
		self.hash.update(str(self).encode())
		while int(self.hash.hexdigest(), 16) > 2**(256 - (difficulty/100)):
			self.hash = hashlib.sha256()
			self.nonce += 1		
			self.hash.update(str(self).encode())
