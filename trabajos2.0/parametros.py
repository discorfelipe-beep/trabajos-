def fibonacci(numero):
    a = 0
    b = 1

    while a < numero:
        a, b = b, a + b

    return a == numero


def verificar(numero):
    if fibonacci(numero):
        print("El número sí pertenece a Fibonacci")
    else:
        print("El número no pertenece a Fibonacci")


n = int(input("Ingrese un número: "))
verificar(n)