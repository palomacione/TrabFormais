from consolemenu import *
from consolemenu.items import *
from AF import * 

menu = ConsoleMenu("Linguagens Formais e Compiladores", "Trabalho de Implementação")
menu_item = MenuItem("Menu Item")
submenu_1 = ConsoleMenu("Automatos")
selection_menu_automatos = SelectionMenu(["Carregar um Autômato", "União de Autômatos", "Determinização de Autômatos", "Salvar um Autômato"])
selection_menu_edições = SelectionMenu(["Adicionar estado", "Adicionar estado de aceitação", "Atualizar estado inicial"])

submenu_automatos = SubmenuItem("Operações sobre Autômatos", selection_menu_automatos, menu)
submenu_edições = SubmenuItem("Edições sobre Autômatos", selection_menu_edições, menu=submenu_1)

menu.append_item(submenu_automatos)

submenu_1.append_item(submenu_edições)
# submenu_automatos.append_item(FunctionItem)




menu.show()