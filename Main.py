" Main driver file "
import pygame as pg 
import Controller as controller
from AI import RLAgent

def main():
    ctrl=controller.Controller()
    """agent=RLAgent(ctrl._model)
    win_rate=ctrl.train(agent)
    players=[agent,controller.Human(ctrl._model,ctrl._view)]
    ctrl.play(players)"""
    ctrl.play()
    
if __name__=="__main__":
    main()