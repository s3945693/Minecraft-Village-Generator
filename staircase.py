from mcpi.minecraft import Minecraft
from mcpi import block

import collections
collections.Iterable=collections.abc.Iterable

mc = Minecraft.create()

#This function generates an alternating staircase for the house. It is called only once for each house (not per floor).
# The parameters are the north-west corner of bottom-most floor/ground of the house, and the number of stories.
def generate_staircase(xPos, floor_yPos, zPos, num_stories):
    
    #initialises direction variable
    direction = True

    #doesn't create a staircase if it's not a multi-story house
    if num_stories == 1:
        return

    #for each story of a multi-story house, except for the top floor, generates a staircase then alternates direction for next iteration/story
    for i in range(num_stories - 1):
        if direction:
            create_stairs(xPos+2, floor_yPos+(i*4), zPos+1, 'z', True)
        else:
            create_stairs(xPos+1, floor_yPos+(i*4), zPos+5, 'z', False)
        direction = not direction


#helper function for the generate_staircase function. creates a single staircase with inputed position and direction
def create_stairs(xPos, floor_yPos, zPos, axis, is_facing_east_south):

    #if the alternating staircase is will alternate east/west (x axis) or south/north (z axis)
    if axis == 'x':
        #if the staircase direction is east
        if is_facing_east_south == True:
            #generate staircase facing east
            mc.setBlock(xPos+1, floor_yPos+1, zPos, block.STAIRS_WOOD.id, 0)
            mc.setBlock(xPos+2, floor_yPos+2, zPos, block.STAIRS_WOOD.id, 0)
            mc.setBlock(xPos+3, floor_yPos+3, zPos, block.STAIRS_WOOD.id, 0)
            mc.setBlock(xPos+4, floor_yPos+4, zPos, block.STAIRS_WOOD.id, 0)

            #clears the flooring of the story above for the staircase
            mc.setBlocks(xPos+1, floor_yPos+4, zPos, xPos+3, floor_yPos+4, zPos, block.AIR.id)
        else:
            #generate staircase facing west
            mc.setBlock(xPos-1, floor_yPos+1, zPos, block.STAIRS_WOOD.id, 1)
            mc.setBlock(xPos-2, floor_yPos+2, zPos, block.STAIRS_WOOD.id, 1)
            mc.setBlock(xPos-3, floor_yPos+3, zPos, block.STAIRS_WOOD.id, 1)
            mc.setBlock(xPos-4, floor_yPos+4, zPos, block.STAIRS_WOOD.id, 1)

            #clears the flooring of the story above for the staircase
            mc.setBlocks(xPos-1, floor_yPos+4, zPos, xPos-3, floor_yPos+4, zPos, block.AIR.id)
    else:
        #if the staircase direction is south
        if is_facing_east_south == True:
            #generate staircase facing south
            mc.setBlock(xPos, floor_yPos+1, zPos+1, block.STAIRS_WOOD.id, 2)
            mc.setBlock(xPos, floor_yPos+2, zPos+2, block.STAIRS_WOOD.id, 2)
            mc.setBlock(xPos, floor_yPos+3, zPos+3, block.STAIRS_WOOD.id, 2)
            mc.setBlock(xPos, floor_yPos+4, zPos+4, block.STAIRS_WOOD.id, 2)

            #clears the flooring of the story above for the staircase
            mc.setBlocks(xPos, floor_yPos+4, zPos+1, xPos, floor_yPos+4, zPos+3, block.AIR.id)
        else:
            #generate staircase facing north
            mc.setBlock(xPos, floor_yPos+1, zPos-1, block.STAIRS_WOOD.id, 3)
            mc.setBlock(xPos, floor_yPos+2, zPos-2, block.STAIRS_WOOD.id, 3)
            mc.setBlock(xPos, floor_yPos+3, zPos-3, block.STAIRS_WOOD.id, 3)
            mc.setBlock(xPos, floor_yPos+4, zPos-4, block.STAIRS_WOOD.id, 3)

            #clears the flooring of the story above for the staircase
            mc.setBlocks(xPos, floor_yPos+4, zPos-1, xPos, floor_yPos+4, zPos-3, block.AIR.id)