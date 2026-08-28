# ==========================================================
# PROGRAMA PRINCIPAL
# Punto de entrada de la aplicación. Se encarga únicamente
# de crear los objetos principales e iniciar el menú.
# ==========================================================

from Models.Matriz import Matriz
from Dao.matriz_dao import MatrizDAO
from Menus.menu_principal import MenuPrincipal


# ==========================================================
# FUNCIÓN PRINCIPAL
# Inicializa el modelo, el DAO y el menú principal.
# ==========================================================

def main():

    matriz = Matriz()
    dao = MatrizDAO()

    menu = MenuPrincipal(
        matriz,
        dao
    )

    menu.ejecutar()


# ==========================================================
# INICIO DEL PROGRAMA
# Ejecuta main() cuando este archivo es ejecutado como
# módulo principal.
# ==========================================================

if __name__ == "__main__":
    main()