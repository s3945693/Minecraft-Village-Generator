from mcpi.minecraft import Minecraft
from mcpi import block
from mcpi import vec3
from time import sleep
from random import Random

import miDic

# these two lines fix the issue for python 3.10
# let us know if this breaks with your version of python
import collections
collections.Iterable=collections.abc.Iterable

# CONSTANT VARIABLES
mc = Minecraft.create()


# Places lamp at the inputted position
def placeLamp(x, y, z):
  mc.setBlocks(x, y, z, x, y+2, z, block.FENCE) # lamp pole
  mc.setBlock(x, y+3, z, block.GLOWSTONE_BLOCK) # lamp
  #check for air otherwise it breaks houses
  if mc.getBlock(x, y+3, z-1) == block.AIR.id:
    mc.setBlock(x, y+3, z-1, block.Block(block.TRAPDOOR.id, 4))
  if mc.getBlock(x, y+3, z+1) == block.AIR.id:
    mc.setBlock(x, y+3, z+1, block.Block(block.TRAPDOOR.id, 5))
  if mc.getBlock(x-1, y+3, z) == block.AIR.id:
    mc.setBlock(x-1, y+3, z, block.Block(block.TRAPDOOR.id, 6))
  if mc.getBlock(x+1, y+3, z) == block.AIR.id:
    mc.setBlock(x+1, y+3, z, block.Block(block.TRAPDOOR.id, 7))
  mc.setBlock(x, y+4, z, block.TRAPDOOR)

# creates a nice 3x3 well
# INPUT: the most north west corner of the well
# OUTPUT: returns the the coordinates of the well corners
def placeWell(x, y, z):
  def createCorner(x, y, z):
    mc.setBlocks(x, y, z, x, y-3, z, block.STONE_BRICK)
    mc.setBlock(x, y+1, z, 139)
    mc.setBlock(x, y+2, z, block.FENCE_NETHER_BRICK)
    mc.setBlock(x, y+3, z, block.STONE_SLAB, 4) # brick slabs
  
  createCorner(x+1, y, z) #return this (left)
  createCorner(x, y, z+1) #return this (bottom)
  createCorner(x+1, y, z+2) #return this (right)
  createCorner(x+2, y, z+1)
  mc.setBlock(x-1, y-1, z+1,block.STONE_BRICK.id)
  #mc.setBlock(x-1, y, z+1, 0)
  mc.setBlock(x+3,y-1,z+1,block.STONE_BRICK.id)
  #mc.setBlock(x+3, y, z+1, 0)
  mc.setBlock(x+1, y-1, z-1,block.STONE_BRICK.id)
  #mc.setBlock(x+1, y, z-1, 0)
  mc.setBlock(x+1, y-1, z+3,block.STONE_BRICK.id)
  #mc.setBlock(x+1, y, z+3, 0)
  #mc.setBlock(x-1, y-1, z+1,z,block.STONE_BRICK.id)

  mc.setBlocks(x+1, y, z+1, x+1, y-3, z+1, block.AIR)
  mc.setBlock(x+1, y-3, z+1, block.WATER)
  mc.setBlock(x+1, y+3, z+1, block.STONE_SLAB_DOUBLE)
  #top, left, right, bottom
  return [(x+3,y-1,z+1),(x+1, y-1, z-1), (x+1, y-1, z+3), (x-1, y-1, z+1)]

# creates a nice pen for a random animal
# INPUT: the most north west corner of the pen
def placePen(x, y, z, xlength, zlength):
  #  "pig": 90,
  #  "sheep": 91,
  #  "cow": 92,
  #  "chicken": 93

  random = Random()

  spawnAmount = random.randrange(2, 5) # number of animals spawned
  animalID = random.randrange(90, 94) # which animal is spawned

  # y+1 so the fence spawns above the ground
  for currX in range(x, x+xlength+1):
    mc.setBlock(currX, mc.getHeight(currX, z)+1, z, block.FENCE, 1)
    mc.setBlock(currX, mc.getHeight(currX, z+zlength)+1, z+zlength, block.FENCE, 1)
  
  # adjust range to account for overlapping area
  for currZ in range(z+1, z+zlength):
    mc.setBlock(x, mc.getHeight(x, currZ)+1, currZ, block.FENCE)
    mc.setBlock(x+xlength, mc.getHeight(x+xlength, currZ)+1, currZ, block.FENCE)
  
  for i in range(spawnAmount): # spawn a random amount of animals
    mc.spawnEntity(x+2, y, z+2, animalID) # +2 to spawn inside the pen
  
  # trying to make the fences not glitch out by updating them
  # mc.setBlock(x, y, z, block.AIR)
  # mc.setBlock(x+xlength, y, z, block.AIR)

  # add log posts to corners because screw fences
  def createCornerPost(x, y, z):
    y = mc.getHeight(x, z)
    mc.setBlock(x, y, z, block.WOOD)
    mc.setBlock(x, y+1, z, block.WOODEN_SLAB)
  createCornerPost(x, y, z)
  createCornerPost(x+xlength, y, z)
  createCornerPost(x, y, z+zlength)
  createCornerPost(x+xlength, y, z+zlength)

  # add fence gate
  # TODO: add ability for fence gate to face any direction?
  mc.setBlock(x+1, y, z, block.FENCE_GATE)
