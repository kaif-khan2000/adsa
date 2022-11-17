

# read the matrix from the file
def readMatrixFromFile(filename):
    matrix = []
    with open(filename) as f:
        matrix = [[int(num) for num in line.split()] for line in f]
    return matrix

    # print the matrix
def printMatrix(matrix):
    for row in matrix:
        for element in row:
            print(element, end=" ")
        print()

# single source shortest path algorithm
def dijkstra(A,s):
    # A is the adjacency matrix
    # s is the source vertex
    # returns the shortest path from s to every other vertex
    # initialize the distance array
    
    # path is the array that stores the shortest path from s to every other vertex
    path = [s]
    
    dist = [float('inf')]*len(A)

    # initialize the predecessor array
    pred = [-1]*len(A)
    # initialize the visited array
    visited = [False]*len(A)
    # set the distance from s to s to 0
    dist[s] = 0
    # set the predecessor of s to s to s
    pred[s] = s+1
    # set the visited of s to True
    visited[s] = True
    # adjacent vertex dist has to be changed
    for i in range(len(A)):
        if A[s][i] != 0:
            dist[i] = A[s][i]
            pred[i] = s
    # while there are unvisited vertices
    count = 0
    while False in visited:
        count += 1
        # find the unvisited vertex with the smallest distance
        minDist = float('inf')
        minVertex = -1
        for i in range(len(A)):
            if visited[i] == False and dist[i] < minDist:
                minDist = dist[i]
                minVertex = i
        # set the visited of minVertex to True
        visited[minVertex] = True
        # for each neighbor of minVertex
        for i in range(len(A)):
            # if the neighbor is unvisited
            if visited[i] == False:
                # if the distance from s to minVertex + the distance from minVertex to i is less than the distance from s to i
                if dist[minVertex] + A[minVertex][i] < dist[i]:
                    # set the distance from s to i to the distance from s to minVertex + the distance from minVertex to i
                    dist[i] = dist[minVertex] + A[minVertex][i]
                    # set the predecessor of i to minVertex
                    pred[i] = minVertex
    
    return dist,pred


# all source shortest path using dijkstra's single source shortest path algorithm
def assp(A):
    # All source shortest path for every vertex in A is stored in B
    B = A.copy()
    pred = [0]*len(A)
    # for each vertex in A
    for i in range(len(A)):
        # compute the shortest path from i to every other vertex
        B[i],pred[i] = dijkstra(A, i)
    return B,pred

# minimum spanning tree using Kruskal's algorithm
def kruskal(A):
    # A is the adjacency matrix
    # returns the minimum spanning tree of A
    # initialize the parent array
    parent = [-1]*len(A)
    # initialize the rank array
    rank = [0]*len(A)
    # initialize the MST array
    MST = []
    # initialize the edges array
    edges = []
    # for each vertex in A
    for i in range(len(A)):
        # for each neighbor of i
        for j in range(len(A)):
            # if i and j are not the same vertex and the edge is not in the edges array
            if i != j and [i,j] not in edges and [j,i] not in edges:
                # add the edge to the edges array
                edges.append([i,j])
    # sort the edges array by weight
    edges.sort(key=lambda x: A[x[0]][x[1]])
    # for each edge in the edges array
    for edge in edges:
        # if the edge does not create a cycle
        if find(parent, edge[0]) != find(parent, edge[1]):
            # add the edge to the MST
            MST.append(edge)
            # union the two vertices
            union(parent, rank, edge[0], edge[1])
    return MST

# union find DS
def find(parent, i):
    # if the parent of i is -1
    if parent[i] == -1:
        # return i
        return i
    # otherwise, return the parent of i
    return find(parent, parent[i])

def union(parent, rank, x, y):
    # find the parent of x
    xset = find(parent, x)
    # find the parent of y
    yset = find(parent, y)
    # if the rank of xset is less than the rank of yset
    if rank[xset] < rank[yset]:
        # set the parent of xset to yset
        parent[xset] = yset
    # otherwise, if the rank of yset is less than the rank of xset
    elif rank[yset] < rank[xset]:
        # set the parent of yset to xset
        parent[yset] = xset
    # otherwise
    else:
        # set the parent of yset to xset
        parent[yset] = xset
        # increment the rank of xset
        rank[xset] += 1


# def printEdge(edge):
#     # print the edge
#     for e in edge:
#         print(e[0]+1,e[1]+1)


# taking edge from MST output and considering actual path.
# i.e converting metric steiner tree to steiner tree
def addEdge(E,x,y,pred):
    if x == y:
        return
    y1 = pred[x][y]
    E[y1][y] = 1
    E[y][y1] = 1
    addEdge(E,x,y1,pred)

def main():
    # read the matrix from the file
    A = readMatrixFromFile("input.txt")

    
    # print the matrix
    print("The input matrix A the program read from the file is displayed below:")
    printMatrix(A)

    # make all zero entries to be infinity
    for i in range(len(A)):
        for j in range(len(A)):
            if A[i][j] == 0 and i!=j:
                A[i][j] = float('inf')
    
    # get the steiner vertices from the user
    # read the vertices until the user enters * to stop
    print("List all the Steiner vertices (type * to quit):")
    steinerVertices = []
    x = input()
    while x != "*":
        steinerVertices.append(int(x))
        x = input()

    # compute all source shortest paths to every vertex.
    B,pred = assp(A)
    

    # remove all the steiner vertices from the graph B
    vertices = [x for x in range(len(B))]
    for v in steinerVertices:
        if v-1 in vertices:
            vertices.remove(v-1)
    lis = []
    for i in range(len(B)):
        for j in range(len(B)):
            if i+1 not in steinerVertices and j+1 not in steinerVertices:
                lis.append(B[i][j])
    n = len(B)-len(steinerVertices)
    
    # B is the new matrix without the steiner vertices
    B = [lis[i:i+n] for i in range(0, len(lis), n)]
    
    # Apply MST on B
    # MST is stored in C
    K = kruskal(B)
    C = []
    cost = 0
    for c in K:
        # making the vertices names valid
        C.append([vertices[c[0]],vertices[c[1]]])
        # calculating the cost
        cost += B[c[0]][c[1]]
    

    # add the steiner vertices back to the MST
    E = [[0]*len(A) for i in range(len(A))]
    for x in C:
        addEdge(E,x[0],x[1],pred)
    
    print("The 2-factor approximate tree we have computed is given below (we describe this tree by listing all the neighbors of all the vertices in the tree):")
    # print the output
    for i in range(len(E)):
        print(f"Neighbors of Vertex {i+1}: ",end=" ")
        for j in range(len(E)):
            if E[i][j] == 1:
                print(str(j+1),end = " ")
        print()
    
    print("The cost of the 2-factor approximate tree is:",cost)

if __name__ == '__main__':
    main()