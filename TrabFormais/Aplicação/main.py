from conversoes import AFD_to_GR, GR_to_AFND, AF_string_recognizer, AFD_minimizer, AFND_determinizer
from GR import RegularGrammar
from AF import *

def main():
	# # a) Lendo, salvando e carregando um AF
	AFND = NDFiniteAutomata()
	AFND.load("../Testes/afndsem&.afnd")
	AFND_determinizer(AFND)
	# AFND.show()
	AFND.save("teste_1")
	# AFND.load('AFND_json')
	# AFND.show()
	# print(AFND.eClosure({"3"}))

	# a) Lendo, salvando e carregando uma GR
	# GR = RegularGrammar()
	# GR.read("../Testes/gramatica_regular_1.gr")
	# GR.save('GR_json')
	# GR = RegularGrammar()
	# GR.load('GR_json')
	# print(GR)

	# b) Transformando um AFD em uma GR
	# AF = FiniteAutomata()
	# AF.read("../Testes/automato_finito_2.txt")
	# GR = AFD_to_GR(AF)
	# AF.show()
	# print(GR)

	# b) Transformando uma GR em um AFND
	# GR = RegularGrammar()
	# GR.read("../Testes/gramatica_regular_1.txt")
	# AF = GR_to_AFND(GR)
	# AF.show()
	# print(GR)

	# d) Reconhecendo uma sentença em um AF
	# AF = FiniteAutomata()
	# AF.read("../Testes/automato_finito_1.txt")
	# recognized = AF_string_recognizer(AF, 'baab')
	# print(recognized)
	# recognized = AF_string_recognizer(AF, 'aababb')
	# print(recognized)

	# e) Minimização de AFD
	# AFD = FiniteAutomata()
	# AFD.read("../Testes/automato_finito_7.txt")
	# AFD_min = AFD_minimizer(AFD)
	# # AFD_min.show()

	pass

if __name__ == "__main__":
    main()
