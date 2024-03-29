from Model import Board,Pawn
from random import uniform
import math

class RLAgent():

    def __init__(self,env,with_trace=False,v=False):

        self._env=env
        # Keys: state_tuple
        # Values: list of lists [action_tuple,reward_value]
        self._qtable=dict()
        self._gamma=0.25
        self._alpha=0.8
        
        #Policy is epsilon-greedy on the value function
        self._epsilon=0.1
        # Action=None and state=None indicates the initial state
        self._prev_act=self._prev_state=None

        # if the agent is created with the trace, these fields
        # manage update of previous seen states during the episode
        self._with_trace=with_trace
        self._lambda=0.5
        self._elegibility_trace=dict()
        #Verbose mode
        self._v=v

    ###LOGIC:
    ###-First update
    ###-Then _takeAction
    ###-When a game is finished, update must be explicitly called by the game controller one more time
    def takeAction(self):
        self.update()
        self._takeAction()
        return True

    #_takeAction is meant to be private method because it must be consistently called after update
    def _takeAction(self):
        actions,state={*self._env.getActions()},self._env.getState()
        valid=[(a,v) for a,v in self._qtable[state].items() if a in actions]

        if self._v:
            print("°°°°°°°°°°°°°°°°°°°°°°°°°")
            print(state)   

            print("State: {0}".format(state))
            for a,v in self._qtable[state].items():
                print("             Action:{0} value:{1}".format(a,v))

        qa_max=max(valid,key=lambda el:el[1])[1]

        greedy,suboptimal=[],[]
        for a in valid:
            if a[1]==qa_max: greedy.append(a[0])
            else: suboptimal.append(a[0])

        if suboptimal and uniform(0,1)<self._epsilon:
            #Choose with uniform probability among suboptimal actions
            a=suboptimal[int(uniform(0,0.99)*len(suboptimal))]
            #If suboptimal action was chosen, stop the propagation
            if self._with_trace:
                for state_action in self._elegibility_trace.keys():
                    self._elegibility_trace[state_action]=0

        else:
            #Choose with uniform probability among greedy (respect to the value function) actions
            a=greedy[int(uniform(0,0.99)*len(greedy))]

        if self._with_trace:
            self._elegibility_trace[(state,a)]=1
        self._env.update(a)
        self._prev_state=state
        self._prev_act=a
        
    #Update the previous action-value function of state and action, given new state and reward
    def update(self):

        if self._env.isTerminal():
            #get reward from the environment
            target=self._env.getHeuristic("won_match")
            self._update(target)
            if self._v:
                print("-"*20+" FINAL UPDATE "+"-"*20)
                print(self._qtable[self._prev_state][self._prev_act])
            #Reset at the end of an episode
            self.startEpisode()

        #If state is not terminal
        else:

            new_state=self._env.getState()

            if new_state not in self._qtable.keys():
                self._qtable[new_state]=dict()
            
            valid={*self._env.getActions()}
            explored={*self._qtable[new_state].keys()}
            for a in valid:
                #Init currently valid actions if these haven't been explored yet
                if a not in explored:
                    self._qtable[new_state][a]=0

            #If not at the start of the episode, update the previous state-action
            #value function given the observed reward and best action selectable 
            #in the new state
            if self._prev_state:
                if self._v:
                    print("***********************")
                    print(new_state)   
                #Select maximum value function between valid actions
                qa_max=max([v for a,v in self._qtable[new_state].items() if a in valid])
                target=self._env.getHeuristic("won_match")+self._gamma*qa_max
                
                self._update(target)

    #update the state,action value table           
    def _update(self,target):

        delta=(target-self._qtable[self._prev_state][self._prev_act])

        if self._with_trace:
            #_prev_state and _prev_act will be in this dict
            for st_act in self._elegibility_trace.keys():
                self._qtable[st_act[0]][st_act[1]]+=\
                    self._alpha*delta*self._elegibility_trace[st_act]

                self._elegibility_trace[st_act]=\
                    self._elegibility_trace[st_act]*self._gamma*self._lambda
        else:
            self._qtable[self._prev_state][self._prev_act]+=self._alpha*delta

    def startEpisode(self):
        self._elegibility_trace=dict()

#Super class which implements methods common to every agent that implements a deterministic policy
class StrategyAgent():

    def __init__(self,env,epsilon=0.1,h_type="shortest_path_next_row"):
        self._env=env
        self._epsilon=epsilon
        self._h_type=h_type

    #step on the shortest path to goal with prob=1-epsilon
    #random step with prob=epsilon 
    def takeOptimalStep(self):
        p=self._env.getMovingPawn()
        #Take a step along the shortest path direction
        next_pos=self._env._graph.shortestPath(p.getPosition(),p.getGoalRow())[1]
        valid=self._env.getPossibleNextMoves()

        #If the square is busy (there's opponent pawn on it) or with probability
        #epsilon (randomized subotmital choice)
        if uniform(0,0.99)<self._epsilon:
            next_pos=valid[int(uniform(0,0.99)*len(valid))]
        
        p=p.getPosition()
        self._env.update(("m",(next_pos[0]-p[0],next_pos[1]-p[1])))
    
    def placeOptimalWall(self):
        free_slots=self._env.getFreeSlots()
        best_slot=(None,math.inf)
        #free_slots["horizontal"],free_slots["vertical"]
        for k in free_slots.keys():
            for slot in free_slots[k]:
                #k[0] is action code "h/w" ("horizontal/vertical")
                self._env.update((k[0],slot))
                #The lower the better in this case (is evaluated during the adversarial turn)
                val=self._env.getHeuristic(self._h_type)
                if val<best_slot[1]:
                    best_slot=((k[0],slot),val)
                elif val==best_slot[1]:
                    if uniform(0,0.99)<0.5:
                        best_slot=((k[0],slot),val)
                self._env.undo()
        if uniform(0,0.99)< self._epsilon:
            wall_moves=[a for a in self._env.getActions() if a[0] in {"h","w"}]
            self._env.update(wall_moves[int(uniform(0,0.99)*len(wall_moves))])
        else:
            self._env.update(best_slot[0])

#The dummy agent 0 moves only the pawn in the direction of the shortest
#path
class DummyAgent0(StrategyAgent):

    def takeAction(self): self.takeOptimalStep()

#The dummy agent 1 waste all walls at the beginning of the match
#then behaves as dummy agent 0.
#Walls are placed by evaluating the board heuristic
class DummyAgent1(StrategyAgent):
        
    def takeAction(self):
        p=self._env.getMovingPawn()

        if p.getWallsLeft():
            self.placeOptimalWall()
        else:
            self.takeOptimalStep()


class NegamaxAgent(StrategyAgent):
    def __init__(self,env,depth=2,h_type="shortest_path_next_row"):
        self._depth=depth
        super().__init__(env,0,h_type)

    def takeAction(self):

        #Return tuple (heuristic_value,move) for negamax algorithm
        def negaMax(depth):
            if self._env.isTerminal() or not depth:
                return (self._env.getHeuristic(self._h_type),None)
            else:
                max_value=(-math.inf,None)
    
                for a in self._env.getActions():
                    self._env.update(a)
                    x=negaMax(depth-1)
                    if -x[0]>max_value[0]:
                        max_value=(-x[0],a)
                    #Choose random between actions that have same value
                    elif -x[0]==max_value[0] and uniform(0,1)>0.5:
                        max_value=(-x[0],a)

                    self._env.undo()
                return max_value
        
        if self._env.getMovingPawn().getWallsLeft():
            self._env.update(negaMax(self._depth)[1])
        else:
            self.takeOptimalStep()

class AlphabetaAgent(StrategyAgent):
    def __init__(self,env,depth=3,h_type="shortest_path_next_row"):
        self._depth=depth
        super().__init__(env,0,h_type)

    def takeAction(self):

        #Return tuple (heuristic_value,move) for alpha-beta pruning algorithm
        #max_p: this attribute is only used to complement or not the static evaluation
        #at the leaves according to the 
        def alphaBeta(depth,alpha,beta):
            if self._env.isTerminal() or not depth:
                heur=self._env.getHeuristic(self._h_type)
                """print("Traceback:")
                for i in range(self._depth):
                    print("-"*i+" {0}".format(self._env._cache[-(i+1)]))
                print("Heuristic value {0} color {1}".format(heur,self._env.getMovingPawn().getColor()))"""
                return (heur,None)
            else:
                max_value=(-math.inf,None)

                #for a in sorted(self._env.getActions(),reverse=True,key=lambda move: self._env.evalAction(move,self._h_type)):
                for a in self._env.getActions():
                    self._env.update(a)
                    x=alphaBeta(depth-1,(-beta[0],beta[1]),(-alpha[0],alpha[1]))
                    
                    if -x[0]>max_value[0]:
                        max_value=(-x[0],a)

                    elif -x[0]==max_value[0] and uniform(0,1)>0.5:
                        max_value=(-x[0],a)

                    self._env.undo()
                    if max_value[0]>alpha[0]:alpha=max_value
                    if alpha[0]>=beta[0]: return alpha

                return max_value

        if self._env.getMovingPawn().getWallsLeft():
            move=alphaBeta(self._depth,(-math.inf,None),(math.inf,None))[1]
            """print("Move chosen {0}".format(move))"""
            self._env.update(move)
        else:
            move=self.takeOptimalStep()



