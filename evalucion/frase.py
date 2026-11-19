def pedir_frase():
    while True:
        frase = input("Ingrese una palabra: ")
        print("Recibí:", repr(frase))
        if frase.strip() != "":
            return frase
frase = pedir_frase()
palabras = frase.split()
mas_larga = palabras[0]
for palabra in palabras:
    if len(palabra) > len(mas_larga):
        mas_larga = palabra
conteo = {}
for letra in frase.lower():
    if letra != " ":
        if letra in conteo:
            conteo[letra] += 1
        else:
            conteo[letra] = 1
print(f"{len(palabras)} palabras")
print(f"Más larga: {mas_larga}")
for letra, cantidad in conteo.items():
    print(f"{letra}:{cantidad}", end=" ")
print()