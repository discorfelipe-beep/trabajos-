def pedir_notas(numero):
    while True:
        texto = input(f"Introduce la nota {numero}: ")
        try:
            nota = float(texto)
        except ValueError:
            print("Error: solo debes ingresar numeros.")
            continue
        if 0.0 <= nota <= 5.0:
            return nota
        else:
            print("Error: la nota debe estar entre 0 y 50.")

nota1 = pedir_notas(1)
nota2 = pedir_notas(2)
nota3 = pedir_notas(3)

promedio = (nota1 + nota2 + nota3) / 3
print(f"el promedio de las notas es: {promedio:.2f}", end="→")
if promedio >=4.5:
    print("Exelente")
elif promedio >=3.0:
    print("Aprobado")
else:
    print("Reprobado")