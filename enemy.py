import pygame
from pygame import Surface

class Enemy:
    img: Surface
    x: int
    y: int
    xChange: int
    yChange: int = 40
    
    def __init__(self, imgPath: str, initX: int, initY: int, speed: float):
        self.img = pygame.image.load(imgPath)
        self.x = initX
        self.y = initY
        self.xChange = speed
    
    def render(self, screen: Surface):
        screen.blit(self.img, (self.x, self.y))