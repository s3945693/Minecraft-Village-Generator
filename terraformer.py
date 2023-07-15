from cgi import test
from tkinter import NW
from mcpi.minecraft import Minecraft
from mcpi import block
from mcpi import vec3
from time import sleep

# these two lines fix the issue for python 3.10
# let us know if this breaks with your version of python
import collections
collections.Iterable=collections.abc.Iterable

# CONSTANT VARIABLES
# you can change these to what you want
mc = Minecraft.create()

# ignore blocks while terraforming list
# also ignores water for smooth underwater terraforming too
obstructionList = [block.WOOD.id, block.LEAVES.id, block.LEAVES2.id, block.CACTUS.id, block.WATER.id, block.WATER_FLOWING.id, block.WATER_STATIONARY.id, block.PUMPKIN.id, block.MELON.id, block.AIR.id, block.GRASS_TALL.id, block.FLOWER_CYAN.id, block.FLOWER_YELLOW.id, 175]
#175 is double height grass

class XZPos:
  def __init__(self, x, z):
    self.x = x
    self.z = z
    self.coordinates = (x,z)
  
  def __getitem__(self, i):
    return self.coordinates[i]


class Terraformer:
  # these are static class variables which you can change using
  # Terraformer.padding = 15
  # or terraformer.setSmoothRadius(15)
  smoothRadius = 10
  padding = 5
  
  def __init__(self):
    pass
  
  # sets the smooth radius to a max value of 15
  def setSmoothRadius(self, newSmoothRadius):
    self.smoothRadius = 15 if newSmoothRadius > 15 else newSmoothRadius
    #if newSmoothRadius < 0:
      #raise Exception("Tried to smooth a negative distance. Coordinates are overlapping built structures")
  
  # robustly returns a fill block
  def _getFillBlock(self, x, y, z):
    fillBlock = mc.getBlock(x, y, z)
    while fillBlock in obstructionList: #fillBlock cannot be air or water. find the lowest non-air block
      y -= 1
      fillBlock = mc.getBlock(x, y, z)
    
    if fillBlock == block.DIRT.id:
      fillBlock = block.GRASS
    return fillBlock


  # deal with overhands by adding support blocks below
  # the land for the house according to terrain
  # NWCorner is a tuple or Vec3 (x, y, z)
  def _bulldoze(self, NWCorner, xlength, zlength):
    x, y, z = NWCorner
    fillBlock = self._getFillBlock(x, y, z)
    # set base
    mc.setBlocks(x-self.padding, y, z-self.padding, x+xlength+self.padding, y-3, z+zlength+self.padding, fillBlock)
    mc.setBlocks(x-self.padding, y-3, z-self.padding, x+xlength+self.padding, y-100, z+zlength+self.padding, block.STONE) # set stone below
    mc.setBlocks(x-self.padding, y+1, z-self.padding, x+xlength+self.padding, y+100, z+zlength+self.padding, block.AIR) # clear above

    mc.postToChat(f"filled with NW corner {x}, {y}, {z}")
    
  
  #   Acts as mc.getHeight but this will spit out a correct
  #   y value that does not mistake trees/cacti for terrain
  # PARAMETERS:
  #   x, z: the coordinates of point to get yValue for
  #   yLevel: pass in the y level of the point chosen to terraform from. Used as the basis of where to start scanning blocks for proper ground
  # OUTPUT:
  #   the y coordinate of the highest ground block
  def _getYIgnoreObstructions(self, x, z, yLevel=120):
    startHeight = yLevel + 30 # only check from some blocks above where the platform was generated
    minHeight = 10

    testStrip = list(mc.getBlocks(x, minHeight, z, x, startHeight, z))
    testStrip.reverse()
    y = startHeight
    for block in testStrip:
      if block not in obstructionList:
        break
      y -= 1
    return y

  # same as getY, but this will return the coordinate of the top level of the body of water
  # used so that houses generate ON TOP of lakes, not inside them / at the bottom of the ocean
  def getBuildHeight(self, x, z, yLevel=120):
    startHeight = yLevel + 30 # only check from some blocks above where the platform was generated
    minHeight = 10

    testStrip = list(mc.getBlocks(x, minHeight, z, x, startHeight, z))
    testStrip.reverse()
    y = startHeight
    for currblock in testStrip:
      if currblock == block.WATER.id or currblock == block.WATER_STATIONARY.id or currblock not in obstructionList:
        break
      y -= 1
    return y

  # y  ___
  # ^ |   |___
  # | |_______|___
  # 0---------------> x/z
  # equation will describe this sloped line
  def _createLineEquation(self, coord1, coord2, yLevel):
    # these two lines will let the terraformer ignore trees and water,
    y1 = self._getYIgnoreObstructions(coord1.x, coord1.z, yLevel)
    y2 = self._getYIgnoreObstructions(coord2.x, coord2.z, yLevel)

    # check along which axis to draw line
    if coord1.x - coord2.x == 0: # line in z direction
      slope = (y2-y1)/(coord2.z - coord1.z)
      intercept = y1 - (slope * coord1.z)
      return lambda w: (slope*w) + intercept # y = mx + c
    elif coord1.z - coord2.z == 0: # line in z direction
      slope = (y2-y1)/(coord2.x - coord1.x)
      intercept = y1 - (slope * coord1.x)
      return lambda w: (slope*w) + intercept # y = mx + c
    else:
      raise Exception("This is not a straight line!")

  
  # smooth and connect an area defined by NW and SE corners
  # coords in format (x, z), can be tuple or XZPos
  def _smoothen(self, NWCornerSmooth, SECornerSmooth, axis, yLevel, fillBlock=block.GRASS):
    XAxisEquations = []
    ZAxisEquations = []

    # helpful code so that the function can also work with tuples (x, z)
    if isinstance(NWCornerSmooth, tuple):
      NWCornerSmooth = XZPos(NWCornerSmooth[0], NWCornerSmooth[1])
    if isinstance(SECornerSmooth, tuple):
      SECornerSmooth = XZPos(SECornerSmooth[0], SECornerSmooth[1])

    # coords here in the format (x, y) or (z, y) for createLine function
    for xRow in range(int(NWCornerSmooth.x), int(SECornerSmooth.x)):
      ZAxisEquations.append(self._createLineEquation(XZPos(xRow, NWCornerSmooth.z), XZPos(xRow, SECornerSmooth.z), yLevel))
    
    for zRow in range(int(NWCornerSmooth.z), int(SECornerSmooth.z)):
      XAxisEquations.append(self._createLineEquation(XZPos(NWCornerSmooth.x, zRow), XZPos(SECornerSmooth.x, zRow), yLevel))

    # actually smooth the terrain in lines going in lines across z axis (by looping over x)
    # which areas to smooth around the flat area are determined according to this
    for i, x in enumerate(range(int(NWCornerSmooth.x), int(SECornerSmooth.x))):
      equationAlongZ = ZAxisEquations[i]
      for j, z in enumerate(range(int(NWCornerSmooth.z), int(SECornerSmooth.z))):
        # fillBlock = mc.getBlock(x, self._getYIgnoreObstructions(x, z, yLevel), z)
        # commented code above will preserve natural terrain blocks but will be EXTREMELY slow
        if axis == "z":
          # lines of z outside of platform
          # will be drawn from edge to edge
          y = round(equationAlongZ(z))
          mc.setBlocks(x, y+1, z, x, y+100, z, block.AIR) # clear above
          mc.setBlocks(x, y, z, x, y-2, z, fillBlock)
          mc.setBlocks(x, y-3, z, x, y-100, z, block.STONE) # fill below
        elif "x":
          # smooth out the sides along x
          equationAlongX = XAxisEquations[j]
          y = round(equationAlongX(x))
          mc.setBlocks(x, y+1, z, x, y+100, z, block.AIR) # clear above
          mc.setBlocks(x, y, z, x, y-2, z, fillBlock)
          mc.setBlocks(x, y-3, z, x, y-100, z, block.STONE) # fill below
        else:
          raise Exception("Not a valid axis to smooth along")

  # This will create a bush border around the house + padding land
  # with little holes in the center of each side
  def _createBorder(self, NWPadding, SEPadding, yLevel, borderMaterial):
    zMid = (NWPadding.z + SEPadding.z) / 2
    xMid = (NWPadding.x + SEPadding.x) / 2
    yLevel += 1

    #creates a border
    mc.setBlocks(NWPadding.x, yLevel, NWPadding.z, SEPadding.x, yLevel, SEPadding.z, borderMaterial)
    mc.setBlocks(NWPadding.x+1, yLevel, NWPadding.z+1, SEPadding.x-1, yLevel, SEPadding.z-1, block.AIR)

    # gaps in the middle of the border
    mc.setBlocks(NWPadding.x, yLevel, zMid-1, NWPadding.x, yLevel, zMid+1, block.AIR)
    mc.setBlocks(SEPadding.x, yLevel, zMid-1, SEPadding.x, yLevel, zMid+1, block.AIR)
    mc.setBlocks(xMid-1, yLevel, NWPadding.z, xMid+1, yLevel, NWPadding.z, block.AIR)
    mc.setBlocks(xMid-1, yLevel, SEPadding.z, xMid+1, yLevel, SEPadding.z, block.AIR)

  # if water was cleared out, fill it back in around the terraformed land
  # PARAMETERS:
  #   the corners of the entire smoothed area
  def _refillWater(self, NW, SE, yLevel):
    # check for ocean / lakes 5 blocks below flattened terrain
    for y in range(int(yLevel), int(yLevel)-5, -1):
      slice = list(mc.getBlocks(NW.x, y, NW.z, SE.x-1, y, SE.z-1))
      if block.WATER.id in slice or block.WATER_STATIONARY.id in slice:
        zlength = SE.z - NW.z
        zStrips = []
        for i in range(0, len(slice), zlength): # split array in strips along z axis
          zStrips.append(slice[i:i+zlength])
        
        x = NW.x
        z = NW.z
        # turn air blocks into water to restore water level
        for zStrip in zStrips:
          for currBlock in zStrip:
            if currBlock == block.AIR.id:
              mc.setBlock(x, y, z, block.WATER)
            #mc.setBlock(x, y, z, block.WOOD_PLANKS)
            z +=1
          x += 1
          z = NW.z
        break


  # Makes an area flat for building and blends with terrain
  # PARAMETERS:
  #   NWCornen: either a Vec3 or tuple(x, y, z) of the most north west
  #   corner of the house
  #   xlength and zlength: the dimensions of the house which the terraforms should accomodate for
  def flattenArea(self, NWCornerCoords, xlength, zlength):
    x, y, z = NWCornerCoords
    
    NWCorner = XZPos(x, z)
    SECorner = XZPos(NWCorner.x + xlength, NWCorner.z + zlength)
    NWPadding = XZPos(NWCorner.x - self.padding, NWCorner.z - self.padding)
    SEPadding = XZPos(SECorner.x + self.padding, SECorner.z + self.padding)
    NWSmooth = XZPos(NWPadding.x - self.smoothRadius, NWPadding.z - self.smoothRadius)
    SESmooth = XZPos(SEPadding.x + self.smoothRadius, SEPadding.z + self.smoothRadius)

    self._bulldoze(NWCornerCoords, xlength, zlength)

    # smooth 4 around the flat platform times for each side
    fillBlock = self._getFillBlock(x, y, z)

    self._smoothen((SEPadding.x, NWSmooth.z), SESmooth, "x", y, fillBlock) #right
    self._smoothen(NWSmooth, (NWPadding.x, SESmooth.z), "x", y, fillBlock) #left
    self._smoothen((NWSmooth.x, SEPadding.z), SESmooth, "z", y, fillBlock) #top
    self._smoothen(NWSmooth, (SESmooth.x, NWPadding.z), "z", y, fillBlock) #bottom

    self._refillWater(NWSmooth, SESmooth, y)

    # add a nice looking stone slab border if you want
    #self._createBorder(NWPadding, SEPadding, y, block.STONE_SLAB)


    
# testing purposes
if __name__ == "__main__":
  mc = Minecraft.create()
  playerPos = mc.player.getPos()
  x, y, z = playerPos
  x = int(x)
  y = int(y)
  z = int(z)

  mc.postToChat("terraforming...")
  terraformer = Terraformer()
  Terraformer.smoothRadius = 7
  Terraformer.padding = 3

  terraformer.flattenArea((x, y-1, z), 5, 5)
  mc.postToChat(f"flattened with NW corner {x}, {y}, {z}")
