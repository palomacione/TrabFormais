import json

class RegularExpression():

	# Inicializador
	def __init__(self):
		self.regex = {}

	# Pretty print
	def __str__(self):
		formatted = []
		for left, right in self.regex.items():
			formatted.append(f"{left}:{right}\n")
		return "".join(formatted)

	# Lê o arquivo
	def load(self, file):
		# Preenche a variável rules
		with open(file, 'r') as f:
			lines = [line.rstrip() for line in f]
			for line in lines:
				line = line.split(':')
				left = line[0]
				right = line[1]
				self.regex[left] = right

	# Salva a GR em um arquivo json local
	def save(self, filename):
		formatted = []
		with open(filename, "w") as writer:
			for left, right in self.regex.items():
				formatted.append(f'{left}:{right}\n')
			writer.write("".join(formatted))
