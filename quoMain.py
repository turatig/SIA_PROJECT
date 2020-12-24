" Main driver file "
import pygame as pg 
import quoView as view
import quoModel as model

def main():
    mainModel=model.GameState()
    mainView=view.View(mainModel)
    running=True

    while running:
        for e in pg.event.get():
            if e.type==pg.QUIT:
                running=False
            mainView.render()

if __name__=="__main__":
    main()