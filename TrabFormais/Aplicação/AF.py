class FiniteAutomata:
    def __init__(self, trans=None, initial="0", accepting=None):
        self.trans = {}
        self.initial = initial
        self.accepting = set()
        
    def addTrans(self, from_, by, to):
        if from_ not in self.trans:
            self.trans[from_] = {}
        self.trans[from_][by] = to

    def addAccepting(self, state):
        self.accepting.add(state)
    
    def load(self, file):
        f = open(file, "r")
        f1 = f.readlines()
        initial = f1[1]
        accepting = f1[2].replace('\n', '').split(',')
        for s in accepting:
            self.addAccepting(s)
        for line in f1[4:]:
            print(line)
            l1 = line.replace('\n', '').split(',')
            from_ = l1[0]
            by = l1[1]
            to = l1[2]
            self.addTrans(from_, by, to)
        self.initial = initial

    def show(self):
        print(self.trans, self.accepting, self.initial)