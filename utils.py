#Helper class used to compute depth-first algorithm to check whether there's a path to a goal row
#from a given position
#Represented as dict={(row,col):neighbours_list}. self._dim:dimension of the grid
class GridGraph():
    def __init__(self,dim):
        self._dim=dim
        self._adjDict=dict()
        self.initadjDict()

    def getDim(self): return self._dim
    def getadjDict(self): return self._adjDict

    def initadjDict(self):
        dirs=[(-1,0),(1,0),(0,-1),(0,1)]
        for i in range(self._dim):
            for j in range(self._dim):
                self._adjDict[(i,j)]=[ (i+d[0],j+d[1]) for d in dirs \
                                if i+d[0]>=0 and i+d[0]<self._dim and j+d[1]>=0 and j+d[1]<self._dim ]

    def cutEdge(self,sq1,sq2):
        self._adjDict[sq1].remove(sq2)
        self._adjDict[sq2].remove(sq1)
    def insertEdge(self,sq1,sq2):
        self._adjDict[sq1].append(sq2)
        self._adjDict[sq2].append(sq1)

    def areNeighbours(self,sq1,sq2):
        try:
            return sq2 in self._adjDict[sq1]
        except KeyError as e:
            return False

    def theresPath(self,src,toRow):

        visited=set()
        visited.add(src)

        def search(src):
            if src[0]==toRow: return True
            else:
                for n in self._adjDict[src]:
                    if n not in visited:
                        visited.add(n)
                        res=search(n)
                        if res: return True
                return False

        return search(src)

    def shortestPath(self,src,toRow):
        visited=set()
        visited.add(src)

        def search(src):
            if src[0]==toRow: return [src]
            else:
                minPath=[]
                for n in self._adjDict[src]:
                    if n not in visited:
                        visited.add(n)
                        res=search(n)
                        if not minPath or len(minPath)>len(res): minPath=res
                visited.remove(src)
                return [src]+minPath

        return search(src)