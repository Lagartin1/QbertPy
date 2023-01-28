
import random
import pygame
import sys
import os

def cuadricula(y,x): #Funcion que genera una cuadricula de los valores indicados (todos los valores de la cuadricula son cero). retorna una lista de listas con la forma: lista[y][x]
    grid = [[] for i in range(x)]
    for j in range(x):
        for h in range(y):
            grid[j].append(0)
    return grid 

def enCuadricula(y,x,grid): #comprobar si coordenadas pretenecen a la cuadriucla
    if (y < 0) or (y > len(grid)-1):
         return False
    if (x < 0) or (x > len(grid[0])-1):
        return False 
    return True  

def obstaculos(numObstaculos,grid): #generacion de obstaculos
    for i in range(numObstaculos): #Colocar cantidad de obstaculos segun numObstaculos
        #Coordenadas aleatorias
        ranY = random.randint(0,len(grid)-1)
        ranX = random.randint(0,len(grid[0])-1)
        print("probando con:",ranY,ranX)
        while (ranX==0 and ranY==0) or (grid[ranY][ranX]!=0) or adyacentesLibres(ranY,ranX,grid) == False: #comprobar que las coordenadas no sean 0,0. que sea en espacio libre y que todos los espacios adyacentes estén disponibles
            ranY = random.randint(0,len(grid)-1)
            ranX = random.randint(0,len(grid[0])-1)
            print("probando con:",ranY,ranX)
        #almacenar coordenadas en una nueva variable para no modificar ranY y ranX
        posY = ranY
        posX = ranX
        grid[ranY][ranX] = 1 #colocar obstaculo
        print("Obstaculo colocado")
        for j in range(i): #agregar cantidad de espacios por obstaculos segun valor de i
            ranEjeY = random.randint(-1,1)
            ranEjeX = random.randint(-1,1)
            print("pos=",posY,posX)
            print("obs=",ranEjeY,ranEjeX)

            while ((ranEjeY == 0) and (ranEjeX == 0)) or ((posY + ranEjeY==0) and (posX + ranEjeX == 0)) or enCuadricula(posY+ranEjeY,posX+ranEjeX,grid)==False or (grid[posY+ranEjeY][posX+ranEjeX]!=0): #comprobar que el espacio no sea igual al valor del obstaculo inicial, que no sea 0,0. que se encuentre dentro de la cuadricula y que el espacio esté libre
                ranEjeY = random.randint(-1,1)
                ranEjeX = random.randint(-1,1)
                print("cambiado!")
                print("obs=",ranEjeY,ranEjeX)

            
            print("pos=",posY,posX)
            print("obs=",ranEjeY,ranEjeX)
            grid[posY+ranEjeY][posX+ranEjeX] = 1 #colocar obstaculo
            print("Obstaculo colocado")
    return grid
   
#(posY+ranEjeY < 0) or (posY+ranEjeY > len(grid)-1) or (posX+ranEjeX < 0) or (posX+ranEjeX > len(grid[0])-1) en cuadricula


def adyacentesLibres(y,x,grid): #comprueba que las casillas adyacentes con respecto a las coordenadas dadas esten libres
    if ((y-1) >= 0) and ((x-1) >= 0):
        if grid[y-1][x-1] != 0: #Arriba izquierda
            print("obstaculo en diagonal superior izquierda")
            return False
    if ((y-1) >= 0) and (x !=(len(grid[0])-1)):
        if grid[y-1][x+1] != 0: #Arriba derecha
            print("obstaculo en diagonal superior derecha")
            return False
    if y != (len(grid)-1) and ((x-1) >= 0):
        if grid[y+1][x-1] != 0: #Abajo izquierda
            print("obstaculo en diagonal inferior izquierda")
            return False
    if (x != len(grid[0])-1) and (y != len(grid)-1):
        if grid[y+1][x+1] != 0: #Abajo derecha
            print("obstaculo en diagonal inferior derecha")
            return False
    if ((y - 1) >= 0):
        if grid[y-1][x] != 0: #Arriba
            print("obstaculo arriba")
            return False
    if (y != (len(grid)-1)):
        if grid[y+1][x] != 0: #Abajo
            print("obstaculo abajo")
            return False
    if ((x - 1) >= 0):
        if grid[y][x-1] != 0:
            print("obstaculo izquierda")
            return False
    if (x != len(grid[0])-1):
        if grid[y][x+1] != 0:
            print("obstaculo derecha")
            return False
    return True
 
def printGrid(grid): #imprime una lista de listas en promt
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            print(grid[i][j],end="  ")
        print()

def genEnemy(enemyNum, grid): #Crea una tabla con los enemigos y sus coordenadas dependiendo de la cantidad de enemigos y el tablero principal
    enemigos=cuadricula(2,enemyNum)
    for i in range(len(enemigos)):
        y=random.randint(0,len(grid)-1)
        x=random.randint(0,len(grid[0])-1)
        while (y==0 and x==0) or (grid[y][x]!=0) :
            y=random.randint(0,len(grid)-1)
            x=random.randint(0,len(grid[0])-1)
        enemigos[i][0] = y
        enemigos[i][1] = x
    return enemigos

def checkPos(posGrid, y, x): #Comprueba que las coordenadas dadas no se encuentren en la cuadricula de posiciones, retorna True si esto ocurre
    for i in range(len(posGrid)):
        if (y == posGrid[i][0]) and (x == posGrid[i][1]):
            return True
    return False

def randomMove(enemyGrid, grid):
    for i in range(len(enemyGrid)):
        #Guardar coordenadas del enemigo actual en variables
        enemyY = enemyGrid[i][0]
        enemyX = enemyGrid[i][1]
        print("Enemigo",i+1,":",enemyY,enemyX)
        #Definir movimiento positivo o negativo de los ejes
        enemyMoveY = random.randint(-1,1)
        enemyMoveX = random.randint(-1,1)
        print("moviendo:",enemyMoveY,enemyMoveX)
        while (enemyMoveY != 0 and enemyMoveX != 0) or (enemyMoveY == 0 and enemyMoveX == 0) or (enCuadricula(enemyY + enemyMoveY,enemyX + enemyMoveX,grid) == False) or (grid[enemyY + enemyMoveY][enemyX + enemyMoveX] == 1) or (enemyY + enemyMoveY == 0 and enemyX + enemyMoveX == 0) or (checkPos(enemyGrid, enemyY + enemyMoveY, enemyX + enemyMoveX) == True): #comprobar que el enemigo se mueva en un solo eje, que el movimiento sea valido, que esté en la cuadricula, que tenga espacio para moverse, que las nuevas coordenadas no sean 0,0
            enemyMoveY = random.randint(-1,1)
            enemyMoveX = random.randint(-1,1)
            print("ERROR, cambiando a:",enemyMoveY,enemyMoveX)
        #Almacenar nuevas coordenadas de enemigo
        enemyGrid[i][0] = enemyY + enemyMoveY
        enemyGrid[i][1] = enemyX + enemyMoveX
        printGrid(enemyGrid)
    return enemyGrid

def compruebaPos(enemigos,y,x,vidas): #comprobar las coordenadas de los enemigos con respecto al jugador y quitar vidas si ambos se encuentran en la misma casilla
    for i in range(len(enemigos)):
        enemyY = enemigos[i][0]
        enemyX = enemigos[i][1]
        if (y,x) == (enemyY,enemyX):
            y = 0
            x = 0
            vidas -= 1
    return (y, x, vidas)

def contadorSeg(contador,segundos,fps): #Cuenta segundos segun los FPS y un contador adjunto
    if contador + 1 == fps:
        contador = 0
        segundos += 1
    else:
        contador += 1
    return contador,segundos

def imgLoad(imgFolder):
    imagen = pygame.image.load(open(os.path.join(sys.path[0], imgFolder), "r"))
    return imagen

#random.randint(a,b)
#lista[x][y]