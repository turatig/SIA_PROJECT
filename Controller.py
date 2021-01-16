import pygame as pg 
import Model as model
import View as view


class Controller():
    def __init__(self):
        self._model=model.Board(5,[model.Pawn("white",(0,2),4,3),model.Pawn("black",(4,2),0,3)])
        self._view=view.View(self._model)
        self._players=[Human(self._model,self._view),Human(self._model,self._view)]

    def play(self):
        running=True
        turn=0
        while(not self._model.checkWinner()):
            
            self._view.render()
            p=self._players[turn]
            res=p.takeAction()
            if not res: 
                break
            turn=(turn+1)%len(self._players)
            self._model.switchTurn()

        print("ya")

class Human():
    def __init__(self,model,view):
        self._model=model
        self._view=view

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
                        el=self._view.getBoard().getElementByPos(pg.mouse.get_pos())
                        if el:
                            if type(el)==view.Square:
                                if el.getIdx() in self._model.getPossibleNextMoves():
                                    self._model.getMovingPawn().setPosition(el.getIdx())
                                    self._view.getBoard().clear()
                                    moved=True
                            elif type(el)==view.Wall:
                                if self._model.insertWall(el.getIdx(),self._model.getMovingPawn().getColor(),el.getVerse()):
                                    self._view.getBoard().clear()
                                    moved=True

                    if e.type==pg.QUIT:
                        running=False

        return running
