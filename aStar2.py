
from decorations import placeLamp
from miDic import dicOfItems
import collections
collections.Iterable=collections.abc.Iterable

from mcpi.minecraft import Minecraft
from betterq import *
from doublyLinkedList import *
mc = Minecraft.create()
import time
#x,y,z = mc.player.getPos()
#print(f'Character is currently at {x},{y},{z}')

item = dicOfItems() 
item.createDic()
#x,y,z = -337,72,19

 
door = [
        block.DOOR_WOOD.id,
        block.DOOR_ACACIA.id,
        block.DOOR_DARK_OAK.id,
        block.DOOR_JUNGLE.id,
        block.DOOR_SPRUCE.id
    ]
class Node():
    #https://medium.com/@nicholas.w.swift/easy-a-star-pathfinding-7e6689c7f7b2
    """A node class for A* Pathfinding"""

    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position

        self.g = 0
        self.y = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.position == other.position


def astar(maze, start, end):
    """Returns a list of tuples as a path from the given start to the given end in the given maze"""

    # Create start and end node
    start_node = Node(None, start)
    start_node.g = start_node.h = start_node.f =   0
    start_node.y = maze[start_node.position[0]][start_node.position[1]]
    end_node = Node(None, end)
    end_node.g = end_node.h = end_node.f = 0
    end_node.y = maze[end_node.position[0]][end_node.position[1]]

    # Initialize both open and closed list
    open_list = []
    closed_list = []

    # Add the start node
    open_list.append(start_node)

    # Loop until you find the end
    while len(open_list) > 0:

        # Get the current node
        current_node = open_list[0]
        current_index = 0
        for index, item in enumerate(open_list):
            #print('checking for best node to proceed to')
            if item.f < current_node.f:
                #print('found node with lower f value', item.position)
                current_node = item
                current_index = index

        # Pop current off open list, add to closed list
        open_list.pop(current_index)
        closed_list.append(current_node)
        #print('this entered closed list', current_node.position)

        # Found the goal
        if current_node == end_node:
            path = []
            current = current_node
            while current is not None:
                path.append(current.position)
                current = current.parent
            return path[::-1] # Return reversed path

        # Generate children
        children = []
        for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]: # Adjacent squares

            # Get node position
            node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])

            # Make sure within range
            if node_position[0] > (len(maze) - 1) or node_position[0] < 0 or node_position[1] > (len(maze[len(maze)-1]) -1) or node_position[1] < 0:
                #print('This node was out of range')
                continue

            # Make sure walkable terrain
            if maze[node_position[0]][node_position[1]] == 999:# or maze[node_position[0]][node_position[1]] >4:
                #print('This node was not walkable')
                continue

            # Create new node
            new_node = Node(current_node, node_position)
            new_node.y = maze[node_position[0]][node_position[1]]
            # Append
            children.append(new_node)

        # Loop through children
        for child in children:
           # Child is on the closed list
            is_closed = False
            for closed_child in closed_list:
                if child == closed_child:
                    is_closed = True
            if is_closed : continue

            # Create the f, g, and h values
            changeInY = abs(child.y - current_node.y)
            if changeInY > 1:
                changeInY = 500
            child.g = current_node.g + changeInY
            
            #tempG = current_node.g + maze[child.position[0]][child.position[1]]
            child.h = ((child.position[0] - end_node.position[0]) ** 2) + ((child.position[1] - end_node.position[1]) ** 2) #create a custom heuristic???
            child.f = child.g + child.h

            # Child is already in the open list
            for open_node in open_list:
                if child == open_node and child.g > open_node.g:
                    continue

            # Add the child to the open list
            open_list.append(child)

def createPath(start, end, pathGen, doorCoordsXZ, doorY, actualDoorCoords):
    #start and end must be coord in tuple or list
    vList,maps = getMap(start,end, doorCoordsXZ,doorY)
    #make an input for the start and end points
    #startx = (int(start[0]))
    #starty = (int(start[1]))
    #startz = (int(start[2]))

    # start is a coordinate in the form (x,y,z)
    # end is a coordinate in the form (x,y,z)
    # maze is a 2D array of 0's and n>0's
    # 0 = walkable
    # n = extra cost walkable
    # 999 = unwalkable
    #
    #
    #
    
    paths = []
    for path in pathGen:
        startm = (path[0][0] - start[0]+15,path[0][2]-start[2]+105) #increase this and next line z values if index out of range occurs
        endm =  (path[1][0]-start[0]+15, path[1][2]-start[2]+105)
        print(startm,endm) #debug
        print('Starting to find a path')
        print(path[0], path[1])
        #print(maps)
        paths.append(astar(maps, startm, endm))
        print('Path found')
        print(paths)
        print()
    

    def flatten(A):
        result = []
        for i in range(len(A)):
            if type(A[i]) != list: 
                result = result + [A[i]]
            if type(A[i]) == list:
                result = (result + flatten(A[i]))
        return result
    
    path = flatten(paths)

    toPlaceBlocks = []
    debug = []
    dLL = DoublyLinkedList()
    for vector in (path): #this is to get the cords of the path
        pos = vector[0] #index of x value
        pos2 = vector[1] #index of the z value for that x value
        toPlaceBlocks.append(vList[pos][pos2])
        dLL.add(NodeDLL(vList[pos][pos2]))
        debug.append(((vList[pos][pos2]),(pos,pos2), (maps[pos][pos2])))
    
    n = dLL.head
    
    smoothPlacedBlocks = []
    while n is not None:
        #print(n.data)#should i create a bridge?
        if n.next is not None:
            nextY = n.next.data[1]
        else:
            nextY = n.data[1]
        if n.prev is not None:
            prevY = n.prev.data[1]
        else:
            prevY = n.data[1]
        if prevY == nextY and prevY != n.data[1]:
            smoothPlacedBlocks.append((n.data[0],prevY,n.data[2]))
        else:
            smoothPlacedBlocks.append(n.data)
        n = n.next
    
    iteration = 0

    for vector in smoothPlacedBlocks: #this is to place the path
            if iteration%15 == 0 and iteration != 0 and iteration != len(smoothPlacedBlocks)-1:
                placeLamp(vector[0],vector[1]+1,vector[2])

            mc.setBlock(vector[0],vector[1],vector[2], 98) 
            print(vector)

            iteration = iteration + 1
            if mc.getBlock(vector[0]+1,vector[1],vector[2]+1) != 0 and mc.getBlock(vector[0]+1,vector[1],vector[2]-1) != 0 or (vector[0]+1,vector[2]+1) not in actualDoorCoords:
                print('ran')
                mc.setBlock(vector[0]+1,vector[1],vector[2], 98)
            if (vector[0],vector[2]+1) not in actualDoorCoords:
                print('ran, ',vector[0],vector[2]+1)
                mc.setBlock(vector[0],vector[1],vector[2]+1, 98)
            if (vector[0],vector[2]-1) not in actualDoorCoords:
                print('ran, ',vector[0],vector[2]-1)
                mc.setBlock(vector[0],vector[1],vector[2]-1, 98)
            if (vector[0]-1,vector[2]) not in actualDoorCoords:
                print('ran, ',vector[0]-1,vector[2])
                mc.setBlock(vector[0]-1,vector[1],vector[2], 98)
    print(doorCoordsXZ)
            


    #for x in debug:
        #print(x)
    return'Path built'