from re import M
from sre_constants import MAX_UNTIL
from turtle import heading, window_width
from mcpi import minecraft
from mcpi import block
import random
import house_interior
import staircase
import time

mc = minecraft.Minecraft.create()

def Generate_House_shell(x,y,z,width, length,material,corner_material,floor_material,i):        
    print("Making shell")

    #floor:
    mc.setBlocks(x,y-1,z,x+width,y-1,z+length,floor_material)

    #Make the walls with the lw and coordinates:
    mc.setBlocks(x,y,z,x+width,y+2,z+length,material)
    mc.setBlocks(x+1,y,z+1,x+width-1,y+3,z+length-1,block.AIR)
    # mc.postToChat("COMLPETED HOUSE3")

    #Corners of the house:
    if i != 0:
        mc.setBlocks(x,y-1,z,x,y+2,z,corner_material)
        mc.setBlocks(x+width,y-1,z,x+width,y+2,z,corner_material)
        mc.setBlocks(x,y-1,z+length,x,y+2,z+length,corner_material)
        mc.setBlocks(x+width,y-1,z+length,x+width,y+2,z+length,corner_material)
    else:
        mc.setBlocks(x,y,z,x,y+2,z,corner_material)
        mc.setBlocks(x+width,y,z,x+width,y+2,z,corner_material)
        mc.setBlocks(x,y,z+length,x,y+2,z+length,corner_material)
        mc.setBlocks(x+width,y,z+length,x+width,y+2,z+length,corner_material)
    
def generate_door(x,y,z,width, length, floor_material):
    #get random coordinates for the door:
    list_axis_for_door = ["x_axis","z_axis"]
    axis_for_door = random.choice(list_axis_for_door) #picks either x or z value
    if axis_for_door == "x_axis":
        mc.postToChat("x axis")
        print("door on x axis")
        door_coordinates_x = random.randrange((x+1), (x+width-1))
        temp_list = [z,z+length]
        door_coordinates_z = random.choice(temp_list)
    else:
        door_coordinates_z = random.randrange((z+1), (z+length-1))
        temp_list = [x,x+width]
        door_coordinates_x = random.choice(temp_list)
        mc.postToChat("z axis")
        print("door on z axis")

    door_coordinates_y = y

    #different doors:
    doors = [
        block.DOOR_WOOD.id,
        block.DOOR_ACACIA.id,
        block.DOOR_DARK_OAK.id,
        block.DOOR_JUNGLE.id,
        block.DOOR_SPRUCE.id
    ]
    door_type = random.choice(doors)

    #place door:
    mc.setBlocks(door_coordinates_x,y,door_coordinates_z,door_coordinates_x,y+1,door_coordinates_z,block.AIR)
    mc.setBlock(door_coordinates_x,y+1,door_coordinates_z,door_type,8)
    mc.setBlock(door_coordinates_x,y,door_coordinates_z,door_type,0)
    print('Door placed @',door_coordinates_x,door_coordinates_y,door_coordinates_z)
    print(floor_material)
    for value in [(door_coordinates_x+1,y-1,door_coordinates_z),(door_coordinates_x-1,y-1,door_coordinates_z),(door_coordinates_x,y-1,door_coordinates_z+1),(door_coordinates_x,y-1,door_coordinates_z-1)]:
            x = mc.getBlockWithData(value)
            
            if (x.id) != floor_material and x .id != 5:
                print('This was not floor material', x.id, ' ', floor_material)
                return ((value[0],value[1],value[2])), (door_coordinates_x,door_coordinates_z)
    
    

def randomise_stories():
    stories = random.randrange(1,4) 
    mc.postToChat(f"{stories} Stories")
    return stories

def material():
    #Randomises material
    materials_list = [
    block.BRICK_BLOCK.id,
    (block.WOOD_PLANKS.id,2),
    block.Block(98)                 #stone bricks
    ]
    material = random.choice(materials_list)
    return material

def material_corners():
    materials_list = [
        block.WOOD,                 #oak wood
        block.Block(162),           #acacia wood
        (block.Block(17),1),        #spruce wood
        (block.Block(155),2)        #pillar quartz
    ]
    corner_material = random.choice(materials_list)
    return corner_material
    
def generate_roof(x,y,z,width,length,roof_block,roof_stair):      
    mc.postToChat("Generating roof...")
    
    roofs = [roof_flat,roof_triangular]
    if width == length:
        roof_pyramid(x,y,z,width,length,roof_block,roof_stair)
    else:
        random.choice(roofs)(x,y,z,width,length,roof_block,roof_stair)

def roof_flat(x,y,z,width,length,roof_block,roof_stair):
    y = y-1
    #flat slab:
    mc.setBlocks(x,y,z,x+width,y,z+length,roof_block)
    offset = 1
    width = width + offset
    length = length + offset
    #A bit of texture with stairs:
    mc.setBlocks(x-offset,y,z-offset,x+width,y,z-offset,roof_stair,2)
    mc.setBlocks(x-offset,y,z+length,x+width,y,z+length,roof_stair,3)
    mc.setBlocks(x-offset,y,z,x-offset,y,z+length,roof_stair)
    mc.setBlocks(x+width,y,z,x+width,y,z+length-offset,roof_stair,1)

def roof_pyramid(x,y,z,width,length,roof_block,roof_stair):
    offset = 1
    width = width + offset
    length = length + offset
    height = width/2
    y=y-offset
    
    while length > 0 :
        mc.setBlocks(x-offset,y,z-offset,x+width,y,z-offset,roof_stair,2)
        mc.setBlocks(x-offset,y,z+length,x+width,y,z+length,roof_stair,3)
        mc.setBlocks(x-offset,y,z,x-offset,y,z+length,roof_stair)
        mc.setBlocks(x+width,y,z,x+width,y,z+length-offset,roof_stair,1)
        y=y+1
        length = length - 2
        width = width - 2
        x = x+1
        z = z+1
    y=y-1
    #plug the hole at the top:
    if width==0:
        mc.setBlocks(x-offset,y,z-offset,x,y,z,block.GLOWSTONE_BLOCK)
    else:
        mc.setBlocks(x-offset,y,z-offset,x-offset,y,z-offset,block.GLOWSTONE_BLOCK)
    
def roof_triangular(x,y,z,width,length,roof_block,roof_stair):
    y = y-1
    height = y
    roof_height = 0
    if width < length:
        #The stairs for the roof to give that triangular shape:
        distance = width +2
        offset = -1
        while distance > 0:
            mc.setBlocks(x+offset,y,z-1,x+offset,y,z+length+1, roof_stair)
            mc.setBlocks(x-offset+width,y,z-1,x-offset+width,y,z+length+1,roof_stair,1)
            y = y+1
            distance = distance-2
            offset = offset+1
        if distance == 0:
            
            mc.setBlocks(x+offset,y-1,z,x+offset,y-1,z+length,roof_block)

        #code for the flat sides of the roof to close it off:
        distance = width
        print(distance,x,height,z)
        offset = 0
        mynum = width/2
        if width // 2 == 0:
            mynum = mynum + 1
        while width - distance < mynum:
            mc.setBlocks(x+offset,height,z, x+distance, height, z, roof_block) #cover up front
            mc.setBlocks(x+offset,height,z+length, x+distance, height, z+length, roof_block) #cover up back
            
            distance = distance - 1
            height = height + 1
            offset = offset + 1
            print(f'{distance}, {z}, {(width-distance)},   {width}')
            if width % 2 == 0:
                print("if statement")
                if width-distance - mynum == 0:
                    mc.setBlock(x+offset,height,z-1,roof_stair,2)
                    mc.setBlock(x+offset,height,z+length+1,roof_stair,3)
                print(width-distance, mynum)
                mc.setBlock(x+offset,height,z+length,roof_block)
    if length < width:
        #The stairs for the roof to give that triangular shape:
        distance = length
        offset = 0
        offset1 = 1
        while distance > 0:
            mc.setBlocks(x,y,z+offset,x+width,y,z+offset, roof_stair,2)
            mc.setBlocks(x,y,z-offset+length,x+width,y,z-offset+length,roof_stair,3)
            #mc.setBlocks(x,y,z+offset1,x,y,z+distance-offset1,block.WOOD)
            y = y+1
            distance = distance-2
            offset = offset+1
            #offset1 = offset1+1
            roof_height = roof_height +1
        if distance == 0:
            mc.setBlocks(x,y,z+offset,x+width,y,z+offset,roof_block)
        
        #code for the flat sides of the roof to close it off:
        distance = length-1
        print(distance,x,height,z)
        offset = 1
        mynum = length/2
        if length // 2 == 0:
            mynum = mynum + 1
        while length - distance < mynum:
            mc.setBlocks(x,height,z+offset,x,height,z+distance,roof_block)
            mc.setBlocks(x+width,height,z+offset,x+width,height,z+distance,roof_block)
            distance = distance - 1
            height = height + 1
            offset = offset + 1
            print(f'{distance}, {z}, {(length-distance)},   {length}')
            if length % 2 == 0:
                print("if statement")
                mc.setBlock(x,height,z+offset,roof_block)
                mc.setBlock(x+width,height,z+offset,roof_block)
            
def roof_trianular_2_0(x,y,z,width,length,roof_block,roof_stair):#in progress
    y = y-1
    height = y
    roof_height = 0
    if width < length:
        #The stairs for the roof to give that triangular shape:
        distance = width
        offset = 0
        while distance > 0:
            mc.setBlocks(x+offset,y,z,x+offset,y,z+length, roof_stair)
            mc.setBlocks(x-offset+width,y,z,x-offset+width,y,z+length,roof_stair,1)
            y = y+1
            distance = distance-2
            offset = offset+1
        if distance == 0:
            mc.setBlocks(x+offset,y,z,x+offset,y,z+length,roof_block)

def z_generate_house(x,y,z,width,length):   #testing purposes
    #number of stories:
    num_of_stories = randomise_stories()

    my_table = [True,False]
    y1=y
    y2=y
    chosen_material = material()
    chosen_material_2= material_corners()
    chosen_palette = house_palettes()
    for i in range(num_of_stories):
        print("For loop activated")
        mc.postToChat("for loop activated")
        Generate_House_shell(x,y,z,width,length,chosen_palette['main_material'],chosen_palette['Complementary_material'],chosen_palette['floor_material'])
        y = y+4
        if i==0:
            door_coords = generate_door(x,y,z,width,length)
        time.sleep(0.5)
        staircase.generate_staircase(x,y1-1,z,num_of_stories)
    for i in range(num_of_stories):
        house_interior.generate_floor(x,y2-1,z,width,length,block.WOOD_PLANKS.id,random.choice(my_table))
        y2 = y2+4
    generate_roof(x,y,z,width,length,chosen_palette['roof_material_block'],chosen_palette['roof_material_stairs'])
    print('door coords in generate house funct:',door_coords)
    return door_coords


def z_generate_house_temp(x,y,z,width,length): #testing purposes
    #number of stories:
    num_of_stories = 2

    my_table = [True,False]
    y1=y
    chosen_material = material()
    chosen_material_2= material_corners()
    chosen_palette = house_palettes()
    for i in range(num_of_stories):
        print("For loop activated")
        mc.postToChat("for loop activated")
        Generate_House_shell(x,y,z,width,length,chosen_palette['main_material'],chosen_palette['Complementary_material'],chosen_palette['floor_material'])
        
        if i==0:
            door_coords = generate_door(x,y,z,width,length)
        house_interior.generate_rooms(x,y-1,z,width,length,block.WOOD_PLANKS.id,random.choice(my_table))
        y = y+4
    house_interior.generate_staircase(x,y1-1,z,num_of_stories)
    #generate_roof(x,y,z,width,length)
    print('door coords in generate house funct:',door_coords)
    return door_coords



def house_palettes():
    #roof_material_stairs doubles as windowsill material
    palette_1 = {       #Wooden house with stone brick starirs
        'main_material' : block.WOOD_PLANKS.id,
        'Complementary_material' : block.WOOD.id,
        'roof_material_block' : block.Block(98).id,             #Stone bricks
        'roof_material_stairs' : block.Block(109).id,           #Stone brick stairs
        'floor_material' : (block.Block(5).id,2),               #Birch Planks
        'wall_material': (block.Block(5).id,4)                  #Acacia Planks
    }
    palette_2 = {
        'main_material' : block.Block(98).id,                   #Stone Bricks
        'Complementary_material' : (block.Block(162).id,1),     #dark oak log(162:1)
        'roof_material' : block.Block(164).id,                  #Dark oak stairs
        'roof_material_block' : (block.Block(5).id,5),          #Dark oak planks
        'roof_material_stairs': block.Block(164).id,            #Dark oak stairs
        'floor_material' : (block.Block(98).id),                #Stone bricks
        'wall_material': (block.Block(155).id)                  #Quartz block
    }
    
    palette_3 = {
        'main_material' : (block.Block(5).id,2),                #Birch planks
        'Complementary_material' : (block.Block(155).id,2),     #pillar quartz,
        'roof_material_block' : (block.Block(155).id,1),        #Chizelled quartz
        'roof_material_stairs': block.Block(156).id,            #quartz stairs
        'floor_material' : (block.Block(98).id),                #Stone bricks
        'wall_material': (block.Block(5).id,2)                  #Birch planks
    }
    palette_4 = {
        'main_material' : (block.Block(45).id),                 #Bricks
        'Complementary_material' : block.Block(98).id,          #Stone Bricks
        'roof_material_block' : (block.Block(45).id),           #Bricks
        'roof_material_stairs': block.Block(109).id,            #Stone brick stairs
        'floor_material' : (block.Block(215).id),               #Red Nether bricks
        'wall_material': (block.Block(5).id,2)                  #Birch planks
    }

    palette_5 = {
        'main_material' : (block.Block(155).id),                #Quartz
        'Complementary_material' : (block.Block(251).id,15),    #Black Concrete
        'roof_material_block' : (block.Block(251).id,15),       #Black Concrete
        'roof_material_stairs': block.Block(114).id,            #Nether brick stairs
        'floor_material' : (block.Block(215).id),               #Red Nether bricks
        'wall_material': (block.Block(5).id,2)                  #Birch planks
    }
    palette_6 = {
        'main_material' : (block.Block(112).id),                #Nether bricks 112
        'Complementary_material' : (block.Block(155).id),       #Quartz
        'roof_material_block' : (block.Block(251).id,15),       #Black Concrete
        'roof_material_stairs': block.Block(156).id,            #Quartz stairs
        'floor_material' : (block.Block(155).id),               #Quartz
        'wall_material': (block.Block(215).id)                  #Red Nether Bricks
    }
    #palette 7 bricks and sandstone
    palette_7 = {
        'main_material' : (block.Block(24).id,2),               #Cut Sandstone
        'Complementary_material' : (block.Block(45).id),        #Bricks
        'roof_material_block' : (block.Block(24).id),           #Sandstone
        'roof_material_stairs': block.Block(108).id,            #Brick stairs
        'floor_material' : (block.Block(215).id),               #Red Nether Bricks
        'wall_material': (block.Block(155).id)                  #Quartz
    }

    list_of_palettes = [palette_1, palette_2, palette_3, palette_4, palette_5, palette_6, palette_7]
    chosen_pallete = random.choice(list_of_palettes)
    
    return chosen_pallete

def clear(x,y,z):
    print('Clearing area.')
    #x, y, z = mc.player.getPos()
    mc.setBlocks(x-30,y,z-300,x+35,y+300,z+300,block.AIR)



