import tkinter as tk 
def es_par(numero):
    return numero % 2 == 0 
def vereficar ():
    texto = entregada.get()
    if not texto-config(text="Escribe un numero entero")
    return
n = int(texto)
if es_par(n):
    resultado.config(text=str(n)+ "es par")
else:
    resultado.config(text=str(n)+ "es impar")
ventana = tK.Tk()
ventana.title("par o imprar")
ventana = tK.Entry(ventana)
entreda.pack()
tk.Button(ventana, text="verificar" , command=vereficar).pack(pady=8)
resultado =tk.Label(ventana, tex="")
resultado.pack()

vetana.mainloop()