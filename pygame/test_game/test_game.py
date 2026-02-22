import pygame
import sys

pygame.init()

# 画面サイズ
WIDTH = 800
HEIGHT = 600

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Day 1 - Game Loop")

running = True

clock = pygame.time.Clock()

x = WIDTH // 2
y = HEIGHT // 2

speed = 10

RADIUS = 50

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT]:
        x -= speed
    if keys[pygame.K_RIGHT]:
        x += speed
    if keys[pygame.K_UP]:
        y -= speed
    if keys[pygame.K_DOWN]:
        y += speed

    x = max(RADIUS, min(WIDTH - RADIUS, x))
    y = max(RADIUS, min(HEIGHT - RADIUS, y))

    screen.fill((30, 30, 30))

    pygame.draw.circle(screen, (250, 0, 0), (x, y), RADIUS)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()