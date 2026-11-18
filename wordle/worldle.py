import json
import os
import random
import tkinter as tk
import tkinter.font as tkfont

# 1. CONFIGURACIÓN

LARGO = 5
INTENTOS = 6
TAM = 66
SEP = 8
ANCHO, ALTO = 480, 770

FONDO = "#FFFFFF"
FICHA_VACIA = "#FFFFFF"
BORDE = "#D3D6DA"
BORDE_ACTIVO = "#878A8C"
TECLA = "#DDE3EA"
TEXTO = "#1A1A1B"
TEXTO_SUAVE = "#6B6E70"
BLANCO = "#FFFFFF"
ACENTO = "#43A047"
COLORES = {
    "correcta": "#43A047",
    "presente": "#E5A823",
    "ausente": "#787C7E",
}
PRIORIDAD = {"ausente": 1, "presente": 2, "correcta": 3}

FILAS_TECLADO = ["QWERTYUIOP", "ASDFGHJKLÑ", "ZXCVBNM"]
ALFABETO = set("ABCDEFGHIJKLMNÑOPQRSTUVWXYZ")
ACENTOS = str.maketrans("ÁÉÍÓÚÜ", "AEIOUU")

PALABRAS = """
opalo palmo viaje viajo deuda tensa circo perro gatos playa fuego plata verde negro rojos nieve cielo nubes tigre bravo
canto canta mundo cosas tarde noche ahora nunca mismo otros antes medio joven
libro hojas papel mesas silla techo suelo calle pared carro avion barco coche
amigo amiga madre padre hijos primo novia novio gente campo monte lagos ondas
arena roble rosas plano grupo banco cable dulce sabor comer beber cenar pizza
pasta queso leche jugos salsa arroz carne pollo pesca fruta mango limon melon
uvas papas sopas torta feliz grave justo firme claro ruido sueño niños clase
aulas notas texto datos redes nodos clave video radio salud dolor calor amado
honor valor juego jugar bailo lucha pelea reina reyes reino torre dados mapas
tesis curso nivel examen grado logro exito deseo ideas mente manos dedos labio
pecho cabra vacas ratas zorro lobos cerdo burro pulpo perla coral tango salto
abeja actor adios afuera aguja ajeno album altar apoyo arbol banda besos bruja
bulto cabos cerca china cobre dueño gafas globo golpe gritos huevo humor isla
lapiz lleno magia mente nariz ojalá oveja pausa pilas plaza pluma quema rayos
razon ritmo rocas ropas rueda sabio sello sitio sobre tigre trato ulises valle
vasos vidas vuelo yegua zonas
""".upper().split()
PALABRAS = sorted({p for p in PALABRAS if len(p) == LARGO and set(p) <= ALFABETO})

RUTA = os.path.dirname(os.path.abspath(__file__))
ARCHIVO_STATS = os.path.join(RUTA, "wordle_stats.json")
ARCHIVO_VALIDAS = os.path.join(RUTA, "palabras_validas.txt")

# 2. LÓGICA DEL JUEGO

def evaluar(intento, secreta):
    resultado = ["ausente"] * LARGO
    disponibles = list(secreta)

    for i in range(LARGO):
        if intento[i] == secreta[i]:
            resultado[i] = "correcta"
            disponibles[i] = None

    for i in range(LARGO):
        if resultado[i] == "correcta":
            continue
        if intento[i] in disponibles:
            resultado[i] = "presente"
            disponibles[disponibles.index(intento[i])] = None

    return resultado


def cargar_validas():
    if not os.path.exists(ARCHIVO_VALIDAS):
        return None
    with open(ARCHIVO_VALIDAS, encoding="utf-8") as f:
        extra = {l.strip().upper().translate(ACENTOS) for l in f}
    return {p for p in extra if len(p) == LARGO} | set(PALABRAS)


def puntos_redondeados(x1, y1, x2, y2, r):
    return [x1 + r, y1, x2 - r, y1, x2, y1, x2, y1 + r, x2, y2 - r, x2, y2,
            x2 - r, y2, x1 + r, y2, x1, y2, x1, y2 - r, x1, y1 + r, x1, y1]

# 3. INTERFAZ

class Wordle:
    def __init__(self, root):
        self.root = root
        root.title("Wordle en español")
        root.resizable(False, False)

        self.canvas = tk.Canvas(root, width=ANCHO, height=ALTO, bg=FONDO,
                                highlightthickness=0)
        self.canvas.pack()

        familia = self.elegir_fuente()
        self.f_titulo = tkfont.Font(family=familia, size=28, weight="bold")
        self.f_ficha = tkfont.Font(family=familia, size=26, weight="bold")
        self.f_tecla = tkfont.Font(family=familia, size=12, weight="bold")
        self.f_texto = tkfont.Font(family=familia, size=12)
        self.f_aviso = tkfont.Font(family=familia, size=13, weight="bold")

        self.validas = cargar_validas()
        self.stats = self.cargar_stats()
        self.id_aviso = None

        self.dibujar_cabecera()
        self.dibujar_tablero()
        self.dibujar_teclado()

        root.bind("<Key>", self.on_key)
        self.nuevo_juego()

    def elegir_fuente(self):
        disponibles = set(tkfont.families(self.root))
        for f in ("Poppins", "Nunito", "Segoe UI", "Helvetica Neue",
                  "Ubuntu", "DejaVu Sans", "Arial"):
            if f in disponibles:
                return f
        return "TkDefaultFont"

    def dibujar_cabecera(self):
        c = self.canvas
        c.create_text(24, 36, text="Wordle", anchor="w",
                      font=self.f_titulo, fill=TEXTO)
        self.id_racha = c.create_text(ANCHO - 24, 36, anchor="e",
                                      font=self.f_texto, fill=TEXTO_SUAVE)
        self.id_aviso = c.create_text(ANCHO / 2, 78, text="",
                                      font=self.f_aviso, fill=TEXTO)

    def dibujar_tablero(self):
        ancho_total = LARGO * TAM + (LARGO - 1) * SEP
        x0 = (ANCHO - ancho_total) / 2 + TAM / 2
        y0 = 118 + TAM / 2
        self.fichas = []
        for f in range(INTENTOS):
            fila = []
            for col in range(LARGO):
                cx = x0 + col * (TAM + SEP)
                cy = y0 + f * (TAM + SEP)
                poly = self.canvas.create_polygon(
                    puntos_redondeados(cx - TAM / 2, cy - TAM / 2,
                                       cx + TAM / 2, cy + TAM / 2, 10),
                    smooth=True, fill=FICHA_VACIA, outline=BORDE, width=2,
                    tags=(f"fila{f}",))
                txt = self.canvas.create_text(cx, cy, text="", fill=TEXTO,
                                              font=self.f_ficha,
                                              tags=(f"fila{f}",))
                fila.append({"poly": poly, "txt": txt, "x": cx, "y": cy,
                             "fill": FICHA_VACIA, "outline": BORDE})
            self.fichas.append(fila)

    def dibujar_teclado(self):
        self.teclas = {}
        y = 572
        for i, letras in enumerate(FILAS_TECLADO):
            nombres = list(letras)
            if i == 2:
                nombres = ["ENTER"] + nombres + ["BORRAR"]
            anchos = [64 if n in ("ENTER", "BORRAR") else 40 for n in nombres]
            total = sum(anchos) + 6 * (len(nombres) - 1)
            x = (ANCHO - total) / 2
            for nombre, w in zip(nombres, anchos):
                tag = f"tecla_{nombre}"
                poly = self.canvas.create_polygon(
                    puntos_redondeados(x, y, x + w, y + 54, 8), smooth=True,
                    fill=TECLA, outline="", tags=(tag,))
                etiqueta = {"ENTER": "✓", "BORRAR": "⌫"}.get(nombre, nombre)
                txt = self.canvas.create_text(x + w / 2, y + 27, text=etiqueta,
                                              fill=TEXTO, font=self.f_tecla,
                                              tags=(tag,))
                self.canvas.tag_bind(tag, "<Button-1>",
                                     lambda e, n=nombre: self.pulsar(n))
                self.teclas[nombre] = {"poly": poly, "txt": txt, "estado": None}
                x += w + 6
            y += 60

    def pintar(self, fila, col, ex=1.0, ey=1.0):
        f = self.fichas[fila][col]
        hx, hy = TAM / 2 * ex, TAM / 2 * ey
        r = min(10, hx, hy)
        self.canvas.coords(f["poly"], *puntos_redondeados(
            f["x"] - hx, f["y"] - hy, f["x"] + hx, f["y"] + hy, r))
        self.canvas.itemconfigure(f["poly"], fill=f["fill"], outline=f["outline"])
        self.canvas.itemconfigure(f["txt"],
                                  state="normal" if ey > 0.4 else "hidden")

    def nuevo_juego(self):
        self.canvas.delete("fin")
        self.secreta = random.choice(PALABRAS)
        self.fila = 0
        self.col = 0
        self.letras = []
        self.bloqueado = False
        self.terminado = False

        for f in range(INTENTOS):
            for c in range(LARGO):
                ficha = self.fichas[f][c]
                ficha.update(fill=FICHA_VACIA, outline=BORDE)
                self.canvas.itemconfigure(ficha["txt"], text="", fill=TEXTO)
                self.pintar(f, c)
        for t in self.teclas.values():
            t["estado"] = None
            self.canvas.itemconfigure(t["poly"], fill=TECLA)
            self.canvas.itemconfigure(t["txt"], fill=TEXTO)
        self.mensaje("")
        self.actualizar_racha()

    def on_key(self, e):
        if e.keysym == "Return":
            self.pulsar("ENTER")
        elif e.keysym == "BackSpace":
            self.pulsar("BORRAR")
        elif e.char:
            ch = e.char.upper().translate(ACENTOS)
            if len(ch) == 1 and ch in ALFABETO:
                self.pulsar(ch)

    def pulsar(self, valor):
        if self.terminado:
            if valor == "ENTER":
                self.nuevo_juego()
            return
        if self.bloqueado:
            return
        if valor == "ENTER":
            self.enviar()
        elif valor == "BORRAR":
            self.borrar()
        else:
            self.escribir(valor)

    def escribir(self, letra):
        if self.col >= LARGO:
            return
        f = self.fichas[self.fila][self.col]
        self.canvas.itemconfigure(f["txt"], text=letra)
        f["outline"] = BORDE_ACTIVO
        self.letras.append(letra)
        fila, col = self.fila, self.col
        self.pintar(fila, col, 1.1, 1.1)
        self.root.after(80, lambda: self.pintar(fila, col))
        self.col += 1

    def borrar(self):
        if self.col == 0:
            return
        self.col -= 1
        self.letras.pop()
        f = self.fichas[self.fila][self.col]
        f["outline"] = BORDE
        self.canvas.itemconfigure(f["txt"], text="")
        self.pintar(self.fila, self.col)

    def enviar(self):
        if self.col < LARGO:
            self.sacudir("Faltan letras")
            return
        palabra = "".join(self.letras)
        if self.validas is not None and palabra not in self.validas:
            self.sacudir("Esa palabra no está en el diccionario")
            return

        estados = evaluar(palabra, self.secreta)
        self.bloqueado = True
        for c in range(LARGO):
            self.root.after(c * 260, lambda c=c: self.voltear(
                self.fila, c, estados[c], c == LARGO - 1, palabra, estados))

    def voltear(self, fila, col, estado, ultima, palabra, estados):
        f = self.fichas[fila][col]
        pasos = 8

        def paso(i):
            if i <= pasos:
                if i == pasos // 2:
                    f["fill"] = COLORES[estado]
                    f["outline"] = COLORES[estado]
                    self.canvas.itemconfigure(f["txt"], fill=BLANCO)
                self.pintar(fila, col, ey=max(abs(1 - 2 * i / pasos), 0.04))
                self.root.after(28, lambda: paso(i + 1))
            elif ultima:
                self.fin_revelado(palabra, estados)

        paso(0)

    def sacudir(self, texto):
        self.mensaje(texto)
        self.bloqueado = True
        etiqueta = f"fila{self.fila}"
        posiciones = [-8, 8, -6, 6, -3, 3, 0]

        def paso(i, previa):
            if i < len(posiciones):
                self.canvas.move(etiqueta, posiciones[i] - previa, 0)
                self.root.after(35, lambda: paso(i + 1, posiciones[i]))
            else:
                self.bloqueado = False

        paso(0, 0)

    def rebotar(self, fila):
        movimientos = [-12, -8, 8, 12]
        for col in range(LARGO):
            f = self.fichas[fila][col]

            def salto(i, f=f):
                if i < len(movimientos):
                    self.canvas.move(f["poly"], 0, movimientos[i])
                    self.canvas.move(f["txt"], 0, movimientos[i])
                    self.root.after(60, lambda: salto(i + 1, f))

            self.root.after(col * 100, salto, 0)

    def mensaje(self, texto, ms=1800):
        self.canvas.itemconfigure(self.id_aviso, text=texto)
        if hasattr(self, "_t_aviso"):
            self.root.after_cancel(self._t_aviso)
        if texto:
            self._t_aviso = self.root.after(
                ms, lambda: self.canvas.itemconfigure(self.id_aviso, text=""))

    def fin_revelado(self, palabra, estados):
        for letra, estado in zip(palabra, estados):
            t = self.teclas[letra]
            if t["estado"] is None or PRIORIDAD[estado] > PRIORIDAD[t["estado"]]:
                t["estado"] = estado
                self.canvas.itemconfigure(t["poly"], fill=COLORES[estado])
                self.canvas.itemconfigure(t["txt"], fill=BLANCO)

        if palabra == self.secreta:
            self.terminado = True
            self.mensaje("¡Excelente!", 2500)
            self.rebotar(self.fila)
            self.registrar(True)
            self.root.after(1000, lambda: self.mostrar_fin(True))
        elif self.fila == INTENTOS - 1:
            self.terminado = True
            self.registrar(False)
            self.root.after(500, lambda: self.mostrar_fin(False))
        else:
            self.fila += 1
            self.col = 0
            self.letras = []
            self.bloqueado = False

    def mostrar_fin(self, gano):
        c = self.canvas
        c.delete("fin")
        c.create_rectangle(0, 556, ANCHO, ALTO, fill=FONDO, outline="", tags="fin")
        titulo = "¡Lo lograste!" if gano else "Casi lo tienes"
        sub = (f"Acertaste en {self.fila + 1} de {INTENTOS} intentos" if gano
               else f"La palabra era {self.secreta}")
        s = self.stats
        pct = round(100 * s["ganadas"] / s["jugadas"]) if s["jugadas"] else 0
        c.create_text(ANCHO / 2, 592, text=titulo, font=self.f_titulo,
                      fill=ACENTO if gano else TEXTO, tags="fin")
        c.create_text(ANCHO / 2, 632, text=sub, font=self.f_texto,
                      fill=TEXTO, tags="fin")
        c.create_text(ANCHO / 2, 660, font=self.f_texto, fill=TEXTO_SUAVE,
                      text=f"Jugadas {s['jugadas']}    Victorias {pct}%    "
                           f"Racha {s['racha']}    Mejor {s['mejor']}",
                      tags="fin")
        c.create_polygon(puntos_redondeados(150, 686, 330, 732, 12), smooth=True,
                         fill=COLORES["correcta"], outline="",
                         tags=("fin", "boton"))
        c.create_text(ANCHO / 2, 709, text="Jugar de nuevo", font=self.f_aviso,
                      fill=BLANCO, tags=("fin", "boton"))
        c.tag_bind("boton", "<Button-1>", lambda e: self.nuevo_juego())

    def cargar_stats(self):
        base = {"jugadas": 0, "ganadas": 0, "racha": 0, "mejor": 0}
        try:
            with open(ARCHIVO_STATS, encoding="utf-8") as f:
                base.update(json.load(f))
        except (OSError, ValueError):
            pass
        return base

    def registrar(self, gano):
        s = self.stats
        s["jugadas"] += 1
        if gano:
            s["ganadas"] += 1
            s["racha"] += 1
            s["mejor"] = max(s["mejor"], s["racha"])
        else:
            s["racha"] = 0
        try:
            with open(ARCHIVO_STATS, "w", encoding="utf-8") as f:
                json.dump(s, f)
        except OSError:
            pass
        self.actualizar_racha()

    def actualizar_racha(self):
        self.canvas.itemconfigure(self.id_racha,
                                  text=f"Racha: {self.stats['racha']}")


if __name__ == "__main__":
    ventana = tk.Tk()
    Wordle(ventana)
    ventana.mainloop()