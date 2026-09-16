# Módulo de conversión entre sistemas numéricos con procedimiento algebraico...

PRECISION_DECIMALES = 8

BASES_DISPONIBLES = {
    1: ("Binario", 2),
    2: ("Octal", 8),
    3: ("Decimal", 10),
    4: ("Hexadecimal", 16),
    5: ("Sexagesimal / Personalizada", 60),
}


def _valor_digito(caracter, base):
    # Traduce un caracter a su valor numérico escalar (ej. 'A' -> 10)
    caracter = caracter.upper()
    if caracter.isdigit():
        valor = int(caracter)
    else:
        valor = ord(caracter) - ord('A') + 10

    if valor < 0 or valor >= base:
        raise ValueError(f"El dígito '{caracter}' no es válido para base {base}")
    return valor


def _digito_valor(valor):
    # Traduce un valor entero a su caracter en la base (ej. 10 -> 'A')
    if valor < 10:
        return str(valor)
    return chr(ord('A') + valor - 10)


def convertir_a_decimal_base(cadena, base):
    # Convierte a decimal mediante la combinación lineal de potencias de la base
    pasos = [f"--- Convertir {cadena} (Base {base}) a Decimal ---"]
    cadena = cadena.strip()
    
    negativo = cadena.startswith('-')
    if negativo:
        cadena = cadena[1:]

    if '.' in cadena:
        parte_entera, parte_frac = cadena.split('.', 1)
    else:
        parte_entera, parte_frac = cadena, ''

    terminos_formula = []
    terminos_valores = []
    
    # Manejo de bases mayores a 36 (ej. sexagesimal usando grupos separados por ':')
    if base > 36:
        grupos_enteros = parte_entera.split(':') if parte_entera else ['0']
        n = len(grupos_enteros)
        valor_entero = 0
        for i, grupo in enumerate(grupos_enteros):
            val_grupo = int(grupo)
            if val_grupo < 0 or val_grupo >= base:
                raise ValueError(f"El grupo '{grupo}' no es válido en base {base}")
            potencia = n - 1 - i
            terminos_formula.append(f"({val_grupo} * {base}^{potencia})")
            resultado_termino = val_grupo * (base ** potencia)
            terminos_valores.append(str(resultado_termino))
            valor_entero += resultado_termino

        valor_frac = 0.0
        if parte_frac:
            grupos_frac = parte_frac.split(':')
            for i, grupo in enumerate(grupos_frac):
                val_grupo = int(grupo)
                if val_grupo < 0 or val_grupo >= base:
                    raise ValueError(f"El grupo '{grupo}' no es válido en base {base}")
                potencia = -(i + 1)
                terminos_formula.append(f"({val_grupo} * {base}^{potencia})")
                resultado_termino = val_grupo / (base ** (i + 1))
                terminos_valores.append(f"{resultado_termino:.6f}")
                valor_frac += resultado_termino
    else:
        # Evalúa la parte entera con potencias positivas de la base
        n = len(parte_entera)
        valor_entero = 0
        for i, caracter in enumerate(parte_entera):
            val_dig = _valor_digito(caracter, base)
            potencia = n - 1 - i
            terminos_formula.append(f"({val_dig} * {base}^{potencia})")
            resultado_termino = val_dig * (base ** potencia)
            terminos_valores.append(str(resultado_termino))
            valor_entero += resultado_termino

        # Evalúa la parte fraccionaria con potencias negativas de la base
        valor_frac = 0.0
        for i, caracter in enumerate(parte_frac):
            val_dig = _valor_digito(caracter, base)
            potencia = -(i + 1)
            terminos_formula.append(f"({val_dig} * {base}^{potencia})")
            resultado_termino = val_dig / (base ** (i + 1))
            terminos_valores.append(f"{resultado_termino:.6f}")
            valor_frac += resultado_termino

    # Muestra la combinación lineal explícita pedida en la guía
    expresion_combinacion = " + ".join(terminos_formula)
    evaluacion_numerica = " + ".join(terminos_valores)
    
    pasos.append("Combinación lineal:")
    pasos.append(f"  N = {expresion_combinacion}")
    pasos.append("Sustituyendo valores:")
    pasos.append(f"  N = {evaluacion_numerica}")

    resultado = valor_entero + valor_frac
    if negativo:
        resultado = -resultado

    pasos.append(f"Resultado en Decimal: {resultado}\n")
    return resultado, "\n".join(pasos)


def convertir_decimal_a_base(numero, base, precision=PRECISION_DECIMALES):
    # Convierte un número decimal a otra base (divisiones y multiplicaciones sucesivas)
    pasos = [f"--- Convertir Decimal {numero} a Base {base} ---"]
    negativo = numero < 0
    numero = abs(numero)
    
    parte_entera = int(numero)
    parte_frac = numero - parte_entera

    # Divisiones sucesivas para la parte entera
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

    # Multiplicaciones sucesivas para la parte fraccionaria
    grupos_frac = []
    if parte_frac > 0:
        pasos.append("Multiplicaciones sucesivas (parte fraccionaria):")
        f = parte_frac
        for _ in range(precision):
            if f == 0:
                break
            f_mult = f * base
            digito = int(f_mult)
            pasos.append(f"  {f:.5f} * {base} = {f_mult:.5f}  (Entero extraído = {digito})")
            grupos_frac.append(digito)
            f = f_mult - digito

    # Formato de salida según el tamaño de la base
    if base > 36:
        texto_entero = ':'.join(str(d) for d in grupos_enteros)
        texto_frac = ':'.join(str(d) for d in grupos_frac)
    else:
        texto_entero = ''.join(_digito_valor(d) for d in grupos_enteros)
        texto_frac = ''.join(_digito_valor(d) for d in grupos_frac)

    resultado = texto_entero
    if texto_frac:
        resultado += '.' + texto_frac

    resultado_final = ('-' if negativo else '') + resultado
    pasos.append(f"Resultado Final en Base {base}: {resultado_final}")
    
    return resultado_final, "\n".join(pasos)


def ejecutar_conversion_completa(cadena, base_origen, base_destino):
    # Función principal: usa base 10 como pivote para convertir entre cualquier par de bases
    log_completo = []
    try:
        if base_origen == 10:
            valor_decimal = float(cadena)
            log_completo.append(f"El número ingresado ya está en Base 10: {valor_decimal}\n")
        else:
            valor_decimal, log_origen = convertir_a_decimal_base(cadena, base_origen)
            log_completo.append(log_origen)

        if base_destino == 10:
            resultado_final = str(valor_decimal)
            log_completo.append(f"Resultado en Base 10: {resultado_final}")
        else:
            resultado_final, log_destino = convertir_decimal_a_base(valor_decimal, base_destino)
            log_completo.append(log_destino)

        return resultado_final, "\n".join(log_completo)

    except Exception as e:
        return "ERROR", f"Error en la conversión:\n{str(e)}"