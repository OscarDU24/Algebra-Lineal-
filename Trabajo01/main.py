from Models.Matriz import Matriz
from Dao.matriz_dao import MatrizDAO
from Menus.menu_principal import MenuPrincipal

def main():

    matriz = Matriz()
    dao = MatrizDAO()

    menu = MenuPrincipal(matriz, dao)

    menu.ejecutar()

if __name__ == "__main__":
    main()