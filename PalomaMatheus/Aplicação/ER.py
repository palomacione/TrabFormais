import json

class RegularExpression:

	# Inicializador
	def __init__(self):
		self.regex = {}

	# Pretty print
	def show(self):
		formatted = []
		for left, right in self.regex.items():
			formatted.append(f"{left}:{right}\n")
		print("".join(formatted))

	# Lê o arquivo
	def load(self, file):
		# Preenche a variável rules
		with open(file, 'r') as f:
			lines = [line.rstrip() for line in f]
			for line in lines:
				line = line.split(':')
				left = line[0]
				right = line[1][1:]
				self.regex[left] = right

	# Salva a GR em um arquivo json local
	def save(self, filename):
		formatted = []
		with open(filename, "w") as writer:
			for left, right in self.regex.items():
				formatted.append(f'{left}:{right}\n')
			writer.write("".join(formatted))


# class Node:
# 	def __init__(self, val = None, firstPos = 0, lastPos = 0, nullable = False, isRoot = False):
# 		self.val = val
# 		self.firstPos = firstPos
# 		self.lastPos = lastPos
# 		self.left = None
# 		self.right = None
# 		self.nullable = nullable
# 		self.isRoot = isRoot
#
# 	def show(self):
# 		print(f'Symbol: {self.val}')
# 		print(f'FirstPos: {self.firstPos}')
# 		print(f'LastPos: {self.lastPos}')
# 		print(f'Left Child: {self.left.val}')
# 		print(f'Right Child: {self.right.val}')
# 		print(f'Nullable: {self.nullable}')
#
# 	def insert(self, other, operands):
# 		if self.val == other.val
# 			return
# 		elif self.right is not None:
# 			self.left = other
# 		else:


