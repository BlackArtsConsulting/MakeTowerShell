from random import randint, uniform

from hypar import glTF

from aecSpace.aecColor import aecColor
from aecSpace.aecPoint import aecPoint
from aecSpace.aecShaper import aecShaper
from aecSpace.aecSpace import aecSpace
from aecSpace.aecSpacer import aecSpacer
from aecSpace.aecSpaceGroup import aecSpaceGroup

def makeTowerShell(xSize: float = 60, 
                   ySize: float = 60, 
                   levels: int = 10,
                   floorType: int = 1):
    
    def randomFloor(point, xSize, ySize):
        try:
            floor = aecSpace()
            shaper = aecShaper()
            if floorType == 1:
                floor.boundary = shaper.makeBox(point, xSize, ySize)
                floor.rotate(uniform(0, 360))
                x = 0
                boundaries = uniform(1, 5)
                tempFloor = aecSpace()
                while x < boundaries:
                    tempFloor.boundary = shaper.makeBox(origin = point, 
                                                        xSize = uniform(65, 100), 
                                                        ySize = uniform(65, 100))
                    tempFloor.rotate(uniform(0, 360))
                    floor.add(tempFloor.points_floor)
                    x += 1
            if floorType == 2:
                floor.boundary = shaper.makeCylinder(aecPoint(point.x + (xSize * 0.5),
                                                              point.y + (ySize * 0.5)),
                                                              radius = (xSize * 0.5))
            if floorType > 2 and floorType < 9:
                floor.boundary = shaper.makePolygon(aecPoint(point.x + (xSize * 0.5), 
                                                             point.y + (ySize * 0.5)),
                                                             radius = (xSize * 0.5), 
                                                             sides = floorType)
            if floorType == 9:
                floor.boundary = shaper.makeCross(point, 
                                                  xSize = xSize, 
                                                  ySize = ySize)                          
            if floorType == 10:
                floor.boundary = shaper.makeH(point, 
                                              xSize = xSize, 
                                              ySize = ySize)
            if floorType == 11:
                floor.boundary = shaper.makeU(point, 
                                              xSize = xSize, 
                                              ySize = ySize)
            floor.height = 15
            return floor
        except:
            return False
              
    spacer = aecSpacer()
    floor = randomFloor(aecPoint(0, 0, 0), xSize, ySize)
    floors = [floor] + spacer.stack(floor, levels - 1)
    if uniform(1, 3) == 1:
        plinth = aecSpace()
        plinthLevels = randint(1, 3)
        plinthHeight = 15 * plinthLevels
        plinth.wrap(floor.points_floor)
        plinth.height = plinthHeight       
        plinth.scale(1.25, 1.25, 1)
        floors = floors[plinthLevels:]
        floors = [plinth] + floors
    colors = [aecColor.blue, aecColor.green, aecColor.white]
    tower = aecSpaceGroup()
    tower.spaces = floors
    tower.setColor(colors[randint(0, 2)])
    if levels >= 10:
        index = 10
        while index < levels:
            tower.scale(0.8, 0.8, 1, index = index)
            index += 1
    if levels >= 30:
        index = 30
        while index < levels:
            tower.scale(0.8, 0.8, 1, index = index)
            index += 1                

    model = glTF()
    colorBlue = model.add_material(0.0, 0.631, 0.945, 0.5, 0.8, "Blue")
    colorWhite = model.add_material(1.0, 1.0, 1.0, 0.5, 0.8, "White")
    colorIndex = randint(0, 1)
    if colorIndex == 0: color = colorBlue
    if colorIndex == 1: color = colorWhite
    area = 0
    for space in floors:
        area += space.area
        spaceMesh = space.mesh_graphic
        model.add_triangle_mesh(spaceMesh.vertices, spaceMesh.normals, spaceMesh.indices, color)   
    return {"model": model.save_base64(), 'computed':{'floors':levels, 'area':area}}

#    model.save_glb('C:\\Users\\Anthony\\Dropbox\\Business\\BlackArts\\Development\\GitHub\\MakeTowerShell\\model.glb')
#
#makeTowerShell(xSize = uniform(40, 100), 
#               ySize = uniform(40, 100), 
#               levels = randint(10, 40), 
#               floorType = randint(1, 11)) 

  



