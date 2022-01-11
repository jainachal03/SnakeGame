import pygame
import time
import random

snake_speed = 12

# This is the default window size, i.e the dimension of the window/screen on which we can play our game.
window_x = 720
window_y = 480

# defining colors, the rgb colors of the default coloring schema used.
black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
red = pygame.Color(255, 0, 0)
green = pygame.Color(0, 255, 0)
blue = pygame.Color(0, 0, 255)

# Initialising pygame
pygame.init()

# Initialize the game window ->
pygame.display.set_caption('Snake Game... HISS!!')
game_window = pygame.display.set_mode((window_x, window_y))

#
fps = pygame.time.Clock()

# defining snake's default position
snake_position = [100, 50]

# defining first 4 blocks of snake body
snake_body = [[100, 50], [90, 50], [80, 50], [70, 50]] # the initial coordinates of the snake body

# obje position
object_position = [int(random.randrange(1, (window_x//10))) * 10,
				int(random.randrange(1, (window_y//10))) * 10]

object_spawn = True

# setting default snake direction towards
# right
direction = 'RIGHT'
change_to = direction

# initial score
score = 0

# displaying Score function
def show_score(choice, color, font, size):
	# creating font object score_font
	score_font = pygame.font.SysFont(font, size, bold = True)

	# create the display surface object
	# score_surface
	score_surface = score_font.render('Score : ' + str(score), True, color)

	# create a rectangular object for the text
	# surface object
	score_rect = score_surface.get_rect()

	# displaying text
	game_window.blit(score_surface, score_rect)

# game over function
def game_over():

	# creating font object my_font
	my_font = pygame.font.SysFont("jokerman", 50, italic = True)

	# creating a text surface on which text
	# will be drawn
	game_over_surface = my_font.render(
		'Your Score : ' + str(score), True, red)

	# create a rectangular object for the text
	# surface object
	game_over_rect = game_over_surface.get_rect()

	# setting position of the text
	game_over_rect.midtop = (window_x/2, window_y/4)

	# blit will draw the text on screen
	game_window.blit(game_over_surface, game_over_rect)
	pygame.display.flip()

	# after 2 seconds we will quit the program
	time.sleep(2)

	# deactivating pygame library
	pygame.quit()

	# quit the program
	quit()


def increase_speed(score):
    """
    Function to increase speed of snake if it's score reaches above certain level.
    """
    global snake_speed

    if score == 0 or score%50 != 0:
        return

    if score>=40:
        return

    if score<=150:
        snake_speed += 2
    elif score<=400:
        snake_speed += 3
    else:
        snake_speed += 5

# Main Function
while True:

	# handling key events
	for event in pygame.event.get():
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_UP:
				change_to = 'UP'
			if event.key == pygame.K_DOWN:
				change_to = 'DOWN'
			if event.key == pygame.K_LEFT:
				change_to = 'LEFT'
			if event.key == pygame.K_RIGHT:
				change_to = 'RIGHT'


    # this is the actual direction assignment to the snake.
    # here we are making sure about aspects such as if the snake is going down and we choose to go up
    # the nothing should happen
    # this is because to reverse direction you need 2 rotations either left left or right right
	if change_to == 'UP' and direction != 'DOWN':
		direction = 'UP'
	if change_to == 'DOWN' and direction != 'UP':
		direction = 'DOWN'
	if change_to == 'LEFT' and direction != 'RIGHT':
		direction = 'LEFT'
	if change_to == 'RIGHT' and direction != 'LEFT':
		direction = 'RIGHT'

	# Moving the snake
	if direction == 'UP':
		snake_position[1] -= 10
	if direction == 'DOWN':
		snake_position[1] += 10
	if direction == 'LEFT':
		snake_position[0] -= 10
	if direction == 'RIGHT':
		snake_position[0] += 10

	# Snake body growing mechanism
	# if objects and snakes collide then scores
	# will be incremented by 10
	snake_body.insert(0, list(snake_position))

	if snake_position[0] == object_position[0] and snake_position[1] == object_position[1]:
            score += 10
            object_spawn = False
            increase_speed(score)

	else:
		snake_body.pop()

	if not object_spawn:
		object_position = [random.randrange(1, (window_x//10)) * 10,
						random.randrange(1, (window_y//10)) * 10]

	object_spawn = True
	game_window.fill(black)

	for pos in snake_body:
		pygame.draw.rect(game_window, green,
						pygame.Rect(pos[0], pos[1], 10, 10))

	pygame.draw.rect(game_window, white, pygame.Rect(
		object_position[0], object_position[1], 10, 10))

	# Game Over conditions
	if snake_position[0] < 0 or snake_position[0] > window_x:
		game_over()
	if snake_position[1] < 0 or snake_position[1] > window_y:
		game_over()

	# if The snakes's head touches any of it's body then game is over.
	for block in snake_body[1:]:
		if snake_position[0] == block[0] and snake_position[1] == block[1]:
			game_over()

	# to display the score continuously
	show_score(1, white, 'Helvetica', 20)

	# Refresh game screen
	pygame.display.update()

	# Frame Per Second /Refresh Rate
	fps.tick(snake_speed)
