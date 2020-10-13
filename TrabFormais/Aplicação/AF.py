import pickle

class FiniteAutomata:
    def __init__(self, trans=None, initial="0", accepting=None):
        self.trans = {} # Dicionário de Transições
        self.initial = initial
        self.accepting = set()

        self.states = set() # Conjunto de estados
        self.alphabet = set() # Conjunto de símobolos do alfabeto

    def addTrans(self, from_, by, to):
        if from_ not in self.trans:
            self.trans[from_] = {}
        self.trans[from_][by] = to

    def addAccepting(self, state):
        self.accepting.add(state)

    def read(self, file):
        f = open(file, "r")
        f1 = f.readlines()
        initial = f1[1].replace('\n', '')
        accepting = f1[2].replace('\n', '').split(',')
        for s in accepting:
            self.addAccepting(s)

		# Preenche os símbolos do alfabeto
        alphabet = f1[3].replace('\n', '').split(',')
        for a in alphabet:
            self.alphabet.add(a)

        for line in f1[4:]:
            l1 = line.replace('\n', '').split(',')
            from_ = l1[0]
            by = l1[1]
            to = l1[2]

			# Preenche o conjunto de estados
            self.states.add(to)
            self.states.add(from_)

            self.addTrans(from_, by, to)
        self.initial = initial

# Verifica se o autômato reconhece a palavra
    def recognizes(self, word):
        current = self.initial
        for c in word:   # Por cada letra da palavra
            if c not in self.trans[current]:  # Se eu não tenho transição pela letra, retorna falso
                return False 
            else:
                current = self.trans[current][c]  # Se não, vou para o estado em que a letra leva

        return current in self.accepting  
    
    def load(self, file):
        with open(file, "rb") as pickle_file:
            AF = pickle.load(pickle_file)
            self.accepting = AF.accepting
            self.trans = AF.trans
            self.alphabet = AF.alphabet
            self.states = AF.states
            self.initial =  AF.initial
            
    # Salva o objeto em um arquivo pickle local
    def save(self, file):
        with open(file, 'wb') as pickle_file:
            pickle.dump(self, pickle_file)

    def show(self):
        print(self.trans, self.accepting, self.initial)

# Classe de AF não Deterministico, filho de um Automato Finito
class NDFiniteAutomata(FiniteAutomata):

    def addTrans(self, from_, by, to):  # Cria um set de estados para cada transição por uma letra do alfabeto ou por &
        if from_ not in self.trans:
            self.trans[from_] = {}
        if by not in self.trans[from_]:
            self.trans[from_][by] = set()
        self.trans[from_][by].add(to)