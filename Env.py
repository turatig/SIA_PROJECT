from Model import Board,Pawn

"""
This class provides compact representation of the state and additional info for the rl agent.
For every pawn state is described by:
len_min_path,walls_left,n_north,n_west,n_south,n_east
"""
class Env(Board):

    def __init__(self,dim,pawnList):
        super().__init__(dim,pawnList)
    
    def getState(self):
        pl=self.getMovingPawn(),self.getAdPawn()

        state=[0 for i in range(12)]
        state[:2]=[len(self._graph.shortestPath(p.getPosition(),p.getGoalRow())) for p in pl]

        state[2:4]=[p.getWallsLeft() for p in pl]

        dirs=[(-1,0),(0,-1),(1,0),(0,1)]
        pl=[p.getPosition() for p in pl]
        k=4

        for p in pl:
            for d in dirs:
                pos=p
                k+=1
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
        moves=[("m",p) for p in self.getPossibleNextMoves()]
        w=self.getFreeSlots()
        hw=[("h",s) for s in w["horizontal"]]
        vw=[("v",s) for s in w["vertical"]]

        return moves+hw+vw



