from Model import Board,Pawn
from utils import GridGraph


"""
This class provides compact representation of the state and additional info for the rl agent.
"""
class Env(Board):

    def __init__(self,dim,pawnList,limit=10):
        super().__init__(dim,pawnList)
        #size of cache for undo stages
        self._limit=limit
        self._cache=[]
    
    #State=(len_min_path,walls_left,n_north,n_west,n_south,n_east)*(pawn1,pawn2)
    def getState(self):
        pl=self.getMovingPawn(),self.getAdPawn()

        #print(list([p.getColor() for p in pl]))
        state=[0 for i in range(12)]
        state[:2]=[self._graph.shortestPath(p.getPosition(),p.getGoalRow()) for p in pl]
        #for p in state[:2]:
            #print(p)

        state[:2]=[len(p) for p in state[:2]]

        state[2:4]=[p.getWallsLeft() for p in pl]

        dirs=[(-1,0),(0,-1),(1,0),(0,1)]
        pl=[p.getPosition() for p in pl]
        k=3

        for p in pl:
            for d in dirs:
                pos=p
                k+=1
                #Move along all directions till it's possible and count the squares
                for i in range(self._dim):
                    prev=pos
                    pos=(pos[0]+d[0],pos[1]+d[1])
                    if(pos in pl or not self._graph.areNeighbours(prev,pos)):
                        state[k]=i
                        break

        return tuple(state)
    # Action code: (m/h/v,(pos[0],pos[1]))
    # (m,p): move the pawn to p
    # (h/v,p): put wall in slot p

    def getActions(self):
        pos=self.getMovingPawn().getPosition()
        moves=[("m",(p[0]-pos[0],p[1]-pos[1])) for p in self.getPossibleNextMoves()]
        w=self.getFreeSlots()

        if self.getMovingPawn().getWallsLeft():
            return moves+[("h",s) for s in w["horizontal"]]+[("v",s) for s in w["vertical"]]
        else:
            return moves

    def update(self,action,breakp=False):
        pos=self.getMovingPawn().getPosition()
        decoder={
            #N.B: action code must be ("m",(ROW_INCREMENT,COL_INCREMENT))
            "m":lambda a: self.movePawn((pos[0]+a[0],pos[1]+a[1])),
            "h":lambda a: self.insertWall(a,self.getMovingPawn().getColor(),"horizontal"),
            "v":lambda a: self.insertWall(a,self.getMovingPawn().getColor(),"vertical")
        }

        if decoder[action[0]](action[1]):
            self._cache.append(action)
            if len(self._cache)>self._limit: self._cache.pop(0)
            #TODO: togliere prima della consegna
            if breakp:
                print(self.getMovingPawn().getColor())
                print("Updating board with action {0}".format(action))
                input()
                print(self._cache)
            self.incrementTurn()
            return True

        return False
    
    def undo(self,breakp=False):
        
        if not self._cache: return False

        decoder={
            "m":lambda a: self.getMovingPawn().setPosition((pos[0]-a[0],pos[1]-a[1])),
            "h":lambda a: self.removeWall(a,self.getMovingPawn().getColor(),"horizontal"),
            "v":lambda a: self.removeWall(a,self.getMovingPawn().getColor(),"vertical")
        }
        #TODO: togliere prima della consegna
        if breakp:
            print("Undoing action {0}".format(self._cache[-1]))
            input()
        self.decrementTurn()
        decoder[self._cache[-1][0]](self._cache[-1][1])
        self._cache.pop()

        return True
        

    def isTerminal(self):
        return [p for p in self._pawns if p.getPosition()[0]==p.getGoalRow()]

    def reset(self):
        self._hwalls=[[0 for i in range(self._dim-1)] for j in range(self._dim-1)]
        self._vwalls=[[0 for i in range(self._dim-1)] for j in range(self._dim-1)]
        self._turn=0
        self._graph=GridGraph(self._dim)
        for p in self._pawns:
            p.reset()

    def getHeuristic(self):
        p1=self.getMovingPawn()
        p2=self.getAdPawn()
        
        if self.isTerminal():
            if p1.isWinner(): return 1000
            else: return -1000
        else:
            #Compute difference of shortest paths heuristics
            return len(self._graph.shortestPath(p2.getPosition(),p2.getGoalRow()))-\
                        len(self._graph.shortestPath(p1.getPosition(),p1.getGoalRow()))
    
    def getReward(self):
        p1=self.getMovingPawn()
        p2=self.getAdPawn()
        
        if self.isTerminal():
            if p1.isWinner(): return 1000
            else: return -1000
        else:
            #Compute difference of shortest paths heuristics
            return len(self._graph.shortestPath(p2.getPosition(),p2.getGoalRow()))-\
                        len(self._graph.shortestPath(p1.getPosition(),p1.getGoalRow()))






