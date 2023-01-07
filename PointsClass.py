class Point:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y
        
    def __str__(self):
        print(f"X: {self.x}  Y: {self.y}")
        
    def returnTuple(self):
        return (self.x, self.y)
        
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y
        
    def __ne__(self, other):
        return not self.x == other or not self.y == other.y