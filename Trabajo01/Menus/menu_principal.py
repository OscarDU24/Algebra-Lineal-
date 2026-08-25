# ==========================================================
# CLASE MENÚ PRINCIPAL
# Controla la interacción principal con el usuario y permite
# acceder a las diferentes funciones del programa.
# ==========================================================

class MenuPrincipal:

    # ======================================================
    # CONSTRUCTOR
    # Recibe la matriz, el DAO y el menú de operaciones para
    # permitir que todos trabajen sobre la misma matriz.
    # ======================================================
    def __init__(self, matriz, dao, menu_operaciones):
        self.matriz = matriz
        self.dao = dao
        self.menu_operaciones = menu_operaciones

    # ======================================================
    # VALIDAR ENTEROS
    # Solicita al usuario un valor entero y repite la entrada
    # hasta recibir un dato válido.
    # ======================================================
    def solicitar_entero(self, mensaje):
        while True:
            try:
                return int(input(mensaje))
            except ValueError:
                print(
                    "Ingrese únicamente un valor entero."
                )

    # ======================================================
    # VALIDAR NÚMEROS
    # Permite introducir números enteros o decimales.
    # Los valores que no sean válidos son rechazados para
    # evitar errores durante la ejecución del programa.
    # ======================================================

    def solicitar_numero(self, mensaje):
        while True:
            try:
                valor = float(input(mensaje))
                if valor.is_integer():
                    return int(valor)
                return valor
            except ValueError:
                print(
                    "Ingrese únicamente un número "
                    "entero o decimal."
                )

    # ======================================================
    # VALIDAR ENTEROS POSITIVOS
    # Solicita un número entero mayor que cero. Se utiliza
    # principalmente para definir las dimensiones de la
    # matriz.
    # ======================================================
    def solicitar_entero_positivo(self, mensaje):
        while True:
            valor = self.solicitar_entero(mensaje)
            if valor > 0:
                return valor
            print(
                "Ingrese únicamente valores positivos."
            )

    # ======================================================
    # MOSTRAR MATRIZ
    # Comprueba si existe una matriz y posteriormente muestra
    # todos los valores almacenados en ella.
    # ======================================================
    def mostrar_matriz(self):
        print("\nMatriz:")
        if self.matriz.filas == 0:
            print(
                "La matriz todavía no ha sido creada."
            )
            return
        self.matriz.mostrar()

    # ======================================================
    # DEFINIR TAMAÑO
    # Solicita al usuario la cantidad de filas y columnas
    # para crear una nueva matriz vacía.
    # ======================================================
    def definir_tamano(self):
        print("\n--- Definir tamaño de la matriz ---")
        filas = self.solicitar_entero_positivo(
            "Ingrese el número de filas: "
        )
        columnas = self.solicitar_entero_positivo(
            "Ingrese el número de columnas: "
        )
        self.matriz.definir_tamano(
            filas,
            columnas
        )
        print("\nMatriz creada correctamente.")
        self.matriz.mostrar()

    # ======================================================
    # INSERTAR VALORES
    # Recorre cada posición de la matriz y solicita al usuario
    # un número entero o decimal para almacenarlo mediante
    # el DAO.
    # ======================================================
    def insertar_valores(self):
        if self.matriz.filas == 0:
            print(
                "Primero debe definir el tamaño de la matriz."
            )
            return

        print("\n--- Insertar valores ---")
        for i in range(self.matriz.filas):
            for j in range(self.matriz.columnas):
                valor = self.solicitar_numero(
                    f"Ingrese el valor para la posición "
                    f"[{i}][{j}]: "
                )
                self.dao.insertar_valor(
                    self.matriz,
                    i,
                    j,
                    valor
                )
        print(
            "\nValores insertados correctamente."
        )

    # ======================================================
    # CONSULTAR VALOR
    # Solicita una fila y una columna y muestra el valor
    # almacenado en la posición indicada.
    # ======================================================
    def consultar_valor(self):
        if not self.matriz.esta_completa():
            print(
                "La matriz no está completa. "
                "Por favor inserte todos los valores primero."
            )
            return

        print("\n--- Consultar valor ---")
        fila = self.solicitar_entero(
            f"Ingrese el número de fila "
            f"(0-{self.matriz.filas - 1}): "
        )
        columna = self.solicitar_entero(
            f"Ingrese el número de columna "
            f"(0-{self.matriz.columnas - 1}): "
        )
        valor = self.dao.consultar_valor(
            self.matriz,
            fila,
            columna
        )
        if valor is not None:
            print(
                f"El valor en la posición "
                f"[{fila}][{columna}] es: {valor}"
            )
        else:
            print(
                "Índice fuera del rango de la matriz."
            )

    # ======================================================
    # EJECUTAR MENÚ PRINCIPAL
    # Mantiene el menú activo hasta que el usuario seleccione
    # la opción de salida y permite acceder a todas las
    # funcionalidades principales del programa.
    # ======================================================
    def ejecutar(self):
        while True:
            print("\nMenú de opciones:")
            print("1. Mostrar la matriz")
            print("2. Definir el tamaño de la matriz")
            print("3. Insertar valores en la matriz")
            print("4. Consultar un valor en la matriz")
            print("5. Realizar operaciones con la matriz")
            print("6. Salir")
            opcion = input(
                "Seleccione una opción (1-6): "
            )

            if opcion == "1":
                self.mostrar_matriz()

            elif opcion == "2":
                self.definir_tamano()

            elif opcion == "3":
                self.insertar_valores()

            elif opcion == "4":
                self.consultar_valor()

            elif opcion == "5":
                self.menu_operaciones.ejecutar()

            elif opcion == "6":
                print("Saliendo del programa.")
                break

            else:
                print(
                    "Opción inválida. "
                    "Seleccione una de las opciones presentes."
                )