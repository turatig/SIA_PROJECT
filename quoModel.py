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
        #-leave a way from every pawn to its goal
        walls=[self._hwalls,self._vwalls] if verse=="horizontal" else [self._vwalls,self._hwalls]

        around= list(map(lambda k: walls[0][i][j+k],\
                        filter(lambda k: j+k>=0 and k>len(walls[0]),\
                            range(-1,2)))) + [walls[1][i][j]]

        print(around)

        if( not [i for i in around if i] ):

            r= (i+1,j) if verse=="horizontal" else (i,j+1)
            l= (i,j+1) if verse=="horizontal" else (i+1,j)
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

    def insertWall(self,pos,color,verse):
        i,j=pos[0],pos[1]
            
        if(not self.isFree((i,j),verse) or not self.getPawnByColor(color).getWallsLeft()): 
            return False

        r= (i+1,j) if verse=="horizontal" else (i,j+1)
        l= (i,j+1) if verse=="horizontal" else (i+1,j)

        self._hwalls[i][j]=__COLOR_CODE__[color]
        self._graph.cutEdge((i,j),r)
        self._graph.cutEdge(l,(i+1,j+1))
        self.getPawnByColor(color).decrementWallsLeft()
            
        return True

    def isValid(self,p):
        return p[0]>=0 and p[0]<self._dim and p[1]>=0 and p[1]<self._dim

    #check whether the pawn can jump
    def getPossibleJumps(self,pawn):
        jumps=[]
        pos=pawn.getPosition()
        direction= 1 if pawn.getGoalRow()>pos[0] else -1
        pos=(pos[0]+direction,pos[1])

        if len([t for t in self._pawns if t.getColor()!=pawn.getColor() and t.getPosition()==pos])==0:
            return jumps

        if self._graph.areNeighbours(pos,(pos[0]+direction,pos[1])):
            jumps.append((pos[0]+direction,pos[1]))
        else:
            if self._graph.areNeighbours(pos,(pos[0],pos[1]+1)):
                jumps.append((pos[0],pos[1]+1))
            if self._graph.areNeighbours(pos,(pos[0],pos[1]-1)):
                jumps.append((pos[0],pos[1]-1))

        return jumps

    def getPossibleNextMoves(self):
        pawn=self._pawns[self._turn]
        color=pawn.getColor()
        pos=pawn.getPosition()
        moves=[(-1,0),(1,0),(0,-1),(0,1)]

        free=list(filter(lambda p: p not in [pawn.getPosition() for pawn in self._pawns],\
                        filter(lambda p: self._graph.areNeighbours(p,pos),\
                            filter(lambda p:self.isValid(p),\
                                map(lambda p:(pos[0]+p[0],pos[1]+p[1]),moves)))))
    
        return free+self.getPossibleJumps(pawn)
        

    def getPawns(self): return self._pawns
    def getMovingPawn(self): return self._pawns[self._turn]

    def getPawnByColor(self,color):
        for p in self.getPawns():
            if p.getColor()==color:
                return p

    def switchTurn(self):
        self._turn=(self._turn+1)%len(self._pawns)

    def checkWinner(self):
        return [p for p in self._pawns if p.getPosition()[0]==p.getGoalRow()]
        

class Pawn():

    def __init__(self,color,startPos,goalRow,wallsLeft=10):
        self._color=color
        self._position=startPos
        self._goalRow=goalRow
        self._colorCode=__COLOR_CODE__[self._color]
        self._wallsLeft=wallsLeft
        

    def setPosition(self,newPos): self._position=newPos
    def getPosition(self): return self._position
    def getColor(self): return self._color
    def getGoalRow(self): return self._goalRow
    def getWallsLeft(self): return self._wallsLeft
    def decrementWallsLeft(self): 
        if(self._wallsLeft>0):
            self._wallsLeft-=1
