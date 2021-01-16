from Model import Board,Pawn

class AI():

    def __init__(self,env,color):

        self._env=env
        self._color=color
        # Keys: state_tuple
        # Values: list of lists [action_tuple,reward_value]
        self._qtable=dict()
        self._gamma=0.25
        self._alpha=0.8
        # Action=None and state=None indicates the initial state
        self._a=self._s=None

        self._adecoder={
                    "m":lambda p:self.getMovingPawn().setPosition(p),
                    "h":lambda p:self.insertWall(p,self.getMovingPawn().getColor(),"horizontal"),
                    "v":lambda p:self.insertWall(p,self.getMovingPawn().getColor(),"vertical")
                    }

    def takeAction(self):
        s,actions=self._env.getState(),self._env.getActions()

        if s not in self._qtable.keys():
            self._qtable[s]=[]
        
        explored={a[0] for a in self._qtable[s]}
        for a in actions:
            if a not in explored:
                self._qtable[s].append([a,0])
        

    def update(self,new_state):
        
        if self._state:
            actions={i for i in self._env.getActions()}
            new_a=max([a for a in self._qtable[new_state] if a[0] in actions],key=lambda a:a[1])
            for i in self._qtable[self._state]


    def startEpisode(self):
        self._a=self._s=None