from GR import RegularGrammar
from collections import defaultdict

# Converte AF para GR
def AF_to_GR(AF):
	GR = RegularGrammar()

	GR.S = AF.initial
	GR.non_terminals = AF.states
	GR.terminals = AF.alphabet

	# Preenche as regras
	rules = defaultdict(set)
	for curr_state, trans_next_state in AF.trans.items():
		# Exemplo: curr_state = 0, trans_next_state = {'a': '1', 'b': '2'}
		for trans, next_state in trans_next_state.items():
			# Exemplo: trans = a, next_state = 1
			symbol = trans + next_state
			rules[curr_state].add(symbol)
			# Se é um estado de aceitação
			if next_state in AF.accepting:
				rules[curr_state].add(trans)
	GR.rules = dict(rules)

	return GR
