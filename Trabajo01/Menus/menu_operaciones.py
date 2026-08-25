class MenuOperaciones:

    def __init__(self, matriz, dao):
        self.matriz = matriz
        self.dao = dao

    def solicitar_entero(self, mensaje):

        while True:
            try:
                return int(input(mensaje))

            except ValueError:
                print("Ingrese únicamente un valor entero.")

    def ejecutar(self):

        if not self.matriz.esta_completa():
            print(
                "La matriz no está completa. "
                "Por favor inserte los valores primero."
            )
            return

        while True:

            print("\nOperaciones Elementales:")
            print("1. Intercambiar filas")
            print("2. Sumar filas")
            print("3. Escalar una fila")
            print("4. Sumar una fila con una fila escalada")
            print("5. Volver al menú principal")

            operacion = input(
                "Seleccione una operación (1-5): "
            )

            if operacion == "1":

                self.intercambiar_filas()

            elif operacion == "2":

                self.sumar_filas()

            elif operacion == "3":

                self.escalar_fila()

            elif operacion == "4":

                self.sumar_fila_escalada()

            elif operacion == "5":

                break

            else:

                print(
                    "Opción inválida. "
                    "Seleccione una de las opciones presentes."
                )

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

            print("\nFilas intercambiadas correctamente.")
            self.matriz.mostrar()

        else:

            print("Índice fuera del rango de la matriz.")

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

            print("\nFilas sumadas correctamente.")
            self.matriz.mostrar()

        else:

            print("Índice fuera del rango de la matriz.")

    def escalar_fila(self):

        fila = self.solicitar_entero(
            f"Ingrese la fila a escalar "
            f"(0-{self.matriz.filas - 1}): "
        )

        escalar = self.solicitar_entero(
            "Ingrese el valor del escalar: "
        )

        if self.dao.escalar_fila(
            self.matriz,
            fila,
            escalar
        ):

            print("\nFila escalada correctamente.")
            self.matriz.mostrar()

        else:

            print("Índice fuera del rango de la matriz.")

    def sumar_fila_escalada(self):

        fila1 = self.solicitar_entero(
            f"Ingrese la fila que desea sumar "
            f"(0-{self.matriz.filas - 1}): "
        )

        fila2 = self.solicitar_entero(
            f"Ingrese la fila a la que se sumará "
            f"(0-{self.matriz.filas - 1}): "
        )

        escalar = self.solicitar_entero(
            "Ingrese el valor del escalar: "
        )

        if self.dao.sumar_fila_escalada(
            self.matriz,
            fila1,
            fila2,
            escalar
        ):

            print("\nOperación realizada correctamente.")
            self.matriz.mostrar()

        else:

            print("Índice fuera del rango de la matriz.")