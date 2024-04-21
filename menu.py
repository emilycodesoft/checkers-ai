# Import the necessary packages
from consolemenu import *
from consolemenu.items import *

# Create the menu
menu = ConsoleMenu("AI", "Escoge un Agente para el jugador RED")


evalfunctions_menu = SelectionMenu(["Función de evaluación basica", "Función de evaluación mejorada"])
# A FunctionItem runs a Python function when selected
yourself_item = MenuItem("Tu Mismo")
random_item = MenuItem("Random")
minimax_item = SubmenuItem("MiniMax", evalfunctions_menu, menu)
poda_item = MenuItem("Minimax Poda Alpha-Beta")


menu.append_item(yourself_item)
menu.append_item(random_item)
menu.append_item(minimax_item)
menu.append_item(poda_item)


# Finally, we call show to show the menu and allow the user to interact
menu.show()


selection = menu.selected_option

print("Seleccionaste: ", selection)