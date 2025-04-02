import pygame
import numpy as np

pygame.init()

SCREEN_HEIGHT = 900
SCREEN_WIDTH = 1000
GRAY = (211, 211, 211)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
left_wall = pygame.Rect(0, 0, 10, SCREEN_HEIGHT)
right_wall = pygame.Rect(SCREEN_WIDTH - 10, 0, 10, SCREEN_HEIGHT)
'''
b1_m = abs(float(input("Enter mass of ball 1: ")))
b1_v = abs(float(input("Enter velocity of ball 1: ")))

while True:
    try:
        rest = abs(float(input("Enter restitution: ")))
        break
    except ValueError:
        print("Inavlid Input")

b2_m = abs(float(input("Enter mass of ball 2: ")))
b2_v = -abs(float(input("Enter velocity of ball 2: ")))
'''
class Ball:
    def __init__(self, x, y, m, v, rad, colour):
        self.x = x 
        self.y = y
        self.m = m
        self.v = v
        self.rad = rad
        self.colour = colour

    def draw_balls(self, screen):
        pygame.draw.circle(screen, self.colour, (self.x, self.y), self.rad)

    def update(self):
        self.x += self.v

    def get_rect(self):
        return pygame.Rect(self.x - self.rad, self.y - self.rad, self.rad * 2, self.rad * 2)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Particle Collision Sim")

ball1 = Ball(250, 300, 5, 13, 10, RED)
ball2 = Ball(750, 300, 6, -7, 10, BLUE)

font = pygame.font.SysFont("Arial", 24)

run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    
    screen.fill(GRAY)

    ball1.update()
    ball2.update()

    if ball1.get_rect().colliderect(left_wall):
        ball1.v = -ball1.v
    elif ball1.get_rect().colliderect(right_wall):
        ball1.v = -ball1.v
    elif ball2.get_rect().colliderect(right_wall):
        ball2.v = -ball2.v
    elif ball2.get_rect().colliderect(left_wall):
        ball2.v = -ball2.v
    elif ball1.get_rect().colliderect(ball2.get_rect()):
        ball1.v = -ball1.v
        ball2.v = -ball2.v

    ball1.draw_balls(screen)
    ball2.draw_balls(screen)
    
    velocity_text = font.render(f'Velocity Red: {ball1.v:.2f}m/s   Mass: {b1_m}kg', True, RED)
    velocity_text2 = font.render(f'Velocity Blue: {ball2.v:.2f}m/s   Mass: {b2_m}kg', True, BLUE)
    screen.blit(velocity_text, (20, 20))
    screen.blit(velocity_text2, (20, 50))

    pygame.display.update()
    pygame.time.Clock().tick(60)

pygame.quit()