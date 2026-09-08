renta = float (input("ingrese su renta: "))
if renta < 10000:
    resultado = renta + (renta * 0.05)
    print("tu renta es del 5% y en total es",resultado)
elif renta >=10000 and renta < 20000:
    resultado = renta + (renta * 0.15)
    print("tu renta es del 15% y en total es",resultado)
elif renta >=20000 and renta < 35000:
    resultado = renta + (renta * 0.20)
    print("tu renta es del 20% y en total es",resultado)
else:
    renta >= 35000
    resultado = renta + (renta * 0.30)
    print("tu renta es del 30% y en total es",resultado)

