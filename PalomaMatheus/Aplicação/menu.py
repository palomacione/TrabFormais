from conversoes import *
from GR import RegularGrammar
from ER import RegularExpression
from AF import *

class Menu():

	# Inicializador
	def __init__(self):
		pass

	# Printa todas as opções do trabalho
	def print_options(self):
		print('\nOpções:\n',
			  'b - Conversão de AFND (com e sem ε) para AFD\n',
			  'c1 - Conversão de AFD para GR\n',
			  'c2 - Conversão de GR para AFND\n',
			  'd - Reconhecimento de sentenças\n',
			  'e - Minimização de AFD\n',
			  'f1 - União de AFD\n',
			  'f2 - Interseção de AFD\n',
			  'g - Conversão de ER para AFD\n',
			  'h - Leitura, gravação e edição de GLC\n',
			  'i - Transformação de GLC para uma GLC na forma normal de Chomsky\n',
			  'j - Eliminação de recursão à esquerda\n',
			  'k - Fatoração\n',
			  'l - Reconhecimento de sentenças em AP\n'
			  'Extra:\n',
			  'epsilon - Eliminação das e-produções\n',
			  'unitarias - Eliminação das produções unitárias\n',
			  'improdutivos - Eliminação dos símbolos improdutivos\n',
			  'inalcancaveis - Eliminação dos símbolos inalcanáveis\n')

	# Requisita continuamente por input do usuário para a execução
	# dos algoritmos implementados no trabalho
	def start(self):
		ext = '../Testes/'

		while(True):
			self.print_options()
			option = input('Escolha uma opção: ')

			if option == 'b': # Conversão AFND para AFD

				input_file = input('Nome do arquivo de entrada: ')
				output_file = input('Nome do arquivo de saída: ')

				AFND = NDFiniteAutomata()
				AFND.load(ext + input_file)
				AFD = AFND_determinizer(AFND)
				AFD.save(ext + output_file)

				print('\nSeu AFND de entrada foi:\n')
				AFND.show()
				print('\nSeu AFD de saída é:\n')
				AFD.show()

			elif option == 'c1': # Conversão AF para GR

				input_file = input('Nome do arquivo de entrada: ')
				output_file = input('Nome do arquivo de saída: ')

				AF = FiniteAutomata()
				AF.load(ext + input_file)
				GR = AFD_to_GR(AF)
				GR.save(ext + output_file)

				print('\nSeu AF de entrada foi:\n')
				AF.show()
				print('\nSua GR de saída é:\n')
				GR.show()

			elif option == 'c2': # Conversão GR para AFND

				input_file = input('Nome do arquivo de entrada: ')
				output_file = input('Nome do arquivo de saída: ')

				GR = RegularGrammar()
				GR.load(ext + input_file)
				AFND = GR_to_AFND(GR)
				AFND.save(ext + output_file)

				print('\nSua GR de entrada foi:\n')
				GR.show()
				print('\nSeu AFND de saída é:\n')
				AFND.show()

			elif option == 'd': # Reconhecendo sentença em AF

				input_file = input('Nome do arquivo de entrada: ')
				to_recognize = input('String para reconhecer: ')

				AF = FiniteAutomata()
				AF.load(ext + input_file)
				recognizes = AF.recognizes(to_recognize)

				print('\nSua estrutura de entrada foi:\n')
				AF.show()
				if recognizes:
					print('\nSeu AF reconhece a linguagem\n')
				else:
					print('\nSeu AF não reconhece a linguagem\n')

			elif option == 'e': # Minimização de AFD

				input_file = input('Nome do arquivo de entrada: ')
				output_file = input('Nome do arquivo de saída: ')

				AFD = FiniteAutomata()
				AFD.load(ext + input_file)
				AFD_min = AFD_minimizer(AFD)
				AFD_min.save(ext + output_file)

				print('\nSeu AFD de entrada foi:\n')
				AFD.show()
				print('\nSeu AFD minimizado de saída é:\n')
				AFD_min.show()

			elif option == 'f1': # União de AFD

				input_file_1 = input('Nome do arquivo de entrada 1: ')
				input_file_2 = input('Nome do arquivo de entrada 2: ')
				output_file = input('Nome do arquivo de saída: ')

				AFD_1 = FiniteAutomata()
				AFD_1.load(ext + input_file_1)
				AFD_2 = FiniteAutomata()
				AFD_2.load(ext + input_file_2)
				AFD_union = AFD_1.union(AFD_2)
				AFD_union.save(ext + output_file)

				print('\nSeu AFD de entrada 1 foi:\n')
				AFD_1.show()
				print('\nSeu AFD de entrada 2 foi:\n')
				AFD_2.show()
				print('\nSeu AFD de saída com união realizada é:\n')
				AFD_union.show()

			elif option == 'f2': # Interseção de AFD

				input_file_1 = input('Nome do arquivo de entrada 1: ')
				input_file_2 = input('Nome do arquivo de entrada 2: ')
				output_file = input('Nome do arquivo de saída: ')

				AFD_1 = FiniteAutomata()
				AFD_1.load(ext + input_file_1)
				AFD_2 = FiniteAutomata()
				AFD_2.load(ext + input_file_2)
				AFD_intersection = AFD_1.intersection(AFD_2)
				AFD_intersection.save(ext + output_file)

				print('\nSeu AFD de entrada 1 foi:\n')
				AFD_1.show()
				print('\nSeu AFD de entrada 2 foi:\n')
				AFD_2.show()
				print('\nSeu AFD de saída com interseção realizada é:\n')
				AFD_intersection.show()

			elif option == 'j': # Eliminação de recursão à esquerda

				input_file = input('Nome do arquivo de entrada: ')
				output_file = input('Nome do arquivo de saída: ')

				GLC = RegularGrammar()
				GLC.load(ext + input_file)
				GLC_no_left_recursion = GLC_remove_left_recursion(GLC)
				GLC_no_left_recursion.save(ext + output_file)

				print('\nSua GLC de entrada foi:\n')
				GLC.show()
				print('\nSua GLC de saída sem recursão à esquerda é:\n')
				GLC_no_left_recursion.show()

			elif option == 'epsilon': # Eliminação das e-produções

				input_file = input('Nome do arquivo de entrada: ')
				output_file = input('Nome do arquivo de saída: ')

				GLC = RegularGrammar()
				GLC.load(ext + input_file)
				GLC_no_e_productions = GLC_remove_e_productions(GLC)
				GLC_no_e_productions.save(ext + output_file)

				print('\nSua GLC de entrada foi:\n')
				GLC.show()
				print('\nSua GLC de saída sem e-produções é:\n')
				GLC_no_e_productions.show()

			elif option == 'unitarias': # Eliminação das produções unitárias

				input_file = input('Nome do arquivo de entrada: ')
				output_file = input('Nome do arquivo de saída: ')

				GLC = RegularGrammar()
				GLC.load(ext + input_file)
				GLC_no_unitary_productions = GLC_remove_unitary_productions(GLC)
				GLC_no_unitary_productions.save(ext + output_file)

				print('\nSua GLC de entrada foi:\n')
				GLC.show()
				print('\nSua GLC de saída sem produções unitárias é:\n')
				GLC_no_unitary_productions.show()

			elif option == 'improdutivos': # Eliminação dos símbolos improdutivos

				input_file = input('Nome do arquivo de entrada: ')
				output_file = input('Nome do arquivo de saída: ')

				GLC = RegularGrammar()
				GLC.load(ext + input_file)
				GLC_no_unproductive_symbols = GLC_remove_unproductive_symbols(GLC)
				GLC_no_unproductive_symbols.save(ext + output_file)

				print('\nSua GLC de entrada foi:\n')
				GLC.show()
				print('\nSua GLC de saída sem símbolos improdutivos é:\n')
				GLC_no_unproductive_symbols.show()

			elif option == 'inalcancaveis': # Eliminação dos símbolos inalcanáveis

				input_file = input('Nome do arquivo de entrada: ')
				output_file = input('Nome do arquivo de saída: ')

				GLC = RegularGrammar()
				GLC.load(ext + input_file)
				GLC_no_unreachable_symbols = GLC_with_unreachable_symbols(GLC)
				GLC_no_unreachable_symbols.save(ext + output_file)

				print('\nSua GLC de entrada foi:\n')
				GLC.show()
				print('\nSua GLC de saída sem símbolos inalcanáveis é:\n')
				GLC_no_unreachable_symbols.show()

			else:
				print('Opção ainda não implementada ou opção inexistente')
