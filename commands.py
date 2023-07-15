from mcpi.minecraft import Minecraft
from mcpi import block
from mcpi import vec3
from time import sleep

from terraformer import Terraformer
import decorations

# these two lines fix the issue for python 3.10
# let us know if this breaks with your version of python
import collections
collections.Iterable=collections.abc.Iterable

# CONSTANT VARIABLES
mc = Minecraft.create()
Terraformer.smoothRadius = 10
Terraformer.padding = 3


status = True
while status == True:
  playerPos = mc.player.getPos()
  x, y, z = playerPos
  x = int(x)
  y = int(y)
  z = int(z)
  
  cmd = ""
  for cmd in mc.events.pollChatPosts():
    if cmd.message == "q":
      status = False
    
    elif cmd.message == "t":
      mc.postToChat("terraforming...")
      terraformer = Terraformer()
      terraformer.flattenArea((x, y-1, z), 5, 5)
      mc.postToChat(f"flattened with NW corner {x}, {y}, {z}")

    elif cmd.message == "lamp":
      decorations.placeLamp(x, y, z)

    elif cmd.message == "well":
      decorations.placeWell(x, y, z)

    elif cmd.message == "pen":
      decorations.placePen(x, y, z, 5, 5)

    elif cmd.message == "runtime":
      arr = mc.getBlocks(x, y, z, x+5, y+5, z+5)
      mc.postToChat(len(list(arr)))


mc.postToChat("quit program")