PRECISION_DECIMALES = 8

# Sistemas numéricos habilitados para este programa (nombre -> base)
SISTEMAS = {
    "Binario": 2,
    "Octal": 8,
    "Decimal": 10,
    "Hexadecimal": 16,
}


def _valor_digito(caracter, base):
    caracter = caracter.upper()
    if caracter.isdigit():
        valor = int(caracter)
    elif 'A' <= caracter <= 'Z':
        valor = ord(caracter) - ord('A') + 10
    else:
        raise ValueError(f"El carácter '{caracter}' no es un dígito válido.")

    if valor < 0 or valor >= base:
        raise ValueError(
            f"El dígito '{caracter}' no es válido para base {base} "
            f"(los dígitos permitidos van de 0 a {base - 1})."
        )
    return valor


def _digito_valor(valor):
    """Traduce un valor entero (0-15) a su carácter en la base (ej. 10 -> 'A')."""
    if valor < 10:
        return str(valor)
    return chr(ord('A') + valor - 10)


def validar_cadena_en_base(cadena, base):
    """
    Verifica que 'cadena' solo contenga dígitos válidos para 'base'.
    Se usa antes de convertir, para dar un mensaje de error claro en el GUI.
    """
    cuerpo = cadena.strip()
    if cuerpo.startswith('-'):
        cuerpo = cuerpo[1:]

    if cuerpo == '' or cuerpo == '.':
        raise ValueError("Debes ingresar un número para convertir.")

    if cuerpo.count('.') > 1:
        raise ValueError("El número solo puede contener un punto decimal.")

    for caracter in cuerpo:
        if caracter == '.':
            continue
        _valor_digito(caracter, base)  # lanza ValueError si el dígito no es válido

def convertir_a_decimal(cadena, base, nombre_base):

    cadena = cadena.strip()
    validar_cadena_en_base(cadena, base)

    pasos = [f"--- Convertir {cadena} de {nombre_base} (Base {base}) a Decimal ---"]

    negativo = cadena.startswith('-')
    if negativo:
        cadena = cadena[1:]

    if '.' in cadena:
        parte_entera, parte_frac = cadena.split('.', 1)
    else:
        parte_entera, parte_frac = cadena, ''

    if parte_entera == '':
        parte_entera = '0'

    # Caso trivial: el número ya está en Decimal, no hay combinación que mostrar.
    if base == 10:
        resultado = float(cadena) if parte_frac else int(parte_entera)
        if negativo:
            resultado = -resultado
        pasos.append("El número ya se encuentra en Base 10 (Decimal).")
        pasos.append(f"Resultado en Decimal: {resultado}\n")
        return resultado, "\n".join(pasos)

    terminos_formula = []
    terminos_valores = []

    # --- Combinación lineal de la parte entera (potencias positivas) ---
    n = len(parte_entera)
    valor_entero = 0
    for i, caracter in enumerate(parte_entera):
        val_dig = _valor_digito(caracter, base)
        potencia = n - 1 - i
        terminos_formula.append(f"{caracter.upper()}x{base}^{potencia}")
        resultado_termino = val_dig * (base ** potencia)
        terminos_valores.append(str(resultado_termino))
        valor_entero += resultado_termino

    # --- Combinación lineal de la parte fraccionaria (potencias negativas) ---
    valor_frac = 0.0
    for i, caracter in enumerate(parte_frac):
        val_dig = _valor_digito(caracter, base)
        potencia = -(i + 1)
        terminos_formula.append(f"{caracter.upper()}x{base}^{potencia}")
        resultado_termino = val_dig / (base ** (i + 1))
        terminos_valores.append(f"{resultado_termino:.6f}")
        valor_frac += resultado_termino

    expresion_combinacion = " + ".join(terminos_formula)
    evaluacion_numerica = " + ".join(terminos_valores)

    resultado = valor_entero + valor_frac
    if negativo:
        resultado = -resultado
    if valor_frac == 0:
        resultado = int(resultado)

    signo = "-" if negativo else ""
    pasos.append("Descomposición polinómica:")
    pasos.append(f"  ({signo}{cadena}){base} = {expresion_combinacion}")
    pasos.append(f"  = {evaluacion_numerica} = {resultado}")
    pasos.append(f"Resultado en Decimal: {resultado}\n")
    return resultado, "\n".join(pasos)


def convertir_decimal_a_base(numero, base, nombre_base, precision=PRECISION_DECIMALES):
    """
    Convierte un número Decimal a la 'base' indicada, usando:
      - Divisiones sucesivas para la parte entera.
      - Multiplicaciones sucesivas para la parte fraccionaria.
    """
    pasos = [f"--- Convertir Decimal {numero} a {nombre_base} (Base {base}) ---"]

    if base == 10:
        pasos.append("El destino es Base 10 (Decimal): el número no cambia.")
        pasos.append(f"Resultado Final en Decimal: {numero}")
        return str(numero), "\n".join(pasos)

    negativo = numero < 0
    numero = abs(numero)

    parte_entera = int(numero)
    parte_frac = numero - parte_entera

    # --- Divisiones sucesivas para la parte entera ---
    grupos_enteros = []
    residuos_enteros = []
    if parte_entera == 0:
        grupos_enteros = [0]
        pasos.append("Parte entera es 0.")
    else:
        pasos.append("Divisiones sucesivas (parte entera):")
        temporal = parte_entera
        while temporal > 0:
            residuo = temporal % base
            cociente = temporal // base
            pasos.append(f"  {temporal} / {base} = {cociente}  (Residuo = {residuo})")
            grupos_enteros.insert(0, residuo)
            residuos_enteros.append(residuo)
            temporal = cociente

        residuos_invertidos = " -> ".join(
            _digito_valor(residuo) for residuo in reversed(residuos_enteros)
        )
        resultado_residuos = "".join(
            _digito_valor(residuo) for residuo in reversed(residuos_enteros)
        )
        pasos.append(
            "Tomando los residuos desde el último al primero: "
            f"{residuos_invertidos} -> {resultado_residuos}"
        )

    # --- Multiplicaciones sucesivas para la parte fraccionaria ---
    grupos_frac = []
    if parte_frac > 0:
        pasos.append("Multiplicaciones sucesivas (parte fraccionaria):")
        f = parte_frac
        for _ in range(precision):
            if f == 0:
                break
            f_mult = f * base
            digito = int(f_mult)
            pasos.append(f"  {f:.6f} x {base} = {f_mult:.6f}  (Entero extraído = {digito})")
            grupos_frac.append(digito)
            f = f_mult - digito

    texto_entero = ''.join(_digito_valor(d) for d in grupos_enteros)
    texto_frac = ''.join(_digito_valor(d) for d in grupos_frac)

    resultado = texto_entero
    if texto_frac:
        resultado += '.' + texto_frac

    resultado_final = ('-' if negativo else '') + resultado
    pasos.append(f"Resultado Final en {nombre_base}: {resultado_final}")

    return resultado_final, "\n".join(pasos)


def parsear_decimal(cadena):
    """Valida y convierte el texto ingresado por el usuario a un número decimal (int o float)."""
    cadena = cadena.strip()
    if cadena == '':
        raise ValueError("Debes ingresar un número decimal para convertir.")
    try:
        valor = float(cadena)
    except ValueError:
        raise ValueError(f"'{cadena}' no es un número decimal válido.")
    if valor != valor or valor in (float("inf"), float("-inf")):
        raise ValueError(f"'{cadena}' debe ser un número decimal finito.")
    if valor == int(valor):
        valor = int(valor)
    return valor

# ==========================================================
# Motor lógico (backend) de la Calculadora Romana bidireccional
# Arábigo <-> Romano, explicado como COMBINACIÓN LINEAL:
#     N = c0*(1000) + c1*(900) + ... + c12*(1)
#
# Diseñado para integrarse con una GUI (devuelve resultado + pasos).
# Solo Python estándar.
# ==========================================================


class ErrorConversion(ValueError):
    """Error interno de validación o conversión."""
    pass

# Hecho por Charly y Oscar B)

class CalculadoraRomana:
    """Backend de la calculadora romana.

    Los métodos principales devuelven:

        (resultado, pasos)
            cuando la conversión es correcta.

        (None, mensaje_error)
            cuando ocurre un error.

    Atributos que la GUI puede leer:
        resultado -> último resultado (str o int; None si hubo error)
        pasos     -> lista de strings con el procedimiento detallado
        error     -> mensaje del último error (None si todo salió bien)
    """

    def __init__(self):

        # Listas de referencia del algoritmo de clase
        # (orden descendente)
        self.valores = [
            1000, 900, 500, 400, 100, 90, 50,
            40, 10, 9, 5, 4, 1
        ]

        self.simbolos = [
            "M", "CM", "D", "CD", "C", "XC", "L",
            "XL", "X", "IX", "V", "IV", "I"
        ]

        self.validos = "MDCLXVI"

        self.minimo = 1
        self.maximo = 3999

        # Estado que consume la interfaz
        self.resultado = None
        self.pasos = []
        self.error = None
        self.encabezado = ""

    # ------------------------------------------------------
    # Utilidades internas
    # ------------------------------------------------------

    def _reiniciar(self):
        """Limpia el estado antes de cada conversión."""

        self.resultado = None
        self.pasos = []
        self.error = None
        self.encabezado = ""

    def _agregar_paso(self, texto):
        """Agrega una línea al historial de pasos."""

        self.pasos.append(texto)

    def _descomponer(self, n):
        """Devuelve la lista de coeficientes."""

        coeficientes = []

        for i in range(len(self.valores)):

            cantidad = n // self.valores[i]

            coeficientes.append(cantidad)

            n = n % self.valores[i]

        return coeficientes

    def _romano_desde_coeficientes(self, coeficientes):
        """Arma la cadena romana a partir de los coeficientes."""

        romano = ""

        for i in range(len(coeficientes)):

            romano = romano + (
                self.simbolos[i] * coeficientes[i]
            )

        return romano

    def _texto_combinacion(self, coeficientes):
        """Devuelve la combinación lineal."""

        terminos = []

        for i in range(len(coeficientes)):

            if coeficientes[i] > 0:

                terminos.append(
                    str(coeficientes[i])
                    + "·("
                    + str(self.valores[i])
                    + ")"
                )

        return " + ".join(terminos)

    # ------------------------------------------------------
    # Validaciones
    # ------------------------------------------------------

    def _validar_arabigo(self, entrada):
        """Valida y devuelve el número arábigo como int."""

        if isinstance(entrada, bool) or not isinstance(
            entrada, (int, str)
        ):

            raise ErrorConversion(
                "La entrada debe ser un número entero "
                "(int) o texto con dígitos."
            )

        if isinstance(entrada, str):

            texto = entrada.strip()

            if texto == "":

                raise ErrorConversion(
                    "La entrada está vacía."
                )

            if not texto.isdigit():

                raise ErrorConversion(
                    "'" + texto
                    + "' no es un entero positivo válido."
                )

            numero = int(texto)

        else:

            numero = entrada

        if numero < self.minimo or numero > self.maximo:

            raise ErrorConversion(
                "El número debe estar entre "
                + str(self.minimo)
                + " y "
                + str(self.maximo)
                + "."
            )

        return numero

    def _validar_romano(self, entrada):
        """Valida y devuelve el romano normalizado."""

        if not isinstance(entrada, str):

            raise ErrorConversion(
                "El número romano debe ser texto (str)."
            )

        texto = entrada.strip().upper()

        if texto == "":

            raise ErrorConversion(
                "La entrada está vacía."
            )

        for caracter in texto:

            if caracter not in self.validos:

                raise ErrorConversion(
                    "'"
                    + caracter
                    + "' no es un símbolo romano válido "
                    "(M, D, C, L, X, V, I)."
                )

        return texto

    # ------------------------------------------------------
    # Arábigo -> Romano
    # ------------------------------------------------------

    def arabigo_a_romano(
        self,
        entrada,
        detallar_ceros=False
    ):
        """Convierte un número arábigo a romano.

        Retorna:

            (romano, pasos)
                si la conversión es correcta.

            (None, mensaje_error)
                si ocurre un error.
        """

        self._reiniciar()

        try:

            numero = self._validar_arabigo(entrada)

            self.encabezado = (
                "PROCEDIMIENTO "
                "(divisiones sucesivas y combinación lineal)"
            )

            self._agregar_paso(
                "--- Convertir Decimal "
                + str(numero)
                + " a Romano ---"
            )

            self._agregar_paso(
                "Divisiones sucesivas (parte entera):"
            )

            # --------------------------------------------------
            # Algoritmo de conversión
            # --------------------------------------------------

            resto = numero
            coeficientes = []

            for i in range(len(self.valores)):

                valor = self.valores[i]

                cantidad = resto // valor

                nuevo_resto = resto % valor

                coeficientes.append(cantidad)

                if cantidad > 0:

                    self._agregar_paso(
                        "  "
                        + str(resto)
                        + " / "
                        + str(valor)
                        + " = "
                        + str(cantidad)
                        + "  (Residuo = "
                        + str(nuevo_resto)
                        + ")"
                        + "  ->  "
                        + str(cantidad)
                        + " x "
                        + self.simbolos[i]
                    )

                elif detallar_ceros:

                    self._agregar_paso(
                        "  "
                        + str(resto)
                        + " / "
                        + str(valor)
                        + " = 0"
                        + "  (Residuo = "
                        + str(resto)
                        + ")"
                        + "  ->  no se usa "
                        + self.simbolos[i]
                    )

                resto = nuevo_resto

            # --------------------------------------------------
            # Construcción del romano
            # --------------------------------------------------

            romano = self._romano_desde_coeficientes(
                coeficientes
            )

            # --------------------------------------------------
            # Combinación lineal
            # --------------------------------------------------

            suma = 0

            for i in range(len(coeficientes)):

                suma = (
                    suma
                    + coeficientes[i] * self.valores[i]
                )

            self._agregar_paso(
                "Combinación lineal: "
                + str(numero)
                + " = "
                + self._texto_combinacion(coeficientes)
                + "  (suma = "
                + str(suma)
                + ")"
            )

            # --------------------------------------------------
            # Unión de símbolos
            # --------------------------------------------------

            partes = []

            for i in range(len(coeficientes)):

                if coeficientes[i] > 0:

                    partes.append(
                        self.simbolos[i]
                        * coeficientes[i]
                    )

            self._agregar_paso(
                "Uniendo los símbolos de mayor a menor: "
                + " -> ".join(partes)
                + " -> "
                + romano
            )

            self._agregar_paso(
                "Resultado Final en Romano: "
                + romano
            )

            self.resultado = romano

            return romano, self.pasos

        except ErrorConversion as e:

            self.resultado = None
            self.error = str(e)

            return None, self.error

    # ------------------------------------------------------
    # Romano -> Arábigo
    # ------------------------------------------------------

    def romano_a_arabigo(self, entrada):
        """Convierte un número romano a arábigo.

        Retorna:

            (entero, pasos)
                si la conversión es correcta.

            (None, mensaje_error)
                si ocurre un error.
        """

        self._reiniciar()

        try:

            texto = self._validar_romano(entrada)

            self.encabezado = (
                "PROCEDIMIENTO "
                "(suma de valores y combinación lineal)"
            )

            self._agregar_paso(
                "--- Convertir Romano "
                + texto
                + " a Decimal ---"
            )

            self._agregar_paso(
                "Símbolos identificados "
                "(de izquierda a derecha, "
                "CM antes que C y M, etc.):"
            )

            # --------------------------------------------------
            # Coeficientes
            # --------------------------------------------------

            coeficientes = [0] * len(self.valores)

            sumandos = []

            pos = 0

            acumulado = 0

            while pos < len(texto):

                encontrado = False

                for i in range(len(self.simbolos)):

                    if texto.startswith(
                        self.simbolos[i],
                        pos
                    ):

                        coeficientes[i] = (
                            coeficientes[i] + 1
                        )

                        acumulado = (
                            acumulado
                            + self.valores[i]
                        )

                        sumandos.append(
                            str(self.valores[i])
                        )

                        self._agregar_paso(
                            "  "
                            + self.simbolos[i]
                            + " = "
                            + str(self.valores[i])
                            + "  (acumulado = "
                            + str(acumulado)
                            + ")"
                        )

                        pos = (
                            pos
                            + len(self.simbolos[i])
                        )

                        encontrado = True

                        break

                if not encontrado:

                    raise ErrorConversion(
                        "No se pudo interpretar "
                        "la cadena romana."
                    )

            # --------------------------------------------------
            # Combinación lineal
            # --------------------------------------------------

            self._agregar_paso(
                "Combinación lineal: "
                + texto
                + " = "
                + self._texto_combinacion(
                    coeficientes
                )
            )

            self._agregar_paso(
                "Sumando los valores: "
                + " + ".join(sumandos)
                + " = "
                + str(acumulado)
            )

            # --------------------------------------------------
            # Verificación de rango
            # --------------------------------------------------

            if (
                acumulado < self.minimo
                or acumulado > self.maximo
            ):

                raise ErrorConversion(
                    "El valor obtenido ("
                    + str(acumulado)
                    + ") está fuera del rango "
                    + str(self.minimo)
                    + "-"
                    + str(self.maximo)
                    + "."
                )

            # --------------------------------------------------
            # Verificación de formato romano
            # --------------------------------------------------

            reconstruido = (
                self._romano_desde_coeficientes(
                    self._descomponer(acumulado)
                )
            )

            self._agregar_paso(
                "Verificación: "
                + str(acumulado)
                + " se escribe "
                + reconstruido
                + " con el algoritmo de clase"
            )

            if reconstruido != texto:

                raise ErrorConversion(
                    "\""
                    + texto
                    + "\" no es un número romano "
                    "bien formado "
                    "(su suma da "
                    + str(acumulado)
                    + ", que se escribe \""
                    + reconstruido
                    + "\")."
                )

            # --------------------------------------------------
            # Resultado
            # --------------------------------------------------

            self._agregar_paso(
                "Resultado Final en Decimal: "
                + str(acumulado)
            )

            self.resultado = acumulado

            return acumulado, self.pasos

        except ErrorConversion as e:

            self.resultado = None
            self.error = str(e)

            return None, self.error


# ==========================================================
# EJEMPLO DE USO
# ==========================================================

if __name__ == '__main__':

    calculadora = CalculadoraRomana()

    # ------------------------------------------------------
    # Arábigo -> Romano
    # ------------------------------------------------------

    resultado, mensaje = (
        calculadora.arabigo_a_romano(1994)
    )

    if resultado is None:

        print("Error:", mensaje)

    else:

        print("=== RESULTADO ===")
        print(resultado)

        print("\n=== PASO A PASO ===")
        print("\n".join(mensaje))

    # ------------------------------------------------------
    # Romano -> Arábigo
    # ------------------------------------------------------

    print("\n" + "-" * 50 + "\n")

    resultado, mensaje = (
        calculadora.romano_a_arabigo("MCMXCIV")
    )

    if resultado is None:

        print("Error:", mensaje)

    else:

        print("=== RESULTADO ===")
        print(resultado)

        print("\n=== PASO A PASO ===")
        print("\n".join(mensaje))

    # ------------------------------------------------------
    # Ejemplo de error
    # ------------------------------------------------------

    print("\n" + "-" * 50 + "\n")

    resultado, mensaje = (
        calculadora.romano_a_arabigo("IIII")
    )

    if resultado is None:

        print("Error:", mensaje)

    else:

        print("=== RESULTADO ===")
        print(resultado)

        print("\n=== PASO A PASO ===")
        print("\n".join(mensaje))