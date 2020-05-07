from random import randint,random
from copy import deepcopy
from math import sqrt


#################################
####Section:Misc functions#######
#################################

def myZeros(r,c,v):
    return [[v for i in range(r)] for j in range(c)]
def calcDist(a,b):
    return sqrt(pow(a[0]-b[0],2)+pow(a[1]-b[1],2))
def printMaze(m):
    rows=[]
    for i in range(len(m)):
        rows.append("")
        for j in range(len(m[0])):
            rows[i]+=str(m[i][j])+" "
    for r in rows:
        print(r)

############################################
####Section:Helper functions for eval#######
############################################

#maze1
#######
#_____#
#_#_#_#
#_#_#_#
#_#_#_#
#_____#
#######
def makeMaze1():
    h=7
    w=7
    maze1=myZeros(h,w,0)
    for i in range(h):
        maze1[i][0]=1
        maze1[i][-1]=1
    for j in range(w):
        maze1[0][j]=1
        maze1[-1][j]=1
    for k in range(2,5):
        maze1[k][2]=1
        maze1[k][4]=1
    return maze1

def printIndy(indy):
    realMoves=[]
    for m in indy[0]:
        if m==0:
            realMoves.append("R")
        elif m==1:
            realMoves.append("D")
        elif m==2:
            realMoves.append("L")
        elif m==3:
            realMoves.append("U")
        else:
            print("Error unknown move ",m)
            realMoves.append("?")
    print(realMoves,indy[1])
def _executeMoves(c,m):
        if m==0: #Right
            return [c[0],c[1]+1]
        elif m==1: #Down
            return [c[0]+1,c[1]]
        elif m==2: #Left
            return [c[0],c[1]-1]
        elif m==3: #Up
            return [c[0]-1,c[1]]
        else:
            print("Unrecognized direction ",m)
            return c

def executeMoves(maze,start,moves,showPath=True):
    current=start
    for m in moves:
        n=_executeMoves(current,m)
        if maze[n[0]][n[1]]!=1: #not a wall
            current=n
            if showPath:
                maze[n[0]][n[1]]='_'
    #fitness is based on final position
    #so it helps to mark that specifically
    if showPath:
        maze[current[0]][current[1]]='F'
    return current


####################################
####Section:Main EA functions#######
####################################

def createPopSimpMaze(pSize,gSize=6):
    pop=[]
    gSize=6
    for i in range(pSize):
        genome=[]
        for j in range(gSize):
            genome.append(randint(0,3))
        #the -9999 is a placeholder for fitness        
        pop.append([genome,-9999])
    return pop

maze=makeMaze1()
def evalSimpMaze(indy):
    moves=indy[0]
    goal=[3,1]
    start=[3,3]

    markedMaze=deepcopy(maze)  #used for debuging
    markedMaze[goal[0]][goal[1]]='G'
    markedMaze[start[0]][start[1]]='S'
        
    finalPosition=executeMoves(markedMaze,start,moves,showPath=True)
    fitness= -1*calcDist(goal,finalPosition)
    indy[1]=fitness

    #printIndy(indy)
    #printMaze(markedMaze)

#assumes pop is sorted such that
#the first individual has
#the highest fitness
def checkTermSimpMaze(pop):
    #fitness of 0 means the robot
    #is right on the goal (i.e. dist b/t
    #robot and goal is zero)
    if abs(pop[0][1])==0:
        return True
    else:
        return False    

def selectTopPercent(pop):
    cutOffPercent=0.5
    cutOff=(len(pop)-1)*int(cutOffPercent)
    i=randint(0,cutOff)
    return deepcopy(pop[i])

def crossover(p1,p2):
    cp=randint(0,len(p1[0])-1) #crossover point
    genome=p1[0][0:cp]+p2[0][cp:len(p1[0])]
    return [genome,-9999]

def mutateSimpMaze(c):
    mRate=0.1
    for i in range(len(c[0])):
        if random()<mRate:
            c[0][i]=randint(0,3)

def runEA(createPop,evaluate,checkTerminate,selection,crossover,mutate):
    pSize=100
    maxGen=100
    currGen=0
    genPrint=True
    
    #intialize population
    pop=createPop(pSize)

    #main EA loop
    while True:
        for p in pop:
            evaluate(p)

        #reverse sort pop by fitness
        pop.sort(key=lambda x:x[1],reverse=True)
        if currGen>=maxGen or checkTerminate(pop):
            break

        #printing for this generation
        if genPrint:
            print("\nCurrent Gen: "+str(currGen))
            print("Best Genome and Fitness:")
            printIndy(pop[0])

        #selection,crossover, and generate new pop
        currGen+=1
        nPop=[]
        while len(nPop)<len(pop):
            p1=selection(pop)
            p2=selection(pop)
            child=crossover(p1,p2)
            mutate(child)
            nPop.append(child)
        pop=nPop

    #end of main EA loop
    print("\nFinal gen: "+str(currGen))
    print("Best Genome and Fitness for final gen:")
    printIndy(pop[0])
        
    return pop

pop = runEA(createPopSimpMaze,evalSimpMaze,checkTermSimpMaze,selectTopPercent,crossover,mutateSimpMaze)
