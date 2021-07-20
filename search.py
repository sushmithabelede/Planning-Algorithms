# Basic searching algorithms

'''
The function, node_validitity checks if a given node is valid to be considered as a neighbor of a given nodes
r < 0 or c < 0 or r >= n or c >= n : condition checks if the nodes are outside the scope of the grid
we know that (grid[r][c] == 1) is an obstacle, hence this condition checks if the node is a neighbor is an obstacle
[r,c] in visited_nodes checks if we are considering a redundant node which we had already considered 
'''
def node_validitity(r,c,grid,visited_nodes): 

    if r < 0 or c < 0 or r >= len(grid) or c >= len(grid[0]): 
        k = True
    elif (visited_nodes[r][c]==True) or (grid[r][c] == 1): 
        k = True
    else:
        k = False
    return k

def explore_neighbors_cost(costq,cost,r,c,grid,visited_nodes,parent_nodes,found,goal,start,algo):
    
    #Direction vectors for right,up,left,down. 
    dr=[0,1,0,-1] 
    dc=[1,0,-1,0]

    #Explore the neighbors nodes
    #This loop is to see if any node of the four neighbouring nodes to the current node can be considered as valid nodes   

    for i in range(4):
        rr=r+dr[i] #the neighbor wrt the ith condition
        cc=c+dc[i]
        m = node_validitity(rr,cc,grid,visited_nodes) #checking if this is a valid neighbor
        if  m == True: continue
        
        if algo == 'A': # A represents astar and hence we use the total cost, cost to come + cost to go
            costq.append([total_cost(rr,cc,start,goal),rr,cc]) #costq is updated with the neighbours (note that we are not sorting them yet)
            
        elif algo == 'D': # D represents Dijkstra and hence we use the total cost, cost to go
            costq.append([manhattan_dis(rr,cc,start),rr,cc]) #costq is updated with the neighbours (note that we are not sorting them yet)

        visited_nodes[rr][cc] = True #in a* too, we can update the visited nodes as soon as they are discovered 
        parent_nodes[rr][cc]=[r,c] #here, the parent node for all the i values will be the initial node r,c
	
	#condition to check if the goal exists in these neighbors we searched
        if [rr,cc]== goal: 
            found = True
            break

    return visited_nodes,parent_nodes,costq,found

def explore_neighbors(rq,cq,r,c,grid,visited_nodes,nodes_in_next_layer,parent_nodes,found,goal): 
    
    #Direction vectors for right,up,left,down. 
    dr=[0,1,0,-1] 
    dc=[1,0,-1,0]

    #Explore the neighbors nodes
    #This loop is to see if any node of the four neighbouring nodes to the current node can be considered as valid nodes   

    for i in range(4):
        rr=r+dr[i] #the neighbor wrt the ith condition
        cc=c+dc[i]
        m = node_validitity(rr,cc,grid,visited_nodes) #checking if this is a valid neighbor
        if  m == True: continue
        rq.append(rr) #the queues are updated with the valid neighbor (from the next layer)
        cq.append(cc)
        visited_nodes[rr][cc] = True #as this is bfs, we can update the visited nodes as soon as they are discovered 
        parent_nodes[rr][cc]=[r,c] #here, the parent node for all the i values will be the initial node r,c
        nodes_in_next_layer += 1
	
	#condition to check if the goal exists in these neighbors we searched
        if [rr,cc]== goal: 
            found = True
            break

    return visited_nodes,parent_nodes,nodes_in_next_layer,rq,cq,found

def manhattan_dis(r,c,node): #this is the cost function we use to calculate cost to go
    return abs(r-node[0])+abs(c-node[1])

def total_cost(r,c,start,goal): #in A* we consider the total cost that is cost ot go + cost to come
    cost_to_go = manhattan_dis(r,c,start)
    cost_to_come = manhattan_dis(r,c,goal)
    return cost_to_go+cost_to_come

def bfs(grid,start,goal):

    path = []
    found = False
    steps_total = 0
    row = len(grid)     # map size
    col = len(grid[0])  # map size

    if start == goal:
        found = True
    
    if found == False:
        #We are using two queues for two dimensions here. 
        #I actually tried using a list [r,c] instead of two different queues, r and c. This required some packaging and unpackaging and using two queues seemed the best. 
        rq=cq=[]
        rq.append(start[0])
        cq.append(start[1])
    
        #Parameters to find out the number of nodes left in the current layer
        nodes_left_in_layer = 1
        nodes_in_next_layer = 0

        visited_nodes = [[False for i in range(col)]for j in range(row)] #to keep track of all the nodes which are visited

        #appending the start node in the queues and changing the start node's status to True
        rq.append(start[0])
        cq.append(start[1])
        visited_nodes[start[0]][start[1]] = True

        parent_nodes=[[None for i in range(col)]for j in range(row)] #parent nodes of all the nodes. We use this for backtracking to understand what node was visited and finding the final path
        parent_nodes[start[0]][start[1]]=[0,0]
        path=[]

        while len(rq) > 0:
            r = rq.pop(0)
            c = cq.pop(0)

            if [r,c] == goal:
                found = True
                break

            #we are updating the queues with the nodes from the next layer 
            visited_nodes,parent_nodes,nodes_in_next_layer,rq,cq,found = explore_neighbors(rq,cq,r,c,grid,visited_nodes,nodes_in_next_layer,parent_nodes,found,goal)
                
            if found == True:
                break

	
            if nodes_left_in_layer == 0: #this automatically translates to len(rq) = 0
                nodes_left_in_layer = nodes_in_next_layer #now the next layer becomes the current layer
                nodes_in_next_layer = 0
            
        
        if (found==True):
       
            steps_total = 0
            for i in range (row):
                for j in range (col):
                    if visited_nodes[i][j] == True :
                        steps_total+=1
            print(f"It takes {steps_total} steps to find a path using BFS")
            path.append(goal)	
            parent = parent_nodes[goal[0]][goal[1]] #if we back track, the first node will be the goal from there we can see what are the parent nodes of these
            path.append(parent) 
            while parent != start:
                parent = parent_nodes[parent[0]][parent[1]]
                path.append(parent)
        else:
            print("No path found")

    return path,steps_total

def dfs(grid,start,goal):

    path = []
    steps_total = 0
    found = False

    if start == goal:
        found = True
    
    if found == False:

        found = False
        row = len(grid)     # map size
        col = len(grid[0])  # map size

        #We are using two queues for two dimensions here. 
        #I actually tried using a list [r,c] instead of two different queues, r and c. This required some packaging and unpackaging and using two queues seemed the best. 
        rq=cq=[]
        rq.append(start[0])
        cq.append(start[1])

        visited_nodes = [[False for i in range(col)]for j in range(row)] #to keep track of all the nodes which are visited

        #appending the start node in the queues and changing the start node's status to True. This queue is considered as frontier
        rq.append(start[0])
        cq.append(start[1])

        parent_nodes=[[None for i in range(col)]for j in range(row)] #parent nodes of all the nodes. We use this for backtracking to understand what node was visited and finding the final path
        parent_nodes[start[0]][start[1]]=[0,0]
        path=[]

        while len(rq) > 0:
            r = rq.pop(0) # [r,c] is the current node
            c = cq.pop(0)

            if [r,c] == goal: 
                found = True
                break

            dr=[0,1,0,-1] #possible neighbors of the cvurrent node
            dc=[1,0,-1,0]

            for i in range(4):
                rr=r+dr[i] #the neighbor wrt the ith condition
                cc=c+dc[i]
                m = node_validitity(rr,cc,grid,visited_nodes) #checking if this is a valid neighbor
                if  m == True: continue
                rq.append(rr) #the frontier queues are updated with the valid neighbor (from the next layer)
                cq.append(cc)
                parent_nodes[rr][cc]=[r,c] #here, the parent node for all the i values will be the initial node r,c

            visited_nodes[r][c] = True

        
        if (found==True):
            
            steps_total = 0
            for i in range (row):
                for j in range (col):
                    if visited_nodes[i][j] == True :
                        steps_total+=1
            print(f"It takes {steps_total} steps to find a path using DFS")
            path.append(goal)	
            parent = parent_nodes[goal[0]][goal[1]] #if we back track, the first node will be the goal from there we can see what are the parent nodes of these
            path.append(parent) 
            while parent != start:
                parent = parent_nodes[parent[0]][parent[1]]
                path.append(parent)
        else:
            print("No path found")

    return path,steps_total


def dijkstra(grid, start, goal):

    path = []
    steps_total = 0
    found = False
    row = len(grid)     # map size
    col = len(grid[0])  # map size

    if start == goal:
        found = True    
    
    if found == False:
        #Here, we also defined a costq parameter as a queue which stores the information of the cost to go to that node and row,col of the node
        cost = 0
        costq = []

        visited_nodes = [[False for i in range(col)]for j in range(row)] #to keep track of all the nodes which are visited

        #appending the cost to start node (0) and start node position in the queues and changing the start node's status to True
        costq.append([cost,start[0],start[1]])
        visited_nodes[start[0]][start[1]] = True

        parent_nodes=[[None for i in range(col)]for j in range(row)] #parent nodes of all the nodes. We use this for backtracking to understand what node was visited and finding the final path
        parent_nodes[start[0]][start[1]]=[0,0]
        path=[]

        while len(costq) > 0:
            
            costq.sort() #sorting the order of popping the nodes wrt to cost to go is the only difference between BFS and Dijkstra 
            [cost,r,c] = costq.pop(0) #in Dijkstra, we pop nodes in the queue which have the least cost to go first 

            if [r,c] == goal:
                found = True
                break

            #we are updating the queues with the nodes from the next layer 
            visited_nodes,parent_nodes,costq,found = explore_neighbors_cost(costq,cost,r,c,grid,visited_nodes,parent_nodes,found,goal,start,'D')
                
            if found == True:
                break           
            
        if (found==True):

            for i in range (row):
                for j in range (col):
                    if visited_nodes[i][j] == True :
                        steps_total+=1
            print(f"It takes {steps_total} steps to find a path using Dijkstra")
            path.append(goal)	
            parent = parent_nodes[goal[0]][goal[1]] #if we back track, the first node will be the goal from there we can see what are the parent nodes of these
            path.append(parent) 
            while parent != start:
                parent = parent_nodes[parent[0]][parent[1]]
                path.append(parent)
        else:
            print("No path found")

    return path,steps_total


def astar(grid, start, goal):
    path = []
    steps_total = 0
    found = False
    row = len(grid)     # map size
    col = len(grid[0])  # map size
    
    if start == goal:
        found = True    
    
    if found == False:    
        #Here, we also defined a costq parameter as a queue which stores the information of the cost to go to that node and row,col of the node
        #note that the initial cost here is not zero, only cost to go to node is zero and cost to come to goal
        cost = total_cost(start[0],start[1],start,goal)
        costq = []

        visited_nodes = [[False for i in range(col)]for j in range(row)] #to keep track of all the nodes which are visited

        #appending the cost to start node (0) and start node position in the queues and changing the start node's status to True
        costq.append([cost,start[0],start[1]])
        visited_nodes[start[0]][start[1]] = True

        parent_nodes=[[None for i in range(col)]for j in range(row)] #parent nodes of all the nodes. We use this for backtracking to understand what node was visited and finding the final path
        parent_nodes[start[0]][start[1]]=[0,0]
        path=[]

        while len(costq) > 0:
            steps_total += 1
            costq.sort() #sorting the order of popping the nodes wrt to cost to go is the only difference between BFS and Dijkstra 
            [cost,r,c] = costq.pop(0) #in Dijkstra, we pop nodes in the queue which have the least cost to go first 

            if [r,c] == goal:
                found = True
                break

        #we are updating the queues with the nodes from the next layer 
            visited_nodes,parent_nodes,costq,found = explore_neighbors_cost(costq,cost,r,c,grid,visited_nodes,parent_nodes,found,goal,start,'A')
                
            if found == True:
                break           
        
        if (found==True):
            steps_total += 1 #adding step count for goal
            print(f"It takes {steps_total} steps to find a path using astar")
            path.append(goal)	
            parent = parent_nodes[goal[0]][goal[1]] #if we back track, the first node will be the goal from there we can see what are the parent nodes of these
            path.append(parent) 
            while parent != start:
                parent = parent_nodes[parent[0]][parent[1]]
                path.append(parent)
        else:
            print("No path found")

    return path,steps_total

# Doctest
if __name__ == "__main__":
    # load doc test
    from doctest import testmod, run_docstring_examples
    # Test all the functions
    testmod()
