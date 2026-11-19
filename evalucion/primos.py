def es_primo(n):
    if n < 2:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True


def pedir_numero():
    while True:
        texto = input("Ingrese un número entero positivo: ")
        try:
            n = int(texto)
        except ValueError:
            print("Error: debe ingresar un número entero.")
            continue

        if n > 0:
            return n
        else:
            print("Error: el número debe ser positivo.")


N = pedir_numero()

primos = []
for i in range(1, N + 1):
    if es_primo(i):
        primos.append(i)

if len(primos) > 0:
    print(", ".join(str(p) for p in primos), end=" → ")
print(f"{len(primos)} primos")