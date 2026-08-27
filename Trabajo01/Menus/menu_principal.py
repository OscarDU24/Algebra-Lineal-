# ==========================================================
# CLASE MENÚ PRINCIPAL
# Controla la interacción con el usuario, la creación del
# sistema de ecuaciones y el acceso al proceso de resolución.
# ==========================================================

class MenuPrincipal:
    def __init__(self, matriz, dao, eliminacion):
        self.matriz = matriz
        self.dao = dao
        self.eliminacion = eliminacion
        self.matriz_original = None

    # ======================================================
    # VALIDAR ENTEROS
    # Solicita un número entero y repite la entrada mientras
    # el usuario introduzca un valor incorrecto.
    # ======================================================
    def solicitar_entero(self, mensaje):
        while True:
            try:
                return int(input(mensaje))
            except ValueError:
                print("Ingrese únicamente un valor entero.")

    # ======================================================
    # VALIDAR ENTEROS POSITIVOS
    # Se utiliza para solicitar cantidades de ecuaciones y
    # variables mayores que cero.
    # ======================================================
    def solicitar_entero_positivo(self, mensaje):
        while True:
            valor = self.solicitar_entero(mensaje)
            if valor > 0:
                return valor
            print("Ingrese únicamente valores positivos.")

    # ======================================================
    # VALIDAR NÚMEROS
    # Permite introducir coeficientes y términos independientes
    # utilizando tanto números enteros como decimales.
    # ======================================================
    def solicitar_numero(self, mensaje):
        while True:
            try:
                valor = float(input(mensaje))
                if valor.is_integer():
                    return int(valor)
                return valor
            except ValueError:
                print("Ingrese únicamente un número entero o decimal.")

    # ======================================================
    # INGRESAR SISTEMA
    # Solicita el número de ecuaciones y variables y construye
    # automáticamente la matriz aumentada A|b.
    # ======================================================
    def ingresar_sistema(self):
        print("\n--- Ingreso del sistema ---")
        ecuaciones = self.solicitar_entero_positivo(
            "Ingrese el número de ecuaciones: "
        )
        variables = self.solicitar_entero_positivo(
            "Ingrese el número de variables: "
        )

        self.matriz.definir_tamano(ecuaciones, variables + 1)

        for i in range(ecuaciones):
            print(f"\n--- Ecuación {i + 1} ---")

            for j in range(variables):
                valor = self.solicitar_numero(
                    f"Ingrese el coeficiente de x{j + 1}: "
                )
                self.dao.insertar_valor(
                    self.matriz, i, j, valor
                )

            independiente = self.solicitar_numero(
                "Ingrese el término independiente: "
            )
            self.dao.insertar_valor(
                self.matriz, i, variables, independiente
            )

        self.matriz_original = self.copiar_matriz()

        print("\nMatriz aumentada creada correctamente.")
        self.matriz.mostrar()

    # ======================================================
    # COPIAR MATRIZ
    # Crea una copia manual de la matriz original para poder
    # utilizarla posteriormente durante la verificación.
    # ======================================================
    def copiar_matriz(self):
        copia = type(self.matriz)()
        copia.definir_tamano(
            self.matriz.filas,
            self.matriz.columnas
        )

        for i in range(self.matriz.filas):
            for j in range(self.matriz.columnas):
                copia.valores[i][j] = self.matriz.valores[i][j]

        return copia

    # ======================================================
    # MOSTRAR MATRIZ
    # Muestra la matriz aumentada almacenada actualmente.
    # ======================================================
    def mostrar_matriz(self):
        print("\n--- Matriz aumentada ---")
        self.matriz.mostrar()

    # ======================================================
    # RESOLVER SISTEMA
    # Ejecuta la eliminación, clasifica el sistema, obtiene
    # la solución cuando corresponde y realiza la verificación.
    # ======================================================
    def resolver_sistema(self):
        if self.matriz.filas == 0:
            print("Primero debe ingresar un sistema.")
            return

        print("\n--- Matriz aumentada inicial ---")
        self.matriz.mostrar()

        clasificacion = self.eliminacion.ejecutar()

        print("\n========================================")
        print("CLASIFICACIÓN DEL SISTEMA")
        print("========================================")

        if clasificacion == "inconsistente":
            print("Sistema Inconsistente: Sin Solución.")

        elif clasificacion == "indeterminado":
            print(
                "Sistema Consistente Indeterminado: "
                "Presenta Infinitas Soluciones."
            )

        else:
            print(
                "Sistema Consistente Determinado: "
                "Presenta Solución Única."
            )

            solucion = self.eliminacion.obtener_solucion()

            print("\n--- Solución ---")
            for i in range(len(solucion)):
                print(f"x{i + 1} = {solucion[i]}")

            if self.eliminacion.verificar(
                self.matriz_original,
                solucion
            ):
                print("\nVerificación: CORRECTA.")
                print("La solución satisface el sistema original.")
            else:
                print("\nVerificación: INCORRECTA.")

    # ======================================================
    # CONSULTAR VALOR
    # Permite consultar un elemento específico de la matriz.
    # ======================================================
    def consultar_valor(self):
        if self.matriz.filas == 0:
            print("Primero debe ingresar un sistema.")
            return

        fila = self.solicitar_entero(
            f"Ingrese la fila (0-{self.matriz.filas - 1}): "
        )
        columna = self.solicitar_entero(
            f"Ingrese la columna (0-{self.matriz.columnas - 1}): "
        )

        valor = self.dao.consultar_valor(
            self.matriz, fila, columna
        )

        if valor is not None:
            print(
                f"El valor en [{fila}][{columna}] es: {valor}"
            )
        else:
            print("Índice fuera del rango de la matriz.")

    # ======================================================
    # EJECUTAR MENÚ
    # Mantiene activo el menú principal hasta que el usuario
    # seleccione la opción de salida.
    # ======================================================
    def ejecutar(self):
        while True:
            print("\n========================================")
            print(" SISTEMA DE ECUACIONES LINEALES")
            print("========================================")
            print("1. Ingresar sistema de ecuaciones")
            print("2. Mostrar matriz aumentada")
            print("3. Resolver sistema")
            print("4. Consultar elemento de la matriz")
            print("5. Salir")

            opcion = input("Seleccione una opción (1-5): ")

            if opcion == "1":
                self.ingresar_sistema()
            elif opcion == "2":
                self.mostrar_matriz()
            elif opcion == "3":
                self.resolver_sistema()
            elif opcion == "4":
                self.consultar_valor()
            elif opcion == "5":
                print("Saliendo del programa.")
                break
            else:
                print("Opción inválida.")