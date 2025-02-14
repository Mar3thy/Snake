import pygame, sys, random

pygame.init()
screen = pygame.display.set_mode((400,500)) # Erzeugt ein display mit 400 x 500 pixeln
clock = pygame.time.Clock() # Objekt, das das 'vergehen der Zeit' im spiel festlegt 
test_surface = pygame.Surface((100,200))
test_surface.fill(pygame.Color('blue'))
test_rect = test_surface.get_rect(center = (200,250)) # Ein Objekt, das besser positioniert ewrden kann, als ein Surface

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    screen.fill([175, 215, 70])
    screen.blit(test_surface, test_rect) # blit = block image transfere
    pygame.display.update()
    clock.tick(60) # legt die FPS auf 60 fest


