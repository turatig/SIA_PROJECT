import pygame as pg

class Square():
    def __init__(self,screen,topOffset,leftOffset,size,model,idx):
        self._screen=screen
        self._toset=topOffset
        self._loset=leftOffset
        self._wd=self._ht=size
        self._border=2
        self._model=model
        self._idx=idx
        self._highlight=False

    def render(self):

        if self._idx in self._model.getPossibleNextMoves():

            if self._highlight:
                pg.draw.rect(self._screen,pg.Color("yellow"),pg.Rect(self._loset,self._toset,self._wd,self._ht))
            else:
                pg.draw.rect(self._screen,pg.Color("gray"),pg.Rect(self._loset,self._toset,self._wd,self._ht))
        else:
            pg.draw.rect(self._screen,pg.Color("gray"),pg.Rect(self._loset,self._toset,self._wd,self._ht),width=self._border)
    
    def clear(self):
        pg.draw.rect(self._screen,pg.Color("white"),pg.Rect(self._loset,self._toset,self._wd,self._ht))

    def getToset(self): return self._toset
    def getLoset(self): return self._loset
    def getBorder(self): return self._border
    def getSize(self): return self._wd
    def getCenter(self): return (self._loset+self._wd/2,self._toset+self._ht/2)
    def getIdx(self): return self._idx
    def highlight(self):self._highlight=True
    def turnoff(self):self._highlight=False

class Wall():
    def __init__(self,screen,verse,topOffset,leftOffset,width,height,model,index):
        
        self._screen=screen
        self._verse=verse
        self._toset=topOffset
        self._loset=leftOffset
        self._wd=width
        self._ht=height
        self._model=model
        self._idx=index
        self._highlight=False

    def highlight(self):self._highlight=True
    def turnoff(self):self._highlight=False
    def getLoset(self): return self._loset
    def getToset(self):return self._toset
    def getWidth(self):return self._wd
    def getHeight(self):return self._ht
    def getIdx(self): return self._idx
    def getVerse(self): return self._verse

    def render(self):

        if self._model.getWall(self._idx,self._verse)==1:
            pg.draw.rect(self._screen,pg.Color("black"),pg.Rect(self._loset,self._toset,self._wd,self._ht),width=3,border_radius=2)
        elif self._model.getWall(self._idx,self._verse)==2:
            pg.draw.rect(self._screen,pg.Color("black"),pg.Rect(self._loset,self._toset,self._wd,self._ht),border_radius=2)
        elif self._model.isFree(self._idx,self._verse) and self._highlight:
            pg.draw.rect(self._screen,pg.Color("yellow"),pg.Rect(self._loset,self._toset,self._wd,self._ht),border_radius=2)

    def clear(self):
        pg.draw.rect(self._screen,pg.Color("white"),pg.Rect(self._loset,self._toset,self._wd,self._ht),border_radius=2)

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
        self._dim=self._model._dim
        self._sqSize=50
        self._border=10
        self._wd=self._sqSize*self._dim+self._border*(self._dim+1)
        self._ht=self._wd
        self._squares=[]
        self.initSquares()
        self._vwalls=[]
        self._hwalls=[]
        self.initWalls()

    def renderBorder(self):
        pg.draw.rect(self._screen,pg.Color("black"),pg.Rect(self._loset,self._toset,self._wd,self._ht),width=self._border)

    def initSquares(self):
        for i in range(self._dim):
            self._squares.append([])
            for j in range(self._dim):
                self._squares[i].append(Square(self._screen,\
                    self._toset+i*self._sqSize+(i+1)*self._border,self._loset+j*self._sqSize+(j+1)*self._border,\
                    self._sqSize,self._model,(i,j)))

    def initWalls(self):
        for i in range(self._dim-1):
            self._hwalls.append([])
            self._vwalls.append([])

            for j in range(self._dim-1):
                toset=self._toset+(i+1)*self._sqSize+(i+1)*self._border
                loset=self._loset+j*self._sqSize+(j+1)*self._border
                width=self._sqSize*2+self._border
                height=self._border
                self._hwalls[i].append(Wall(self._screen,"horizontal",toset,loset,width,height,\
                                        self._model,(i,j)))

                toset=self._toset+i*self._sqSize+(i+1)*self._border
                loset=self._loset+(j+1)*self._sqSize+(j+1)*self._border
                width=self._border
                height=self._sqSize*2+self._border
                self._vwalls[i].append(Wall(self._screen,"vertical",toset,loset,width,height,\
                                        self._model,(i,j)))

    def render(self):
        self.renderBorder()
        for row in self._squares:
            for sq in row:
                sq.render()
        self.renderWalls()

    def renderWalls(self):
        for i in range(len(self._vwalls)):
            for j in range(len(self._vwalls[i])):
                self._vwalls[i][j].render()
                self._hwalls[i][j].render()

    def getSquaresMap(self):
        return [[sq.getCenter() for sq in row]for row in self._squares]

    def getSquare(self,idx):
        return self._squares[idx[0]][idx[1]]
    def getHorizontalWall(self,idx):
        return self._hwalls[idx[0]][idx[1]]
    def getVerticalWalls(self,idx):
        return self._vwalls[idx[0]][idx[1]]

    def getElementByPos(self,p):
        for row in self._squares:
            for sq in row:
                if p[0]>=sq.getLoset() and p[0]<=sq.getLoset()+sq.getSize()\
                    and p[1]>=sq.getToset() and p[1]<=sq.getToset()+sq.getSize():
                    return sq

        for v in self._vwalls:
            for w in v:
                if p[0]>=w.getLoset() and p[0]<=w.getLoset()+w.getWidth()\
                    and p[1]>=w.getToset() and p[1]<=w.getToset()+self._squares[0][0].getSize():
                    return w
        
        for v in self._hwalls:
            for w in v:
                if p[0]>=w.getLoset() and p[0]<=w.getLoset()+self._squares[0][0].getSize()\
                    and p[1]>=w.getToset() and p[1]<=w.getToset()+w.getHeight():
                    return w

        return False

    def clear(self):
        [[(sq.clear(),sq.turnoff()) for sq in row] for row in self._squares]
        [[(w.clear(),w.turnoff()) for w in row] for row in self._vwalls]
        [[(w.clear(),w.turnoff()) for w in row] for row in self._hwalls]
    
        

                

class View():

    # view class takes in argument a quoridor model
    def __init__(self,model):
        pg.init()
        self._model=model
        self._screenWd=850
        self._screenHt=650
        self._screen=pg.display.set_mode((self._screenWd,self._screenHt))
        self._screen.fill(pg.Color("white"))

        self._board=Board(self._model,self._screen,50,150)
        Pawn.setSquareMap(self._board.getSquaresMap())
        self._pawns=[Pawn(self._screen,p,16) for p in self._model.getPawns()]

        self._maxFps=15
        self._clock=pg.time.Clock()
        pg.display.set_caption("Quoridor")
        pg.font.init()
        self._font=pg.font.SysFont("Courier New",20)

    def render(self):
        self._screen.fill(pg.Color("white"))
        self._board.render()
        for p in self._pawns:
            p.render()
        self.renderWallsLeft()
        self._clock.tick(self._maxFps)
        pg.display.flip()

    def renderWallsLeft(self):
        w=self._font.render("White player: {0} walls left".format(self._model.getPawnByColor("white").getWallsLeft()),1,"black")
        b=self._font.render("Black player: {0} walls left".format(self._model.getPawnByColor("black").getWallsLeft()),1,"black")
        self._screen.blit(w,(150,20))
        self._screen.blit(b,(150,self._board._ht+60))

    def getBoard(self):return self._board




        
