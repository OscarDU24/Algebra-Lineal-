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
        terminos_formula.append(f"({val_dig} x {base}^{potencia})")
        resultado_termino = val_dig * (base ** potencia)
        terminos_valores.append(str(resultado_termino))
        valor_entero += resultado_termino

    # --- Combinación lineal de la parte fraccionaria (potencias negativas) ---
    valor_frac = 0.0
    for i, caracter in enumerate(parte_frac):
        val_dig = _valor_digito(caracter, base)
        potencia = -(i + 1)
        terminos_formula.append(f"({val_dig} x {base}^{potencia})")
        resultado_termino = val_dig / (base ** (i + 1))
        terminos_valores.append(f"{resultado_termino:.6f}")
        valor_frac += resultado_termino

    expresion_combinacion = " + ".join(terminos_formula)
    evaluacion_numerica = " + ".join(terminos_valores)

    pasos.append("Combinación lineal (sumatoria de potencias de la base):")
    pasos.append(f"  N = {expresion_combinacion}")
    pasos.append("Sustituyendo cada término:")
    pasos.append(f"  N = {evaluacion_numerica}")

    resultado = valor_entero + valor_frac
    if negativo:
        resultado = -resultado
    if valor_frac == 0:
        resultado = int(resultado)

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
            temporal = cociente

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
    if valor == int(valor):
        valor = int(valor)
    return valor