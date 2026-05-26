# Busca Virus - Juego inspirado en Buscaminas
# Proyecto Final

import tkinter as tk
import random as r
import pygame

pygame.mixer.init()
pygame.mixer.music.load("audio.mpeg")
pygame.mixer.music.play(-1)

filas = 9
cols = 9
num_virus = 10

colores = {
    1: "blue",
    2: "green",
    3: "red",
    4: "navy"
}

def crear_tablero():
    tab = []
    for i in range(filas):
        fila = []
        for j in range(cols):
            fila.append(0)
        tab.append(fila)
    return tab

def poner_virus(tab):
    puestos = 0
    while puestos < num_virus:
        f = r.randint(0, filas-1)
        c = r.randint(0, cols-1)

        if tab[f][c] != -1:
            tab[f][c] = -1
            puestos += 1

def calcular(tab):
    for f in range(filas):
        for c in range(cols):

            if tab[f][c] == -1:
                continue

            cont = 0

            for df in [-1,0,1]:
                for dc in [-1,0,1]:

                    nf = f + df
                    nc = c + dc

                    if 0 <= nf < filas and 0 <= nc < cols:
                        if tab[nf][nc] == -1:
                            cont += 1

            tab[f][c] = cont

def pintar(f,c):

    btn = botones[f][c]

    if descubierto[f][c]:

        valor = tablero[f][c]

        if valor == -1:
            btn.config(text="X", bg="red")

        elif valor == 0:
            btn.config(text="", bg="lightgray")

        else:
            btn.config(
                text=str(valor),
                fg=colores.get(valor,"black"),
                bg="lightgray"
            )

    elif marcado[f][c]:
        btn.config(text="F")

    else:
        btn.config(text="")

def revelar(f,c):

    if descubierto[f][c]:
        return

    descubierto[f][c] = True
    pintar(f,c)

    if tablero[f][c] == 0:

        for df in [-1,0,1]:
            for dc in [-1,0,1]:

                nf = f + df
                nc = c + dc

                if 0 <= nf < filas and 0 <= nc < cols:
                    revelar(nf,nc)

def clic(f,c):

    global juego

    if not juego:
        return

    revelar(f,c)

    if tablero[f][c] == -1:
        juego = False
        estado.config(text="Perdiste")

def bandera(event,f,c):

    if descubierto[f][c]:
        return

    marcado[f][c] = not marcado[f][c]

    pintar(f,c)

def reiniciar():

    global tablero
    global descubierto
    global marcado
    global juego

    tablero = crear_tablero()

    poner_virus(tablero)
    calcular(tablero)

    descubierto = [[False]*cols for i in range(filas)]
    marcado = [[False]*cols for i in range(filas)]

    juego = True

    for f in range(filas):
        for c in range(cols):
            botones[f][c].config(
                text="",
                bg="SystemButtonFace"
            )

vent = tk.Tk()
vent.title("Busca Virus")

estado = tk.Label(vent,text="Juego iniciado")
estado.pack()

frm = tk.Frame(vent)
frm.pack()

botones = []

for f in range(filas):

    fila = []

    for c in range(cols):

        b = tk.Button(
            frm,
            width=3,
            command=lambda f=f,c=c: clic(f,c)
        )

        b.grid(row=f,column=c)

        b.bind("<Button-3>",
               lambda e,f=f,c=c: bandera(e,f,c))

        fila.append(b)

    botones.append(fila)

btn = tk.Button(
    vent,
    text="Reiniciar",
    command=reiniciar
)

btn.pack()

tablero = crear_tablero()
poner_virus(tablero)
calcular(tablero)

descubierto = [[False]*cols for i in range(filas)]
marcado = [[False]*cols for i in range(filas)]

juego = True

vent.mainloop()