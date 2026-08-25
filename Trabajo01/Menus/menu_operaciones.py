# ==========================================================
# CLASE MENÚ DE OPERACIONES
# Contiene el menú encargado de ejecutar las operaciones
# elementales sobre la matriz.
# ==========================================================

class MenuOperaciones:

    # ======================================================
    # CONSTRUCTOR
    # Recibe la matriz y el DAO para poder realizar las
    # operaciones sobre la misma matriz utilizada por el
    # menú principal.
    # ======================================================
    def __init__(self, matriz, dao):
        self.matriz = matriz
        self.dao = dao

    # ======================================================
    # VALIDAR ENTEROS
    # Solicita un valor entero para posiciones e índices
    # utilizados durante las operaciones.
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
    # Permite introducir valores enteros o decimales para
    # utilizarlos como escalares en las operaciones.
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
    # INTERCAMBIAR FILAS
    # Solicita dos filas y las intercambia utilizando el
    # método correspondiente del DAO.
    # ======================================================

    def intercambiar_filas(self):
        fila1 = self.solicitar_entero(
            f"Ingrese la primera fila "
            f"(0-{self.matriz.filas - 1}): "
        )
        fila2 = self.solicitar_entero(
            f"Ingrese la segunda fila "
            f"(0-{self.matriz.filas - 1}): "
        )
        if self.dao.intercambiar_filas(
            self.matriz,
            fila1,
            fila2
        ):
            print(
                "\nFilas intercambiadas correctamente."
            )
            self.matriz.mostrar()
        else:
            print(
                "Índice fuera del rango de la matriz."
            )

    # ======================================================
    # SUMAR FILAS
    # Solicita dos filas y suma los elementos de la primera
    # con los elementos correspondientes de la segunda.
    # ======================================================
    def sumar_filas(self):
        fila1 = self.solicitar_entero(
            f"Ingrese la fila que desea sumar "
            f"(0-{self.matriz.filas - 1}): "
        )
        fila2 = self.solicitar_entero(
            f"Ingrese la fila a la que se sumará "
            f"(0-{self.matriz.filas - 1}): "
        )
        if self.dao.sumar_filas(
            self.matriz,
            fila1,
            fila2
        ):
            print(
                "\nFilas sumadas correctamente."
            )
            self.matriz.mostrar()
        else:
            print(
                "Índice fuera del rango de la matriz."
            )

    # ======================================================
    # ESCALAR FILA
    # Solicita una fila y un número entero o decimal para
    # multiplicar todos sus elementos por dicho escalar.
    # ======================================================
    def escalar_fila(self):
        fila = self.solicitar_entero(
            f"Ingrese la fila a escalar "
            f"(0-{self.matriz.filas - 1}): "
        )
        escalar = self.solicitar_numero(
            "Ingrese el valor del escalar: "
        )
        if self.dao.escalar_fila(
            self.matriz,
            fila,
            escalar
        ):
            print(
                "\nFila escalada correctamente."
            )
            self.matriz.mostrar()
        else:
            print(
                "Índice fuera del rango de la matriz."
            )

    # ======================================================
    # SUMAR FILA ESCALADA
    # Solicita dos filas y un escalar para realizar la
    # operación F2 = F2 + kF1.
    # ======================================================
    def sumar_fila_escalada(self):
        fila1 = self.solicitar_entero(
            f"Ingrese la fila que desea sumar "
            f"(0-{self.matriz.filas - 1}): "
        )
        fila2 = self.solicitar_entero(
            f"Ingrese la fila a la que se sumará "
            f"(0-{self.matriz.filas - 1}): "
        )
        escalar = self.solicitar_numero(
            "Ingrese el valor del escalar: "
        )
        if self.dao.sumar_fila_escalada(
            self.matriz,
            fila1,
            fila2,
            escalar
        ):
            print(
                "\nOperación realizada correctamente."
            )
            self.matriz.mostrar()
        else:
            print(
                "Índice fuera del rango de la matriz."
            )

    # ======================================================
    # EJECUTAR MENÚ DE OPERACIONES
    # Muestra las operaciones elementales disponibles y
    # mantiene el menú activo hasta que el usuario decida
    # regresar al menú principal.
    # ======================================================
    def ejecutar(self):
        if not self.matriz.esta_completa():
            print(
                "La matriz no está completa. "
                "Por favor inserte todos los valores primero."
            )
            return
        while True:
            print("\nOperaciones Elementales:")
            print("1. Intercambiar filas")
            print("2. Sumar filas")
            print("3. Escalar una fila")
            print("4. Sumar una fila con una fila escalada")
            print("5. Volver al menú principal")
            opcion = input(
                "Seleccione una operación (1-5): "
            )
            if opcion == "1":
                self.intercambiar_filas()
            elif opcion == "2":
                self.sumar_filas()
            elif opcion == "3":
                self.escalar_fila()
            elif opcion == "4":
                self.sumar_fila_escalada()
            elif opcion == "5":
                break
            else:
                print(
                    "Opción inválida. "
                    "Seleccione una de las opciones presentes."
                )