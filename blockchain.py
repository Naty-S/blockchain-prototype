import hashlib
from datetime import datetime
from block import Block
from merkleTree import MerkleTree

chain = []
pool = []

class Blockchain():
	def __init__(self, difficulty):
		self.difficulty = difficulty
		self.genesisBlock()
		global chain
		global pool

		# crea el bloque genesis
	def genesisBlock(self):
		hash = hashlib.sha256()
		hash.update('genesis'.encode())
		genesis = Block(str([0]), hash)
		genesis.mineB((self.difficulty/100))
		chain.append(genesis)
		print('\n\n=================================================================\n\n')
		print('Hash:\t\t', genesis.hash.hexdigest())
		print('previousHash:\t\t', genesis.previousHash.hexdigest())
		print('Nonce:\t\t', genesis.nonce)
		print('Transaction:\t\t', '[0]')

		# valida que el hash del bloque enviado es igual al que se crea
		# valida que el hash supero la dificultad preestablecidad de minado
		# valida que el hash que recibe del bloque anterior es en efecto el prevHash
	def validation(self, block):	
		hash = hashlib.sha256() 
		hash.update(str(block).encode())
		return block.hash.hexdigest() == hash.hexdigest() and int(block.hash.hexdigest(),16) < 2**(256-(self.difficulty)/100) and block.previousHash == chain[-1].hash
		
		# agrega una transaccion al mempool
	def addTransaction(self, transaction):
		pool.append(transaction)

		# agrega un bloque a la cadena luego de validarlo 
	def addToBlockchain(self, block):
		if self.validation(block) == True:
			chain.append(block)

		# agrega transacciones al bloque y lo añade a la cadena
	def createNewBlock(self):

		transactions = []

		while len(pool)>0:
			transaction = pool.pop(0)
			transactions.append(transaction)
		
		newBlock = Block(transactions, chain[-1].hash)
		newBlock.mineB(self.difficulty)
		newBlock.merkleTree = MerkleTree(transactions)
		newBlock.rootHash = str(newBlock.merkleTree.getRootHash())
		newBlock.time = str(datetime.now())
		self.addToBlockchain(newBlock)
		
		print('\n\n=================================================================\n\n')
		print('Hash:                 ', newBlock.hash.hexdigest())
		print('previousHash:         ', newBlock.previousHash.hexdigest())
		print('transactions:         ', newBlock.transactions)
		print('Nonce:                ', newBlock.nonce)
		print('Creation time:        ', newBlock.time)
		print('merkleTree root hash: ', newBlock.merkleTree.getRootHash())
		
	def blockExplorer(self, h, x):
		i = 0
		if h == '-h':
			for i in range(len(chain)):
				t = str(chain[i].hash.hexdigest())
				if x == t:
					return int(i)
				else:
					pass
		elif h == '-a':
			if  int(x) > -1 and int(x) < len(chain) :
				return int(x)
			else:
				print('\n\nout of range')

	







# Prueba blockCreation

blockchain = Blockchain(2000)

for i in range(3):
	
	blockchain.addTransaction('t'+str(i+1))
	blockchain.createNewBlock()


# Prueba blockExplorer

q = blockchain.blockExplorer('-h','00000e45525e82cb9ca68b16354e364d23c9034bc796aec41a343c93cd686096')


print('\n\n=================================================================\n\n')

print('Hash:                  ', str(chain[q].hash.hexdigest()))
print('Previous Hash:         ', str(chain[q].previousHash.hexdigest()))
print('Block height:          ', str(q))
print('Transactions:          ', str(chain[q].transactions))
print('Nonce:                 ', str(chain[q].nonce))
print('Creation Time:         ', str(chain[q].time))
#print('MerkleTree root hash:  ', str(chain[q].merkleTree.getRootHash())
