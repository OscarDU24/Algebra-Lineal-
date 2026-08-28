# ==========================================================
# MENÚ PRINCIPAL
# Contiene la interacción principal con el usuario.
# Desde este menú se ingresan los sistemas de ecuaciones,
# se selecciona el método y se muestran los resultados.
# ==========================================================

from Services.logica_matematica import (
    eliminacion_gaussiana,
    eliminacion_gauss_jordan,
    clasificar_sistema,
    obtener_solucion_gauss,
    obtener_solucion_gauss_jordan,
    verificar_solucion
)


class MenuPrincipal:

    # ======================================================
    # CONSTRUCTOR
    # Recibe el modelo de matriz y el DAO encargado del
    # almacenamiento de la información.
    # ======================================================

    def __init__(self, matriz, dao):
        self.matriz = matriz
        self.dao = dao

    # ======================================================
    # EJECUTAR MENÚ
    # Controla el ciclo principal del programa.
    # ======================================================

    def ejecutar(self):
        while True:
            print("\n" + "=" * 60)
            print("       CALCULADORA DE ÁLGEBRA LINEAL")
            print("=" * 60)
            print("1. Ingresar sistema de ecuaciones")
            print("2. Mostrar sistema actual")
            print("3. Resolver por método de Gauss")
            print("4. Resolver por método de Gauss-Jordan")
            print("5. Salir")
            print("=" * 60)
            opcion = input("Seleccione una opción (1-5): ")

            if opcion == "1":
                self.ingresar_sistema()

            elif opcion == "2":
                self.mostrar_matriz()

            elif opcion == "3":
                self.resolver_gauss()

            elif opcion == "4":
                self.resolver_gauss_jordan()

            elif opcion == "5":
                print("Saliendo del programa.")
                break

            else:
                print("Opción inválida. Seleccione una opción del 1 al 5.")

    # ======================================================
    # INGRESAR SISTEMA
    # Solicita al usuario la cantidad de ecuaciones y
    # variables y posteriormente construye la matriz
    # aumentada A|b.
    # ======================================================

    def ingresar_sistema(self):
        print("\n--- INGRESO DEL SISTEMA ---")
        filas = self.pedir_entero_positivo(
            "Ingrese el número de ecuaciones: "
        )
        columnas = self.pedir_entero_positivo(
            "Ingrese el número de variables: "
        )
        matriz = []
        print("\nIngrese los coeficientes y términos independientes.")
        for i in range(filas):
            fila = []
            print(f"\nEcuación {i + 1}:")
            for j in range(columnas + 1):
                if j < columnas:
                    texto = f"Ingrese el coeficiente de x{j + 1}: "
                else:
                    texto = "Ingrese el término independiente: "
                valor = self.pedir_numero(texto)
                fila.append(valor)
            matriz.append(fila)
        self.matriz.definir_tamano(
            filas,
            columnas + 1
        )
        for i in range(filas):
            for j in range(columnas + 1):
                self.matriz.insertar_valor(
                    i,
                    j,
                    matriz[i][j]
                )
        self.dao.guardar(matriz)
        print("\nSistema ingresado correctamente.")
        self.mostrar_matriz()

    # ======================================================
    # MOSTRAR MATRIZ
    # Despliega la matriz aumentada utilizando una barra para
    # separar los coeficientes de los términos independientes.
    # ======================================================

    def mostrar_matriz(self):
        matriz = self.dao.obtener()
        if len(matriz) == 0:
            print("\nNo existe ningún sistema ingresado.")
            return
        print("\nMatriz aumentada A|b:")
        self.imprimir_matriz(matriz)

    # ======================================================
    # RESOLVER POR GAUSS
    # Ejecuta el proceso de eliminación gaussiana y muestra
    # cada paso representativo.
    # ======================================================

    def resolver_gauss(self):
        matriz_original = self.dao.obtener()
        if len(matriz_original) == 0:
            print("\nPrimero debe ingresar un sistema.")
            return
        print("\n" + "=" * 60)
        print("        ELIMINACIÓN POR GAUSS")
        print("=" * 60)
        matriz_resultado, pasos = eliminacion_gaussiana(
            matriz_original
        )
        print("\nMatriz aumentada inicial:")
        self.imprimir_matriz(matriz_original)
        self.mostrar_pasos(pasos)
        clasificacion = clasificar_sistema(
            matriz_resultado
        )
        self.mostrar_resultado(
            clasificacion,
            matriz_original,
            matriz_resultado,
            "gauss"
        )

    # ======================================================
    # RESOLVER POR GAUSS-JORDAN
    # Ejecuta el proceso de eliminación Gauss-Jordan y
    # muestra cada paso representativo.
    # ======================================================

    def resolver_gauss_jordan(self):
        matriz_original = self.dao.obtener()
        if len(matriz_original) == 0:
            print("\nPrimero debe ingresar un sistema.")
            return
        print("\n" + "=" * 60)
        print("        ELIMINACIÓN GAUSS-JORDAN")
        print("=" * 60)
        matriz_resultado, pasos = eliminacion_gauss_jordan(
            matriz_original
        )
        print("\nMatriz aumentada inicial:")
        self.imprimir_matriz(matriz_original)
        self.mostrar_pasos(pasos)
        clasificacion = clasificar_sistema(
            matriz_resultado
        )
        self.mostrar_resultado(
            clasificacion,
            matriz_original,
            matriz_resultado,
            "gauss-jordan"
        )

    # ======================================================
    # MOSTRAR PASOS
    # Muestra en pantalla las operaciones elementales
    # realizadas durante el proceso de eliminación.
    # ======================================================

    def mostrar_pasos(self, pasos):
        for descripcion, matriz in pasos:
            print("\n" + descripcion + ":")
            self.imprimir_matriz(matriz)

    # ======================================================
    # MOSTRAR RESULTADO
    # Presenta la clasificación del sistema y, cuando existe
    # una solución única, muestra las variables y realiza
    # automáticamente la verificación.
    # ======================================================

    def mostrar_resultado(
        self,
        clasificacion,
        matriz_original,
        matriz_resultado,
        metodo
    ):

        print("\n" + "=" * 60)
        print(f"RESULTADO: {clasificacion.upper()}")
        print("=" * 60)
        if clasificacion == "Sistema Consistente Determinado":
            if metodo == "gauss":
                solucion = obtener_solucion_gauss(
                    matriz_resultado
                )
            else:
                solucion = obtener_solucion_gauss_jordan(
                    matriz_resultado
                )
            print("\n--- SOLUCIÓN ÚNICA ---")
            for i in range(len(solucion)):
                print(
                    f"x{i + 1} = {solucion[i]:.6f}"
                )
            # ----------------------------------------------
            # VERIFICACIÓN AUTOMÁTICA
            # ----------------------------------------------
            verificacion = verificar_solucion(
                matriz_original,
                solucion
            )
            print("\n--- VERIFICACIÓN ---")
            if verificacion:
                print(
                    "Comprobación exitosa: la solución "
                    "satisface el sistema original."
                )
            else:
                print(
                    "Advertencia: la solución no pudo "
                    "ser verificada correctamente."
                )

        elif clasificacion == "Sistema Consistente Indeterminado":
            print(
                "\nEl sistema posee infinitas soluciones."
            )
            print(
                "Existen una o más variables libres."
            )
        elif clasificacion == "Sistema Inconsistente":
            print(
                "\nEl sistema no posee solución."
            )
            print(
                "Se detectó una contradicción matemática "
                "del tipo 0 = k, donde k es diferente de cero."
            )

    # ======================================================
    # IMPRIMIR MATRIZ
    # Formatea la matriz aumentada para facilitar su lectura.
    # ======================================================

    def imprimir_matriz(self, matriz):
        if len(matriz) == 0:
            return
        columnas = len(matriz[0])
        for fila in matriz:
            print("| ", end="")
            for j in range(columnas - 1):
                print(
                    f"{fila[j]:10.4f}",
                    end=" "
                )
            print(
                f"| {fila[-1]:10.4f} |"
            )

    # ======================================================
    # PEDIR ENTERO POSITIVO
    # Valida que el usuario introduzca un número entero
    # mayor que cero.
    # ======================================================

    def pedir_entero_positivo(self, mensaje):
        while True:
            try:
                valor = int(input(mensaje))
                if valor <= 0:
                    print(
                        "Ingrese únicamente un entero positivo."
                    )
                    continue
                return valor
            except ValueError:
                print(
                    "Ingrese únicamente un valor entero."
                )

    # ======================================================
    # PEDIR NÚMERO
    # Permite introducir números enteros, decimales o
    # fracciones simples como 1/2, 3/4, etc.
    # ======================================================

    def pedir_numero(self, mensaje):
        while True:
            entrada = input(mensaje).strip()
            if entrada == "":
                print("No puede dejar el campo vacío.")
                continue

            # ------------------------------------------------
            # INTENTAR CONVERTIR DIRECTAMENTE A FLOAT
            # ------------------------------------------------
            try:
                return float(entrada)
            except ValueError:
                pass

            # ------------------------------------------------
            # INTENTAR CONVERTIR UNA FRACCIÓN
            # ------------------------------------------------

            if "/" in entrada:
                partes = entrada.split("/")
                if len(partes) == 2:
                    try:
                        numerador = float(partes[0])
                        denominador = float(partes[1])
                        if denominador == 0:
                            print(
                                "El denominador no puede ser cero."
                            )
                            continue
                        return numerador / denominador
                    except ValueError:
                        pass
            print(
                "Valor inválido. Ingrese un entero, decimal "
                "o fracción. Ejemplos: 5, 2.5, 1/2."
            )