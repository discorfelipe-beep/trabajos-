def estudiante():
    nombre = input("Nombre del estudiante: ")
    nota1 = float(input("Nota 1: "))
    nota2 = float(input("Nota 2: "))
    nota3 = float(input("Nota 3: "))
    promedio = (nota1 + nota2 + nota3) / 3
    return nombre, promedio
def resultado(promedio):
    if promedio > 60:
        return "APROBÓ"
    else:
        return "NO APROBÓ"
nombre, promedio = estudiante()
print("\nEstudiante:", nombre)
print("Promedio:", promedio)
print("Resultado:", resultado(promedio))