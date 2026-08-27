# ==========================================================
# IMPORTACIÓN DE CLASES
# Se importan las clases necesarias para construir la matriz,
# acceder a sus datos, ejecutar la eliminación y mostrar
# el menú principal.
# ==========================================================

from Models.Matriz import Matriz
from Dao.matriz_dao import MatrizDAO
from Services.eliminacion import Eliminacion
from Menus.menu_principal import MenuPrincipal

# ==========================================================
# FUNCIÓN PRINCIPAL
# Crea los objetos del programa y los relaciona entre sí
# antes de ejecutar el menú principal.
# ==========================================================

def main():
    matriz = Matriz()
    dao = MatrizDAO()
    eliminacion = Eliminacion(matriz)
    menu = MenuPrincipal(matriz, dao, eliminacion)
    menu.ejecutar()

# ==========================================================
# PUNTO DE ENTRADA
# Ejecuta la función principal cuando el archivo es iniciado
# directamente.
# ==========================================================

if __name__ == "__main__":
    main()