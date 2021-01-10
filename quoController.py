import pygame as pg 
import quoModel as model
import quoView as view


class Controller():
    def __init__(self):
        self._model=model.Board(5,[model.Pawn("white",(0,2),4,3),model.Pawn("black",(4,2),0,3)])
        self._view=view.View(self._model)

    def play(self):
        running=True
        while(running and not self._model.checkWinner()):

            self._view.render()
            moved=False
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

            self._model.switchTurn()
