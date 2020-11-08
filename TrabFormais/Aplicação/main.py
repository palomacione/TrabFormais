from conversoes import AFD_to_GR, GR_to_AFND, AFD_minimizer, AFND_determinizer
from GR import RegularGrammar
from AF import *

def main():
	# # a) Lendo, salvando e carregando um AF
	# AF1 = FiniteAutomata()
	# AF1.load("../Testes/automato_finito_9.afd")
	# AF1.show()
	# AF2 = FiniteAutomata()
	# AF2.load("../Testes/automato_finito_8.afd")
	# AFD_minimizer(AF1)
	# Re = AF1.union(AF2)
	# AF1.show()

	# Re = AFND_determinizer(R)
	# Re.show()
	# AFND = NDFiniteAutomata()
	# AFND.load("../Testes/afndsem&.afnd")
	# AFND.show()
	# AF = AFND_determinizer(AFND)
	# AF.show()
	# AFND.save("teste_1")
	# AFND.load('AFND_json')
	# AFND.show()
	# print(AFND.eClosure({"3"}))

	# a) Lendo, salvando e carregando uma ER
	ER = RegularGrammar()

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
	AFD = FiniteAutomata()
	AFD.load("../Testes/automato_finito_7.txt")
	AFD_min = AFD_minimizer(AFD)
	AFD_min.show()

	pass

if __name__ == "__main__":
    main()
