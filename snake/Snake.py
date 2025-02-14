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
    def __init__(self, color):
        self.body = [Vector2(5, 10), Vector2(4, 10), Vector2(3, 10)]
        self.direction = Vector2(0, 0)
        self.new_block = False
        self.color = color

        self.head_up = pygame.image.load(f'pygame_app/Graphics/snakes/{color}_head_up.png').convert_alpha()
        self.head_down = pygame.image.load(f'pygame_app/Graphics/snakes/{color}_head_down.png').convert_alpha()
        self.head_right = pygame.image.load(f'pygame_app/Graphics/snakes/{color}_head_right.png').convert_alpha()
        self.head_left = pygame.image.load(f'pygame_app/Graphics/snakes/{color}_head_left.png').convert_alpha()
        
        self.tail_up = pygame.image.load(f'pygame_app/Graphics/snakes/{color}_tail_up.png').convert_alpha()
        self.tail_down = pygame.image.load(f'pygame_app/Graphics/snakes/{color}_tail_down.png').convert_alpha()
        self.tail_right = pygame.image.load(f'pygame_app/Graphics/snakes/{color}_tail_right.png').convert_alpha()
        self.tail_left = pygame.image.load(f'pygame_app/Graphics/snakes/{color}_tail_left.png').convert_alpha()

        self.body_vertical = pygame.image.load(f'pygame_app/Graphics/snakes/{color}_body_vertical.png').convert_alpha()
        self.body_horizontal = pygame.image.load(f'pygame_app/Graphics/snakes/{color}_body_horizontal.png').convert_alpha()

        self.body_tr = pygame.image.load(f'pygame_app/Graphics/snakes/{color}_body_tr.png').convert_alpha()
        self.body_tl = pygame.image.load(f'pygame_app/Graphics/snakes/{color}_body_tl.png').convert_alpha()
        self.body_br = pygame.image.load(f'pygame_app/Graphics/snakes/{color}_body_br.png').convert_alpha()
        self.body_bl = pygame.image.load(f'pygame_app/Graphics/snakes/{color}_body_bl.png').convert_alpha()
    
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
        self.random_fruit = apple

    def draw_fruit(self):
        fruit_rect = pygame.Rect(int(self.pos.x * cell_size), int(self.pos.y * cell_size), cell_size, cell_size)
        screen.blit(self.random_fruit, fruit_rect)

    def random_fruit_function(self):
        while self.fruit_switch:
            random_fruit = random.choice([apple, grape, lemon])
            return random_fruit
        # random_fruit = apple
        # return random_fruit

    def randomize(self):
        while self.fruit_switch:
            self.x = random.randint(1, cell_number - 2)
            self.y = random.randint(1, cell_number - 2)
            self.pos = Vector2(self.x, self.y)
            self.fruit_switch = False

class GRASS:
    def __init__(self, color):
        self.draw_grass(color)
    def draw_grass(self, color):
        if color == 'b':
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
        if color == 'g':
            grass_color = (102, 0, 102)
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
        if color == 'p':
            grass_color = (204, 102, 0)
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

class MAIN:
    def __init__(self):
        self.snake = SNAKE(snake_color)
        self.grass = GRASS(snake_color)
        self.fruit = FRUIT()

    def update(self):
        self.snake.move_snake()
        self.check_collison()
        self.check_fail()

    def draw_elements(self):
        self.grass.draw_grass(snake_color)
        self.draw_score()
        self.fruit.draw_fruit()
        self.snake.draw_snake()
        
    def check_collison(self):
        if self.fruit.pos == self.snake.body[0]:
            self.fruit.fruit_switch = True
            self.fruit.random_fruit = self.fruit.random_fruit_function()
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
        previous_score = len(self.snake.body) - 3
        highscore = 0

        # Read the current high score from the file
        try:
            with open('pygame_app/highscore.txt', 'r') as file:
                highscore = int(file.readline())
        except FileNotFoundError:
            # If the file does not exist, create it with the current score
            with open('pygame_app/highscore.txt', 'w') as file:
                file.write(str(previous_score))
            highscore = previous_score
        except ValueError:
            # If the file is empty, write the current score to it
            with open('pygame_app/highscore.txt', 'w') as file:
                file.write(str(previous_score))
            highscore = previous_score

        # Update the high score if the current score is higher
        if previous_score > highscore:
            highscore = previous_score
            with open('pygame_app/highscore.txt', 'w') as file:
                file.write(str(highscore))

        self.snake.reset()
        self.fruit.randomize()

    def draw_score(self):
        highscore = 0
        if snake_color == 'p':
            score_r, score_g, score_b = 204, 102, 0
            font_r, font_g, font_b = 255, 229, 204
        elif snake_color == 'g':
            score_r, score_g, score_b = 102, 0, 102
            font_r, font_g, font_b = 255, 204, 255
        else:
            score_r, score_g, score_b = 167, 209, 61
            font_r, font_g, font_b = 56, 74, 12
        
        score_text = str(len(self.snake.body) - 3)
        score_surface = game_font.render(score_text, True, (font_r, font_g, font_b))
        score_x = int(cell_size * cell_number - 60)
        score_y = int(cell_size * cell_number - 40)
        score_rect = score_surface.get_rect(center = (score_x, score_y))
        apple_rect = apple.get_rect(midright = (score_rect.left, score_rect.centery))

        try :
            with open('pygame_app/highscore.txt', 'r') as file:
                for line in file:
                    highscore = int(line)
        except FileNotFoundError:
            with open('pygame_app/highscore.txt', 'w') as file:
                file.write(str(highscore))
        hs_text = str(highscore)
        hs_surface = game_font.render(hs_text, True, (font_r, font_g, font_b))
        hs_x = int(cell_size * cell_number - 60)
        hs_y = int(cell_size * cell_number - 80)
        hs_rect = hs_surface.get_rect(center = (hs_x, hs_y))
        lem_rect_hs = lemon.get_rect(midright = (hs_rect.left, hs_rect.centery))
        bg_rect = pygame.Rect(lem_rect_hs.left, lem_rect_hs.top, lem_rect_hs.width + hs_rect.width + 8, lem_rect_hs.height + apple_rect.height)

        pygame.draw.rect(screen, (score_r, score_g, score_b), bg_rect)
        screen.blit(score_surface, score_rect)
        screen.blit(apple, apple_rect)
        
        screen.blit(hs_surface, hs_rect)
        screen.blit(lemon, lem_rect_hs)

        pygame.draw.rect(screen, (font_r, font_g, font_b), bg_rect, 2)

# import base graphics, set up sound and initialize pygame
pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()
cell_size = 40
cell_number = 20
screen = pygame.display.set_mode((cell_number * cell_size, cell_number * cell_size)) # Erzeugt ein display mit 600 x 600 pixeln
pygame.display.set_caption('Sneeek') # Setzt den Titel des Fensters
clock = pygame.time.Clock() # Objekt, das das 'vergehen der Zeit' im spiel festlegt 
apple = pygame.image.load('pygame_app/Graphics/fruits/apple.png').convert_alpha()
grape = pygame.image.load('pygame_app/Graphics/fruits/grape.png').convert_alpha()
lemon = pygame.image.load('pygame_app/Graphics/fruits/lemon.png').convert_alpha()
game_font = pygame.font.Font('pygame_app/Font/TheHand.ttf', 25)

start_img = pygame.image.load('pygame_app/Graphics/Buttons/start.png').convert_alpha()
exit_img = pygame.image.load('pygame_app/Graphics/Buttons/exit.png').convert_alpha()
resume_img = pygame.image.load('pygame_app/Graphics/Buttons/resume.png').convert_alpha()
purple_snake_img = pygame.image.load('pygame_app/Graphics/Buttons/purple_snake.png').convert_alpha()
green_snake_img = pygame.image.load('pygame_app/Graphics/Buttons/green_snake.png').convert_alpha()
blue_snake_img = pygame.image.load('pygame_app/Graphics/Buttons/blue_snake.png').convert_alpha()

SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, 150)

# game variables
snake_color = 'b'
game_paused = False
button_pressed = False # True / false nach bewegungseingabe einstellen, dass nicht direkt nacheinander die buttons gedrückt werden können
highscore = 0
previos_score = 0
main_game = MAIN()

# Buttons
resume_rect = resume_img.get_rect(center = ((cell_number*cell_size)/2, 100))
resume_button = Button(150, 100, resume_img, 0.8, resume_rect)
start_rect = start_img.get_rect(center = ((cell_number*cell_size)/2, 200))
start_button = Button(150, 200, start_img, 0.8, start_rect)
blue_snake_rect = blue_snake_img.get_rect(center = ((cell_number*cell_size)/2, 300))
blue_snake_button = Button(150, 300, blue_snake_img, 0.8, blue_snake_rect)
green_snake_rect = green_snake_img.get_rect(center = ((cell_number*cell_size)/2, 400))
green_snake_button = Button(150, 400, green_snake_img, 0.8, green_snake_rect)
purple_snake_rect = purple_snake_img.get_rect(center = ((cell_number*cell_size)/2, 500))
purple_button = Button(150, 500, purple_snake_img, 0.8, purple_snake_rect)
exit_rect = exit_img.get_rect(center = ((cell_number*cell_size)/2, 600))
exit_button = Button(150, 600, exit_img, 0.8, exit_rect)

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
        blue_snake_clicked = blue_snake_button.draw()
        green_snake_clicked = green_snake_button.draw()
        purple_snake_clicked = purple_button.draw()
        exit_clicked = exit_button.draw()
        if resume_clicked:
            game_paused = False
        elif start_clicked:
            game_paused = False
            main_game = MAIN()
        elif blue_snake_clicked:
            game_paused = False
            snake_color = 'b'
            main_game = MAIN()
        elif green_snake_clicked:
            game_paused = False
            snake_color = 'g'
            main_game = MAIN()
        elif purple_snake_clicked:
            game_paused = False
            snake_color = 'p'
            main_game = MAIN()
        elif exit_clicked:
            pygame.quit()
            sys.exit()
    else:
        if snake_color == 'g':
            screen.fill([51, 0, 51])
            main_game.draw_elements()
        elif snake_color == 'p':
            screen.fill([153, 76, 0])
            main_game.draw_elements()
        else:
            screen.fill([175, 215, 70])
            main_game.draw_elements()

    pygame.display.update()
    clock.tick(60) # legt die FPS auf 60 fest