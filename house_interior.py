from mcpi.minecraft import Minecraft
from mcpi import block
import random
from mcpi import entity

import collections
collections.Iterable=collections.abc.Iterable

mc = Minecraft.create()

#This list contains all the types of doors used in the house
doors = [
        block.DOOR_WOOD.id,
        block.DOOR_ACACIA.id,
        block.DOOR_DARK_OAK.id,
        block.DOOR_JUNGLE.id,
        block.DOOR_SPRUCE.id
    ]


#This function compiles the functions below to generate a single story of a house
#Parameters are x,y,z position of north-west corner of the floor (ground), the lengths of the house (subtracted by 1) in the x and y axis, the room wall material and windowsill material
def generate_interior(xPos, yPos, zPos, xlength, zlength, wall_material, windowsill_material):
    splitZAxis = True
    if xlength > zlength:
        splitZAxis = False
    generate_outerwall_torches(xPos, yPos, zPos, xlength, zlength)
    generate_rooms(xPos, yPos, zPos, xlength, zlength, wall_material, splitZAxis)
    generate_windows(xPos, yPos, zPos, xlength, zlength, windowsill_material)



#This function splits a single story of a house into rooms.
#The parameters are the x, y and z position of the north-west corner of the floor (ground), the lengths of the house - 1 in the x and y axis,
#the material of the room walls and the direction of the first split for the house
def generate_rooms(xPos, floor_yPos, zPos, xlength, zlength, wall_material, splitZAxis):
    #specifies the minimum length of blocks for a room
    min_room_size = 4

    #base case: only splits a room if it has a minimum of 10 blocks
    #8 blocks to satisfy the minimum size for each room, 1 block for the wall dividing the rooms, and 1 block to give margin for a door
    if xlength <= 2 * min_room_size + 2 or zlength <= 2 * min_room_size + 2:
        return
    
    #if a room is split along the x axis and perpendicular to the z axis
    if splitZAxis == True:
        # gets a random position for where the room will split, making sure that both rooms have a minimum of 4 blocks of space
        splitLength = random.randint(min_room_size + 1, zlength - (min_room_size + 1))
        # gets a different random position if splitting the room in that location would obstruct a door or a staircase
        while mc.getBlock(xPos, floor_yPos+1, zPos + splitLength) in doors or mc.getBlock(xPos + xlength, floor_yPos+1, zPos + splitLength) in doors or block.STAIRS_WOOD.id in mc.getBlocks(xPos+1, floor_yPos, zPos+splitLength, xPos+xlength-1, floor_yPos+3, zPos+splitLength):
            splitLength = random.randint(min_room_size + 1, zlength - (min_room_size + 1))

        #gets a random position for where the door will be in the newly created room wall
        doorPos = random.randint(2, xlength-2)

        #splits the room into 2 by generating a wall using the specified material
        mc.setBlocks(xPos+1, floor_yPos+1, zPos + splitLength, xPos + xlength - 1, floor_yPos+3, zPos + splitLength, wall_material)

        #calls 2 functions to generate torches and decorations on either side of the created wall
        generate_room_torches(xPos+1, floor_yPos+3, zPos + splitLength, xlength - 1, True)
        generate_decorations(xPos+1, floor_yPos+2, zPos + splitLength, xlength - 1, True)

        #creates a door in the chosen random position in the new wall
        mc.setBlock(xPos + doorPos, floor_yPos+2, zPos + splitLength, block.DOOR_WOOD.id, 8)
        mc.setBlock(xPos + doorPos, floor_yPos+1, zPos + splitLength, block.DOOR_WOOD.id, 0)

        #clears blocks in front of both sides of the created door, just in case a decoration is obstructing it
        mc.setBlocks(xPos + doorPos-1, floor_yPos+1, zPos + splitLength-1, xPos + doorPos+1, floor_yPos+2, zPos+splitLength-1, block.AIR.id)
        mc.setBlocks(xPos + doorPos-1, floor_yPos+1, zPos + splitLength+1, xPos + doorPos+1, floor_yPos+2, zPos+splitLength+1, block.AIR.id)

    #otherwise splits a room along the z axis and perpendicular to the x axis
    else:
        # gets a random position for where the room will split, making sure that both rooms have a minimum of 4 blocks of space
        splitLength = random.randint(min_room_size + 1, xlength - (min_room_size + 1))
        # gets a different random position if splitting the room in that location would obstruct a door or a staircase
        while mc.getBlock(xPos + splitLength, floor_yPos+1, zPos) in doors or mc.getBlock(xPos + splitLength, floor_yPos+1, zPos + zlength) in doors or block.STAIRS_WOOD.id in mc.getBlocks(xPos+splitLength, floor_yPos, zPos+1, xPos+splitLength, floor_yPos+3, zPos+zlength-1):
            splitLength = random.randint(min_room_size + 1, xlength - (min_room_size + 1))
        
        #gets a random position for where the door will be in the newly created room wall
        doorPos = random.randint(2, zlength-2)
        #fixes issue of infinite loop when there are no suitable locations for the dividing wall that wouldn't obstruct a door or staircase while keeping minimum room size
        while doorPos == 6:
            doorPos = random.randint(2, zlength-2)

        #splits the room into 2 by generating a wall using the specified material
        mc.setBlocks(xPos + splitLength, floor_yPos+1, zPos + 1, xPos + splitLength, floor_yPos+3, zPos + zlength - 1, wall_material)

        #calls 2 functions to generate torches and decorations on either side of the created wall
        generate_room_torches(xPos + splitLength, floor_yPos+3, zPos + 1, zlength - 1, False)
        generate_decorations(xPos + splitLength, floor_yPos+2, zPos + 1, zlength - 1, False)

        #creates a door in the chosen random position in the new wall
        mc.setBlock(xPos + splitLength, floor_yPos+2, zPos + doorPos, block.DOOR_WOOD.id, 8)
        mc.setBlock(xPos + splitLength, floor_yPos+1, zPos + doorPos, block.DOOR_WOOD.id, 0)

        #clears blocks in front of both sides of the created door, just in case a decoration is obstructing it
        mc.setBlocks(xPos + splitLength-1, floor_yPos+1, zPos + doorPos-1, xPos + splitLength-1, floor_yPos+2, zPos + doorPos+1, block.AIR.id)
        mc.setBlocks(xPos + splitLength+1, floor_yPos+1, zPos + doorPos-1, xPos + splitLength+1, floor_yPos+2, zPos + doorPos+1, block.AIR.id)
    
    #alternates the direction of how a room will be split for further subdivisions
    splitZAxis = not splitZAxis

    #checks whether the 2 created rooms are bordering each other east-west, or south-north, to identify the north-west corner of both rooms
    if splitZAxis == False:
        #if the rooms are bordering along the x axis, calls the recursive function for the generated northern room and the generated southern room
        generate_rooms(xPos, floor_yPos, zPos, xlength, splitLength, wall_material, splitZAxis)
        generate_rooms(xPos, floor_yPos, zPos + splitLength, xlength, zlength - splitLength, wall_material, splitZAxis)
    else:
        #if the rooms are bordering along the z axis, calls the recursive function for the western room and the eastern room
        generate_rooms(xPos, floor_yPos, zPos, splitLength, zlength, wall_material, splitZAxis)
        generate_rooms(xPos + splitLength, floor_yPos, zPos, xlength - splitLength, zlength, wall_material, splitZAxis)

    

#generate windows for a single story of the house.
#parameters are x,y,z position of north-west floor corner of the house, length/width of the house - 1, and windowsill material (stair block)
def generate_windows(xPos, floor_yPos, zPos, xlength, zlength, windowsill_material):
    window_positions = list()

    #gets the outer wall material (not the corner material if the corners of the house are a different material than the rest of the wall)
    wall_material = mc.getBlock(xPos + 1, floor_yPos+3, zPos)

    #for the walls along the x axis, checks if a position is suitable for a window and doesn't have a door, then adds that position into a list of potential window positions
    for i in [x for x in range(xlength) if x not in range(2, xlength, 4) and x not in range(3, xlength, 4)]:
        if mc.getBlock(xPos+i, floor_yPos+2, zPos) == wall_material and mc.getBlock(xPos+i, floor_yPos+2, zPos+1) == block.AIR.id:
            window_positions.append((xPos+i, floor_yPos+2, zPos))
        
        if mc.getBlock(xPos+i, floor_yPos+2, zPos+zlength) == wall_material and mc.getBlock(xPos+i, floor_yPos+2, zPos+zlength-1) == block.AIR.id:
            window_positions.append((xPos+i, floor_yPos+2, zPos+zlength))
    
    #does the same as above for the 2 walls of the house along the z axis
    for i in [x for x in range(zlength) if x not in range(2, zlength, 4) and x not in range(3, zlength, 4)]:
        if mc.getBlock(xPos, floor_yPos+2, zPos+i) == wall_material and mc.getBlock(xPos+1, floor_yPos+2, zPos+i) == block.AIR.id:
            window_positions.append((xPos, floor_yPos+2, zPos+i))

        if mc.getBlock(xPos+xlength, floor_yPos+2, zPos+i) == wall_material and mc.getBlock(xPos+xlength-1, floor_yPos+2, zPos+i) == block.AIR.id:
            window_positions.append((xPos+xlength, floor_yPos+2, zPos+i))

    for position in window_positions:
        #creates a window for each selected window position
        mc.setBlock(position[0], position[1], position[2], block.GLASS.id)
        mc.setBlock(position[0], position[1]+1, position[2], block.GLASS.id)

        #creates a windowsill for each selected window position, with its direction depending on which outer wall the window is in
        if position[0] == xPos:
            mc.setBlock(position[0] - 1, position[1] - 1, position[2], windowsill_material, 4)
        elif position[0] == xPos + xlength:
            mc.setBlock(position[0] + 1, position[1] - 1, position[2], windowsill_material, 5)
        elif position[2] == zPos:
            mc.setBlock(position[0], position[1] - 1, position[2] - 1, windowsill_material, 6)
        elif position[2] == zPos + zlength:
            mc.setBlock(position[0], position[1] - 1, position[2] + 1, windowsill_material, 7)



#This function generates decorations on either side of a wall.
#parameters are x,y,z position of the western/northern end of a dividing wall, the length of the wall, and the axis of the wall
def generate_decorations(xPos, yPos, zPos, wall_length, isXaxis):
    
    possible_decoration_positions = list()

    #these blocks are not in mcpi.block
    flowerpot = 140
    jukebox = 84
    noteblock = 25
    anvil = 145
    enchanting_table = 116
    cauldron = 118
    brewing_stand = 117

    #gets the material of the wall
    wall_material = mc.getBlock(xPos, yPos + 1, zPos)

    #if the wall is along the x axis, adds all positions from the second block of the wall to the second last block, that doesn't obstruct a door or a staircase
    #and adds it to a list of potential decoration positions
    if isXaxis == True:
        for i in range(1, wall_length-1):
            #makes sure that a decoration isn't placed on top of a staircase
            if mc.getBlock(xPos + i, yPos - 2, zPos - 1) != block.STAIRS_WOOD.id:
                possible_decoration_positions.append((xPos + i, yPos, zPos - 1))
            if mc.getBlock(xPos + i, yPos - 2, zPos + 1) != block.STAIRS_WOOD.id:
                possible_decoration_positions.append((xPos + i, yPos, zPos + 1))
    #if the wall is along the z axis, adds all positions from the second block of the wall to the second last block, that doesn't obstruct a door or a staircase
    #and adds it to a list of potential decoration positions
    else:
        for i in range(1, wall_length-1):
            #makes sure that a decoration isn't placed on top of a staircase
            if mc.getBlock(xPos - 1, yPos, zPos + i) != block.STAIRS_WOOD.id:
                possible_decoration_positions.append((xPos - 1, yPos, zPos + i))
            if mc.getBlock(xPos + 1, yPos, zPos + i) != block.STAIRS_WOOD.id:
                possible_decoration_positions.append((xPos + 1, yPos, zPos + i))
    
    #chooses a variable number of potential positions for decorations
    decoration_positions = random.sample(possible_decoration_positions, wall_length//2)
    
    #for each chosen position for decoration, chooses a random decoration with varying probability of being chosen
    #air blocks are used to clear any previous decorations if they have different block requirements. e.g. bookshelfs are 2 block high, while a furnace is 1 block high
    for position in decoration_positions:
        decoration_type = random.random() * 100

        if decoration_type < 20:
            mc.setBlock(position[0], position[1], position[2], block.BOOKSHELF.id)
            mc.setBlock(position[0], position[1] - 1, position[2], block.BOOKSHELF.id)

        elif decoration_type < 30:
            #flower pot
            mc.setBlock(position[0], position[1] - 1, position[2], flowerpot)
            mc.setBlock(position[0], position[1], position[2], block.AIR.id)

        elif decoration_type < 35:
            mc.setBlock(position[0], position[1] - 1, position[2], block.CRAFTING_TABLE.id)
            mc.setBlock(position[0], position[1], position[2], block.AIR.id)

        elif decoration_type < 40:
            #jukebox
            mc.setBlock(position[0], position[1] - 1, position[2], jukebox)
            mc.setBlock(position[0], position[1], position[2], block.AIR.id)

        elif decoration_type < 45:
            #noteblock
            mc.setBlock(position[0], position[1] - 1, position[2], noteblock)
            mc.setBlock(position[0], position[1], position[2], block.AIR.id)

        elif decoration_type < 50:
            #anvil
            mc.setBlock(position[0], position[1] - 1, position[2], anvil)
            mc.setBlock(position[0], position[1], position[2], block.AIR.id)

        elif decoration_type < 55:
            #enchanting table
            mc.setBlock(position[0], position[1] - 1, position[2], enchanting_table)
            mc.setBlock(position[0], position[1], position[2], block.AIR.id)

        elif decoration_type < 60:
            #cauldron
            mc.setBlock(position[0], position[1] - 1, position[2], cauldron)
            mc.setBlock(position[0], position[1], position[2], block.AIR.id)

        elif decoration_type < 65:
            #brewing stand
            mc.setBlock(position[0], position[1] - 1, position[2], brewing_stand)
            mc.setBlock(position[0], position[1], position[2], block.AIR.id)

        elif decoration_type < 80:
            #sets the chests face direction away from the wall
            face_direction = 0
            if mc.getBlock(position[0], position[1] - 1, position[2] + 1) == wall_material:
                face_direction = 2
            elif mc.getBlock(position[0], position[1] - 1, position[2] - 1) == wall_material:
                face_direction = 3
            elif mc.getBlock(position[0] + 1, position[1] - 1, position[2]) == wall_material:
                face_direction = 4
            else:
                face_direction = 5
            
            mc.setBlock(position[0], position[1] - 1, position[2], block.CHEST.id, face_direction)
            mc.setBlock(position[0], position[1], position[2], block.AIR.id)

        elif decoration_type < 90:
            #sets the furnace's face direction away from the wall
            face_direction = 0
            if mc.getBlock(position[0], position[1] - 1, position[2] + 1) == wall_material:
                face_direction = 2
            elif mc.getBlock(position[0], position[1] - 1, position[2] - 1) == wall_material:
                face_direction = 3
            elif mc.getBlock(position[0] + 1, position[1] - 1, position[2]) == wall_material:
                face_direction = 4
            else:
                face_direction = 5
            
            mc.setBlock(position[0], position[1] - 1, position[2], block.FURNACE_ACTIVE.id, face_direction)
            mc.setBlock(position[0], position[1], position[2], block.AIR.id)

        else:
            #ignores any errors that may occur when spawning an entity inside of a block (previously placed decoration)
            try:
                mc.spawnEntity(position[0], position[1], position[2], entity.PAINTING.id)
            except:
                pass
        

#This function generates torches on both sides of a wall
#parameters are x,y,z position of western/northern end of the wall, the length of the wall, and the axis of the wall.
def generate_room_torches(xPos, yPos, zPos, wall_length, isXaxis):
    #Generates a torch starting from the second block of the wall, every 4 blocks. e.g. 'i' = torch, '-' = empty wall  -i---i---i-
    #the axis of the wall is required for the direction of the torches
    if isXaxis:
        for i in range(2, wall_length - 1, 4):
            mc.setBlock(xPos + i, yPos, zPos - 1, block.TORCH.id, 4)
            mc.setBlock(xPos + i, yPos, zPos + 1, block.TORCH.id, 3)
    else:
        for i in range(1, wall_length - 1, 4):
            mc.setBlock(xPos - 1, yPos, zPos + i, block.TORCH.id, 2)
            mc.setBlock(xPos + 1, yPos, zPos + i, block.TORCH.id, 1)


#This function generates torches on the inside of the outer walls of a house
#parameters are x,y,z position of north-west floor corner of a house, and the lengths minus 1 of the house on the x axis and z axis
def generate_outerwall_torches(xPos, floor_yPos, zPos, xlength, zlength):
    #Generates a torch starting from the second block of the wall, every 4 blocks on the 2 walls along the x axis
    for i in range(2, xlength - 1, 4):
        mc.setBlock(xPos + i, floor_yPos + 3, zPos + 1, block.TORCH.id, 3)
        mc.setBlock(xPos + i, floor_yPos + 3, zPos + zlength - 1, block.TORCH.id, 4)
    
    #Generates a torch starting from the second block of the wall, every 4 blocks on the 2 walls along the z axis
    for i in range(2, zlength - 1, 4):
        if mc.getBlock(xPos + 1, floor_yPos + 3, zPos + i) != block.STAIRS_WOOD.id:
            mc.setBlock(xPos + 1, floor_yPos + 3, zPos + i, block.TORCH.id, 1)
        if mc.getBlock(xPos + xlength - 1, floor_yPos + 3, zPos + i) != block.STAIRS_WOOD.id:
            mc.setBlock(xPos + xlength - 1, floor_yPos + 3, zPos + i, block.TORCH.id, 2)

