import pygame

class Shape:
    def __init__(self, num:int, shape:str, color:str, size:str, filled:bool, width:int, height:int) -> None:
        self.colors = {"blue":(0, 0, 255), "red":(255, 0, 0)}
        
        self.num = num
        self.shape = shape
        self.color = color
        self.size = size
        self.filled = filled
        self.width = width
        self.height = height
        self.shape_color = self.colors[color]
        if self.size == "little":
            self.shape_size = min(width, height) // 6
        else:
            self.shape_size = min(width, height) // 3
        if not filled:
            self.shape_width = 5
        else:
            self.shape_width = 0 


    def getSize(self):
        return self.size

    def getShape(self):
        return self.shape
    
    def getColor(self):
        return self.color
    
    def getFilled(self):
        return self.filled

    def getCaract(self):
        return (self.shape, self.color, self.size, self.filled)
    
    def getNum(self):
        return self.num


    def draw(self, surface):
        if self.shape == "circle":
            pygame.draw.circle(surface, self.shape_color, (self.width//2, self.height//2), self.shape_size, width=self.shape_width)
        else:
            pygame.draw.rect(surface, self.shape_color, pygame.Rect((self.width - 2 * self.shape_size) / 2, (self.height - 2 * self.shape_size) / 2, 2 * self.shape_size, 2 * self.shape_size), width=self.shape_width)
    
