frase = input("Ingrese una frase: ")
sin_espacios = frase.replace(" ", "")

print("Cantidad de letras:", len(sin_espacios))
print("Cantidad de palabras:", len(frase.split()))
print("En mayúsculas:",frase.upper())
print("En minisculas:",frase.lower())
