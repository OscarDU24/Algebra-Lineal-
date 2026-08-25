from Models.Matriz import Matriz
from Dao.matriz_dao import MatrizDAO
from Menus.menu_principal import MenuPrincipal
from Menus.menu_operaciones import MenuOperaciones


def main():
    matriz = Matriz()
    dao = MatrizDAO()
    menu_operaciones = MenuOperaciones(
        matriz,
        dao
    )
    
    menu_principal = MenuPrincipal(
        matriz,
        dao,
        menu_operaciones
    )
    menu_principal.ejecutar()

if __name__ == "__main__":
    main()