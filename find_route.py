#import
import sys
import heapq

#find the shortest route from prev
def shortest_route(vertex,  route):
	if vertex.prev:
		route.append(vertex.prev.get_node())
		shortest_route(vertex.prev, route)
	return None
	
#function to find route if it exists
def find_route(graph, source, destination, flag, heuristics):
    
    #set source nodes distance to 0
    source.set_cost(0)

    #insert unvisited nodes into fringe
    fringe_queue = [(vertex.get_cost(),vertex) for vertex in graph]
    heapq.heapify(fringe_queue)
	
    while len(fringe_queue):
		#pop edge with least cost
        unvisited = heapq.heappop(fringe_queue)
        now = unvisited[1]
        now.set_visited()
        #for next adj edge skip if already visited and update route cost
        for next in now.adj:
            if next.visited:
                continue
            if flag == "uninf":
                new_cost = now.get_cost() + now.get_distance(next)
                if new_cost < next.get_cost():
                  next.set_cost(new_cost)
                  next.set_prev(now)
                  if next.get_node() == destination.get_node():
                      print ""
                      print "distance:", next.get_cost(), "km"
            else:
                new_cost = now.get_cost() + now.get_distance(next) + int(heuristics[now.get_node()])
                if new_cost < next.get_cost():
                  next.set_cost(new_cost - int(heuristics[now.get_node()]))
                  next.set_prev(now)
                  if next.get_node() == destination.get_node():
                      print ""
                      print "distance:", next.get_cost(), "km"
        while len(fringe_queue):
            heapq.heappop(fringe_queue)
        fringe_queue = [(vertex.get_cost(),vertex) for vertex in graph if not vertex.visited]
        heapq.heapify(fringe_queue)

#create graph class for storing nodes, adjencies and costs
class Graph:
    def __init__(self):
        self.vertex_dic = {}
        self.number_of_vertices = 0

    def __iter__(self):
        return iter(self.vertex_dic.values())
	
    def insert_node(self, edge):
        self.number_of_vertices = self.number_of_vertices + 1
        new_node = Vertices(edge)
        self.vertex_dic[edge] = new_node
        return new_node

    def get_node(self, n):
        if n in self.vertex_dic:
            return self.vertex_dic[n]
        else:
            return None

    def add_edgeNode(self, city1, city2, cost = 0):
        if city1 not in self.vertex_dic:
            self.insert_node(city1)
        if city2 not in self.vertex_dic:
            self.insert_node(city2)

        self.vertex_dic[city1].add_adjacentNode(self.vertex_dic[city2], cost)
        self.vertex_dic[city2].add_adjacentNode(self.vertex_dic[city1], cost)

    def get_vertices(self):
        return self.vertex_dic.vert()

    def set_prev(self, now):
        self.prev = now

    def get_prev(self, now):
        return self.prev
    
#create object for graph class
g = Graph()

#create vertex class for storing list of nodes
class Vertices:
    def __init__(self, edge):
        self.id = edge
        self.adj = {}
        self.distance = sys.maxint
        self.visited = False
        self.prev = None

    def __eq__(self, new):
        if isinstance(new, self.__class__):
            return self.distance == new.distance
        return Voided

    def __lt__(self, new):
        if isinstance(new, self.__class__):
            return self.distance < new.distance
        return Voided

    def __hash__(self):
        return id(self)

    def __str__(self):
        return str(self.id) + str([i.id for i in self.adj])

    def add_adjacentNode(self, neighbor, cost=0):
        self.adj[neighbor] = cost

    def get_adjacentNode(self):
        return self.adj.vert()

    def get_node(self):
        return self.id

    def get_distance(self, neighbor):
        return self.adj[neighbor]

    def set_cost(self, dist):
        self.distance = dist

    def get_cost(self):
        return self.distance

    def set_prev(self, prev):
        self.prev = prev

    def set_visited(self):
        self.visited = True   

	

#oopen file for reading input data and store edge data into graph
flag = sys.argv[1]
f=open(sys.argv[2], 'r')
data=f.read()
list=data.split()
p=0
while p < (len(list)-3):
    g.insert_node(list[p])
    p=p+3
i=0
j=1
k=2
while k < (len(list)-1):
    g.add_edgeNode(list[i],list[j],int(list[k]))
    i=i+3
    j=j+3
    k=k+3

#arguments for source and destination
city1=sys.argv[3]
city2=sys.argv[4]

heuristics = {}
if flag == 'inf':
    file2 = open(sys.argv[5], 'r')
    for line in file2:
        if "END OF INPUT" in line:
            break
        line_content = line.split()
        city = line_content[0]
        heuristic = line_content[1]
        heuristics[city] = heuristic

#call find route function
find_route(g, g.get_node(city1), g.get_node(city2),flag, heuristics) 

#define source and destination and call function
destination = g.get_node(city2)
path = [destination.get_node()]
shortest_route(destination, path)
list1=path[::-1]

#print path if found
if list1[0]==city2:
    string1=path[::-1]
    print ""
    print "distance: infinity"
    print "route:"
    print "none"
else:
    string1=path[::-1]
    str1 = ' -> '.join(path[::-1])
    print "route:"
length=(len(list)-3)
s=(len(string1)-1)
p=0
q=1
r=2
for j in range(0,s,1):
    for i in range(0,length,1):
        if string1[j] == list[p] and string1[j+1] == list[q]:
            print list[p],"to",list[q],",",list[r],"km"
        elif string1[j] == list[q] and string1[j+1] == list[p]:
            print list[q],"to",list[p],",",list[r],"km"
        p=p+3
        q=q+3
        r=r+3
        if r > length:
            break
    p=0
    q=1
    r=2
