class FiniteAutomata:
    def __init__(self, trans=None, initial="0", accepting=None):
        self.trans = {}
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

    def show(self):
        print(self.trans, self.accepting, self.initial)
