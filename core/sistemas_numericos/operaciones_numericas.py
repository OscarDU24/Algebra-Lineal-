# ============================================================
# OPERACIONES - SISTEMAS NUMÉRICOS (CON DESGLOSE PASO A PASO)
# ============================================================

PRECISION_DECIMALES = 8

def _valor_digito(caracter, base):
    caracter = caracter.upper()
    if caracter.isdigit():
        valor = int(caracter)
    else:
        valor = ord(caracter) - ord('A') + 10
    if valor < 0 or valor >= base:
        raise ValueError(f"El dígito '{caracter}' no es válido en base {base}")
    return valor

def _digito_valor(valor):
    if valor < 10:
        return str(valor)
    return chr(ord('A') + valor - 10)

def convertir_a_decimal_base(cadena, base):
    pasos = [f"--- PASO 1: Convirtiendo {cadena} (Base {base}) a Decimal ---"]
    cadena = cadena.strip()
    negativo = cadena.startswith('-')
    if negativo:
        cadena = cadena[1:]

    if '.' in cadena:
        parte_entera, parte_frac = cadena.split('.', 1)
    else:
        parte_entera, parte_frac = cadena, ''

    if base > 36:
        grupos_enteros = parte_entera.split(':') if parte_entera else ['0']
        valor_entero = 0
        pasos.append(f"Evaluando parte entera (grupos sexagesimales/mayores):")
        for grupo in grupos_enteros:
            valor_grupo = int(grupo)
            if valor_grupo < 0 or valor_grupo >= base:
                raise ValueError(f"El grupo '{grupo}' no es válido en base {base}")
            valor_entero = valor_entero * base + valor_grupo
            pasos.append(f" -> Acumulado: {valor_entero}")

        valor_frac = 0.0
        if parte_frac:
            grupos_frac = parte_frac.split(':')
            pasos.append(f"Evaluando parte fraccionaria:")
            for i, grupo in enumerate(grupos_frac):
                valor_grupo = int(grupo)
                if valor_grupo < 0 or valor_grupo >= base:
                    raise ValueError(f"El grupo '{grupo}' no es válido en base {base}")
                incremento = valor_grupo / (base ** (i + 1))
                valor_frac += incremento
                pasos.append(f" -> Grupo {grupo} / {base}^{i+1} = {incremento:.6f}")
    else:
        valor_entero = 0
        pasos.append(f"Expansión polinomial entera:")
        for caracter in parte_entera:
            val_dig = _valor_digito(caracter, base)
            valor_entero = valor_entero * base + val_dig
            pasos.append(f" -> Procesando '{caracter}': Acumulado = {valor_entero}")

        valor_frac = 0.0
        if parte_frac:
            pasos.append(f"Expansión polinomial fraccionaria:")
            for i, caracter in enumerate(parte_frac):
                val_dig = _valor_digito(caracter, base)
                incremento = val_dig / (base ** (i + 1))
                valor_frac += incremento
                pasos.append(f" -> Procesando '{caracter}': {val_dig} / {base}^{i+1} = {incremento:.6f}")

    resultado = valor_entero + valor_frac
    if negativo:
        resultado = -resultado
    
    pasos.append(f">> Equivalente Decimal: {resultado}\n")
    return resultado, "\n".join(pasos)

def convertir_decimal_a_base(numero, base, precision=PRECISION_DECIMALES):
    pasos = [f"--- PASO 2: Convirtiendo Decimal {numero} a Base {base} ---"]
    negativo = numero < 0
    numero = abs(numero)
    parte_entera = int(numero)
    parte_frac = numero - parte_entera

    # --- Parte entera ---
    if parte_entera == 0:
        grupos_enteros = [0]
        pasos.append("Parte entera es 0.")
    else:
        grupos_enteros = []
        temporal = parte_entera
        pasos.append("Divisiones sucesivas de la parte entera:")
        while temporal > 0:
            residuo = temporal % base
            cociente = temporal // base
            pasos.append(f" -> {temporal} / {base} = {cociente} (Residuo: {residuo})")
            grupos_enteros.insert(0, residuo)
            temporal = cociente

    # --- Parte fraccionaria ---
    grupos_frac = []
    if parte_frac > 0:
        pasos.append("Multiplicaciones sucesivas de la parte fraccionaria:")
        f = parte_frac
        for _ in range(precision):
            if f == 0:
                break
            f_mult = f * base
            digito = int(f_mult)
            pasos.append(f" -> {f:.5f} * {base} = {f_mult:.5f} (Extraemos entero: {digito})")
            grupos_frac.append(digito)
            f = f_mult - digito

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
    pasos.append(f">> Resultado Final en Base {base}: {resultado_final}")
    return resultado_final, "\n".join(pasos)

def ejecutar_conversion_completa(cadena, base_origen, base_destino):
    """Función unificadora que maneja el pivoteo y junta los registros de texto."""
    log_completo = []
    try:
        # 1. Pasar origen a Decimal
        if base_origen == 10:
            valor_decimal = float(cadena)
            log_completo.append(f"El número ingresado ya es base 10: {valor_decimal}\n")
        else:
            valor_decimal, log_origen = convertir_a_decimal_base(cadena, base_origen)
            log_completo.append(log_origen)

        # 2. Pasar Decimal a Destino
        if base_destino == 10:
            resultado_final = str(valor_decimal)
            log_completo.append(f"--- PASO 2: Resultado Final en Base 10: {resultado_final} ---")
        else:
            resultado_final, log_destino = convertir_decimal_a_base(valor_decimal, base_destino)
            log_completo.append(log_destino)

        texto_consola = "\n".join(log_completo)
        return resultado_final, texto_consola
    except Exception as e:
        return "ERROR", f"Error en la conversión:\n{str(e)}"