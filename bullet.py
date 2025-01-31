import pygame
from pygame import Surface

class Bullet:
    img: Surface
    x: int
    y: int
    xChange: int = 0
    yChange: int
    isFromPlayer: bool
    
    def __init__(self, imgPath: str, initX: int, initY: int, speed: float, isFromPlayer: bool):
        self.img = pygame.transform.rotate(pygame.image.load(imgPath), 0 if isFromPlayer else 180)
        self.x = initX
        self.y = initY
        self.yChange = speed if isFromPlayer else -speed
        self.isFromPlayer = isFromPlayer
    
    def render(self, screen: Surface):
        screen.blit(self.img, (self.x + 16, self.y + 16))