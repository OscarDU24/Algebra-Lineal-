def biseccionar(a, b, error_max):
    c = 0.0
    f_a = 0.0
    f_b = 0.0
    f_c = 0.0
    error = 0.0

    while True:
        c = (a + b)/2

        # Nota: Reemplazar la funcion fija por una dinamica con ayuda de SymPy
        f_a =   (  1 * pow(a, 4) ) + ( -5 * pow(a, 3) ) + (0.5 * pow(a, 2) ) + (-11 * pow(a, 1) ) + ( 10 * pow(a, 0) )
        f_b =   (  1 * pow(b, 4) ) + ( -5 * pow(b, 3) ) + (0.5 * pow(b, 2) ) + (-11 * pow(b, 1) ) + ( 10 * pow(b, 0) )
        f_c =   (  1 * pow(c, 4) ) + ( -5 * pow(c, 3) ) + (0.5 * pow(c, 2) ) + (-11 * pow(c, 1) ) + ( 10 * pow(c, 0) )

        error = abs(f_c)

        if (f_a > 0) == (f_c > 0):
            a = c
        else:
            b = c

        if(error <= error_max):
            break
    return c


print(biseccionar(5.1, 5.3, 0.0001))