import javax.swing.*;
import javax.swing.Timer;
import java.awt.*;
import java.awt.event.*;
import java.awt.geom.*;
import java.io.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.util.*;
import java.util.List;

public class Wordle extends JPanel {

    // ------------------------------------------------------------------
    // 1. CONFIGURACION
    // ------------------------------------------------------------------
    static final int LARGO = 5;
    static final int INTENTOS = 6;
    static final int TAM = 66;
    static final int SEP = 8;
    static final int ANCHO = 480;
    static final int ALTO = 770;

    static final Color FONDO = Color.WHITE;
    static final Color FICHA_VACIA = Color.WHITE;
    static final Color BORDE = new Color(0xD3D6DA);
    static final Color BORDE_ACTIVO = new Color(0x878A8C);
    static final Color TECLA = new Color(0xDDE3EA);
    static final Color TEXTO = new Color(0x1A1A1B);
    static final Color TEXTO_SUAVE = new Color(0x6B6E70);
    static final Color BLANCO = Color.WHITE;
    static final Color VERDE = new Color(0x43A047);
    static final Color AMARILLO = new Color(0xE5A823);
    static final Color GRIS = new Color(0x787C7E);

    enum Estado { AUSENTE, PRESENTE, CORRECTA }

    static final String[] FILAS_TECLADO = {"QWERTYUIOP", "ASDFGHJKL\u00D1", "ZXCVBNM"};
    static final String ALFABETO = "ABCDEFGHIJKLMN\u00D1OPQRSTUVWXYZ";

    static final String PALABRAS_TXT =
        "opalo palmo viaje viajo deuda tensa circo perro gatos playa fuego plata verde negro rojos nieve cielo nubes tigre bravo " +
        "canto canta mundo cosas tarde noche ahora nunca mismo otros antes medio joven " +
        "libro hojas papel mesas silla techo suelo calle pared carro avion barco coche " +
        "amigo amiga madre padre hijos primo novia novio gente campo monte lagos ondas " +
        "arena roble rosas plano grupo banco cable dulce sabor comer beber cenar pizza " +
        "pasta queso leche jugos salsa arroz carne pollo pesca fruta mango limon melon " +
        "uvas papas sopas torta feliz grave justo firme claro ruido sue\u00F1o ni\u00F1os clase " +
        "aulas notas texto datos redes nodos clave video radio salud dolor calor amado " +
        "honor valor juego jugar bailo lucha pelea reina reyes reino torre dados mapas " +
        "tesis curso nivel examen grado logro exito deseo ideas mente manos dedos labio " +
        "pecho cabra vacas ratas zorro lobos cerdo burro pulpo perla coral tango salto " +
        "abeja actor adios afuera aguja ajeno album altar apoyo arbol banda besos bruja " +
        "bulto cabos cerca china cobre due\u00F1o gafas globo golpe gritos huevo humor isla " +
        "lapiz lleno magia mente nariz ojala oveja pausa pilas plaza pluma quema rayos " +
        "razon ritmo rocas ropas rueda sabio sello sitio sobre tigre trato ulises valle " +
        "vasos vidas vuelo yegua zonas";

    static final Path ARCHIVO_STATS = Paths.get(System.getProperty("user.dir"), "wordle_stats.properties");
    static final Path ARCHIVO_VALIDAS = Paths.get(System.getProperty("user.dir"), "palabras_validas.txt");
    static final Rectangle BOTON = new Rectangle(150, 686, 180, 46);

    // ------------------------------------------------------------------
    // 2. LOGICA DEL JUEGO
    // ------------------------------------------------------------------
    static Estado[] evaluar(String intento, String secreta) {
        Estado[] resultado = new Estado[LARGO];
        Arrays.fill(resultado, Estado.AUSENTE);
        char[] disponibles = secreta.toCharArray();

        for (int i = 0; i < LARGO; i++) {
            if (intento.charAt(i) == secreta.charAt(i)) {
                resultado[i] = Estado.CORRECTA;
                disponibles[i] = 0;
            }
        }

        for (int i = 0; i < LARGO; i++) {
            if (resultado[i] == Estado.CORRECTA) continue;
            for (int j = 0; j < LARGO; j++) {
                if (disponibles[j] == intento.charAt(i)) {
                    resultado[i] = Estado.PRESENTE;
                    disponibles[j] = 0;
                    break;
                }
            }
        }
        return resultado;
    }

    static String normalizar(String s) {
        return s.toUpperCase()
                .replace('\u00C1', 'A').replace('\u00C9', 'E').replace('\u00CD', 'I')
                .replace('\u00D3', 'O').replace('\u00DA', 'U').replace('\u00DC', 'U');
    }

    static boolean esPalabraValida(String p) {
        if (p.length() != LARGO) return false;
        for (char c : p.toCharArray()) {
            if (ALFABETO.indexOf(c) < 0) return false;
        }
        return true;
    }

    static Color color(Estado e) {
        if (e == Estado.CORRECTA) return VERDE;
        if (e == Estado.PRESENTE) return AMARILLO;
        return GRIS;
    }

    static class Tecla {
        final String nombre;
        final Rectangle2D.Double r;
        Tecla(String nombre, double x, double y, double w, double h) {
            this.nombre = nombre;
            this.r = new Rectangle2D.Double(x, y, w, h);
        }
    }

    // ------------------------------------------------------------------
    // 3. INTERFAZ
    // ------------------------------------------------------------------
    final String[] lista;
    Set<String> validas = null;
    String secreta;
    int fila, col, idPartida;
    boolean bloqueado, terminado, panelFin, gano;
    String aviso = "";
    Timer avisoTimer;
    int filaSacudida = -1, sacudidaX = 0;
    int jugadas, ganadas, racha, mejor;

    final char[][] letras = new char[INTENTOS][LARGO];
    final Color[][] relleno = new Color[INTENTOS][LARGO];
    final Color[][] borde = new Color[INTENTOS][LARGO];
    final boolean[][] revelada = new boolean[INTENTOS][LARGO];
    final double[][] escalaX = new double[INTENTOS][LARGO];
    final double[][] escalaY = new double[INTENTOS][LARGO];
    final int[][] saltoY = new int[INTENTOS][LARGO];
    final Map<Character, Estado> colorTeclas = new HashMap<>();
    final List<Tecla> listaTeclas = new ArrayList<>();

    final Font fTitulo, fFicha, fTecla, fTexto, fAviso;

    public Wordle() {
        setPreferredSize(new Dimension(ANCHO, ALTO));
        setBackground(FONDO);
        setFocusable(true);

        String familia = elegirFuente();
        fTitulo = new Font(familia, Font.BOLD, 28);
        fFicha = new Font(familia, Font.BOLD, 26);
        fTecla = new Font(familia, Font.BOLD, 14);
        fTexto = new Font(familia, Font.PLAIN, 14);
        fAviso = new Font(familia, Font.BOLD, 15);

        TreeSet<String> set = new TreeSet<>();
        for (String p : PALABRAS_TXT.toUpperCase().trim().split("\\s+")) {
            if (esPalabraValida(p)) set.add(p);
        }
        lista = set.toArray(new String[0]);
        cargarValidas(set);
        cargarStats();
        crearTeclas();

        addKeyListener(new KeyAdapter() {
            @Override public void keyPressed(KeyEvent e) {
                if (e.getKeyCode() == KeyEvent.VK_ENTER) pulsar("ENTER");
                else if (e.getKeyCode() == KeyEvent.VK_BACK_SPACE) pulsar("BORRAR");
            }
            @Override public void keyTyped(KeyEvent e) {
                String s = normalizar(String.valueOf(e.getKeyChar()));
                if (s.length() == 1 && ALFABETO.indexOf(s.charAt(0)) >= 0) pulsar(s);
            }
        });

        addMouseListener(new MouseAdapter() {
            @Override public void mousePressed(MouseEvent e) {
                requestFocusInWindow();
                Point p = e.getPoint();
                if (panelFin) {
                    if (BOTON.contains(p)) nuevoJuego();
                    return;
                }
                for (Tecla t : listaTeclas) {
                    if (t.r.contains(p)) {
                        pulsar(t.nombre);
                        return;
                    }
                }
            }
        });

        nuevoJuego();
    }

    String elegirFuente() {
        Set<String> disponibles = new HashSet<>(Arrays.asList(
            GraphicsEnvironment.getLocalGraphicsEnvironment().getAvailableFontFamilyNames()));
        for (String f : new String[]{"Poppins", "Nunito", "Segoe UI", "Helvetica Neue", "Ubuntu", "DejaVu Sans", "Arial"}) {
            if (disponibles.contains(f)) return f;
        }
        return Font.SANS_SERIF;
    }

    void cargarValidas(Set<String> base) {
        if (!Files.exists(ARCHIVO_VALIDAS)) return;
        try {
            Set<String> extra = new HashSet<>(base);
            for (String linea : Files.readAllLines(ARCHIVO_VALIDAS, StandardCharsets.UTF_8)) {
                String p = normalizar(linea.trim());
                if (esPalabraValida(p)) extra.add(p);
            }
            validas = extra;
        } catch (IOException e) {
            validas = null;
        }
    }

    void crearTeclas() {
        double y = 572;
        for (int i = 0; i < FILAS_TECLADO.length; i++) {
            List<String> nombres = new ArrayList<>();
            if (i == 2) nombres.add("ENTER");
            for (char ch : FILAS_TECLADO[i].toCharArray()) nombres.add(String.valueOf(ch));
            if (i == 2) nombres.add("BORRAR");

            double total = 6.0 * (nombres.size() - 1);
            for (String n : nombres) total += anchoTecla(n);
            double x = (ANCHO - total) / 2;
            for (String n : nombres) {
                double w = anchoTecla(n);
                listaTeclas.add(new Tecla(n, x, y, w, 54));
                x += w + 6;
            }
            y += 60;
        }
    }

    double anchoTecla(String n) {
        return (n.equals("ENTER") || n.equals("BORRAR")) ? 64 : 40;
    }

    void nuevoJuego() {
        idPartida++;
        secreta = lista[new Random().nextInt(lista.length)];
        fila = 0;
        col = 0;
        bloqueado = false;
        terminado = false;
        panelFin = false;
        filaSacudida = -1;
        sacudidaX = 0;
        colorTeclas.clear();
        for (int f = 0; f < INTENTOS; f++) {
            for (int c = 0; c < LARGO; c++) {
                letras[f][c] = 0;
                relleno[f][c] = FICHA_VACIA;
                borde[f][c] = BORDE;
                revelada[f][c] = false;
                escalaX[f][c] = 1;
                escalaY[f][c] = 1;
                saltoY[f][c] = 0;
            }
        }
        mostrarAviso("", 0);
        repaint();
    }

    void despues(int ms, Runnable r) {
        final int mio = idPartida;
        Timer t = new Timer(ms, e -> {
            if (mio == idPartida) r.run();
        });
        t.setRepeats(false);
        t.start();
    }

    void pulsar(String valor) {
        if (terminado) {
            if (valor.equals("ENTER")) nuevoJuego();
            return;
        }
        if (bloqueado) return;
        if (valor.equals("ENTER")) enviar();
        else if (valor.equals("BORRAR")) borrar();
        else escribir(valor.charAt(0));
    }

    void escribir(char letra) {
        if (col >= LARGO) return;
        final int f = fila, c = col;
        letras[f][c] = letra;
        borde[f][c] = BORDE_ACTIVO;
        escalaX[f][c] = 1.1;
        escalaY[f][c] = 1.1;
        repaint();
        despues(80, () -> {
            escalaX[f][c] = 1;
            escalaY[f][c] = 1;
            repaint();
        });
        col++;
    }

    void borrar() {
        if (col == 0) return;
        col--;
        letras[fila][col] = 0;
        borde[fila][col] = BORDE;
        repaint();
    }

    void enviar() {
        if (col < LARGO) {
            sacudir("Faltan letras");
            return;
        }
        final String palabra = new String(letras[fila]);
        if (validas != null && !validas.contains(palabra)) {
            sacudir("Esa palabra no est\u00E1 en el diccionario");
            return;
        }
        final Estado[] estados = evaluar(palabra, secreta);
        final int f = fila;
        bloqueado = true;
        for (int c = 0; c < LARGO; c++) {
            final int cc = c;
            despues(c * 260, () -> voltear(f, cc, estados[cc], cc == LARGO - 1, palabra, estados, 0));
        }
    }

    void voltear(int f, int c, Estado estado, boolean ultima, String palabra, Estado[] estados, int i) {
        final int pasos = 8;
        if (i <= pasos) {
            if (i == pasos / 2) {
                relleno[f][c] = color(estado);
                borde[f][c] = color(estado);
                revelada[f][c] = true;
            }
            escalaY[f][c] = Math.max(Math.abs(1 - 2.0 * i / pasos), 0.04);
            repaint();
            despues(28, () -> voltear(f, c, estado, ultima, palabra, estados, i + 1));
        } else {
            escalaY[f][c] = 1;
            repaint();
            if (ultima) finRevelado(palabra, estados);
        }
    }

    void sacudir(String texto) {
        mostrarAviso(texto, 1800);
        bloqueado = true;
        filaSacudida = fila;
        sacudirPaso(new int[]{-8, 8, -6, 6, -3, 3, 0}, 0);
    }

    void sacudirPaso(int[] pos, int i) {
        if (i < pos.length) {
            sacudidaX = pos[i];
            repaint();
            despues(35, () -> sacudirPaso(pos, i + 1));
        } else {
            sacudidaX = 0;
            bloqueado = false;
            repaint();
        }
    }

    void rebotar(int f) {
        final int[] mov = {-12, -8, 8, 12};
        for (int c = 0; c < LARGO; c++) {
            final int cc = c;
            despues(c * 100, () -> saltoPaso(f, cc, mov, 0));
        }
    }

    void saltoPaso(int f, int c, int[] mov, int i) {
        if (i < mov.length) {
            saltoY[f][c] += mov[i];
            repaint();
            despues(60, () -> saltoPaso(f, c, mov, i + 1));
        }
    }

    void mostrarAviso(String texto, int ms) {
        aviso = texto;
        if (avisoTimer != null) avisoTimer.stop();
        if (!texto.isEmpty()) {
            avisoTimer = new Timer(ms, e -> {
                aviso = "";
                repaint();
            });
            avisoTimer.setRepeats(false);
            avisoTimer.start();
        }
        repaint();
    }

    void finRevelado(String palabra, Estado[] estados) {
        for (int i = 0; i < LARGO; i++) {
            char l = palabra.charAt(i);
            Estado anterior = colorTeclas.get(l);
            if (anterior == null || estados[i].ordinal() > anterior.ordinal()) {
                colorTeclas.put(l, estados[i]);
            }
        }
        repaint();

        if (palabra.equals(secreta)) {
            terminado = true;
            mostrarAviso("\u00A1Excelente!", 2500);
            rebotar(fila);
            registrar(true);
            despues(1000, () -> {
                gano = true;
                panelFin = true;
                repaint();
            });
        } else if (fila == INTENTOS - 1) {
            terminado = true;
            registrar(false);
            despues(500, () -> {
                gano = false;
                panelFin = true;
                repaint();
            });
        } else {
            fila++;
            col = 0;
            bloqueado = false;
        }
    }

    void cargarStats() {
        Properties p = new Properties();
        try (InputStream in = Files.newInputStream(ARCHIVO_STATS)) {
            p.load(in);
            jugadas = Integer.parseInt(p.getProperty("jugadas", "0"));
            ganadas = Integer.parseInt(p.getProperty("ganadas", "0"));
            racha = Integer.parseInt(p.getProperty("racha", "0"));
            mejor = Integer.parseInt(p.getProperty("mejor", "0"));
        } catch (Exception e) {
            jugadas = ganadas = racha = mejor = 0;
        }
    }

    void registrar(boolean victoria) {
        jugadas++;
        if (victoria) {
            ganadas++;
            racha++;
            mejor = Math.max(mejor, racha);
        } else {
            racha = 0;
        }
        Properties p = new Properties();
        p.setProperty("jugadas", String.valueOf(jugadas));
        p.setProperty("ganadas", String.valueOf(ganadas));
        p.setProperty("racha", String.valueOf(racha));
        p.setProperty("mejor", String.valueOf(mejor));
        try (OutputStream out = Files.newOutputStream(ARCHIVO_STATS)) {
            p.store(out, "Wordle");
        } catch (IOException e) {
        }
    }

    // ------------------------------------------------------------------
    // DIBUJO
    // ------------------------------------------------------------------
    static final int IZQ = 1, CENTRO = 0, DER = 2;

    void texto(Graphics2D g, String s, double x, double cy, Font f, Color c, int alin) {
        g.setFont(f);
        g.setColor(c);
        FontMetrics fm = g.getFontMetrics();
        double w = fm.stringWidth(s);
        double px = (alin == CENTRO) ? x - w / 2 : (alin == IZQ ? x : x - w);
        double py = cy + (fm.getAscent() - fm.getDescent()) / 2.0;
        g.drawString(s, (float) px, (float) py);
    }

    @Override
    protected void paintComponent(Graphics g0) {
        super.paintComponent(g0);
        Graphics2D g = (Graphics2D) g0.create();
        g.setRenderingHint(RenderingHints.KEY_ANTIALIASING, RenderingHints.VALUE_ANTIALIAS_ON);
        g.setRenderingHint(RenderingHints.KEY_TEXT_ANTIALIASING, RenderingHints.VALUE_TEXT_ANTIALIAS_ON);

        texto(g, "Wordle", 24, 36, fTitulo, TEXTO, IZQ);
        texto(g, "Racha: " + racha, ANCHO - 24, 36, fTexto, TEXTO_SUAVE, DER);
        texto(g, aviso, ANCHO / 2.0, 78, fAviso, TEXTO, CENTRO);

        dibujarTablero(g);
        dibujarTeclado(g);
        if (panelFin) dibujarFin(g);
        g.dispose();
    }

    void dibujarTablero(Graphics2D g) {
        double anchoTotal = LARGO * TAM + (LARGO - 1) * SEP;
        double x0 = (ANCHO - anchoTotal) / 2.0 + TAM / 2.0;
        double y0 = 118 + TAM / 2.0;
        for (int f = 0; f < INTENTOS; f++) {
            for (int c = 0; c < LARGO; c++) {
                double cx = x0 + c * (TAM + SEP) + (f == filaSacudida ? sacudidaX : 0);
                double cy = y0 + f * (TAM + SEP) + saltoY[f][c];
                double hx = TAM / 2.0 * escalaX[f][c];
                double hy = TAM / 2.0 * escalaY[f][c];
                double arco = Math.min(20, Math.min(hx, hy) * 2);
                Shape s = new RoundRectangle2D.Double(cx - hx, cy - hy, hx * 2, hy * 2, arco, arco);
                g.setColor(relleno[f][c]);
                g.fill(s);
                g.setColor(borde[f][c]);
                g.setStroke(new BasicStroke(2f));
                g.draw(s);
                if (escalaY[f][c] > 0.4 && letras[f][c] != 0) {
                    texto(g, String.valueOf(letras[f][c]), cx, cy, fFicha,
                          revelada[f][c] ? BLANCO : TEXTO, CENTRO);
                }
            }
        }
    }

    void dibujarTeclado(Graphics2D g) {
        for (Tecla t : listaTeclas) {
            Estado e = t.nombre.length() == 1 ? colorTeclas.get(t.nombre.charAt(0)) : null;
            g.setColor(e == null ? TECLA : color(e));
            g.fill(new RoundRectangle2D.Double(t.r.x, t.r.y, t.r.width, t.r.height, 16, 16));
            double cx = t.r.getCenterX(), cy = t.r.getCenterY();

            if (t.nombre.equals("ENTER")) {
                Path2D check = new Path2D.Double();
                check.moveTo(cx - 8, cy + 1);
                check.lineTo(cx - 3, cy + 6);
                check.lineTo(cx + 8, cy - 6);
                g.setColor(TEXTO);
                g.setStroke(new BasicStroke(3f, BasicStroke.CAP_ROUND, BasicStroke.JOIN_ROUND));
                g.draw(check);
            } else if (t.nombre.equals("BORRAR")) {
                Path2D caja = new Path2D.Double();
                caja.moveTo(cx - 13, cy);
                caja.lineTo(cx - 5, cy - 8);
                caja.lineTo(cx + 12, cy - 8);
                caja.lineTo(cx + 12, cy + 8);
                caja.lineTo(cx - 5, cy + 8);
                caja.closePath();
                g.setColor(TEXTO);
                g.setStroke(new BasicStroke(2f, BasicStroke.CAP_ROUND, BasicStroke.JOIN_ROUND));
                g.draw(caja);
                g.draw(new Line2D.Double(cx, cy - 3, cx + 6, cy + 3));
                g.draw(new Line2D.Double(cx + 6, cy - 3, cx, cy + 3));
            } else {
                texto(g, t.nombre, cx, cy, fTecla, e == null ? TEXTO : BLANCO, CENTRO);
            }
        }
    }

    void dibujarFin(Graphics2D g) {
        g.setColor(FONDO);
        g.fillRect(0, 556, ANCHO, ALTO - 556);
        String titulo = gano ? "\u00A1Lo lograste!" : "Casi lo tienes";
        String sub = gano ? "Acertaste en " + (fila + 1) + " de " + INTENTOS + " intentos"
                          : "La palabra era " + secreta;
        long pct = jugadas > 0 ? Math.round(100.0 * ganadas / jugadas) : 0;
        texto(g, titulo, ANCHO / 2.0, 592, fTitulo, gano ? VERDE : TEXTO, CENTRO);
        texto(g, sub, ANCHO / 2.0, 632, fTexto, TEXTO, CENTRO);
        texto(g, "Jugadas " + jugadas + "    Victorias " + pct + "%    Racha " + racha + "    Mejor " + mejor,
              ANCHO / 2.0, 660, fTexto, TEXTO_SUAVE, CENTRO);
        g.setColor(VERDE);
        g.fill(new RoundRectangle2D.Double(BOTON.x, BOTON.y, BOTON.width, BOTON.height, 24, 24));
        texto(g, "Jugar de nuevo", ANCHO / 2.0, 709, fAviso, BLANCO, CENTRO);
    }

    public static void main(String[] args) {
        SwingUtilities.invokeLater(() -> {
            JFrame ventana = new JFrame("Wordle en espa\u00F1ol");
            ventana.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
            Wordle juego = new Wordle();
            ventana.add(juego);
            ventana.setResizable(false);
            ventana.pack();
            ventana.setLocationRelativeTo(null);
            ventana.setVisible(true);
            juego.requestFocusInWindow();
        });
    }
}