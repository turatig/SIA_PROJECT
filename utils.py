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

    #compute the Djikstra Algorithm ordering the by distance in row from goal row
    def shortestPath(self,src,toRow,jumps=None):
        if src[0]==toRow: return [src]

        visited=set()
        queue=[]
        
        visited.add(src)
        #just to fix the case in which the moving pawn can jump
        for node in self._adjDict[src]+jumps if jumps else self._adjDict[src]:
            visited.add(node)
                    
            if node[0]==toRow: return [src]+[node]
            queue.append([src]+[node])
        queue.sort(key=lambda path: abs(path[-1][0]-toRow))

        while queue:
            path=queue.pop(0)
            for node in self._adjDict[path[-1]]:
                if node not in visited:
                    visited.add(node)
                    
                    if node[0]==toRow: return path+[node]
                    queue.append(path+[node])
            queue.sort(key=lambda path: abs(path[-1][0]-toRow))

        return None
