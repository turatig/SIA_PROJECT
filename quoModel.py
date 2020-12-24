"Model of a quoridor game"
from utils import GridGraph


__COLOR_CODE__={
    "white":1,
    "black":2
}

class Board():

    def __init__(self):
        #wall slots
        self._hwalls=[[0 for i in range(8)] for j in range(8)]
        self._vwalls=[[0 for i in range(8)] for j in range(8)]
        self._pawns=[Pawn("white",(0,4)),Pawn("black",(8,4))]
        self._graph=GridGraph(9)
    
    def getHorizontalWalls(self): return self._hwalls
    def getVerticalWalls(self): return self._vwalls


    def getFreeSlots(self):
        free={"horizontal":[],"vertical":[]}
        for i in range(len(self._hwalls)):
            for j in range(len(self._hwalls[i])):

                #tested slot must:
                #-be surrounded by free slots
                #-leave a way from every pawn to its goal
                #horizontal
                around=[self._hwalls[i][j+k] for k in range(-1,2) if j+k>=0 and j+k<len(self._hwalls[i])]
                around.append(self._vwalls[i][j])

                if(len([i for i in around if i])==0):
                    self._graph.cutEdge((i,j),(i+1,j))
                    self._graph.cutEdge((i,j+1),(i+1,j+1))

                    if( all([self._graph.depthFirst(p.getPosition(),p.getGoalRow()) for p in self.getPawns()]) ): 
                        free["horizontal"].append((i,j))

                    self._graph.insertEdge((i,j),(i+1,j))
                    self._graph.insertEdge((i,j+1),(i+1,j+1))

                #vertical
                around=[self._vwalls[i+k][j] for k in range(-1,2) if i+k>=0 and i+k<len(self._vwalls)]
                around.append(self._hwalls[i][j])
                
                if(len([i for i in around if i])==0):
                    self._graph.cutEdge((i,j),(i,j+1))
                    self._graph.cutEdge((i+1,j),(i+1,j+1))

                    if( all([self._graph.depthFirst(p.getPosition(),p.getGoalRow()) for p in self.getPawns()]) ): 
                        free["vertical"].append((i,j))

                    self._graph.insertEdge((i,j),(i,j+1))
                    self._graph.insertEdge((i+1,j),(i+1,j+1))

        return free

    def insertHorizontalWall(self,pos,color):
        i,j=pos[0],pos[1]

        if(pos not in self.getFreeSlots()["horizontal"]): return False

        self._hwalls[i][j]=__COLOR_CODE__[color]
        self._graph.cutEdge((i,j),(i+1,j))
        self._graph.cutEdge((i,j+1),(i+1,j+1))
        self.getPawnByColor(color).decrementWallsLeft()

        return True

    def insertVerticalWall(self,pos,color):
        i,j=pos[0],pos[1]
        if(pos not in self.getFreeSlots()["vertical"]): return False

        self._vwalls[pos[0]][pos[1]]=__COLOR_CODE__[color]
        self._graph.cutEdge((i,j),(i,j+1))
        self._graph.cutEdge((i+1,j),(i+1,j+1))
        self.getPawnByColor(color).decrementWallsLeft()

        return True

    def getPawns(self): return self._pawns

    def getPawnByColor(self,color):
        for p in self.getPawns():
            if p.getColor()==color:
                return p
        

class Pawn():

    __GOAL_ROWS__={
        (0,4):8,
        (8,4):0
    }
    def __init__(self,color,startPos):
        self._color=color
        self._position=startPos
        self._goalRow=Pawn.__GOAL_ROWS__[self._position]
        self._colorCode=__COLOR_CODE__[self._color]
        self._wallsLeft=10
        

    def setPosition(self,newPos): self._position=newPos
    def getPosition(self): return self._position
    def getColor(self): return self._color
    def getGoalRow(self): return self._goalRow
    def getWallsLeft(self): return self._wallsLeft
    def decrementWallsLeft(self): 
        if(self._wallsLeft>0):
            self._wallsLeft-=1

class GameState():

    def __init__(self):
        self._board=Board()
        self.getPawnByColor("black").setPosition((8,8))
        self._board.insertHorizontalWall((7,7),"white")
        self._board.insertVerticalWall((7,6),"black")

        self._turn=1

    def getBoard(self): return self._board
    def getTurn(self): return self._turn
    def getPawns(self):return self._board.getPawns()
    def getPawnByColor(self,color):
        for p in self._board.getPawns():
            if p.getColor()==color:
                return p
