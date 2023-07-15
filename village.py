# Assignment 1 main file
# Feel free to add additional modules/files as you see fit.

from mcpi.minecraft import Minecraft
from mcpi import block
from mcpi import vec3
from time import sleep
import random 

import decorations
import house_interior
import staircase
from terraformer import Terraformer
import aStar2
import Walls_test

# these two lines fix the issue for python 3.10
# let us know if this breaks with your version of python
import collections
collections.Iterable=collections.abc.Iterable
import timeit


starttime = timeit.default_timer()
mc = Minecraft.create()
#/setworldspawn 0 0 0
playerPos = mc.player.getPos()
x,y,z = playerPos
x = int(x)
y = int(y)
z = int(z)

forMapCoords = []
doorXZ = []
doorXYZ = []
actualDoorCoords = []
def genHouse(x,y,z, wellCoord):

    ranLengthX = random.randrange(11,20) #width
    ranLengthZ = random.randrange(11,25)
    num_of_stories = Walls_test.randomise_stories()
    y_staircase = y-1
    y_floor = y
    chosen_palette = Walls_test.house_palettes()
    #terraform the area
    yt = y - 1
    terraformer.setSmoothRadius(4)
    terraformer.flattenArea((x, yt, z), ranLengthX, ranLengthZ)
    #generate the outer layers of the house
    for i in range(num_of_stories):
        Walls_test.Generate_House_shell(x,y,z,ranLengthX,ranLengthZ,chosen_palette['main_material'],chosen_palette['Complementary_material'],chosen_palette['floor_material'],i)
        if i==0:
            door_coords,dC = Walls_test.generate_door(x,y,z,ranLengthX,ranLengthZ,chosen_palette['floor_material'])
            print("Door path coords:", door_coords)
        y = y + 4
    
    Walls_test.generate_roof(x,y,z,ranLengthX,ranLengthZ,chosen_palette['roof_material_block'],chosen_palette['roof_material_stairs'])

    sleep(0.1)
    staircase.generate_staircase(x,y_staircase,z,num_of_stories)

    for i in range(num_of_stories):
        house_interior.generate_interior(x,y_floor-1,z,ranLengthX,ranLengthZ,chosen_palette['wall_material'],chosen_palette['roof_material_stairs'])
        y_floor = y_floor+4
    #lines to return needed for path generation
    
    forMapCoords.append((wellCoord, door_coords))
    actualDoorCoords.append(dC)
    doorXZ.append((door_coords[0],door_coords[2]))
    doorXYZ.append(door_coords[1])
    return 'Path created between house and well'

terraformer = Terraformer()

#first create a well, connect to another well. each well has two/three houses connected to it
coordToGenMap = []

def createWells(x,y,z,num):
    #generate num of wells, and records their coordinates
    coordsOfWells = []
    Terraformer.padding = 1
    terraformer.setSmoothRadius(3)
    y -= 1
    for number in range(num):
        terraformer.flattenArea((x, y, z), 3, 3)
        coordsOfWells.append(decorations.placeWell(x,y+1,z))
        
        if number == num-1:
            #used for map creation, return value of first wells top edge and last created wells bottom edge
            coordToGenMap.append((coordsOfWells[0][0],coordsOfWells[number][3]))
        #chekc if block is leave
        x = x+random.randrange(35,40,1)
        z = z+random.randrange(-10,10,5)
        y = terraformer.getBuildHeight(x, z)

        if number > 0:
            #used for map creation
            forMapCoords.append((coordsOfWells[number-1][0], coordsOfWells[number][3]))
    return coordsOfWells

# place a random amount of wells
# and generate random houses surrounding these central wells
numWells = 2
CoorForWells = createWells(x, y, z, numWells)
iteration = 0
terraformer.setSmoothRadius(5)
Terraformer.padding = 3
for well in CoorForWells:
    #GEN HOUSE LEFT OF WELL
    x = well[1][0]+ random.randrange(-5,5,2)
    z = well[1][2]+ random.randrange(-45,-35,5)
    y = terraformer.getBuildHeight(x, z)
    genHouse(x,y+1,z, well[1])
    
    #GEN HOUSE RIGHT OF WELL
    x = well[2][0]+ random.randrange(-5,5,2)
    z = well[2][2]+ random.randrange(10,20,5)
    y = terraformer.getBuildHeight(x, z)
    genHouse(x,y+1,z, well[2])
    
    iteration  = iteration + 1
    if iteration == len(CoorForWells): # randomise chance of end house spawning only if there are 3 wells
        chance = random.random()
        if numWells == 2:
            chance = 1

        if chance > 0.5:
            #GEN A HOUSE AT TOP OF WELL IF LAST
            x = well[0][0]+ random.randrange(30,32,1)
            z = well[0][2]+ random.randrange(-5,5,2)
            y = terraformer.getBuildHeight(x, z)
            genHouse(x,y+1,z, well[0])

# create paths between wells and houses
aStar2.createPath(coordToGenMap[0][0], coordToGenMap[0][1], forMapCoords, doorXZ,doorXYZ,actualDoorCoords)

endtime = timeit.default_timer()
print('This took {} seconds'.format(endtime - starttime))
print('COOL!!!! AWESOME!!!')
