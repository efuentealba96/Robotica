import pygame as pyg
import sys

aMAPA = [
    [1, 1, 1, 1, 1, -1, 1, 1],
    [1, -1, -1, -1, 1, -1, 1, 1],
    [1, -1, 1, -1, 1, 1, 1, 1],
    [1, -1, 1, 1, 1, -1, -1, -1],
    [1, 1, 1, 1, 1, 1, 1, 1],
    [-1, -1, -1, 1, -1, -1, -1, 1],
    [1, 1, 1, 1, 1, 1, -1, 1],
    [1, -1, -1, 1, -1, 1, -1, 1],
    [1, 1, -1, 1, -1, 1, 1, 1],
    [-1, 1, -1, 1, -1, 1, -1, 1],
    [-1, 1, -1, 1, 1, 1, -1, -1],
    [1, 1, -1, 1, -1, 1, 1, 1],

]

pyg.init()
size = width, height = 400, 600
screen = pyg.display.set_mode(size)
pyg.display.set_caption("Proyecto final")
icon = pyg.image.load("images/terminator.png")
pyg.display.set_icon(icon)

sizeImage = (50, 50)

muro = pyg.transform.scale(pyg.image.load("images/muro.png"), sizeImage)
nave = pyg.transform.scale(pyg.image.load("images/nave.png"), (40, 40))
star = pyg.transform.scale(pyg.image.load("images/star.png"), sizeImage)
fondo = pyg.transform.scale(pyg.image.load("images/fondo.jpg"), sizeImage)

x = 0
y = 0
screen.blit(nave, (0, 0))
for i in range(12):
    for j in range(8):
        if aMAPA[i][j] == -1:
            screen.blit(muro, (x, y))
            x += 50
        else:
            screen.blit(fondo, (x, y))
            x += 50
    screen.blit(star, (200, 50*10))
    x = 0
    y += 50
screen.blit(nave, (12, 12))
while True:
    pyg.display.update()
    pyg.time.delay(500)
    for event in pyg.event.get():
        if event.type == pyg.QUIT:
            sys.exit()
