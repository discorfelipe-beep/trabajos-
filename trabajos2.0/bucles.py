import random
numero = random.randint(1,10)
usuario = int(input("dame un numero"))

contador = 0 
intentos = 0 

while numero != usuario and intentos < 5:
    
     
     if usuario<numero:
        print("es mayor")
        usuario = int(input("dame un numero"))
        contador += 1
        intentos += 1 
     else:
        print(" es menor")
        usuario = int(input("dame un numero"))
        contador += 1
        intentos += 1
        asistencias +=1

if intentos < 5 and usuario == numero:
    print("correcto")
    print (f"usaste {contador} intentos")
else: 
    print("perdiste, el numero era:",numero)
