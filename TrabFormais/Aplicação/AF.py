from prettytable import PrettyTable
from copy import deepcopy

class FiniteAutomata:
    def __init__(self, trans=None, initial="0", accepting=None, states=None, alphabet=None):
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

    def load(self, file):
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
            
    # Salva o objeto em um arquivo json local
    def save(self, filename):
        with open(filename, "w") as writer:
            writer.write(str(len(self.states))+"\n")
            writer.write(self.initial+"\n")
            writer.write(str(",".join(sorted(self.accepting)))+"\n")
            writer.write(str(",".join(sorted(self.alphabet)))+"\n")

            for t in self.trans:
                for b in self.trans[t]:
                    writer.write("{},{},{}".format(t, b, self.trans[t][b]+"\n"))

    def show(self):
        table = PrettyTable()

        alphabet = sorted(list(self.alphabet)) # Como é set, preciso colocar em ordem
        states = sorted(list(self.states))
        states1 = deepcopy(states)

        for i, s in enumerate(states):
            if s in self.accepting:
                states1[i] = "*"+states1[i]
            if s == self.initial:
                states1[i] = "->"+states1[i]
                
        table.add_column("Estados", states1)

        for a in alphabet: # Então aqui eu vou fazer de forma ordenada, começando por (a, q0), (a,q1), etc
            column = []
            for s in states:
                if a not in self.trans[s]:
                    column.append("Ø")
                else:
                    column.append(self.trans[s][a])
            table.add_column(a, column)
    
        print(table)

# Classe de AF não Deterministico, filho de um Automato Finito
class NDFiniteAutomata(FiniteAutomata):

    def addTrans(self, from_, by, to):  # Cria um set de estados para cada transição por uma letra do alfabeto ou por &
        if from_ not in self.trans:
            self.trans[from_] = {}
        if by not in self.trans[from_]:
            self.trans[from_][by] = set()
        self.trans[from_][by].add(to)
    
    def eClosure(self, states):  # Retorna os estados alcancaveis por & a partir de um estado ou um conjunto de estados
        eClosure = set()
        while states:
            s = states.pop()
            eClosure.add(s)
            if "&" in self.trans[s]:
                for x in self.trans[s]["&"]:
                    if x not in eClosure:
                        states.add(x)
        return eClosure
    
    def load(self, filename):
        f = open(filename, "r")
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

            if "-" in l1[2]:
                to = l1[2].split("-") 
                for s in to:
                    self.states.add(s)
                    self.addTrans(from_, by, s)
            else:   
                # Adiciona conjunto de estados
                self.states.add(to)
                self.states.add(from_)
                self.addTrans(from_, by, to)
        
        for s in self.states:
            if s not in self.trans:
                self.trans[s] = {}

        self.initial = initial

    def save(self, filename):
        with open(filename, "w") as writer:
            writer.write(str(len(self.states))+"\n")
            writer.write(self.initial+"\n")
            writer.write(str(",".join(sorted(self.accepting)))+"\n")
            writer.write(str(",".join(sorted(self.alphabet)))+"\n")

            for t in self.trans:
                for b in self.trans[t]:
                        f = '-'.join(self.trans[t][b])
                        writer.write("{},{},{}".format(t, b, f)+"\n")
