import json
from copy import deepcopy
from collections import defaultdict

class ContextFreeGrammar():
	# Inicializador
	def __init__(self):
		self.rules = {}
		self.initial_state = ''
		self.terminals = set()
		self.non_terminals = set()
		self.heads_sorted = []

	# Pretty print
	def show(self):
		formatted = []

		for head, body in self.rules.items():
			formatted_body = []
			for b in body:
				formatted_body.append(b)
				formatted_body.append(' | ')
			formatted_body = formatted_body[:-1]
			formatted_body = "".join(formatted_body)
			formatted.append(f'{head} -> {formatted_body}\n')

		print("".join(formatted))

	# Lê o arquivo
	def load(self, file):
		# Preenche a variável rules
		i = 0
		with open(file, 'r') as f:
			lines = [line.rstrip() for line in f]
			for line in lines:
				line = line.split(' ')
				head = line[0]
				body = set()
				# Lê os símbolos após a string "->"
				for symbol in line[2:]:
					if symbol != '|':
						body.add(symbol)
						i += 1
				self.rules[head] = body

		# Preenche o símbolo inicial
		self.initial_state = next(iter(self.rules))

		# Preenche os símbolos terminais e não-terminais
		for head, body in self.rules.items():
			for symbols in body:
				for char in symbols:
					if char.isupper():
						self.non_terminals.add(char)
					elif char != "'":
						self.terminals.add(char)
			self.heads_sorted.append(head)
			self.non_terminals.add(head)

	# Salva a GR em um arquivo json local
	def save(self, filename):
		formatted = []
		with open(filename, "w") as writer:
			for head, body in self.rules.items():
				formatted_body = []
				for b in body:
					formatted_body.append(b)
					formatted_body.append(' | ')
				formatted_body = formatted_body[:-1]
				formatted_body = "".join(formatted_body)
				formatted.append(f'{head} -> {formatted_body}\n')
			writer.write("".join(formatted))

	def addRule(self, head, body):
		if head not in self.rules:
			self.rules[head] = ''
		self.rules[head] = body

class RegularGrammar(ContextFreeGrammar):
	def __init__(self):
		super().__init__()
