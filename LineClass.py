from PointsClass import *
class Line:
    def __init__(self, start, end):
        self.start = start
        self.end = end
        
    def __str__(self):
        return f"({self.start.x}, {self.start.y}) ({self.end.x}, {self.end.y})"
        
    def getSlope():
        return (self.end.y - self.start.y) / (self.end.x - self.start.x)
        
    def lerp(self, tVal):
        return (self.start.x + (self.end.x - self.start.x) * tVal, self.start.y + (self.end.y - self.start.y) * tVal)
        
    def updateStartPoints(self, start):
        self.start.x = start.x
        self.start.y = start.y
 