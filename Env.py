from Model import Board,Pawn
from utils import GridGraph


"""
This class provides compact representation of the state and additional info for the rl agent.
"""
class Env(Board):
    def __init__(self,dim,pawnList,limit=10,rw_type="win_match"):
        super().__init__(dim,pawnList)
        #size of cache for undo stages
        self._limit=limit
        self._cache=[]
        #save the reward type
        self._rewardType=rw_type
    
    def getHeuristic(self):
        p1=self.getMovingPawn()
        p2=self.getOpponentPawn()
        
        if self.isTerminal():
            if p1.isWinner(): return 1000
            else: return -1000
        else:
            #Compute difference of shortest paths heuristics
            return len(self._graph.shortestPath(p2.getPosition(),p2.getGoalRow()))-\
                        len(self._graph.shortestPath(p1.getPosition(),p1.getGoalRow()))

    def getWmHeuristic(self):
        p1=self.getMovingPawn()
        p2=self.getOpponentPawn()
        
        if self.isTerminal():
            if p1.isWinner(): return 1000
            else: return -1000
        else: 0

    def getReward(self):
        if self._rewardType=="win_matrch": return self.getWmHeuristic()
        else: return self.getHeuristic()
                        
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
        pos=self.getMovingPawn().getPosition()
        decoder[self._cache[-1][0]](self._cache[-1][1])
        self._cache.pop()

        return True

    def getActions(self):
        pos=self.getMovingPawn().getPosition()
        moves=[("m",(p[0]-pos[0],p[1]-pos[1])) for p in self.getPossibleNextMoves()]
        w=self.getFreeSlots()

        if self.getMovingPawn().getWallsLeft():
            return moves+[("h",s) for s in w["horizontal"]]+[("v",s) for s in w["vertical"]]
        else:
            return moves

class Env1(Env):
    
    #State=(len_min_path,walls_left,n_sq_front,n_sq_back,n_sq_right,n_sq_left)*(pawn1,pawn2)
    def getState(self):
        pl=self.getMovingPawn(),self.getOpponentPawn()

        #print(list([p.getColor() for p in pl]))
        state=[0 for i in range(12)]
        state[:]=[len(self._graph.shortestPath(p.getPosition(),p.getGoalRow())) for p in pl]

        state[2:]=[p.getWallsLeft() for p in pl]

        state[4:]=self.getFreeWay(pl[0])+self.getFreeWay(pl[1])  

        #print(state)
        return tuple(state)

class Env2(Env):

    #State(moving_pawn_pos,opponent_pawn_pos,[placed_walls])
    def getState(self):
        return tuple([self.getMovingPawn().getPosition(),self.getOpponentPawn().getPosition()]+\
                        self.getPlacedSlots())






