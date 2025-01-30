import pygame
import random
import math
from enemy import Enemy
import asyncio

async def main():
    pygame.init()

    WIDTH = 800
    HEIGHT = 600
    FPS = 60

    PLAYER_SPEED = 5
    BULLET_SPEED = 8

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    # screen.fill((150, 150, 150))
    pygame.display.set_caption('Invaders Game')

    # Player
    playerImg = pygame.image.load('player.png')
    playerX, playerY = 370, 480
    playerX_change = 0

    # enemyImg = pygame.image.load('enemy.png')
    # enemyX = random.randint(0, 736)
    # enemyY = random.randint(50, 150)
    # enemyX_change, enemyY_change = enemy_speed, 40
    enemySpeed = 2
    enemyCount = 1

    def newEnemy() -> Enemy:
        return Enemy('enemy.png', random.randint(0, 736), random.randint(50, 150), enemySpeed)

    enemies: list[Enemy] = [newEnemy()]

    bulletImg = pygame.image.load('bullet.png')
    bulletX, bulletY = 0, 480
    bulletX_change, bulletY_change = 0, BULLET_SPEED
    bullet_state = 'ready'

    score_value = 0
    stage_count = 1

    font = pygame.font.SysFont(None, 76)
    gameOverText = font.render("GameOver", True, (255, 0, 0))
    gameOverRect = gameOverText.get_rect(center=(WIDTH//2, HEIGHT//2))

    clock = pygame.time.Clock()

    def player(x, y):
        screen.blit(playerImg, (x, y))

    def fire_bullet(x, y):
        global bullet_state
        bullet_state = 'fire'
        screen.blit(bulletImg, (x + 16, y + 16))

    def isCollision(enemyX, enemyY, bulletX, bulletY):
        distance = math.sqrt(math.pow(enemyX - bulletX, 2) + math.pow(enemyY - bulletY, 2))
        if distance < 48:
            return True
        else:
            return False

    def killEnemy(target: Enemy):
        global enemies
        enemies = list(filter(lambda e: target is not e, enemies))

    endFlag = False
    gameOver = False

    while endFlag == False:
        screen.fill((0, 0, 0))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                endFlag = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    playerX_change = -PLAYER_SPEED
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    playerX_change = PLAYER_SPEED
                if event.key == pygame.K_SPACE or event.key == pygame.K_KP_ENTER:
                    if bullet_state is 'ready':
                        bulletX = playerX
                        fire_bullet(bulletX, bulletY)
                
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT or event.key == pygame.K_a or event.key == pygame.K_d:
                    playerX_change = 0
        
        if not gameOver:
            playerX += playerX_change
            if playerX <= 0:
                playerX = 0
            elif playerX > 736:
                playerX = 736

            for enemy in enemies:
                if enemy.y <= 440:
                    enemy.x += enemy.x_change
                    if enemy.x <= 0:
                        enemy.x_change = enemySpeed
                        enemy.y += enemy.y_change
                    elif enemy.x >= 736:
                        enemy.x_change = -enemySpeed
                        enemy.y += enemy.y_change
                else:
                    gameOver = True
                collision = isCollision(enemy.x, enemy.y, bulletX, bulletY)
                if collision:
                    bulletY = 480
                    bullet_state = 'ready'
                    score_value += 1
                    killEnemy(enemy)
                
                    if len(enemies) == 0:
                        stage_count += 1
                        
                        if stage_count % 5 == 0:
                            enemySpeed += 1
                        if stage_count % 10 == 0:
                            enemyCount += 1

                        print(enemyCount)
                    
                        enemies = [newEnemy() for _ in range(enemyCount)]
                    
        
            if bulletY <= 0:
                bulletY = 480
                bullet_state = 'ready'

            if bullet_state is 'fire':
                fire_bullet(bulletX, bulletY)
                bulletY -= bulletY_change

            font = pygame.font.SysFont(None, 32)
            score = font.render(f"Score : {str(score_value)}", True, (255, 255, 255))
            screen.blit(score, (20, 50))
        
        else:
            screen.blit(gameOverText, gameOverRect)

        player(playerX, playerY)
        for enemy in enemies:
            enemy.render(screen)

        clock.tick(FPS)
        await asyncio.sleep(0)
        
        pygame.display.update()

asyncio.run(main())