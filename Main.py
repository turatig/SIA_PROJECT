" Main driver file "
import pygame as pg 
import Controller as controller
from AI import RLAgent,DummyAgent0,DummyAgent1,NegamaxAgent
import matplotlib.pyplot as plt

def main():
    ctrl=controller.Controller()
    agent=RLAgent(ctrl._model,with_trace=True)

    win_rate=ctrl.train(agent,DummyAgent0(ctrl._model),n_match=1)
    plotWinRate(win_rate,"DummyAgent0")

    win_rate=ctrl.train(agent,DummyAgent1(ctrl._model),n_match=1)
    plotWinRate(win_rate,"DummyAgent1")

    win_rate=ctrl.train(agent,NegamaxAgent(ctrl._model),n_match=1)
    plotWinRate(win_rate,"NegaMaxAgent")

    plt.show()

    ctrl.setPlayers([controller.Human(ctrl),agent])
    ctrl.game_loop()

def plotWinRate(win_rate,agent_str):
    fig,ax=plt.subplots(1)
    ax.set_title("Win rate against "+agent_str)
    ax.set_xlabel("Match index")
    ax.set_ylabel("Won match / Played match")
    ax.plot([i for i in range(len(win_rate))],win_rate)

if __name__=="__main__":
    main()
    """ctrl=controller.Controller()
    ctrl.game_loop()"""
