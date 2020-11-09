from GR import RegularGrammar
from AF import *
from collections import defaultdict
import copy

# Converte AFD para GR
def AFD_to_GR(AFD):
	GR = RegularGrammar()

	GR.initial_state = AFD.initial
	GR.non_terminals = AFD.states
	GR.terminals = AFD.alphabet

	# Preenche as regras
	rules = defaultdict(set)
	for curr_state, trans_next in AFD.trans.items():
		# Exemplo: curr_state = '0', trans_next = {'a': '1', 'b': '2'}
		for trans, next_state in trans_next.items():
			# Exemplo: trans = 'a', next_state = '1'
			symbol = trans + next_state
			rules[curr_state].add(symbol)
			# Se é um estado de aceitação
			if next_state in AFD.accepting:
				rules[curr_state].add(trans)
	# Se o estado inicial do AFD é um estado de aceitação
	if AFD.initial in AFD.accepting:
		# Cria um novo estado inicial S' que aceita tudo que
		# o antigo estado inicial aceitava mais epsilon
		rules["S'"] = rules[GR.initial_state].union('&')
		GR.initial_state = "S'"

	GR.rules = dict(rules)

	return GR

# Converte GR para AFND
def GR_to_AFND(GR):
	AFND = NDFiniteAutomata()

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
		# Exemplo: head = '0', body = {'a1', 'b', 'b2', 'a'}
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
	# Todos os símbolos do alfabeto vão do estado final para o estado morto
	for symbol in AFND.alphabet:
		trans['F'][symbol] = 'Ø'

	AFND.trans = dict(trans)

	return AFND

# Minimiza o AFD
def AFD_minimizer(AFD):

	# Eliminando os estados inalcançáveis
	unreachable = set()
	reachable_all = set(AFD.initial)
	visited = set()
	unvisited = set(AFD.trans[AFD.initial].values())
	# Exemplo: unvisited = {'1', '2'}
	while unvisited:
		reachable = unvisited.pop()
		reachable_all.add(reachable)
		# Se o estado alcanável ainda não foi verificado então
		# adicione todos os estados que ele alcança
		if reachable not in visited:
			unvisited.update(set(AFD.trans[reachable].values()))
			visited.add(reachable)
	unreachable = AFD.states - reachable_all - {AFD.initial}
	# Realizando a eliminação
	for state in unreachable:
		del AFD.trans[state]
	AFD.accepting = AFD.accepting - unreachable
	AFD.states = AFD.states - unreachable

	# Eliminando estados mortos
	reach_all = AFD.accepting
	reachable = set()
	visited = set()
	while reach_all:
		next_reach_all = set()
		for state, trans_next in AFD.trans.items():
			# Exemplo: state = 'A', trans_next = {'0': 'G', '1': 'B'}
			for reach in reach_all:
				# Se o state é alcanável por algum estado de qualquer outra estado
				if reach in trans_next.values():
					# Exemplo: reach = 'A', trans_next.values() = {'E', 'A'}
					reachable.add(state)
					if reach not in visited:
						next_reach_all.add(state)
		visited.update(reach_all)
		reach_all = next_reach_all
	unreachable = AFD.states - reachable - AFD.accepting
	# Realizando a eliminação
	for state in unreachable:
		del AFD.trans[state]
	AFD.accepting = AFD.accepting - unreachable
	AFD.states = AFD.states - unreachable

	# Montando estados equivalentes
	equivalencies = []
	equivalencies.append(AFD.accepting)
	equivalencies.append(AFD.states - AFD.accepting)
	next_equivalencies = []
	equivalencies_control = equivalencies[:]
	# Equanto houver mudanças nas classes de equivalência
	while (True):
		for char in AFD.alphabet:
			equivalencies_prev = []
			for equivalent in equivalencies:
				goes_to_index = defaultdict(set)
				# Exemplo: equivalent = {'E', 'C'}
				for state in equivalent:
					n_equivalencies = len(equivalencies)
					# Para qual estado state vai por char
					goes_to = AFD.trans[state].get(char, n_equivalencies)
					# Caso o estado não tenha transição por char
					# vár para nenhuma classe de equivalência existente
					if goes_to == n_equivalencies:
						goes_to_index[n_equivalencies].add(state)
					for i in range(len(equivalencies)):
						# Identifica a classe de equivalencia do estado atual
						if goes_to in equivalencies[i]:
							goes_to_index[i].add(state)
							break
					# Caso o estado não vá para nenhuma classe de equivalência existente
					else:
						goes_to_index[n_equivalencies].add(state)
				for new_equivalence in goes_to_index.values():
					equivalencies_prev.append(new_equivalence)
			# Substitui as classes de equivalências antigas
			equivalencies = equivalencies_prev
		if equivalencies_control == equivalencies:
			break
		equivalencies_control = equivalencies

	# Montando as transições do AFD minimizado
	# Renomeando os estados, criando o mapeamento
	mapping = {}
	i = 0
	while equivalencies:
		char = 'c' + str(i)
		mapping[char] = equivalencies.pop()
		i += 1
	print('Mapeamento:', mapping)

	trans = defaultdict(dict)
	initial = ''
	accepting = set()

	# Remapeando estados de aceitação, inicial e transações
	for map_char, states in mapping.items():
		state = next(iter(states))
		# Criando os estados de aceitação
		if state in AFD.accepting:
			accepting.add(map_char)
		# Criando o estado inicial
		if state == AFD.initial:
			initial = map_char
		# Remapeando as transações
		for char in AFD.alphabet:
			goes_to = AFD.trans[state].get(char)
			if goes_to:
				for map_char_aux, states_aux in mapping.items():
					if goes_to in states_aux:
						trans[map_char][char] = map_char_aux

	AFD_min = FiniteAutomata()
	AFD_min.trans = trans
	AFD_min.initial = initial
	AFD_min.accepting = accepting
	AFD_min.states = mapping.keys()
	AFD_min.alphabet = AFD.alphabet

	return AFD_min

def getState(l):
    if len(l) > 1:
        l = list(l)
        l.sort()
        return ''.join(l)
    else:
        return list(l)[0]

def AFND_determinizer(AFND):
	AF = FiniteAutomata()
	AF.initial = AFND.initial
	alph = AFND.alphabet

	if "&" in alph:
		AF.alphabet = alph.remove("&")
	else:
		AF.alphabet = alph
	AF.alphabet = AFND.alphabet
	tState = []  # Novos estados que surgem a partir de transições
	AF.initial = AFND.initial

	for state in AFND.states:
		tState.append({state})  # Aqui eu adiciono os estados para começar a transitar por eles
	while tState:
		stateList = list(tState.pop())
		init = False
		if len(stateList) == 1 and stateList[0] == AFND.initial:
			init = True
		(stateClosure, isAccepting) = AFND.eClosure(stateList)
		s = getState(stateClosure)  # Essa parte deixa o estado [0,1,2] como "012" na lista de estados
		AF.addState(s)

		if init:
			AF.initial = s
		if isAccepting:
			AF.addAccepting(s)

		for a in AFND.alphabet:  # Pra cada letra do alfabeto
			if a == "&":   # (não irei mais transitar por &)
				continue
			trans = set() # Cria um set com as novas transições
			for toState in stateClosure:  # Pra cada estado do meu e-fecho
				if a not in AFND.trans[toState]:   # Se eu não transito pela letra, continua pro próx estado do e-fecho
					continue
				trans.update(AFND.trans[toState][a])  # Se não, coloca no set o estado para qual eu transito pela letra
			if len(trans) == 0:   # Se não tenho transição, continua pra próxima letra
				continue
			(closure, isAccepting) = AFND.eClosure(list(trans)) # Se eu tenho, então faço o e-fecho dos estados que eu adicionei
			newState = getState(closure)  # Transforma naquele jeito bonitinho
			if not newState in AF.trans and not newState in tState:  # Se eu ainda não tenho esse estado nas minha lista de transições, adiciona
				tState.append(closure)
			AF.addTrans(s, a, newState)

	return AF

# Converte ER para AFD
def ER_to_AFD(ER):
	er = ER.regex['er']
	print(ER)
	# TODO

# Realiza a fatoração de um GLC
def GLC_remove_left_recursion(GLC_with_recursion):
	GLC = copy.deepcopy(GLC_with_recursion)

	# Ordenando a lista A
	# Exemplo de formato ordenado: S'', S', S, A, B, C...
	A_unsorted = sorted(list(GLC.non_terminals))
	A = []
	for symbol in A_unsorted:
		if symbol[0] != 'S':
			A.append(symbol)
		else:
			A.insert(0, symbol)

	# Eliminando recursividade à esquerda
	for i in range(len(A)):

		# Recursões indiretas
		for j in range(i):
			# Para todos os símbolos em A[i]
			alpha = ''
			production = ''
			found = False
			if A[i] in GLC.rules:
				for p in GLC.rules[A[i]]:
					# Se A[j]alpha pertence a uma das produções de A[i]
					if len(p) > 1 and p[0] == A[j]:
						# Armazenando alpha
						alpha = p[1:]
						# Produção a ser removida
						production = p
						# Avisa que produção foi encontrada
						found = True
						break
				if found:
					#  Removendo produção de A[i]
					GLC.rules[A[i]].remove(production)
				Aj_body = GLC.rules.get(A[j])
				# Se A[j] existir como cabeça
				if Aj_body:
					# Adicione todas as produções de A[j] (concatenado com alpha)
					# no corpo de A[i]
					for p in Aj_body:
						GLC.rules[A[i]].add(p + alpha)

		# Recursões diretas
		new_head = A[i] + "'"
		new_body = set()
		to_keep = set()
		# Caso o terminal seja cabeça de alguma produção
		if A[i] in GLC.rules:
			for p in GLC.rules[A[i]]:
				# Se houver recursão direta à esquerda da produção
				if p[0] == A[i]:
					# Adicione o restante da produção mais a nova cabeça no novo corpo
					new_body.add(p[1:] + new_head)
				else:
					to_keep.add(p + new_head)
			# Se alguma recursão direta foi encontrada atualize as cabeças
			if new_body:
				GLC.rules[A[i]] = to_keep
				new_body.add('&')
				GLC.rules[new_head] = new_body

	return GLC

























#
