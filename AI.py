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
            target=self._env.getReward()
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
                target=self._env.getReward()+self._gamma*qa_max
                
                self._update(target)

                
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




class NegamaxAgent():
    def __init__(self,env,depth=2):
        self._env=env
        self._depth=depth

    def takeAction(self):

        #Return tuple (heuristic_value,move) for negamax algorithm
        def negaMax(depth):
            if self._env.isTerminal() or not depth:
                return (self._env.getHeuristic(),None)
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

        self._env.update(negaMax(self._depth)[1])

#The dummy agent 0 moves only the pawn in the direction of the shortest
#path
class DummyAgent0():
    def __init__(self,env):
        self._env=env
        self._epsilon=0.1

    def takeAction(self):
        p=self._env.getMovingPawn()
        #Take a step along the shortest path direction
        next_pos=self._env._graph.shortestPath(p.getPosition(),p.getGoalRow())[1]
        valid=self._env.getPossibleNextMoves()

        #If the square is busy (there's opponent pawn on it) or with probability
        #epsilon
        if next_pos not in valid or uniform(0,0.99)<self._epsilon:
            next_pos=valid[int(uniform(0,0.99)*len(valid))]
        
        p=p.getPosition()
        self._env.update(("m",(next_pos[0]-p[0],next_pos[1]-p[1])))

#The dummy agent 1 waste all walls at the beginning of the match
#then behaves as dummy agent 0.
#Walls are placed evaluating the board heuristic
class DummyAgent1(DummyAgent0):
    def __init__(self,env):
        self._env=env
        self._epsilon=0.1

    def takeAction(self):
        p=self._env.getMovingPawn()

        if p.getWallsLeft():
            free_slots=self._env.getFreeSlots()
            best_slot=(None,math.inf)
            #free_slots["horizontal"],free_slots["vertical"]
            for k in free_slots.keys():
                for slot in free_slots[k]:
                    self._env.update((k[0],slot))
                    #The lower the better in this case (is evaluated during the adversarial turn)
                    val=self._env.getHeuristic()
                    if val<best_slot[1]:
                        best_slot=((k[0],slot),val)
                    elif val==best_slot[1]:
                        if uniform(0,0.99)<0.5:
                            best_slot=((k[0],slot),val)
                    self._env.undo()
            self._env.update(best_slot[0])
        else:
            super().takeAction()

