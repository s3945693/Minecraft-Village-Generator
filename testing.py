from aStar2 import *
from mcpi.minecraft import Minecraft
from betterq import *
import Walls_test

import random
import collections
collections.Iterable=collections.abc.Iterable
import timeit


starttime = timeit.default_timer()
mc = Minecraft.create()

playerPos = mc.player.getPos()
x,y,z = playerPos
x = int(x)
y = int(y)
z = int(z)

forMapCoords = []
doorXZ = []
doorXYZ = []
def genHouse(x,y,z, wellCoord):

    ranLengthX = 15 #width
    ranLengthZ = 20
    num_of_stories = Walls_test.randomise_stories()
    y_staircase = y-1
    y_floor = y

    my_table = [True,False]
    chosen_palette = Walls_test.house_palettes()
    #generates stories, todo: change floor
    for i in range(num_of_stories):
        Walls_test.Generate_House_shell(x,y,z,ranLengthX,ranLengthZ,chosen_palette['main_material'],chosen_palette['Complementary_material'],chosen_palette['floor_material'])
        if i==0:
            door_coords = Walls_test.generate_door(x,y,z,ranLengthX,ranLengthZ, chosen_palette['floor_material'])
            print("Door path coords:", door_coords)
        y = y + 4
    
    Walls_test.roof_triangular(x,y,z,ranLengthX,ranLengthZ,chosen_palette['roof_material_block'],chosen_palette['roof_material_stairs'])

    #rooms.generate_staircase(x,y_staircase,z,num_of_stories)

    #for i in range(num_of_stories):
        #rooms.generate_floor(x,y_floor-1,z,ranLengthX,ranLengthZ,block.WOOD_PLANKS.id,block.STAIRS_STONE_BRICK.id)
        #y_floor = y_floor+4
    #lines to return needed for path generation
    if wellCoord[0] > x:
        forMapCoords.append((door_coords,wellCoord))
    else:
        forMapCoords.append((wellCoord, door_coords))
    
    doorXZ.append((door_coords[0],door_coords[2]))
    doorXYZ.append(door_coords[1])
    return 'Path created between house and well'
genHouse(x,y,z, (x+10,y,z+10))

endtime = timeit.default_timer()
print('This took {} seconds'.format(endtime - starttime))