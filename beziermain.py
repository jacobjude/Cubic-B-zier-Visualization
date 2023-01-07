import sys, pygame
from PointsClass import *
from pygame import gfxdraw
from pygame.locals import *
from LineClass import *
pygame.init()

# colors and font
red = (255,15,86)
blue = (67, 181, 238)
white = (255,255,255)
dark_blue = (14,26,37)
circleSize = 15

pygame.display.set_caption("Cubic Bézier Visualization Tool")
font = pygame.font.Font('freesansbold.ttf', 64)

# setup pygame, window resolution
screen = pygame.display.set_mode((1280, 720))
pygame.mouse.set_cursor(*pygame.cursors.diamond)
default_font = pygame.font.get_default_font()
font_renderer = pygame.font.Font(default_font, 64)
width = 1280
height = 720

# T-Value for lerps
tVal = 0.0

# Keep track of oscillating T-Value
global isIncreasing
isIncreasing = True

# colors and gui configuration
red = (255,15,86)
blue = (67, 181, 238)
white = (255,255,255)
dark_blue = (14,26,37)
circleSize = 15

# create initial draggable points
p0 = Point(0 * width + 20, 0 * height + 20)
p1 = Point(0.25 * width, 1 * height - 20)
p2 = Point(0.75 * width, 1 * height - 20)
p3 = Point(1 * width - 20, 0 * height + 20)
draggablePoints = [p0, p1, p2, p3]

# these lines move based on the position of the draggable points
line1 = Line(p0, p1)
line2 = Line(p1, p2)
line3 = Line(p2, p3)
lines = [line1, line2, line3]

# create lerped points from the initial lines (points A, B, and C)
pA = Point(*line1.lerp(tVal))
pB = Point(*line2.lerp(tVal))
pC = Point(*line3.lerp(tVal))
lerpPoints = [pA, pB, pC]

#create two lines from the lerped points
lerpedLine1 = Line(pA, pB)
lerpedLine2 = Line(pB, pC)
lerpedLines = [lerpedLine1, lerpedLine2]

# create lerp from the above two lines (points D and E)
pD = Point(*lerpedLines[0].lerp(tVal))
pE = Point(*lerpedLines[1].lerp(tVal))

# create a line from the above two points
lerpedLine3 = Line(pD, pE)
lerpedLine3.start = pD
lerpedLine3.end = pE

# lerp the above line to create point P (this creates the curve)
pointP = Point(*lerpedLine3.lerp(tVal))

# store the path of point P so that we can draw it later
pathList = []

def drawLines(lineList, color):
    for line in lineList:
        pygame.draw.line(screen, color, line.start.returnTuple(), line.end.returnTuple(), width=2)
        
def findLerpPoints(lineList, tVal):
    return [line.lerp(tVal) for line in lineList]
        
# main loop
clock = pygame.time.Clock()

while True:
    # set fps to 200
    clock.tick(300)
    
    # quit condition
    for event in pygame.event.get():
        if event.type == QUIT: sys.exit()    
        
    # oscillate tVal linearly
    if isIncreasing and tVal < 1.0:
        tVal += 0.001
    elif not isIncreasing and tVal > 0.0:
        tVal -= 0.001
    elif isIncreasing and tVal > 1.0:
         isIncreasing = False
    elif not isIncreasing and tVal < 0.0:
        isIncreasing = True

    # clear screen
    screen.fill(dark_blue)
    # T-Value text
    tText = font.render(f"T: {round(tVal, 3)}", True, white)
    screen.blit(tText, (500, 20))
    
    # get mouse position and relative movement
    relMouseX, relMouseY = pygame.mouse.get_rel()
    mouseX, mouseY = pygame.mouse.get_pos()
    
    # bounding box for dragging the points
    bbox = circleSize + 20
    
    # draw lines and get lerp values for those lines
    drawLines(lines, white)
    lerpPoints = findLerpPoints(lines, tVal)
    
    # update the starts and ends of the lerped lines    
    lerpedLines[0].start = Point(*lerpPoints[0])
    lerpedLines[0].end = Point(*lerpPoints[1])
    lerpedLines[1].start = Point(*lerpPoints[1])
    lerpedLines[1].end = Point(*lerpPoints[2])
    
    # lerp above lines
    pD = Point(*lerpedLines[0].lerp(tVal))
    pE = Point(*lerpedLines[1].lerp(tVal))
    
    # update the final line with the above lerps
    lerpedLine3 = Line(pD, pE)
    lerpedLine3.start = pD
    lerpedLine3.end = pE
    
    # draw blue points 
    for point in lerpPoints:
        pygame.gfxdraw.aacircle(screen, round(point[0]), round(point[1]), circleSize - 4, blue)
        
    # draw red points
    for point in [pD, pE]:
        pygame.gfxdraw.aacircle(screen, round(point.x), round(point.y), circleSize - 4, red)
    
    # draw final line
    pygame.draw.line(screen, red, lerpedLine3.start.returnTuple(), lerpedLine3.end.returnTuple(), width=2)
    
    # point p creates the curve
    pointP = Point(*lerpedLine3.lerp(tVal))
    
    # draw point p
    pygame.gfxdraw.aacircle(screen, round(pointP.x), round(pointP.y), circleSize - 5, white)
    
    # draw point p's path. limiting the list to 2001 values (which is more than enough)
    if len(pathList) <= 2001:
        pathList.append(pointP)
        
    for point in pathList:
        pygame.draw.circle(screen, white, point.returnTuple(), 3, width=4)

    # draw the blue lerped lines
    drawLines(lerpedLines, blue)
    
    # draw the draggable points
    for i in range(len(draggablePoints)):
        
        # draw circle
        pygame.gfxdraw.aacircle(screen, int(draggablePoints[i].x), int(draggablePoints[i].y), circleSize, white)

        # move point when dragged and update lines. reset path.
        if (pygame.mouse.get_pressed()[0] == True
        and mouseX < draggablePoints[i].x + bbox 
        and mouseX > draggablePoints[i].x - bbox
        and mouseY < draggablePoints[i].y + bbox
        and mouseY > draggablePoints[i].y - bbox):
            pathList.clear()
            draggablePoints[i].x += relMouseX
            draggablePoints[i].y += relMouseY
            match i:
                case 0:
                    lines[i].start = draggablePoints[i]
                case 1:
                    lines[i].start = draggablePoints[i]
                    lines[i - 1].end = draggablePoints[i]
                case 2:
                    lines[i].start = draggablePoints[i]
                    lines[i - 1].end = draggablePoints[i]
                case 3:
                    lines[i - 1].end = draggablePoints[i]
                    
    pygame.display.flip()