from funciones import *
from sprites import *
import pygame
import sys
import random
import os

ANCHO_VENTANA = 640
ALTO_VENTANA = 480
NOMBRE_DISPLAY = "K*bert"
FPS = 60

def main():
    pygame.init()

    pause = False

    #variables efectos
    fxDelay = 1
    fxPlay = True
    fxSpeed = 20
    fxColor = 0,0,0
    fxAlto = 0
    fxAncho = ANCHO_VENTANA

    ventana = pygame.display.set_mode((ANCHO_VENTANA,ALTO_VENTANA))
    pygame.display.set_caption(NOMBRE_DISPLAY)
    ventana.fill((147,90,71))
    
    numObstaculos = 3
    mainGrid = cuadricula(10,10)
    mainGrid = obstaculos(numObstaculos,mainGrid)
    printGrid(mainGrid)
    while (mainGrid[0][1] == 1) and (mainGrid[1][0] == 1):
        mainGrid = cuadricula(10,10)
        print("Jugador atrapadooooo, nooo aaa")
        mainGrid = obstaculos(numObstaculos,mainGrid)
        printGrid(mainGrid)
    mainGrid[0][0] = 2
    pintado = 1 #cantidad de cuadrados pintados


    #calcular cantidad de espacios por los que te puedes mover
    totalEspacios = len(mainGrid)*len(mainGrid[0])
    espaciosOcupados = 0
    for i in range(numObstaculos):
        espaciosOcupados += (i+1)

    espaciosLibres = totalEspacios - espaciosOcupados
    print("total espacios:",espaciosLibres)

 
    #sprites
    #sprImagen = pygame.image.load(open(os.path.join(sys.path[0], "sprites\imagen.png"), "r"))
    sprEspacio      = imgLoad("sprites\espacio.png")
    sprPintado      = imgLoad("sprites\pintado.png")
    sprObstaculo    = imgLoad("sprites\obstaculo.png")
    sprPlayerLeft   = imgLoad("sprites\playerLeft.png")
    sprPlayerRight  = imgLoad("sprites\playerRight.png")
    sprEnemy1       = imgLoad("sprites\enemy1.png")
    sprEnemy2       = imgLoad("sprites\enemy2.png")
    sprVidaLlena    = imgLoad("sprites\_vidaLLena.png")
    sprVidaVacia    = imgLoad("sprites\_vidaVacia.png")
    sprPause        = imgLoad("sprites\pause.png")
    sprPauseText    = imgLoad("sprites\pauseText.png")

    playerDraw = sprPlayerLeft

    reloj = pygame.time.Clock()

    font = pygame.font.Font(os.path.join(sys.path[0], "arcade.TTF"), 31)

    clrLibre = 255,255,255
    clrPintado = 121,3,125
    clrObstaculo = 0,40,0
    clrPlayer = 237,83,222
    clrEnemy = 252,48,3


    playerGridX = 0 #Posicion X del jugador dentro del grid
    playerGridY = 0 #Posicion Y del jugador dentro del grid

    enemigos = genEnemy(2,mainGrid)
    vidaTotal = 3
    vidas = vidaTotal
    puntaje = 0

    contador = 0 #contador de fotogramas
    segundos = 0 #contador de segundos


    ejecutando = "juego"
    while ejecutando == "juego":

        reloj.tick(FPS)

        ventana.fill((52, 191, 145))

        #Variables del grid
        gridPosX = 22 #Posicion X de creación del grid
        gridPosY = 22 #Posicion Y de creación del grid
        gridInter = 4 #Espacio entre cada cuadrado
        tamCuadrado = 40 #Tamaño de los cuadrados

        

        #Dibujado de cuadricula
        for i in range(len(mainGrid)):
            for j in range(len(mainGrid[0])):
                #definir color
                if mainGrid[i][j] == 1:
                    color = clrObstaculo
                    sprite = sprObstaculo
                else:
                    if mainGrid[i][j] == 0:
                        color = clrLibre
                        sprite = sprEspacio
                    else:
                        if mainGrid[i][j] == 2:
                            color = clrPintado
                            sprite = sprPintado
                
                #Dibujado del espacio en la cuadricula segun color
                #pygame.draw.rect(ventana, color, pygame.Rect(gridPosX, gridPosY, tamCuadrado, tamCuadrado))
                sprite = pygame.transform.scale(sprite, (tamCuadrado, tamCuadrado))
                ventana.blit(sprite, (gridPosX, gridPosY, tamCuadrado, tamCuadrado))
                gridPosX += (tamCuadrado + gridInter)
            gridPosX -= (tamCuadrado + gridInter)*len(mainGrid[0])
            gridPosY += (tamCuadrado + gridInter)
        gridPosY -= (tamCuadrado + gridInter)*len(mainGrid) 

        #Posición en pixeles del jugador
        playerPosX= gridPosX + playerGridX * (tamCuadrado + gridInter)
        playerPosY= gridPosY + playerGridY * (tamCuadrado + gridInter)
        #Dibujar jugador en pantalla
        playerDraw = pygame.transform.scale(playerDraw, (tamCuadrado, tamCuadrado))
        ventana.blit(playerDraw, (playerPosX,playerPosY-8,tamCuadrado, tamCuadrado))

        #pygame.draw.rect(ventana, clrPlayer, pygame.Rect(playerPosX + 2,playerPosY + 2,tamCuadrado -4, tamCuadrado - 4)) #Dibujado de jugador (sin sprite)

        for i in range(len(enemigos)):
            #Posición en pixeles del enemigo
            enemyPosX= gridPosX + enemigos[i][1] * (tamCuadrado + gridInter)
            enemyPosY= gridPosY + enemigos[i][0] * (tamCuadrado + gridInter)
            #Dibujar enemigo en pantalla
            if i % 2 == 0:
                enemyDraw = sprEnemy1
            else:
                enemyDraw = sprEnemy2
            
            #pygame.draw.rect(ventana, clrEnemy, pygame.Rect(enemyPosX + 2,enemyPosY + 2,tamCuadrado -4, tamCuadrado - 4)) #Dibujado de enemigo (sin sprite)
            enemyDraw = pygame.transform.scale(enemyDraw, (tamCuadrado, tamCuadrado))
            ventana.blit(enemyDraw, (enemyPosX,enemyPosY-8,tamCuadrado, tamCuadrado))
        


        for event in pygame.event.get():
            if (event.type == pygame.QUIT):
                ejecutando = False

            if (event.type == pygame.KEYDOWN):
                tecla_presionada =  pygame.key.name(event.key)

                if tecla_presionada == "t":
                    ejecutando = "resultado"

                if tecla_presionada == "escape":
                    pause = not(pause)
                    print("pausa:",pause)
                
                if tecla_presionada == "w":
                    if pause == False:
                        if (playerGridY -1) >= 0:
                            if mainGrid[playerGridY - 1][playerGridX] != 1:
                                #pintar
                                if mainGrid[playerGridY - 1][playerGridX] == 0:
                                    mainGrid[playerGridY - 1][playerGridX] = 2
                                    pintado += 1
                                else:
                                    mainGrid[playerGridY - 1][playerGridX] = 0
                                    pintado -= 1
                                playerGridY -=1
                                print("🡩")
                                enemigos = randomMove(enemigos,mainGrid)
                    
                if tecla_presionada == "a":
                    if pause == False:
                        if (playerGridX -1) >= 0:
                            if mainGrid[playerGridY][playerGridX -1] != 1:
                                if mainGrid[playerGridY][playerGridX -1] == 0:
                                    mainGrid[playerGridY][playerGridX -1] = 2
                                    pintado += 1
                                else:
                                    mainGrid[playerGridY][playerGridX -1] = 0
                                    pintado -= 1
                                playerGridX -=1

                                playerDraw = sprPlayerLeft #Definir sprite izquierda
                                print("🡠")
                                enemigos = randomMove(enemigos,mainGrid)

                if tecla_presionada == "s":
                    if pause == False:
                        if (playerGridY +1) <= len(mainGrid)-1:
                            if mainGrid[playerGridY + 1][playerGridX] != 1:
                                if mainGrid[playerGridY + 1][playerGridX] == 0:
                                    mainGrid[playerGridY + 1][playerGridX] = 2
                                    pintado += 1
                                else:
                                    mainGrid[playerGridY + 1][playerGridX] = 0
                                    pintado -= 1
                                playerGridY +=1
                                print("🡣")
                                enemigos = randomMove(enemigos,mainGrid)

                if tecla_presionada == "d":
                    if pause == False:
                        if (playerGridX +1) <= len(mainGrid[0])-1:
                            if mainGrid[playerGridY][playerGridX + 1] != 1:
                                if mainGrid[playerGridY][playerGridX + 1] == 0:
                                    mainGrid[playerGridY][playerGridX + 1] = 2
                                    pintado += 1
                                else:
                                    mainGrid[playerGridY][playerGridX + 1] = 0
                                    pintado -= 1
                                playerGridX +=1

                                playerDraw = sprPlayerRight #Definir sprite derecha
                                print("🡢")
                                enemigos = randomMove(enemigos,mainGrid)

                print("pintado:",pintado)

                (playerGridY,playerGridX,vidas) = compruebaPos(enemigos, playerGridY, playerGridX, vidas) #regresar a 0,0 y perder una vida al chocar con enemigo
        
        #Calcular puntaje
        if pause == False:
            (contador,segundos) = contadorSeg(contador, segundos, FPS)
            puntaje = (pintado*1000)//(segundos+1)

        pygame.draw.rect(ventana, (0,0,0), pygame.Rect(480,0,160,480)) #Dibujado panel con estadisticas

        textoPuntaje = font.render('score', False, (255,255,255))
        ventana.blit(textoPuntaje,(486,22))

        drawPuntaje = font.render(str(puntaje), False, (255,255,255))
        ventana.blit(drawPuntaje,(486,55))

        #mostrar vidas
        vidasX = 486
        vidasY = 150
        for i in range(vidaTotal):
            if i+1 <= vidas:
                drawVidas = sprVidaLlena
            else:
                drawVidas = sprVidaVacia
            drawVidas = pygame.transform.scale(drawVidas, (52, 48))
            ventana.blit(drawVidas,(vidasX,vidasY))
            vidasX += 48
        
        panelEnemyX = 495
        panelEnemyY = 220
        for j in range(2):
            if j%2 == 0:
                drawPanelEnemy = sprEnemy1
            else:
                drawPanelEnemy = sprEnemy2
            drawPanelEnemy = pygame.transform.scale(drawPanelEnemy, (64, 64))
            ventana.blit(drawPanelEnemy,(panelEnemyX,panelEnemyY))
            panelEnemyX += 64
        
        #Calcular  y mostrar porcentaje de completado
        porcentaje = int((pintado/espaciosLibres)*100)

        drawPorcentaje = font.render(str(porcentaje)+"%", False, (255,255,255))
        ventana.blit(drawPorcentaje,(516,300))

        #mostrar boton pausa
        drawPause = sprPause
        drawPause = pygame.transform.scale(sprPause, (160, 96))
        ventana.blit(drawPause,(480,384))


        #Indicar pausa al estar activo
        if pause == True:
            sprPauseText = pygame.transform.scale(sprPauseText, (162, 44))
            ventana.blit(sprPauseText,(159,218))
        
        if (porcentaje == 100) or (vidas == 0):
            if fxDelay == 0:
                ejecutando = "resultado"
            else:
                fxDelay -= 1
            



        '''
        textoVidas = font.render('vidas '+ str(vidas), False, (255,255,255))
        ventana.blit(textoVidas,(500,66))

        textoPuntaje = font.render('score '+ str(puntaje), False, (255,255,255))
        ventana.blit(textoPuntaje,(500,88))
        '''
        

        pygame.display.flip()

    while ejecutando == "resultado":
        reloj.tick(FPS)
        #mostrar transicion "fx"
        if fxPlay == True:
            pygame.draw.rect(ventana, fxColor, pygame.Rect(0,0, fxAncho,fxAlto)) #Dibujado de efecto
            if fxAlto < ALTO_VENTANA:
                fxAlto += fxSpeed
            else:
                fxPlay = False
                print ("listo!")
        else:
            ventana.fill((0,0,0))
            #mostrar puntaje
            textoPuntaje = font.render('score', False, (255,255,255))
            ventana.blit(textoPuntaje,(32, 50))

            drawScore = font.render(str(puntaje), False, (255,255,255))
            drawScore = ventana.blit(drawScore,(32, 100))

            #mostrar vidas
            vidasX = 32
            vidasY = 150
            for i in range(vidaTotal):
                if i+1 <= vidas:
                    drawVidas = sprVidaLlena
                else:
                    drawVidas = sprVidaVacia
                drawVidas = pygame.transform.scale(drawVidas, (52, 48))
                ventana.blit(drawVidas,(vidasX,vidasY))
                vidasX += 48
            
            #mostrar tiempo
            textoTime = font.render('time', False, (255,255,255))
            ventana.blit(textoTime,(32, 230))

            drawTime = font.render(str(segundos)+ " sec", False, (255,255,255))
            drawTime = ventana.blit(drawTime,(32, 280))

            #mostrar porcentaje
            if vidas <= 0:
                textoPorcentaje = font.render('completed', False, (255,255,255))
                ventana.blit(textoPorcentaje,(32, 340))

                drawPorcentaje = font.render(str(porcentaje)+"%", False, (255,255,255))
                ventana.blit(drawPorcentaje,(32,390))



        for event in pygame.event.get():
            if (event.type == pygame.QUIT):
                ejecutando = "none"
        
        pygame.display.flip()


    sys.exit()

main()