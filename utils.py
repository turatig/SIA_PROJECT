import heapq

#Helper class used to compute depth-first algorithm to check whether there's a path to a goal row
#from a given position
#Represented as dict={(row,col):neighbours_list}. self._dim:dimension of the grid
class GridGraph():
    def __init__(self,dim):
        self._dim=dim
        self._adjDict=dict()
        self.initadjDict()
        #helper dict to keep temporary edge and partitions
        self._tmp_edges=dict()

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
    
    #set temporary edges from a source to a list of destination blocks
    def setTmpEdges(self,src,dst_list):
        self._tmp_edges={src: dst_list}

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

    def shortestPath2(self,src,toRow):
        visited=set()
        
        def search(node):
            if node[0]==toRow: return [node]
            else:
                visited.add(node)
                minPath=[]
                for n in self._adjDict[node]+self._tmp_edges[node] if node in self._tmp_edges.keys() else self._adjDict[node]:
                    if n not in visited:
                        res=search(n)
                        if res and (not minPath or len(minPath)>=len(res)): 
                            minPath=res
                            
                visited.remove(node)
                return [node]+minPath if minPath else []

        return search(src)

    #Dijkstra algorithm implementation
    #paths cost: length_of_already_found_path+row_distance_from_goal_row
    def shortestPath(self,src,toRow):
        visited=set()
        queue=[(abs(src[0]-toRow)+1,[src])]

        while queue:
            cost,path=heapq.heappop(queue)
            #current node
            n=path[-1]
            if n[0]==toRow: return path
            neigh=self._adjDict[n]+self._tmp_edges[n] if n in self._tmp_edges.keys() else self._adjDict[n]
            for node in neigh:
                heapq.heappush(queue,(abs(src[0]-toRow)+len(path)+1,path+[node]))
        return None
