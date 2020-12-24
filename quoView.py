import pygame as pg

class Square():
    def __init__(self,screen,topOffset,leftOffset,size):
        self._screen=screen
        self._toset=topOffset
        self._loset=leftOffset
        self._wd=self._ht=size
        self._border=2

    def render(self):
        pg.draw.rect(self._screen,pg.Color("gray"),pg.Rect(self._loset,self._toset,self._wd,self._ht),width=self._border)

    def getToset(self): return self._toset
    def getLoset(self): return self._loset
    def getBorder(self): return self._border
    def getSize(self): return self._wd
    def getCenter(self): return (self._loset+self._wd/2,self._toset+self._ht/2)

class Pawn():
    __SQUARE_MAP__=[]
    def __init__(self,screen,pawnModel,radius):
        self._screen=screen
        self._pawnMod=pawnModel
        self._radius=radius

    @staticmethod
    def setSquareMap(l):
        for i in l:
            Pawn.__SQUARE_MAP__.append([p for p in i])

    def setCenter(self,center): self._center=center
    def render(self):
        pos=self._pawnMod.getPosition()
        self.setCenter(Pawn.__SQUARE_MAP__[pos[0]][pos[1]])
        if(self._pawnMod.getColor()=="black"):
            pg.draw.circle(self._screen,pg.Color("black"),self._center,self._radius)
        else:
            pg.draw.circle(self._screen,pg.Color("black"),self._center,self._radius,3)

class Board():

    def __init__(self,model,screen,topOffset,leftOffset):
        self._model=model
        self._screen=screen
        self._toset=topOffset
        self._loset=leftOffset
        self._dim=9
        self._wd=550
        self._ht=550
        self._sqSize=50
        self._border=10
        self._squares=[]
        self.initSquares()

    def renderBorder(self):
        pg.draw.rect(self._screen,pg.Color("black"),pg.Rect(self._loset,self._toset,self._wd,self._ht),width=self._border)

    def initSquares(self):
        for i in range(9):
            self._squares.append([])
            for j in range(9):
                self._squares[i].append(Square(self._screen,self._toset+i*self._sqSize+(i+1)*self._border,self._loset+j*self._sqSize+(j+1)*self._border,self._sqSize))

    def render(self):
        self.renderBorder()
        for row in self._squares:
            for sq in row:
                sq.render()
        self.renderWalls()

    def renderWalls(self):
        hwalls=self._model.getBoard().getHorizontalWalls()
        vwalls=self._model.getBoard().getVerticalWalls()
        for i in range(len(hwalls)):
            for j in range(len(hwalls[i])):
                toset=self._toset+(i+1)*self._sqSize+(i+1)*self._border
                loset=self._loset+j*self._sqSize+(j+1)*self._border
                if(hwalls[i][j]==1):
                    pg.draw.rect(self._screen,pg.Color("black"),pg.Rect(loset,toset,self._sqSize*2+self._border,self._border),width=3,border_radius=2)
                if(hwalls[i][j]==2):
                    pg.draw.rect(self._screen,pg.Color("black"),pg.Rect(loset,toset,self._sqSize*2+self._border,self._border),border_radius=2)
                toset=self._toset+i*self._sqSize+(i+1)*self._border
                loset=self._loset+(j+1)*self._sqSize+(j+1)*self._border
                if(vwalls[i][j]==1):
                    pg.draw.rect(self._screen,pg.Color("black"),pg.Rect(loset,toset,self._border,self._sqSize*2+self._border),width=3,border_radius=2)
                if(vwalls[i][j]==2):
                    pg.draw.rect(self._screen,pg.Color("black"),pg.Rect(loset,toset,self._border,self._sqSize*2+self._border),border_radius=2)

    def getSquaresMap(self):
        return [[sq.getCenter() for sq in row]for row in self._squares]
                

class View():

    # view class takes in argument a quoridor model
    def __init__(self,model):
        pg.init()
        self._model=model
        self._screenWd=850
        self._screenHt=650
        self._screen=pg.display.set_mode((self._screenWd,self._screenHt))
        self._maxFps=15
        self._clock=pg.time.Clock()
        # number of squares in the grid
        self._screen.fill(pg.Color("white"))
        self._board=Board(self._model,self._screen,50,150)
        Pawn.setSquareMap(self._board.getSquaresMap())
        self._pawns=[Pawn(self._screen,p,16) for p in self._model.getPawns()]

    def render(self):
        self._board.render()
        for p in self._pawns:
            p.render()
        #self.renderWallsLeft()
        self._clock.tick(self._maxFps)
        pg.display.flip()

    def renderWallsLeft(self):
        myfont=pg.font.SysFont("Comics Sans MS",30)
        myfont.render("White player has {0} walls left".format(self._model.getWleftWalls()),1,"black")
        #b=myfont.render("Black player has {0} walls left".format(self._model.getBleftWalls()),1,black)
        #self._screen.blit(w,(20,150))




        
