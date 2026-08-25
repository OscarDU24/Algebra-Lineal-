from Menus.menu_operaciones import MenuOperaciones


class MenuPrincipal:

    def __init__(self, matriz, dao):
        self.matriz = matriz
        self.dao = dao
        self.menu_operaciones = MenuOperaciones(matriz, dao)

    def solicitar_entero(self, mensaje):

        while True:
            try:
                return int(input(mensaje))

            except ValueError:
                print("Ingrese únicamente un valor entero.")

    def solicitar_entero_positivo(self, mensaje):

        while True:
            valor = self.solicitar_entero(mensaje)

            if valor > 0:
                return valor

            print("Ingrese únicamente valores positivos.")

    def mostrar_matriz(self):

        print("\nMatriz:")

        if self.matriz.filas == 0:
            print("La matriz todavía no ha sido creada.")
            return

        self.matriz.mostrar()

    def definir_tamano(self):

        filas = self.solicitar_entero_positivo(
            "Ingrese el número de filas: "
        )

        columnas = self.solicitar_entero_positivo(
            "Ingrese el número de columnas: "
        )

        self.matriz.definir_tamano(filas, columnas)

        print("\nMatriz creada correctamente.")

    def insertar_valores(self):

        if self.matriz.filas == 0:
            print("Primero debe definir el tamaño de la matriz.")
            return

        for i in range(self.matriz.filas):

            for j in range(self.matriz.columnas):

                valor = self.solicitar_entero(
                    f"Ingrese el valor para la posición [{i}][{j}]: "
                )

                self.dao.insertar_valor(
                    self.matriz,
                    i,
                    j,
                    valor
                )

        print("\nValores insertados correctamente.")

    def consultar_valor(self):

        if not self.matriz.esta_completa():
            print(
                "La matriz no está completa. "
                "Por favor inserte todos los valores primero."
            )
            return

        fila = self.solicitar_entero(
            f"Ingrese el número de la fila "
            f"(0-{self.matriz.filas - 1}): "
        )

        columna = self.solicitar_entero(
            f"Ingrese el número de la columna "
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
            print("Índice fuera del rango de la matriz.")

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