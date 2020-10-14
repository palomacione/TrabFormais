from GR import RegularGrammar
from AF import FiniteAutomata
from collections import defaultdict

# Converte AFD para GR
def AFD_to_GR(AFD):
	GR = RegularGrammar()

	GR.initial_state = AFD.initial
	GR.non_terminals = AFD.states
	GR.terminals = AFD.alphabet

	# Preenche as regras
	rules = defaultdict(set)
	for curr_state, trans_next_state in AFD.trans.items():
		# Exemplo: curr_state = '0', trans_next_state = {'a': '1', 'b': '2'}
		for trans, next_state in trans_next_state.items():
			# Exemplo: trans = 'a', next_state = '1'
			symbol = trans + next_state
			rules[curr_state].add(symbol)
			# Se é um estado de aceitação
			if next_state in AFD.accepting:
				rules[curr_state].add(trans)
	# Se o estado inicial do AFD é um estado de aceitação
	if AFD.initial in AFD.accepting:
		# Procura pelo estado inicial no corpo das regras
		for body in rules.values():
			# Se estado inicial foi encontrado no corpo de uma regra
			if AFD.initial in body:
				# TODO
				# Fazer L(G) U {&} (?)
				break
		# O estado inicial não foi encontrado no corpo de uma regra
		else:
			rules[GR.initial_state].add('&')

	GR.rules = dict(rules)

	return GR

# Converte GR para AFND
def GR_to_AFND(GR):
	AFND = FiniteAutomata()
	print(GR)

	AFND.states = GR.non_terminals.union('F')
	AFND.alphabet = GR.terminals
	AFND.initial = GR.initial_state

	# Preenche os estados finais
	if '&' in GR.rules[GR.initial_state]:
		AFND.accepting.add('&')
	AFND.accepting.add('F')

	# Preenche a tabela de transições
	trans = defaultdict(dict)
	for head, body in GR.rules.items():
		# Exemplo: head = '0', body = {'a1', 'b', 'b2': 'a'}
		for symbol in body:
			# Se símbolo é um símbolo terminal
			if len(symbol) == 1 and symbol in GR.terminals:
				for accept in AFND.accepting:
					# Exemplo: head = '0', symbol = 'a', accept = 'F'
					if symbol not in trans[head]:
						trans[head][symbol] = {accept}
					else:
						trans[head][symbol].add(accept)
			else:
				# Examplo: head = '0', symbol = 'a1'
				if symbol[0] not in trans[head]:
					trans[head][symbol[0]] = {symbol[1]}
				else:
					trans[head][symbol[0]].add(symbol[1])
	# Todo os símbolos do alfabeto vão do estado final para o estado morto
	for symbol in AFND.alphabet:
		trans['F'][symbol] = {'M'}
	# Todo os símbols do alfabeto vão do estado morto para o estado morto
	for terminal in AFND.alphabet:
		trans['M'][terminal] = {'M'}

	AFND.trans = dict(trans)

	return AFND

# Returns True if AF recognizes the string s
def AF_string_recognizer(AF, s):
	# TODO
	# AFD = AFND_to_AFD(AF) melhor converter para AFD primeiro (método ainda não existe)
	AFD = AF
	curr_state = AFD.initial
	for char in s:
		next_state = AFD.trans[curr_state].get(char)
		# Se é possível ir de curr_state para next_state por char
		if next_state:
			curr_state = next_state
		else:
			return False
	# Se o estado em que a computação parou for um estado final
	if curr_state in AFD.accepting:
		return True
	else:
		return False
