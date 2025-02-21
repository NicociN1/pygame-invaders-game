import pygame
import random
import math
from enemy import Enemy
from bullet import Bullet
import asyncio
from pygame import mixer
from typing import Literal

pygame.init()

PLAYER_PATH = "player.png"
BULLET_PATH = "bullet.png"
ENEMY_PATH = "enemy.png"
BGM_PATH = "background.wav"
LASER_SOUND_PATH = "laser.wav"

WIDTH = 800
HEIGHT = 600
FPS = 60

PLAYER_SPEED = 5
PLAYER_BULLET_SPEED = 12

SOUNDS_VOLUME = 0.2

enemySpeed = 2
enemyCount = 1
enemyBulletSpeed = 4

screen = pygame.display.set_mode((WIDTH, HEIGHT))
# screen.fill((150, 150, 150))
pygame.display.set_caption('Invaders Game')

# Player
playerImg = pygame.image.load(PLAYER_PATH)
playerX, playerY = 370, 480
playerXChange = 0
playerBulletState: Literal['ready', 'fired'] = 'ready'

def newEnemy() -> Enemy:
    return Enemy(ENEMY_PATH, random.randint(0, 736), random.randint(50, 150), enemySpeed)

enemies: list[Enemy] = [newEnemy()]

bullets: list[Bullet] = []

scoreValue = 0
stageCount = 1

font = pygame.font.SysFont(None, 76)
gameOverText = font.render("GameOver", True, (255, 0, 0))
gameOverRect = gameOverText.get_rect(center=(WIDTH//2, HEIGHT//2))

shootingSound = mixer.Sound(LASER_SOUND_PATH)
shootingSound.set_volume(SOUNDS_VOLUME)

mixer.music.load(BGM_PATH)
mixer.music.set_volume(SOUNDS_VOLUME)
mixer.music.play(-1, 0, 5)

clock = pygame.time.Clock()


async def main():
    global playerX, playerY, playerXChange, playerBulletState, enemySpeed, enemyCount, enemyBulletSpeed, enemies, bullets, scoreValue, stageCount
    
    def player(x, y):
        screen.blit(playerImg, (x, y))

    def isCollision(enemyX, enemyY, bulletX, bulletY):
        distance = math.sqrt(math.pow(enemyX - bulletX, 2) + math.pow(enemyY - bulletY, 2))
        if distance < 48:
            return True
        else:
            return False

    def killEnemy(target: Enemy):
        global enemies
        enemies = list(filter(lambda e: target is not e, enemies))
        
    def fireBullet(x: int, y: int, isFromPlayer: bool) -> Bullet:
        bullets.append(Bullet(BULLET_PATH, x, y, PLAYER_BULLET_SPEED if isFromPlayer else enemyBulletSpeed, isFromPlayer))
    
    def deleteBullet(target: Bullet):
        global bullets
        bullets = list(filter(lambda b: target is not b, bullets))

    endFlag = False
    gameOver = False

    while endFlag == False:
        screen.fill((0, 0, 0))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                endFlag = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    playerXChange = -PLAYER_SPEED
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    playerXChange = PLAYER_SPEED
                if event.key == pygame.K_SPACE and playerBulletState == 'ready':
                    fireBullet(playerX, playerY, True)
                    playerBulletState = 'fired'
                
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT or event.key == pygame.K_a or event.key == pygame.K_d:
                    playerXChange = 0
        
        if not gameOver:
            playerX += playerXChange
            if playerX <= 0:
                playerX = 0
            elif playerX > 736:
                playerX = 736

            for enemy in enemies:
                if enemy.y <= 440:
                    enemy.x += enemy.xChange
                    if enemy.x <= 0:
                        enemy.xChange = enemySpeed
                        enemy.y += enemy.yChange
                    elif enemy.x >= 736:
                        enemy.xChange = -enemySpeed
                        enemy.y += enemy.yChange
                else:
                    gameOver = True
                    break
                
                if random.random() <= 0.01:
                    fireBullet(enemy.x, enemy.y, False)
                        
        
            for bullet in bullets:
                if bullet.y <= 0:
                    playerBulletState = 'ready'
                    deleteBullet(bullet)
                    continue
                bullet.y -= bullet.yChange
                bullet.render(screen)
                
                if bullet.isFromPlayer:
                    for enemy in enemies:      
                        collision = isCollision(enemy.x, enemy.y, bullet.x, bullet.y)
                        if collision:
                            scoreValue += 1
                            killEnemy(enemy)
                        
                            if len(enemies) == 0:
                                stageCount += 1
                                
                                if stageCount % 5 == 0:
                                    enemyCount += 1
                                if stageCount % 10 == 0:
                                    enemySpeed += 2
                                    enemyBulletSpeed = min(20, enemyBulletSpeed + 2)

                                enemies = [newEnemy() for _ in range(enemyCount)]
                            
                            playerBulletState = 'ready'
                            deleteBullet(bullet)
                            continue
                else:
                    collision = isCollision(playerX, playerY, bullet.x, bullet.y)
                    if collision:
                        gameOver = True
                        break

            font = pygame.font.SysFont(None, 32)
            score = font.render(f"Score : {str(scoreValue)}", True, (255, 255, 255))
            screen.blit(score, (20, 50))
            
            player(playerX, playerY)
            for enemy in enemies:
                enemy.render(screen)
        else:
            screen.blit(gameOverText, gameOverRect)

        clock.tick(FPS)
        await asyncio.sleep(0)
        
        pygame.display.update()

asyncio.run(main())