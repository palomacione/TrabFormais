from GR import RegularGrammar
from AF import *
from ER import *
from collections import defaultdict
import copy
from prettytable import PrettyTable

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
	while True:
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

# Verifica se a GLC é &-livre
def epsilon_free(GLC):
	# Encontra se há alguma &-produção (que não esteja no símbolo inicial da GLC)
	for head, body in GLC.rules.items():
		if head != GLC.initial_state:
			for production in body:
				if production == '&':
					return False
	return True

# Realiza a fatoração da GLC
def GLC_remove_left_recursion(GLC_with_recursion):
	GLC = copy.deepcopy(GLC_with_recursion)

	if not epsilon_free(GLC):
		GLC = GLC_remove_e_productions(GLC)
		print('\nSua GLC foi transformada em &-livre')
		print('Sua nova GLC &-livre é:')
		GLC.show()

	# Lista ordenada de cabeças A
	A = GLC.heads_sorted

	# Eliminando recursividade à esquerda
	for i in range(len(A)):

		# Recursões indiretas
		for j in range(i):
			# Para todos os símbolos em A[i]
			alphas = []
			productions = []
			if A[i] in GLC.rules:
				for p in GLC.rules[A[i]]:
					# Se A[j]alpha pertence a uma das produções de A[i]
					if len(p) > 1 and p[0] == A[j]:
						# Armazenando alpha
						alphas.append(p[1:])
						# Produção a ser removida
						productions.append(p)
				for k in range(len(productions)):
					#  Removendo produção de A[i]
					GLC.rules[A[i]].remove(productions[k])
					Aj_body = GLC.rules.get(A[j])
					# Se A[j] existir como cabeça
					if Aj_body:
						# Adicione todas as produções de A[j] (concatenado com alpha)
						# no corpo de A[i]
						for p in Aj_body:
							GLC.rules[A[i]].add(p + alphas[k])

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

	# (adicionado posteriormente) Renova os não-terminais da GLC
	# (adicionado posteriormente) Renova a haeds sorted da GLC
	new_non_terminals = set()
	new_heads_sorted = GLC.heads_sorted[:]
	for non_terminal in GLC.rules.keys():
		new_non_terminals.add(non_terminal)
		if non_terminal not in new_heads_sorted:
			new_heads_sorted.append(non_terminal)
	GLC.non_terminals = new_non_terminals
	GLC.heads_sorted = new_heads_sorted

	return GLC

# Remove as &-produções da GLC
def GLC_remove_e_productions(GLC_with_e_productions):
	GLC = copy.deepcopy(GLC_with_e_productions)

	# Criando o cojunto E (conjunto dos &-não-terminais)
	E = {'&'}
	new_head_added = True
	# Enquanto E ainda continua mudando, ou seja, enquanto ainda há N sendo encontrados
	while new_head_added:
		new_head_added = False
		# Passe por todas as produções
		for head, body in GLC.rules.items():
			# Passe por todas as produções que ainda não estão em E
			if head not in E:
				# Se alguma produção for totalmente marcada, adicione sua cabeça à E
				for production in body:
					i = 0
					while i < len(production):
						char = production[i]
						# Considerando que pode haver não-terminais do tipo X'''...
						while i+1 < len(production) and production[i+1] == "'":
							char += "'"
							i += 1
						if char not in E:
							break
						i += 1
					else:
						new_head_added = True
						E.add(head)

	# Realiza o powerset de uma lista
	def powerset(l):
		x = len(l)
		ps = []
		for i in range(1 << x):
			ps.append(''.join([l[j] for j in range(x) if (i & (1 << j))]))
		return ps

	# Removendo as &-produções e incluindo novas produções
	# Passando por todas as regras
	for head, body in GLC.rules.items():
		new_productions = set()
		for production in body:
			# As produções que a regra já tinha são mantidas
			if production != '&':
				new_productions.add(production)
				# Se a produção tiver um símbolo (ou conjunto de
				# símbolos, por isso a utilização de combinations)
				# que está em E então descarte tal símbolo da produção e
				# adicione o restante da produção como uma nova produção
				if len(production) > 1:
					to_remove = []
					i = 0
					while i < len(production):
						char = production[i]
						# Considerando que pode haver não-terminais do tipo X'''...
						while i+1 < len(production) and production[i+1] == "'":
							char += "'"
							i += 1
						if char in E:
							to_remove.append(char)
						i += 1
					to_remove = powerset(to_remove)
					for symbols in to_remove:
						new_production = production
						for symbol in symbols:
							new_production = new_production.replace(symbol, '')
						if new_production != "":
							new_productions.add(new_production)
		# Atualiza as produções antigas
		GLC.rules[head] = new_productions

	# Se o estado inicial pertence ao conjunto E
	if GLC.initial_state in E:
		# Salvando as regras antigas para deixar o estado final
		# como primeiro elemento do dicionário
		previous_rules = GLC.rules
		GLC.rules = {}
		new_initial_state = GLC.initial_state + "'"
		GLC.rules[new_initial_state] = {GLC.initial_state, '&'}
		GLC.rules.update(previous_rules)
		GLC.non_terminals.add(new_initial_state)
		GLC.initial_state = new_initial_state

	return GLC

# Remove as produções unitárias da GLC
def GLC_remove_unitary_productions(GLC_with_unitary_productions):

	# Passa por todos as produções de uma regra e recursivamente entra
	# em não-terminal isolados para adicionar suas produções
	def search_productions(head, body):
		visited_heads.add(head)
		for production in body:
			# Se for um não-terminal isolado ainda não visitado
			if len(production) == 1 and production in GLC.non_terminals and production not in visited_heads:
				search_productions(production, GLC.rules[production])
			elif production not in GLC.non_terminals:
				new_rules[master_head].add(production)

	GLC = copy.deepcopy(GLC_with_unitary_productions)

	# Novas regras da gramática serão armazenadas em new_rules
	new_rules = {}
	for head in GLC.rules.keys():
		new_rules[head] = set()

	# Usado para saber em qual cabeça adicionar a nova produção
	master_head = ''

	for head, body in GLC.rules.items():
		master_head = head
		# Usado para evitar loop infinito
		visited_heads = set()
		search_productions(head, body)

	GLC.rules = new_rules

	return GLC

# Remove os símbolos improdutivos
def GLC_remove_unproductive_symbols(GLC_with_unproductive_symbols):
	GLC = copy.deepcopy(GLC_with_unproductive_symbols)
	SP = GLC.terminals.union('&')

	new_symbol_added = True
	# Enquanto ainda há novos símbolos sendo adicionados em SP
	while new_symbol_added:
		new_symbol_added = False
		# Percorre todas as cabeças que ainda não estão em SP
		for head, body in GLC.rules.items():
			if head not in SP:
				for production in body:
					for symbol in production:
						# Se algum dos símbolos da produção não está em SP
						# então a produção não está totalmente marcada
						# portanto não podemos adicionar a cabeça em SP
						if symbol not in SP:
							break
						# Caso todos os símbolos de uma produção estejam marcados
						# então adicione a cabeça em SP
					else:
						new_symbol_added = True
						SP.add(head)
						# Basta que uma produção esteja totalmente marcada
						break

	# Remove os símbolos improdutivos
	unproductives = GLC.non_terminals - SP
	for unproductive in unproductives:
		GLC.rules.pop(unproductive)
	GLC.non_terminals = SP.intersection(GLC.non_terminals)

	# Remove as produções que não foram totalmente marcadas
	rules = defaultdict(set)

	for head, body in GLC.rules.items():
		for production in body:
			for symbol in production:
				# Se algum símbolo na produção não está marcado,
				# não adicionamos a produção no corpo da regra
				if symbol not in SP:
					break
			else:
				rules[head].add(production)

	GLC.rules = dict(rules)

	return GLC

# Remove os símbolos inalcançáveis
def GLC_with_unreachable_symbols(GLC_with_unreachable_symbols):
	GLC = copy.deepcopy(GLC_with_unreachable_symbols)

	SA = {GLC.initial_state}

	new_symbol_added = True
	# Enquanto ainda há novos símbolos sendo adicionados em SA
	while new_symbol_added:
		new_symbol_added = False
		for head, body in GLC.rules.items():
			if head in SA:
				for production in body:
					for symbol in production:
						if symbol not in SA:
							new_symbol_added = True
							SA.add(symbol)

	# Remove os símbolos improdutivos
	unreachables = GLC.non_terminals - SA
	for unreachable in unreachables:
		GLC.rules.pop(unreachable)
	GLC.non_terminals = SA.intersection(GLC.non_terminals)
	GLC.terminals = SA.intersection(GLC.terminals)

	# Remove as produções que não foram totalmente marcadas
	rules = defaultdict(set)

	for head, body in GLC.rules.items():
		for production in body:
			for symbol in production:
				# Se algum símbolo na produção não está marcado,
				# não adicionamos a produção no corpo da regra
				if symbol not in SA:
					break
			else:
				rules[head].add(production)

	GLC.rules = dict(rules)

	return GLC

# INCOMPLETO
# Remove os símbolos inalcançáveis


def rewrite_chomsky(GLC):
	# Reescrevendo as produções para que toda produção com mais de dois simbolos tenha somente não terminais
	terminals_list = copy.deepcopy(GLC.terminals) # Controle de criação dos novos estados
	new_p_counter = 1  # A criação vai ser X1, X2, X3 ...
	new_rules = copy.deepcopy(GLC.rules)

	for head, body in GLC.rules.items():
		for production in body:
			if len(production) >= 2:  # Se minha produção tem mais de 2 símbolos
				prods = list(production)
				new_production = production
				for i, symbol in enumerate(prods):  # Para cada símbolo da minha produção
					if symbol in GLC.terminals: # Se meu símbolo é um não terminal e eu ainda não marquei ele
						if symbol in terminals_list:
							terminals_list.remove(symbol)  # "Marca" ele
							new = "X{}".format(new_p_counter)  # Cria um novo estado que leva para esse terminal
							GLC.non_terminals.add(new)
							new_rules[new] = symbol
							prods[i] = new
							new_p_counter += 1
						else:    # Se já marquei, busque o estado que leva a esse terminal
							key = list(new_rules.keys())[list(new_rules.values()).index(symbol)]
							prods[i] = key
				new_production = "".join(prods)
				if production in new_rules[head]:
					new_rules[head].remove(production)
				new_rules[head].add(new_production)   #Adiciona a nova forma de produção

	GLC.rules = new_rules
	return GLC, new_p_counter


def getNonTerminals(GLC, production):
	prods = list(production)
	for i, symbol in enumerate(production):
		if symbol == "X":
			prods[i] = prods[i]+prods[i+1]
	for symbol in prods:
		if symbol not in GLC.non_terminals:
			prods.remove(symbol)
	return prods


def chomsky_cascate(GLC, counter):
	new_rules = copy.deepcopy(GLC.rules)
	prods = []
	is_new_production = set()
	for head, body in GLC.rules.items():
		for production in body:
			before = production
			prods = getNonTerminals(GLC, production)
			while (len(prods) >= 3):
				# print("A lista é", prods)
				new_production = prods.pop(1) + prods.pop(1)
				new_production = "".join(new_production)
				if new_production in is_new_production:  # Se a produção já existe, pego a cabeça q produz ela
					key = list(new_rules.keys())[list(new_rules.values()).index({new_production})]
					new_p = "".join(prods)+key  # Junto a produção Ex: (E + X1 -> EX1)
					if before in new_rules[head]:
						new_rules[head].remove(before)
					new_rules[head].add(new_p)

				else:
					is_new_production.add(new_production)  # Se não, adiciono na lista
					# print("Estados a serem reescritos", new_production)
					new = "X{}".format(counter)  # Crio uma nova cabeça
					GLC.non_terminals.add(new)   # Coloco a cabeça no meu conjunto de não terminais
					new_p = "".join(prods)+new   # Junto a produção
					# print("Nova produção é", new_p)
					counter += 1 # Somo o contador de novos estados
					new_rules[new] = {new_production}  # A nova cabeça agora possui aquela produção
					# print(head, "recebe", new_p)
					if before in new_rules[head]:
						new_rules[head].remove(before)
					new_rules[head].add(new_p)
					# print(new_rules)

	GLC.rules = new_rules
	return GLC


def GLC_chomsky_normal_form(GLC):
	GLC.show()
	GLC = GLC_remove_e_productions(GLC)
	GLC = GLC_remove_unitary_productions(GLC)
	GLC = GLC_remove_unproductive_symbols(GLC)
	GLC, counter = rewrite_chomsky(GLC)
	chomsky_cascate(GLC, counter)
	return GLC

def GLC_factoring(GLC_not_factored):
	GLC = copy.deepcopy(GLC_not_factored)

	print('\nRemovendo produções-& e recursão direta à esquerda (caso existir)')
	print('Sua GLC transfomada é:')

	# Eliminando recursão direta à esquerda
	# Lista ordenada de cabeças A
	A = GLC.heads_sorted
	for i in range(len(A)):
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

	GLC = GLC_remove_e_productions(GLC)
	GLC.show()

	# Remove os ND diretos
	def remove_direct_ND(GLC):
		new_list_of_rules = []

		for head, body in GLC.rules.items():
			new_rules = {}
			new_rules[head] = body
			poss_new_productions = defaultdict(set)

			# Monta as possíveis novas produções
			for production in body:
				if production[0] in GLC.terminals:
					if len(production) == 1:
						poss_new_productions[production[0]].add('&')
					else:
						poss_new_productions[production[0]].add(production[1:])

			# Checa se realmente há ND direto, sabendo que precisamos
			# de mais de uma produção que começa com o mesmo símbolo terminal
			for terminal, new_productions in poss_new_productions.items():
				# Se encontramos um ND direto
				if len(new_productions) > 1:
					# Construímos a nova produção
					new_head = head
					while True:
						new_head += "'"
						if new_head not in GLC.rules.keys() and new_head not in new_rules.keys():
							break
					# Excluímos as produções antigas
					to_remove = set()
					for production in new_productions:
						if production != '&':
							to_remove.add(terminal + production)
						else:
							to_remove.add(terminal)
					# Incluímos a produção nova
					to_add = terminal + new_head
					# Armazenamos as mudanças
					new_rules[head] = new_rules[head] - to_remove
					new_rules[head].add(to_add)
					new_rules[new_head] = new_productions

			new_list_of_rules.append(new_rules)

		# Atualiza a GLC
		rules = {}
		for rule in new_list_of_rules:
			rules.update(rule)
		GLC.rules = rules

		return GLC

	# Remove os ND indiretos
	def remove_indirect_ND(GLC):

		# Identifica se há ND e retorna os terminais que geram o ND
		def identify_ND_terminals(possible_new_ps):
			counter = defaultdict(int)
			for p in possible_new_ps:
				counter[p[0]] += 1
			nd_terminals = set()
			for terminal, count in counter.items():
				if count > 1:
					nd_terminals.add(terminal)
			return nd_terminals

		# Entra recursivamente em produções que começam com não-terminais
		# até encontrar apenas producções com terminais
		def get_recursive(body):
			new_ps_appended = set()
			for production in body:
				if production[0] in GLC.non_terminals:
					new_ps_set = get_recursive(GLC.rules[production[0]])
					for n_p in new_ps_set:
						new_ps_appended.add(n_p + production[1:])
				else:
					new_ps_appended.add(production)
			return new_ps_appended

		# Elimina o ND
		for head, body in GLC.rules.items():
			# Faz o mapeamento da produção com todas as produções que ela consegue alcançar
			map_prod_reaches = {}
			for production in body:
				production_aux = set()
				production_aux.add(production)
				map_prod_reaches[production] = get_recursive(production_aux)
			# Cria as possíveis novas produções que seriam criadas caso todas participassem do ND
			poss_new_productions = set()
			for productions in map_prod_reaches.values():
				poss_new_productions.update(productions)
			# Se algum ND for identificado, um novo corpo é criado a o código encerra
			nd_terminals = identify_ND_terminals(poss_new_productions)
			new_body = set()
			for production, reaches_productions in map_prod_reaches.items():
				for r in reaches_productions:
					if r[0] in nd_terminals:
						new_body.update(reaches_productions)
						break
				else:
					new_body.add(production)
			# Se um ND foi encontrado
			if new_body != body:
				GLC.rules[head] = new_body
		return GLC

	previous_rules = GLC.rules
	# Considera-se que entrou em loop caso haja 20 operaçõe de remoção de ND indireto
	# e ND direto. Além disso caso as regras parem de se alterar, o método também para
	for i in range(20):
		GLC = remove_indirect_ND(GLC)
		GLC = remove_direct_ND(GLC)
		curret_rules = GLC.rules
		if previous_rules == curret_rules:
			break
		previous_rules = copy.deepcopy(curret_rules)

	return GLC

def format_er(ER):
	# Insere os símbolos de concatenação na ER
	# Também conta a quantidade de nós folha
	formatted_ER = []
	n_leafs = 1
	for i in range(len(ER) - 1):
		if ER[i].isalnum() and (ER[i + 1].isalnum() or ER[i + 1] == '('):
			formatted_ER.append(ER[i])
			formatted_ER.append('.')
		elif ER[i].isalnum() and ER[i + 1] == '#':
			formatted_ER.append(ER[i])
			formatted_ER.append('.')
		elif ER[i] == '*' and ER[i + 1] != '|':
			formatted_ER.append(ER[i])
			formatted_ER.append('.')
		else:
			formatted_ER.append(ER[i])
		if ER[i].isalnum():
			n_leafs += 1
	ER = ''.join(formatted_ER) + "#"
	return ER

def convertRPN(er):
	stack = []
	output = []
	operands = ["|", ".", "*", "?", "+"]
	precedencia = {".": 1, "|": 0}
	postfix = ["?", "*", "+"]
	prefix = ["|", "."]
	for symbol in er:
		if symbol in operands:
			if symbol in postfix:
				output.append(symbol)
			elif symbol in prefix:
				if len(stack) != 0:
					if stack[-1] in precedencia.keys():
						while precedencia[stack[-1]] >= precedencia[symbol]:
								output.append(stack.pop())
								if len(stack) == 0:
									break
				stack.append(symbol)
		elif symbol == "(":
			stack.append(symbol)
		elif symbol == ")":
			while stack[-1] != "(":
				output.append(stack.pop())
			stack.pop()
		else:
			output.append(symbol)
	while len(stack) != 0:
		output.append(stack.pop())
	return output

def post_to_pre(ER):
	pre = []
	for symbol in ER[::-1]:
		pre.append(symbol)
	return pre

def construct_tree(ER):
	BINARY_OPS = [".", "|"]
	UNARY_OPS = ["*", "?", "+"]
	def parse(s):
		if s[0] in BINARY_OPS:
			lhs = parse(s[1:])
			lhs_end = 1 + len(lhs.span)
			rhs = parse(s[lhs_end:])
			rhs_end = lhs_end + len(rhs.span)
			return Node(s[:rhs_end], s[0], [rhs, lhs], 0, 0)
		elif s[0] in UNARY_OPS:
			operand = parse(s[1:])
			end = 1 + len(operand.span)
			return Node(s[:end], s[0], [operand], 0, 0)
		else:
			return Node(s[0], s[0], [], 0, 0)
	new_ER = parse("".join(ER))
	return new_ER

def isLeaf(s):
	if len(s.children) == 0:
		return True

def isNullable(s):
	if s.value == "&":
		return True
	elif s.value == "|":
		return isNullable(s.children[0]) or isNullable(s.children[1])
	elif s.value == "*":
		return True
	elif s.value == ".":
		return isNullable(s.children[0]) and isNullable(s.children[1])
	elif s.value == "?":
		return True
	else:
		return False

counter = 1
def parseLeaves(node):
	if isLeaf(node):
		global counter
		node.fPos = counter
		node.lPos = counter
		counter +=1
	else:
		for c in node.children:
			parseLeaves(c)

def first_and_lastPos(symbol):
	if symbol.fPos != 0 and symbol.lPos != 0:
		return [symbol.fPos, symbol.lPos]
	elif symbol.value == "*":
		symbol.fPos = first_and_lastPos(symbol.children[0])[0]
		symbol.lPos = symbol.fPos
		return [symbol.fPos, symbol.lPos]
	elif symbol.value == "|":
		symbol.fPos = [first_and_lastPos(symbol.children[0])[0]]
		symbol.fPos.append(first_and_lastPos(symbol.children[1])[0])
		symbol.lPos = symbol.fPos
		return [symbol.fPos, symbol.lPos]
	elif symbol.value == ".":
		if isNullable(symbol.children[0]):
			symbol.fPos = [first_and_lastPos(symbol.children[0])[0]]
			symbol.fPos.append(first_and_lastPos(symbol.children[1])[0])
		else:
			symbol.fPos = first_and_lastPos(symbol.children[0])[0]
		if isNullable(symbol.children[1]):
			symbol.lPos = [first_and_lastPos(symbol.children[0])[0]]
			symbol.lPos.append(first_and_lastPos(symbol.children[1])[0])
		else:
			symbol.lPos = first_and_lastPos(symbol.children[1])[0]
		return [symbol.fPos, symbol.lPos]

def flatten(it):
	for x in it:
		try:
			for y in flatten(x):
				yield y
		except TypeError:
			yield x

followp = {}
def follow(root):
	global followp
	followpos(root, followp)
	for c in root.children:
		if c.value == "#":
			followp[c.fPos] = []
			continue
		elif isLeaf(c):
			continue
		else:
			follow(c)
	return followp

def followpos(node, followp):
	if node.value == ".":
		c1 = node.children[0]
		c2 = node.children[1]
		first = list(flatten([c2.fPos]))
		last = list(flatten([c1.lPos]))
		for i in last:
			for pos in first:
				try:
					followp[i].append(pos)
				except KeyError:
					followp[i] = []
					followp[i].append(pos)

	elif node.value == "*":
		l = list(flatten(node.lPos))
		first = list(flatten(node.fPos))
		for i in l:
			for pos in first:
				try:
					followp[i].append(pos)
				except KeyError:
					followp[i] = []
					followp[i].append(pos)

	return followp

def getInputs(ER):
	r = set()
	operators = ['.', "*", "|", "?", "+"]
	for symbol in ER.span:
		if symbol not in operators:
			r.add(symbol)
	return r

correspond = {}
def getC(node, inputs, correspond):
	if node.value in inputs:
		try:
			correspond[node.value].append(node.fPos)
		except KeyError:
			correspond[node.value] = []
			correspond[node.value].append(node.fPos)

def getCorrespond(node, inputs):
	global correspond
	getC(node, inputs, correspond)
	for c in node.children:
		getCorrespond(c, inputs)
	return correspond

def createAFD(node, followp):
	AF = FiniteAutomata()
	state = "".join(str(e) for e in (list(flatten(node.fPos))))
	AF.initial = state
	Dstates = [state]
	inputs = getInputs(node)
	correspond = getCorrespond(node, inputs)

	while len(Dstates) != 0:
		S = Dstates.pop(0)
		S = "".join(str(e) for e in (S))
		AF.addState(S)
		for symbol in inputs:
			AF.alphabet.add(symbol)
			new = set()
			for c in correspond[symbol]:
				if str(c) in S:
					for x in followp[c]:
						new.add(x)
			new = "".join(str(e) for e in (new))
			if new not in AF.states:
				Dstates.append(new)
			AF.addTrans(S, symbol, new)
			for x in correspond["#"]:
				if str(x) in new:
					AF.addAccepting(new)
	return AF
# Converte ER para AFD usando árvore sintática
def ER_to_AFD(ER):
	ER = ER.regex['er'] + "#"
	regex = format_er(ER)
	rpn_regex = convertRPN(regex)
	prefixed = post_to_pre(rpn_regex)
	new = construct_tree(prefixed)
	parseLeaves(new)
	first_and_lastPos(new)
	print("Arvore Sintática:")
	print(new.__repr__())
	def show(symbol):
		print(symbol.value, "First Pos:", symbol.fPos, "Last Pos:", symbol.lPos)
		for c in symbol.children:
			show(c)
	print("First e Last Pos:")
	show(new)
	followp = follow(new)
	table = PrettyTable()
	table.add_column("n", list(followp.keys()))
	table.add_column("followpos", list(followp.values()))
	print("\n")
	print("Followpos:")
	print(table)
	AF = createAFD(new, followp)
	print("\n")
	print("Autômato:")
	AF.show()

# Reconhece sentenças usando um AP
def recognizer_AP(GLC, sentence):
	# (Incluir a remoção da recursividade à esquerda e fatoração após finalizar o código)
	print('Sabemos que é necessário remover a recursividade à esquerda e fatorar a GLC.' \
		  ' Para remover a recursividade à esquerda precisamos primeiramente torná-la &-livre.' \
		  ' Ao eliminar a recursividade à esquerda, é possível que ela entre em loop infinito durante a fatoração.' \
		  ' Portanto, tentaremos primeiramente remover a recursividade à esquerda e fatorar a GLC.' \
		  ' Em seguida tentaremos apenas com a GLC sem recursividade à esquerda.' \
		  ' Por último tentaremos rodar o reconhecedor com a GLC original.' \
		  ' A sentença será reconhecida se qualquer uma dessas 3 opções reconhecer a sentença.')

	def recognizer_AP_aux(GLC, sentence):
		try:
			# Cada produção é mapeada para um número único
			i = 0
			bodies_mapped = defaultdict(dict)
			bodies_mapped_reversed = defaultdict(dict)
			for head, body in GLC.rules.items():
				for symbols in body:
					bodies_mapped[head][symbols] = i
					bodies_mapped_reversed[head][i] = symbols
					i += 1

			firsts = {}
			follows = {}
			# Inicialização dos firsts e follows
			for head in GLC.rules.keys():
				firsts[head] = set()
				follows[head] = set()
			follows[GLC.initial_state].add('$')

			# Preenche os firsts não terminais
			def get_firsts(head, firsts):
				for symbols in GLC.rules[head]:
					i = 0
					while i < len(symbols):
						char = symbols[i]
						# Considerando que pode haver não-terminais do tipo X'''...
						while i+1 < len(symbols) and symbols[i+1] == "'":
							char += "'"
							i += 1
						if char in GLC.non_terminals:
							get_firsts(char, firsts)
							if '&' in firsts[char]:
								# Se o último simbolo for terminal então não inclui &
								if symbols[-1] in GLC.non_terminals:
									firsts[head].update(firsts[char])
								else:
									firsts[head].update(firsts[char] - set('&'))
							else:
								# Se não contem '&' então não continua
								firsts[head].update(firsts[char])
								break
						else:
							firsts[head].add(char)
							break
						i += 1
			for head in GLC.rules.keys():
				get_firsts(head, firsts)

			# Preenche os firsts terminais
			for terminal in GLC.terminals.union('&'):
				firsts[terminal] = {terminal}

			# Preenche os follows
			for head, body in GLC.rules.items():
				for symbols in body:
					i = 0
					while i < len(symbols):
						char = symbols[i]
						while i+1 < len(symbols) and symbols[i+1] == "'":
							char += "'"
							i += 1
						if char in GLC.non_terminals:
							has_epsilon = True
							j = i+1
							# Segue enquanto há & nos firsts dos não terminais seguintes
							while has_epsilon and j != len(symbols):
								char_aux = symbols[j]
								while j+1 != len(symbols) and symbols[j+1] == "'":
									char_aux += "'"
									j += 1
								follows[char].update(firsts[char_aux])
								if '&' in firsts[char_aux]:
									j += 1
								else:
									has_epsilon = False
						i += 1
			# Os últimos não terminais dos corpos recebem o follow da cabeça enquanto houver & nos firsts
			for head, body in GLC.rules.items():
				for symbols in body:
					symbols_reversed = symbols[::-1]
					i = 0
					while i < len(symbols):
						char = symbols_reversed[i]
						while char[0] == "'":
							i += 1
							char = symbols_reversed[i] + char
						if char in GLC.non_terminals:
							follows[char].update(follows[head])
							# Continua enquanto houver '&' nos firsts
							if '&' not in firsts[char]:
								break
						else:
							break
						i += 1
			# Remove os & que foram adicionados nos follows
			for head, follow in follows.items():
				follow.discard('&')

			# Inicializando tabela de análise
			table = {}
			for non_terminal in GLC.non_terminals:
				table[non_terminal] = {}
				for terminal in GLC.terminals:
					table[non_terminal][terminal] = -1

			# Montando a tabela de análise (tabela inicia em 0)
			for head, body in GLC.rules.items():
				for symbols in body:
					i = 0
					while i < len(symbols):
						char = symbols[i]
						while i+1 < len(symbols) and symbols[i+1] == "'":
							char += "'"
							i += 1
						for first in firsts[char]:
							table[head][first] = bodies_mapped[head][symbols]
						# Continua para o first do próximo terminal enquanto houver '&'
						if '&' in firsts[char]:
							for follow in follows[head]:
								table[head][follow] = bodies_mapped[head][symbols]
						else:
							break
						i += 1

			# Remove os & que foram adicionados na tabela
			for symbols in table.values():
				symbols.pop('&', None)

			# Reconhecendo a sentença
			AP = ['$', GLC.initial_state]
			sentence = list(sentence)
			sentence_symbol = sentence.pop(0)
			AP_print = [] # Apenas utilizado para printar
			while True:
				AP_print.append(AP[:])
				top = AP.pop()
				# Desempilha os terminais e avança na senteça enquanto eles forem iguais
				while top in GLC.terminals:
					AP_print.append(AP[:])
					if top == sentence_symbol:
						top = AP.pop()
						sentence_symbol = sentence.pop(0)
					else:
						break
				# Se chegamos no fim de pilha $, e temos '$' na setença então aceita
				# Também printa os firsts, follows e tabela
				if top == '$' and sentence_symbol == '$':
					print('\nFirsts:')
					for head, first in firsts.items():
						print(f'head: {head}, first: {first}')
					print('\nFollows:')
					for head, follow in follows.items():
						print(f'head: {head}, follow: {follow}')
					print('\nTabela de análise:')
					for head, symbols in table.items():
						print(f'head: {head}, symbols: {symbols}')
					print('\nAP:')
					for ap in AP_print:
						print(f'AP: {ap}')
					print()
					return True
				# Se não temos para onde ir dado o topo da pilha e a
				# sentença de entrada atual, então não aceita a sentença
				if not (top in table and sentence_symbol in table[top]):
					return False
				# Empilha de acordo com a nova produção
				body_idx = table[top][sentence_symbol]
				to_stack = bodies_mapped_reversed[top][body_idx]

				symbols_reversed = to_stack[::-1]
				i = 0
				while i < len(to_stack):
					char = symbols_reversed[i]
					while char[0] == "'":
						i += 1
						char = symbols_reversed[i] + char
					if char != '&':
						AP.append(char)
					i += 1
		except:
			return False

	GLC_original = copy.deepcopy(GLC)
	GLC_no_recursion = GLC_remove_left_recursion(GLC)
	GLC_no_recursion_and_factored = GLC_factoring(GLC_no_recursion)

	if not recognizer_AP_aux(GLC_no_recursion_and_factored, sentence):
		if not recognizer_AP_aux(GLC_no_recursion, sentence):
			if not recognizer_AP_aux(GLC_original, sentence):
				return False
			else:
				print('A GLC original reconheceu a linguagem:\n')
				GLC.show()
				return True
		else:
			print('A GLC sem recursividade à esquerda reconheceu a linguagem:\n')
			GLC.show()
			return True
	else:
		print('A GLC sem recursividade à esquerda e fatorada reconheceu a linguagem:\n')
		GLC.show()
		return True