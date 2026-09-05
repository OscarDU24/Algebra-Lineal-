from prettytable import PrettyTable, HRuleStyle, VRuleStyle

# 1. Crear la tabla
table = PrettyTable()
table.hrules = HRuleStyle.HEADER
table.vrules = VRuleStyle.FRAME

# 2. Matriz de ejemplo
matriz = [[0,0,0,0],[0,0,0,0],[0,0,0,0]]

# 3. Generar los campos a partir de la matriz
campos = []
for i in range(len(matriz[0])-1):
    campos.append(f"X{i+1}")
campos.append(f"TI")
table.field_names = campos

# 4. Añadir cada ecuacion a la tabla
for i in matriz:
    table.add_row(i)

# 5. Mostrar la tabla
s = "" 
s += str(table) # Se añade en vez de igualar para probar la conversión a string
print(s)


