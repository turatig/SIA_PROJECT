"Model of a quoridor game"
from utils import GridGraph


__COLOR_CODE__={
    "white":1,
    "black":2
}

class Board():

    def __init__(self,dim,pawnList):
        #wall slots
        self._dim=dim
        self._hwalls=[[0 for i in range(self._dim-1)] for j in range(self._dim-1)]
        self._vwalls=[[0 for i in range(self._dim-1)] for j in range(self._dim-1)]
        self._pawns=[p for p in pawnList]
        self._turn=0
        self._graph=GridGraph(self._dim)
    
    def getHorizontalWalls(self): return self._hwalls
    def getVerticalWalls(self): return self._vwalls

    def getWall(self,slot,verse):
        if verse=="horizontal":
            return self._hwalls[slot[0]][slot[1]]
        else:
            return self._vwalls[slot[0]][slot[1]]

    def isFree(self,wallSlot,verse):
        res=False
        i,j=wallSlot[0],wallSlot[1]

        #tested slot must:
        #-be surrounded by free slots
        if  verse=="horizontal":
            around= [self._hwalls[i][j+k] for k in range(-1,2) if j+k>=0 and j+k<len(self._vwalls)]\
                            + [self._vwalls[i][j]]
        else:
            around= [self._vwalls[i+k][j] for k in range(-1,2) if i+k>=0 and i+k<len(self._vwalls)]\
                            + [self._hwalls[i][j]]

        if(not [i for i in around if i]):

            #-leave a way from every pawn to its goal
            r,l= ((i+1,j),(i,j+1)) if verse=="horizontal" else ((i,j+1),(i+1,j))
            self._graph.cutEdge((i,j),r)
            self._graph.cutEdge(l,(i+1,j+1))

            if( all([self._graph.theresPath(p.getPosition(),p.getGoalRow()) for p in self.getPawns()]) ): 
                res=True

            self._graph.insertEdge((i,j),r)
            self._graph.insertEdge(l,(i+1,j+1))

        return res


    def getFreeSlots(self):
        free={"horizontal":[],"vertical":[]}

        for i in range(len(self._hwalls)):
            for j in range(len(self._hwalls[i])):
                if(self.isFree((i,j),"horizontal")):
                    free["horizontal"].append((i,j))
                if(self.isFree((i,j),"vertical")):
                    free["vertical"].append((i,j))
        return free

    def getPlacedSlots(self):
        full={"horizontal":[],"vertical":[]}

        for i in range(len(self._hwalls)):
            for j in range(len(self._hwalls[i])):
                if self._hwalls[i][j]:
                    full["horizontal"].append((i,j))
                if self._vwalls[i][j]:
                    full["vertical"].append((i,j))
        return full["horizontal"]+full["vertical"]

    def insertWall(self,pos,color,verse):
        i,j=pos[0],pos[1]
            
        if(not self.isFree((i,j),verse) or not self.getPawnByColor(color).getWallsLeft()): 
            return False

        r,l,walls= ((i+1,j),(i,j+1),self._hwalls) if verse=="horizontal" else \
                    ((i,j+1),(i+1,j),self._vwalls)

        walls[i][j]=__COLOR_CODE__[color]
        self._graph.cutEdge((i,j),r)
        self._graph.cutEdge(l,(i+1,j+1))
        self.getPawnByColor(color).decrementWallsLeft()
            
        return True

    def removeWall(self,pos,color,verse):
        i,j=pos[0],pos[1]
        if(self.isFree((i,j),verse)): 
            return False

        r,l,walls= ((i+1,j),(i,j+1),self._hwalls) if verse=="horizontal" else \
                    ((i,j+1),(i+1,j),self._vwalls)

        walls[i][j]=0
        self._graph.insertEdge((i,j),r)
        self._graph.insertEdge(l,(i+1,j+1))
        self.getPawnByColor(color).incrementWallsLeft()

        return True


    def isValid(self,p):
        return p[0]>=0 and p[0]<self._dim and p[1]>=0 and p[1]<self._dim

    #check whether the pawn can jump
    def getPossibleJumps(self):
        jumps=[]
        pos=self.getMovingPawn().getPosition()
        directions=[(1,0),(0,1),(-1,0),(0,-1)]
        
        for d in directions:
            p=(pos[0]+d[0],pos[1]+d[1])
            #If there's an opponent on the square
            if self._graph.areNeighbours(pos,p) and self.getOpponentPawn().getPosition()==p:
                #If there's no wall behind the opponent
                if self._graph.areNeighbours(p,(p[0]+d[0],p[1]+d[1])):
                    jumps.append((p[0]+d[0],p[1]+d[1]))
                else:
                    if self._graph.areNeighbours(p,(p[0]+d[1],p[1]+d[0])):
                        jumps.append((p[0]+d[1],p[1]+d[0]))
                    if self._graph.areNeighbours(p,(p[0]-d[1],p[1]-d[0])):
                        jumps.append((p[0]-d[1],p[1]-d[0]))
        return jumps

    def getPossibleNextMoves(self):
        pos=self.getMovingPawn().getPosition()
        directions=[(-1,0),(1,0),(0,-1),(0,1)]

        #Possible next positions are filtered according to following rules:
        #1-Must be in the range [0,dim-1]
        #2-Must be reachable from moving pawn current position
        #3-Must be empty
        free=list(filter(lambda p: p!= self.getOpponentPawn().getPosition(),\
                        filter(lambda p: self._graph.areNeighbours(p,pos),\
                            filter(lambda p:self.isValid(p),\
                                map(lambda d:(pos[0]+d[0],pos[1]+d[1]),directions)))))

        return free+self.getPossibleJumps()

    #Get the number of free squares along any direction from the specified position
    def getFreeWay(self,pawn):
        pos=pawn.getPosition()
        ways=[]
        dirs=[(-1,0),(1,0),(0,-1),(0,1)]

        for d in dirs:
            #Move along all directions till it's possible and count the squares
            for i in range(self._dim):
                if(not self._graph.areNeighbours(\
                        (pos[0]+d[0]*(i+1),pos[1]+d[1]*(i+1)),\
                        (pos[0]+d[0]*(i),pos[1]+d[1]*i)\
                )):
                    ways.append(i)
                    break

        if pawn.getGoalRow()==self._dim-1:
            ways[:2]=ways[1::-1]
            ways[2:]=ways[3:1:-1]

        return ways

        

    def getPawns(self): return self._pawns
    def getMovingPawn(self): return self._pawns[self.getTurnIdx()]
    def getOpponentPawn(self): return self._pawns[(self.getTurnIdx()+1)%2]
    def movePawn(self,p):
        if p in self.getPossibleNextMoves():
            self.getMovingPawn().setPosition(p)
            return True
        return False

    def getPawnByColor(self,color):
        for p in self.getPawns():
            if p.getColor()==color:
                return p

    def getTurn(self): return self._turn
    def getTurnIdx(self):return self._turn%len(self._pawns)
    def incrementTurn(self): self._turn+=1
    def decrementTurn(self):self._turn-=1

    #return a list the list of horizontal and vertical wall slots
    #1=slot_busy, 0=slot_free
    def getWallsMap(self):
        return [0 if not self._hwalls[i][j] else 1 for i in range(len(self._hwalls)) for j in range(len(self._hwalls[i]))]+\
                [0 if not self._vwalls[i][j] else 1 for i in range(len(self._vwalls)) for j in range(len(self._vwalls[i]))]

    def reset(self):
        self._hwalls=[[0 for i in range(self._dim-1)] for j in range(self._dim-1)]
        self._vwalls=[[0 for i in range(self._dim-1)] for j in range(self._dim-1)]
    
        self._graph=GridGraph(self._dim)
        for p in self._pawns:
            p.reset()
        self._turn=0
    
    def isTerminal(self):
        return [p for p in self._pawns if p.getPosition()[0]==p.getGoalRow()]

    def checkWinner(self):
        win=[p for p in self._pawns if p.getPosition()[0]==p.getGoalRow()]
        if win:
            return win[0]
        else: return False
        

class Pawn():

    def __init__(self,color,startPos,goalRow,wallsLeft=10):
        self._color=color
        self._startPos=startPos
        self._position=startPos
        self._goalRow=goalRow
        self._colorCode=__COLOR_CODE__[self._color]
        self._wallsLeft=self._maxWalls=wallsLeft
        

    def setPosition(self,newPos): self._position=newPos
    def getPosition(self): return self._position
    def getColor(self): return self._color
    def getGoalRow(self): return self._goalRow
    def getWallsLeft(self): return self._wallsLeft
    def isWinner(self): return self.getPosition()[0]==self.getGoalRow()
    def decrementWallsLeft(self): 
        if(self._wallsLeft>0):
            self._wallsLeft-=1
    def incrementWallsLeft(self):
        self._wallsLeft+=1
    def reset(self):
        self._wallsLeft=self._maxWalls
        self.setPosition(self._startPos)
