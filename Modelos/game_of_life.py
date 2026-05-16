import time
import sys
import pygame
import numpy as np

pygame.init()

width, height = 800, 800
ventana = pygame.display.set_mode((width, height))

pygame.display.set_caption("Game of Life (Conway)")

#Casi negro
bg = 0,0,0
ventana.fill(bg)

#Cantidad de celdas
cX, cY = 40, 40

dimW = width // cX
dimH = height // cY

#Estado del las celdas (Vivas = 1, Muertas = 0)
estadoJuego = np.zeros((cX, cY))


pause = False


estadoJuego[21,21] = 1
estadoJuego[22,21] = 1
estadoJuego[22,22] = 1
estadoJuego[22,23] = 1
estadoJuego[21,20] = 1
estadoJuego[21,23] = 1
estadoJuego[20,21] = 1


#Bucle principal del juego
while True:

    copy_estadoJuego = np.copy(estadoJuego)

    ventana.fill(bg)
    time.sleep(0.1)

    ev = pygame.event.get()

    for evento in ev:
        if evento.type == pygame.KEYDOWN:
            pause = not pause
        elif evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        click = pygame.mouse.get_pressed()

        if sum(click) > 0:
            posX, posY = pygame.mouse.get_pos()
            celX, celY = int(np.floor(posX/dimW)), int(np.floor(posY/dimH))
            copy_estadoJuego[celX, celY] = not click[2]


    for y in range(0,cX):
        for x in range(0, cY):

            if not pause:

                #Vecinos
                vec =   estadoJuego[(x-1)   %cX, (y-1)  %cY] + \
                        estadoJuego[(x)     %cX, (y-1)  %cY] + \
                        estadoJuego[(x+1)   %cX, (y-1)  %cY] + \
                        estadoJuego[(x-1)   %cX, (y)    %cY] + \
                        estadoJuego[(x+1)   %cX, (y)    %cY] + \
                        estadoJuego[(x-1)   %cX, (y+1)  %cY] + \
                        estadoJuego[(x)     %cX, (y+1)  %cY] + \
                        estadoJuego[(x+1)   %cX, (y+1)  %cY] 

                #Regla 1: Celula muerta con 3 vecinas vivas REVIVE
                if estadoJuego[x,y] == 0 and vec == 3:
                    copy_estadoJuego[x,y] = 1

                #Regla 2: Celula viva con menos de 2 o mas de 3 vecinas vivas MUERE
                elif estadoJuego[x,y] == 1 and (vec < 2 or vec > 3):
                    copy_estadoJuego[x,y] = 0

            poly = [((x)    *dimW, y    *dimH),
                    ((x+1)  *dimW, y    *dimH),
                    ((x+1)  *dimW, (y+1)*dimW),
                    ((x)    *dimW, (y+1)*dimW)]
            
            if copy_estadoJuego[x,y] == 0:
                pygame.draw.polygon(ventana,(128,128,128), poly, 1)
            else:
                pygame.draw.polygon(ventana,(255,255,255), poly, 0)

    estadoJuego = np.copy(copy_estadoJuego)

    pygame.display.flip()