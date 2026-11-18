numeros = []

while True:
    entrada = input("Ingresa un número (o escribe 'fin' para terminar): ").strip()

    if entrada.lower() == "fin":
        break

    try:
        numeros.append(float(entrada))
    except ValueError:
        print("Eso no es un número válido, intenta de nuevo.")

if not numeros:
    print("No se ingresó ningún número.")
else:
    promedio = sum(numeros) / len(numeros)
    print(f"Promedio: {promedio:.2f}")
    print(f"Mayor: {max(numeros)}")
    print(f"Menor: {min(numeros)}") 