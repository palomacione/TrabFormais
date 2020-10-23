import json
from copy import deepcopy

class RegularGrammar():

	# Inicializador
	def __init__(self):
		self.rules = {}
		self.initial_state = ''
		self.terminals = set()
		self.non_terminals = set()

	# Pretty print
	def __str__(self):
		formatted = []

		formatted.append('\nRepresentacao interna:\n')
		formatted.append(f"Estado inicial: '{self.initial_state}'\n")
		formatted.append(f'Terminais: {self.terminals}\n')
		formatted.append(f'Nao-terminais: {self.non_terminals}\n')
		formatted.append('Regras:\n')
		for head, body in self.rules.items():
			formatted.append(f"'{head}': {body}\n")

		formatted.append('\nRepresentacao ao usuario:\n')
		for head, body in self.rules.items():
			print(body)
			formatted_body = []
			for b in body:
				formatted_body.append(b)
				formatted_body.append(' | ')
			formatted_body = formatted_body[:-1]
			formatted_body = "".join(formatted_body)
			formatted.append(f'{head} -> {formatted_body}\n')

		return "".join(formatted)

	# Lê o arquivo
	def load(self, file):
		# Preenche a variável rules
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
				self.rules[head] = body

		# Preenche o símbolo inicial
		self.initial_state = next(iter(self.rules))

		# Preenche os símbolos terminais e não-terminais
		for body in self.rules.values():
			for symbols in body:
				for char in symbols:
					if char.islower():
						self.terminals.add(char)
					else:
						self.non_terminals.add(char)

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

