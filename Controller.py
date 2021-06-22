import pygame as pg 
import Model as model
import Env as env
import View as view
from AI import RLAgent,NegamaxAgent,DummyAgent0
import time


class Controller():
    def __init__(self,mod=None,players=None):
        if mod is None:
            self._model=env.Env2(5,[model.Pawn("white",(0,2),4,3),model.Pawn("black",(4,2),0,3)])
        else:
            self._model=mod
        self._view=view.View(self._model)

        if players is None:
            self._players=[Human(self),Human(self)]
        else:
            self._players=players
        self._running=False


    def quit(self): self._running=False

    def game_loop(self):
        
        self._running=True

        while self._running:
            while not self._model.checkWinner() and self._running:

                self._view.render()
                print("Heuristic value for {0} player:{1}".format(self._model.getMovingPawn().getColor(),self._model.getHeuristic()))
                self._players[self._model.getTurnIdx()].takeAction()

                if type(self._players[self._model.getTurnIdx()])!=Human:
                    for e in pg.event.get():
                        if e.type==pg.QUIT:
                            self._running=False

            if self._running:
                winner=self._model.checkWinner().getColor()
                for p in self._players:
                    if type(p)==RLAgent:
                        #Calling the last update is mandatory
                        if p!=self._players[self._model.getTurnIdx()]:
                            self._model.incrementTurn()
                        p.update()
                turn_count=self._model.getTurn()
                self._model.reset()
                return winner,turn_count
        return False
            
    def setPlayers(self,players):
        self._players=[p for p in players]

    #Train an RLAgent
    def train(self,RLplayer,opponentPlayer,color="white",n_match=200):
        win_count,lose_count=1,1
        #Win rate:[win_count/lose_count] at the iteration number i
        win_rate=[]
        self.setPlayers([RLplayer,opponentPlayer])
        if color!="white":
            players=players[::-1]
        for i in range(n_match):
            res=self.game_loop()
            #The game was quitted, during the train
            if not res:
                return False
            winner,turn_count=res
            print("{0} player won match number {1} in {2} turns".format(winner,i+1,turn_count))
            if winner==color:
                win_count+=1
            else:
                lose_count+=1
            win_rate.append(win_count/lose_count)
        
        return win_rate


class Human():
    def __init__(self,controller):
        self._model=controller._model
        self._view=controller._view
        self._game_controller=controller

    def takeAction(self):
        moved=False
        running=True

        while(running and not moved):
                for e in pg.event.get():

                    if e.type==pg.MOUSEMOTION:
                        self._view.getBoard().clear()
                        el=self._view.getBoard().getElementByPos(pg.mouse.get_pos())
                        if el: 
                            el.highlight()
                            self._view.render()
                    if e.type==pg.MOUSEBUTTONUP:
                        """if self._view.undo_button.collidepoint(pg.mouse.get_pos()):
                            self._model.undo()
                            self._view.render()"""
                        el=self._view.getBoard().getElementByPos(pg.mouse.get_pos())
                        if el:
                            if type(el)==view.Square:
                                p=self._model.getMovingPawn().getPosition()
                                p=(el.getIdx()[0]-p[0],el.getIdx()[1]-p[1])
                                moved=self._model.update(("m",p))
                                    
                            elif type(el)==view.Wall:
                                slot=el.getIdx()
                                code="h" if el.getVerse()=="horizontal" else "v"
                                moved=self._model.update((code,slot))
                            
                            if moved:
                                self._view.getBoard().clear()


                    if e.type==pg.QUIT:
                        self._game_controller.quit()
                        running=False
                        pg.event.clear()
