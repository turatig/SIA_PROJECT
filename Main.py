" Main driver file "
import pygame as pg 
import Controller as controller
from AI import RLAgent

def main():
    ctrl=controller.Controller()
    agent=RLAgent(ctrl._model,with_trace=True)
    win_rate=ctrl.train(agent)
    
if __name__=="__main__":
    main()