inventario = {}

def pedir_texto(mensaje):
    while True:
        texto = input(mensaje).strip()
        if texto != "":
            return texto
def pedir_entero(mensaje):
    while True:
        try:
            numero = int(input(mensaje))
        except ValueError:
            print("Error: debe ingresar un número entero.")
            continue
        if numero > 0:
            return numero
        print("Error: el número debe ser positivo.")

def agregar_producto():
    nombre = pedir_texto("Nombre del producto: ").lower()
    cantidad = pedir_entero("Cantidad a agregar: ")
    if nombre in inventario:
        inventario[nombre] += cantidad
    else:
        inventario[nombre] = cantidad
    print(f"Se agregaron {cantidad} unidades de {nombre}.")
def vender_producto():
    nombre = pedir_texto("Nombre del producto: ").lower()
    if nombre not in inventario:
        print("Error: el producto no existe.")
        return
    cantidad = pedir_entero("Cantidad a vender: ")
    if cantidad > inventario[nombre]:
        print(f"Error: solo hay {inventario[nombre]} unidades de {nombre}.")
    else:
        inventario[nombre] -= cantidad
        print(f"Se vendieron {cantidad} unidades de {nombre}.")
def ver_inventario():
    if len(inventario) == 0:
        print("El inventario está vacío.")
    else:
        for nombre, cantidad in inventario.items():
            print(f"{nombre}: {cantidad}")

while True:
    print()
    print("1. Agregar producto")
    print("2. Vender producto")
    print("3. Ver inventario")
    print("4. Salir")
    opcion = input("Elija una opción: ").strip()
    if opcion == "1":
        agregar_producto()
    elif opcion == "2":
        vender_producto()
    elif opcion == "3":
        ver_inventario()
    elif opcion == "4":
        print("¡Hasta luego!")
        break
    else:
        print("Opción no válida. Elija 1, 2, 3 o 4.")