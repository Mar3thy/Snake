import pygame, sys, random
from pygame.math import Vector2

class Button:
    def __init__(self, x, y, image, scale, rect):
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (int(width*scale), int(height * scale)))
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False
        self.rect = rect
    
    def draw(self):
        action = False
        # get mouse position
        pos = pygame.mouse.get_pos()
        # check if mouse is over the button
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] and self.clicked == False:
                self.clicked = True
                action = True
        if not pygame.mouse.get_pressed()[0]:
            self.clicked = False
        # draw button
        screen.blit(self.image, (self.rect.x, self.rect.y))
        return action

class SNAKE:
    def __init__(self):
        self.body = [Vector2(5,10), Vector2(4,10), Vector2(3,10)]
        self.direction = Vector2(0,0)
        self.new_block = False

        self.head_up = pygame.image.load('pygame_app/Graphics/snakes/b_head_up.png').convert_alpha()
        self.head_down = pygame.image.load('pygame_app/Graphics/snakes/b_head_down.png').convert_alpha()
        self.head_right = pygame.image.load('pygame_app/Graphics/snakes/b_head_right.png').convert_alpha()
        self.head_left = pygame.image.load('pygame_app/Graphics/snakes/b_head_left.png').convert_alpha()
		
        self.tail_up = pygame.image.load('pygame_app/Graphics/snakes/b_tail_up.png').convert_alpha()
        self.tail_down = pygame.image.load('pygame_app/Graphics/snakes/b_tail_down.png').convert_alpha()
        self.tail_right = pygame.image.load('pygame_app/Graphics/snakes/b_tail_right.png').convert_alpha()
        self.tail_left = pygame.image.load('pygame_app/Graphics/snakes/b_tail_left.png').convert_alpha()

        self.body_vertical = pygame.image.load('pygame_app/Graphics/snakes/b_body_vertical.png').convert_alpha()
        self.body_horizontal = pygame.image.load('pygame_app/Graphics/snakes/b_body_horizontal.png').convert_alpha()

        self.body_tr = pygame.image.load('pygame_app/Graphics/snakes/b_body_tr.png').convert_alpha()
        self.body_tl = pygame.image.load('pygame_app/Graphics/snakes/b_body_tl.png').convert_alpha()
        self.body_br = pygame.image.load('pygame_app/Graphics/snakes/b_body_br.png').convert_alpha()
        self.body_bl = pygame.image.load('pygame_app/Graphics/snakes/b_body_bl.png').convert_alpha()
    
        self.crunch_sound = pygame.mixer.Sound('pygame_app/Sound/503492__larakaa__yumyum.wav')

    def draw_snake(self):
        self.update_head_graphics()
        self.update_tail_graphics()

        for index, block in enumerate(self.body):
            x_pos = int(block.x * cell_size)
            y_pos = int(block.y * cell_size)
            block_rect = pygame.Rect(x_pos, y_pos, cell_size, cell_size)
        
            if index == 0:
                screen.blit(self.head, block_rect)
            elif index == len(self.body) - 1:
                screen.blit(self.tail, block_rect)
            else:
                previous_block = self.body[index + 1] - block
                next_block = self.body[index - 1] - block
                if previous_block.x == next_block.x:
                    screen.blit(self.body_vertical, block_rect)
                elif previous_block.y == next_block.y:
                    screen.blit(self.body_horizontal, block_rect)
                else:
                    if previous_block.x == -1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == -1:
                        screen.blit(self.body_tl, block_rect)
                    elif previous_block.x == -1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == -1:
                        screen.blit(self.body_bl, block_rect)
                    elif previous_block.x == 1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == 1:
                        screen.blit(self.body_tr, block_rect)
                    elif previous_block.x == 1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == 1:
                        screen.blit(self.body_br, block_rect)
    
    def update_head_graphics(self):
        head_relation = self.body[1] - self.body[0]
        if head_relation == Vector2(1,0): self.head = self.head_left
        elif head_relation == Vector2(-1,0): self.head = self.head_right
        elif head_relation == Vector2(0,1): self.head = self.head_up
        elif head_relation == Vector2(0,-1): self.head = self.head_down

    def update_tail_graphics(self):
        tail_relation = self.body[-2] - self.body[-1]
        if tail_relation == Vector2(1,0): self.tail = self.tail_left
        elif tail_relation == Vector2(-1,0): self.tail = self.tail_right
        elif tail_relation == Vector2(0,1): self.tail = self.tail_up
        elif tail_relation == Vector2(0,-1): self.tail = self.tail_down

    def move_snake(self):
        if self.direction != Vector2(0,0):
            if self.new_block == True:
                body_copy = self.body[:]
                body_copy.insert(0,body_copy[0] + self.direction)
                self.body = body_copy[:]
                self.new_block = False
            else:
                body_copy = self.body[:-1]
                body_copy.insert(0,body_copy[0] + self.direction)
                self.body = body_copy[:]

    def add_block(self):
        self.new_block = True

    def play_crunch_sound(self):
        self.crunch_sound.play()

    def reset(self):
        self.body = [Vector2(5,10), Vector2(4,10), Vector2(3,10)]
        self.direction = Vector2(0, 0)

class FRUIT:
    def __init__(self):
        
        self.fruit_switch = True
        self.randomize()

    def draw_fruit(self):
        fruit_rect = pygame.Rect(int(self.pos.x * cell_size), int(self.pos.y * cell_size), cell_size, cell_size)
        screen.blit(apple, fruit_rect)
        # pygame.draw.rect(screen, (126,166,144), fruit_rect)

    def randomize(self):
        while self.fruit_switch:
            self.x = random.randint(1, cell_number - 2)
            self.y = random.randint(1, cell_number - 2)
            self.pos = Vector2(self.x, self.y)
            self.fruit_switch = False
        
        #self.x = random.randint(0, cell_number - 1)
        #self.y = random.randint(0, cell_number - 1)
        #self.pos = Vector2(self.x, self.y)
         
class MAIN:
    def __init__(self):
        self.snake = SNAKE()
        self.fruit = FRUIT()

    def update(self):
        self.snake.move_snake()
        self.check_collison()
        self.check_fail()

    def draw_elements(self):
        self.draw_grass()
        self.draw_score()
        self.fruit.draw_fruit()
        self.snake.draw_snake()
        
    def check_collison(self):
        if self.fruit.pos == self.snake.body[0]:
            self.fruit.fruit_switch = True
            self.fruit.randomize()
            self.snake.add_block()
            self.snake.play_crunch_sound()

        for block in self.snake.body[1:]:
            if block == self.fruit.pos:
                self.fruit.randomize()

    def check_fail(self):
        if self.snake.direction != Vector2(0,0):
            if not 0 <= self.snake.body[0].x < cell_number or not 0 <= self.snake.body[0].y < cell_number:
                self.game_over()
            for block in self.snake.body[1:]:
                if block == self.snake.body[0]:
                    self.game_over()

    def game_over(self):
        self.snake.reset()
        self.fruit.randomize()

    def draw_grass(self):
        grass_color = (167, 209, 61)
        for row in range(cell_number):
            if row % 2 == 0:
                for col in range(cell_number):
                    if col % 2 == 0 :
                        grass_rect =pygame.Rect(col *cell_size, row* cell_size, cell_size, cell_size)
                        pygame.draw.rect(screen, grass_color, grass_rect)
            else:
                for col in range(cell_number):
                    if col % 2 != 0 :
                        grass_rect =pygame.Rect(col *cell_size, row* cell_size, cell_size, cell_size)
                        pygame.draw.rect(screen, grass_color, grass_rect)

    def draw_score(self):
        score_text = str(len(self.snake.body) - 3)
        score_surface = game_font.render(score_text, True, (56,74,12))
        score_x = int(cell_size * cell_number - 60)
        score_y = int(cell_size * cell_number - 40)
        score_rect = score_surface.get_rect(center = (score_x, score_y))
        apple_rect = apple.get_rect(midright = (score_rect.left, score_rect.centery))
        bg_rect = pygame.Rect(apple_rect.left, apple_rect.top, apple_rect.width + score_rect.width + 8, apple_rect.height)

        pygame.draw.rect(screen, (167,209, 61), bg_rect)
        screen.blit(score_surface, score_rect)
        screen.blit(apple, apple_rect)
        pygame.draw.rect(screen, (56,74,12), bg_rect, 2)

pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()
cell_size = 40
cell_number = 20
screen = pygame.display.set_mode((cell_number * cell_size, cell_number * cell_size)) # Erzeugt ein display mit 600 x 600 pixeln
pygame.display.set_caption('Sneeek') # Setzt den Titel des Fensters
clock = pygame.time.Clock() # Objekt, das das 'vergehen der Zeit' im spiel festlegt 
apple = pygame.image.load('pygame_app/Graphics/fruits/apple.png').convert_alpha()
game_font = pygame.font.Font('pygame_app/Font/TheHand.ttf', 25)

start_img = pygame.image.load('pygame_app/Graphics/Buttons/start.png').convert_alpha()
exit_img = pygame.image.load('pygame_app/Graphics/Buttons/exit.png').convert_alpha()
resume_img = pygame.image.load('pygame_app/Graphics/Buttons/resume.png').convert_alpha()

SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, 150)

# game variables
main_game = MAIN()
resume_rect = resume_img.get_rect(center = ((cell_number*cell_size)/2, 100))
resume_button = Button(150, 100, resume_img, 0.8, resume_rect)
start_rect = start_img.get_rect(center = ((cell_number*cell_size)/2, 200))
start_button = Button(150, 200, start_img, 0.8, start_rect)
exit_rect = exit_img.get_rect(center = ((cell_number*cell_size)/2, 300))
exit_button = Button(150, 300, exit_img, 0.8, exit_rect)
game_paused = False
button_pressed = False # True / false nach bewegungseingabe einstellen, dass nicht direkt nacheinander die buttons gedrückt werden können

while True:
    button_pressed = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == SCREEN_UPDATE:
            main_game.update()
        if event.type == pygame.KEYDOWN:
            if (event.key == pygame.K_UP and not button_pressed) or (event.key == pygame.K_w and not button_pressed):
                if main_game.snake.direction.y != 1:
                    main_game.snake.direction = Vector2(0,-1)
            if (event.key == pygame.K_DOWN and not button_pressed) or (event.key == pygame.K_s and not button_pressed):
                if main_game.snake.direction.y != -1:
                    main_game.snake.direction = Vector2(0,1)
            if (event.key == pygame.K_LEFT and not button_pressed) or (event.key == pygame.K_a and not button_pressed):
                if main_game.snake.direction.x != 1:
                    main_game.snake.direction = Vector2(-1,0)
            if (event.key == pygame.K_RIGHT and not button_pressed) or (event.key == pygame.K_d and not button_pressed):
                if main_game.snake.direction.x != -1:
                    main_game.snake.direction = Vector2(1,0)
            button_pressed = True
            
            if event.key == pygame.K_ESCAPE:
                game_paused = True
    
    if game_paused == True:
        main_game.snake.direction = Vector2(0,0)
        resume_clicked = resume_button.draw()
        start_clicked = start_button.draw()
        exit_clicked = exit_button.draw()
        if resume_clicked:
            game_paused = False
        elif start_clicked:
            game_paused = False
            main_game = MAIN()
        elif exit_clicked:
            pygame.quit()
            sys.exit()
    else:
        screen.fill([175, 215, 70])
        main_game.draw_elements()

    pygame.display.update()
    clock.tick(60) # legt die FPS auf 60 fest