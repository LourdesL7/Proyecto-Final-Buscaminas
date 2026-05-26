# Busca Virus - Juego inspirado en Buscaminas
# Autores: Kembeck López, Lourdes Lemus, Daniel Chou-Jo, María Chávez y Angel García.
# Asignación: Proyecto Final de Introducción a CC
# Fecha de entrega: 26/05/2026

import tkinter as tk
import random as r

# Reproducir audio
import pygame
pygame.mixer.init()                 
pygame.mixer.music.load("audio.mpeg")     
pygame.mixer.music.play(-1)          
pygame.mixer.music.set_volume(0.05)  

# Configuración
# Proporciones del tablero y cantidad de virus presentes.
filas    = 9    # cuántas filas tiene el tablero
cols     = 9    # cuántas columnas tiene el tablero
num_virus  = 10   # cuántos virus hay escondidos

# Colores para mostrar los números
colores = {
    1: "blue",
    2: "green3",
    3: "red",
    4: "navy",
    5: "maroon",
    6: "cyan4",
    7: "black",
    8: "gray50"
}

# Preparación del tablero
# Matriz para el tablero
# Cada celda guarda un número:
#   -1  → hay un virus
#    0  → no hay virus cerca
#    1-8 → virus vecinos

def crear_tablero():
    # Devuelve un tablero lleno de ceros (sin virus aún).
    tab = []
    for f in range(filas):
        fila = []
        for c in range(cols):
            fila.append(0)   # empieza vacío
        tab.append(fila) # ir añadiendo datos de cada fila para el tablero.
    return tab


def poner_virus(tab, pf, pc):
    # Coloca num_virus virus en posiciones aleatorias.
    # pf, pc = fila y columna del primer clic por el usuario (nunca se pone virus ahí).
    colocados = 0
    while colocados < num_virus:
        f = r.randint(0, filas - 1)
        c = r.randint(0, cols  - 1)
        # Solo colocar si la celda está vacía y no es la del primer clic
        if tab[f][c] != -1 and not (f == pf and c == pc):
            tab[f][c] = -1
            colocados += 1


def calcular_numeros(tab):
    # Recorre todo el tablero y, en cada celda sin virus cuenta cuántos virus hay en las 8 celdas vecinas.
    for f in range(filas):
        for c in range(cols):
            if tab[f][c] == -1:
                continue  # es virus, se salta
            cuenta = 0
            # df y dc van de -1 a 1, explorando los 8 espacios cercanos
            # Al ser por decirlo así, 3x3 casillas sin contar la central a explorar, hay que ir uno hacia atrás y adelante para ver cada celda o casilla.
            for df in [-1, 0, 1]:
                for dc in [-1, 0, 1]:
                    nf = f + df   # fila vecina
                    nc = c + dc   # columna vecina
                    # Verificar que el vecino esté dentro del tablero
                    if 0 <= nf  and nf < filas and 0 <= nc and nc < cols:
                        if tab[nf][nc] == -1:
                            cuenta += 1
            tab[f][c] = cuenta


# Funciones para mostrar el tablero
def pintar_boton(f, c):
    # Actualiza el texto y color visual de un botón.
    btn = botones[f][c]

    if descubierto[f][c]:
        val = tablero[f][c]
        if val == -1:
            # Hay un virus
            btn.config(text="🦠", bg="red", state="disabled", fg="black")
        elif val == 0:
            # Celda vacía
            btn.config(text="", bg="#cccccc", state="disabled")
        else:
            # Número de virus cercanos con su color
            btn.config(text=str(val), bg="#cccccc", state="disabled", fg = colores.get(val, "black"))

    elif marcado[f][c]:
        # Casilla marcada
        btn.config(text="🚩", bg="#ffe066", relief="raised")

    else:
        # Celda sin descubrir ni marcada.
        btn.config(text="", bg="#b0b0b0", relief="raised", state="normal", fg="black")


def mostrar_todos_virus():
    # Cuando el jugador pierde, muestra dónde estaban todos los virus
    for f in range(filas):
        for c in range(cols):
            if tablero[f][c] == -1:
                descubierto[f][c] = True
                pintar_boton(f, c)


# Lógica del juego
def revelar(f, c):
    # Descubre la celda (f, c).
    # Si tiene 0 virus alrededor, también descubre las casillas cercanas
    # Si ya está descubierta o marcada, no hacer nada
    if descubierto[f][c] or marcado[f][c]:
        return

    descubierto[f][c] = True
    pintar_boton(f, c)

    # Si la celda es 0, abrir automáticamente las vecinas
    if tablero[f][c] == 0:
        for df in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                nf = f + df
                nc = c + dc
                if 0 <= nf < filas and 0 <= nc < cols:
                    if not descubierto[nf][nc]:
                        revelar(nf, nc)   # llamada recursiva


def victoria():
    # Retorna True si el jugador ganó.
    # Gana cuando todas las celdas sin virus ya están descubiertas.
    for f in range(filas):
        for c in range(cols):
            if tablero[f][c] != -1 and not descubierto[f][c]:
                return False
    return True


# Eventos de clic
def clic_izq(f, c):
    # Se llama cuando el jugador hace clic izquierdo en (f, c).
    global juego_activo, primer_clic
    if not juego_activo:
        return                    # el juego terminó, ignorar clics
    if marcado[f][c]:
        return                    # celda marcada, no revelar
    if descubierto[f][c]:
        return                    # ya estaba descubierta

    # Generar tablero con primer clic.
    if primer_clic:
        poner_virus(tablero, f, c)
        calcular_numeros(tablero)
        primer_clic = False

    # Revelar la celda
    revelar(f, c)

    # Si se explota o toca un virus.
    if tablero[f][c] == -1:
        juego_activo = False
        mostrar_todos_virus()
        lbl_estado.config(text="'¡Te infectaste! Has perdido, renicia el juego.", fg="red")
        return
    if victoria():
        juego_activo = False
        lbl_estado.config(text="¡Ganaste! Eliminaste todos los virus.", fg="lime")


def clic_der(event, f, c):
    # Se llama con clic derecho para poner o quitar una bandera 🚩.
    # La bandera sirve para marcar celdas que el jugador cree que tienen un virus, sin revelarlas.
    global virus_restantes

    if not juego_activo:
        return
    if descubierto[f][c]:
        return   # no se puede marcar algo ya descubierto

    # Alternar la marca
    if marcado[f][c]:
        marcado[f][c] = False
        virus_restantes += 1      # devolvemos un "conteo"
    else:
        marcado[f][c] = True
        virus_restantes -= 1

    pintar_boton(f, c)
    lbl_virus.config(text=f"🦠 Virus restantes: {virus_restantes}")


# Reiniciar juego.
def reiniciar():
    # Resetea todas las variables y botones para una nueva partida.
    global tablero, descubierto, marcado, juego_activo, primer_clic, virus_restantes
    pygame.mixer.music.stop()
    pygame.mixer.music.play(-1)   # vuelve a sonar musiquita desde el principio
    tablero = crear_tablero()
    descubierto = [[False] * cols for _ in range(filas)]
    marcado = [[False] * cols for _ in range(filas)]
    juego_activo = True
    primer_clic = True
    virus_restantes = num_virus

    lbl_estado.config(text="¡Haz clic en una celda para empezar!", fg="white")
    lbl_virus.config(text=f"🦠 Virus restantes: {num_virus}")

    # Restaurar cada botón a su estado inicial
    for f in range(filas):
        for c in range(cols):
            botones[f][c].config(text="", bg="#b0b0b0", relief="raised", state="normal", fg="black")

# Construir ventana con Tkinter
# Ventana principal
vent = tk.Tk()
vent.title("🦠 Busca Virus")
vent.resizable(False, False) # Para que la ventanano alteresus dimensiones (punto investigado)
vent.configure(bg="#1e1e2e")   # fondo oscuro

# Título
tk.Label(vent, text="🦠  BUSCA VIRUS",
         font=("Arial", 18, "bold"),
         bg="#1e1e2e", fg="#a6e3a1").pack(pady=8)

# Barra superior: contador y botón reiniciar
frm_sup = tk.Frame(vent, bg="#1e1e2e")
frm_sup.pack(fill="x", padx=15)

lbl_virus = tk.Label(frm_sup, text=f"🦠 Virus restantes: {num_virus}", font=("Arial", 12), bg="#1e1e2e", fg="white")
lbl_virus.pack(side="left")

btn_reiniciar = tk.Button(frm_sup, text="🔄 Reiniciar", font=("Arial", 11, "bold"), bg="#45475a", fg="white", activebackground="#585b70", command=reiniciar)
btn_reiniciar.pack(side="right")

# Etiqueta de estado
lbl_estado = tk.Label(vent, text="¡Haz clic en una celda para empezar!", font=("Arial", 10), bg="#1e1e2e", fg="white")
lbl_estado.pack(pady=4)

# Marco que contiene el tablero
frm_tablero = tk.Frame(vent, bg="#1e1e2e")
frm_tablero.pack(padx=12, pady=6)

# Crear la cuadrícula de botones
# botones[f][c] guarda la referencia al botón de cada celda
botones = []
for f in range(filas):
    fila_btns = []
    for c in range(cols):
        # f=f y c=c capturan el valor actual (importante en lambdas dentro de bucles)
        btn = tk.Button(frm_tablero, width=3, height=1, bg="#b0b0b0", relief="raised", font=("Arial", 10, "bold"), command=lambda f=f, c=c: clic_izq(f, c)) # Envía la fila y columna del botón
        btn.grid(row=f, column=c, padx=1, pady=1)

        # Clic derecho → marcar con bandera
        btn.bind("<Button-3>", lambda e, f=f, c=c: clic_der(e, f, c)) # Fila y columna usando una función de un clic o botón con bind (evento)

        fila_btns.append(btn)
    botones.append(fila_btns)

# Instrucciones al pie
tk.Label(vent, text="Clic izquierdo: revelar celda  |  Clic derecho: poner/quitar bandera 🚩", font=("Arial", 8), bg="#1e1e2e", fg="#7f849c").pack(pady=5)

# Variables globales
# Se declaran después de la ventana.
tablero         = crear_tablero()           # matriz con valores
descubierto     = [[False]*cols for _ in range(filas)]  # ¿revelada?
marcado         = [[False]*cols for _ in range(filas)]  # ¿bandera?
juego_activo    = True
primer_clic     = True
virus_restantes = num_virus

# Se arranca con un bucle principal.
vent.mainloop()