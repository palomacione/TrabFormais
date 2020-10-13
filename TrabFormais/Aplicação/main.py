from conversoes import AF_to_GR
from GR import RegularGrammar
from AF import *

def main():
    # AF = FiniteAutomata()
    # AF.load("../Testes/teste.txt")
    # AF.show()

	GR = RegularGrammar()
	GR.load("../Testes/gramatica_regular_1.txt")
	print(GR)

	AF = FiniteAutomata()
	AF.load("../Testes/teste.afd")
	GR = AF_to_GR(AF)
	print(GR)

if __name__ == "__main__":
    main()
