from menu import Menu

from conversoes import AFD_to_GR, GR_to_AFND, AFD_minimizer, AFND_determinizer, ER_to_AFD, GLC_remove_left_recursion, GLC_remove_e_productions, GLC_remove_unitary_productions, GLC_remove_unproductive_symbols
from GR import RegularGrammar
from ER import RegularExpression
from AF import *


def main():
	menu = Menu()
	menu.start()

if __name__ == "__main__":
    # main()
	# ext = '../Testes/'
	# GLC = RegularGrammar()
	# GLC.load(ext + 'teste10RecuGlc_1.txt')
	# print('\nSua GLC de entrada foi:\n')
	# GLC.show()
	# GLC = GLC_remove_unproductive_symbols(GLC)
	# GLC.show()
