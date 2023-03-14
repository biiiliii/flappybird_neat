import pygame
import random
import sys
import time

bird_img = pygame.image.load('bird1.png')
pipe_img = pygame.image.load('pipe.png')
bg_img = pygame.image.load('bg_large.png')
 
pygame.init()
WINDOW_WIDTH = bg_img.get_width()
WINDOW_HEIGHT = bg_img.get_height()
FPS = 60
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
clock = pygame.time.Clock()

l = [29, 273, 155, 145, 84, 290, 146, 123, 144, 103, 200, 274, 61, 100, 127, 177, 253, 165, 154, 242, 222, 30, 107, 30, 133, 88, 211, 227, 255, 178, 194, 191, 14, 229, 97, 292, 245, 62, 237, 135, 178, 187, 143, 235, 230, 33, 240, 148, 71, 136, 211, 208, 150, 226, 273, 256, 178, 1, 23, 108, 253, 227, 74, 5, 285, 125, 123, 46, 14, 273, 291, 170, 205, 151, 18, 279, 281, 207, 61, 273, 136, 122, 294, 44, 244, 162, 30, 210, 113, 22, 156, 127, 123, 31, 199, 183, 266, 144, 24, 82]
cont = 0

score_ia = 0

class Bird:
	def __init__(self):
		self.x = 50
		self.y = 200
		self.gravity = 1
		self.velocity = 0
		self.image = bird_img
		self.width = self.image.get_width()
		self.height = self.image.get_height()

class Pipe:
	def __init__(self, x):
		global cont
		self.x = x
		self.top = random.randint(0 , 250)
		# self.top = l[cont]
		# cont += 1
		# if cont == len(l):
		# 	cont = 0
		self.bottom = self.top + 150
		self.width = pipe_img.get_width()
		self.image = pipe_img

class Score:
	def __init__(self):
		self.score = 0
		self.font = pygame.font.SysFont('Arial', 20)

def draw():
	window.blit(bg_img, (0, 0))
	window.blit(bird.image, (bird.x, bird.y))
	for pipe in pipes:
		window.blit(pipe.image, (pipe.x, pipe.top - pipe.image.get_height()))
		window.blit(pipe.image, (pipe.x, pipe.bottom))

def update():
	bird.velocity += bird.gravity
	bird.y += bird.velocity

	for pipe in pipes:
		pipe.x -= 2

	if pipes[0].x < -pipe_img.get_width():
		pipes.pop(0)
		pipes.append(Pipe(WINDOW_WIDTH))

	if bird.y > WINDOW_HEIGHT or bird.y < 0:
		return True
 
	for pipe in pipes:
		if bird.x + bird.width - 5 > pipe.x and bird.x < pipe.x + pipe.width:
			if bird.y + 5 < pipe.top or bird.y + bird.height - 10 > pipe.bottom:
				return True

	return False

def handle_events():
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_SPACE:
				bird.velocity = -10

def display_score():
	score_text = score.font.render(f"Score: {score.score}", True, (255, 255, 255))
	window.blit(score_text, (10, 10))

bird = Bird()  
pipes = [Pipe(WINDOW_WIDTH), Pipe(WINDOW_WIDTH + ((WINDOW_WIDTH + pipe_img.get_width()) / 4)), Pipe(WINDOW_WIDTH + ((WINDOW_WIDTH + pipe_img.get_width()) / 4) * 2), Pipe(WINDOW_WIDTH + ((WINDOW_WIDTH + pipe_img.get_width()) / 4) * 3 )]
score = Score()

time.sleep(1)
while True:
	clock.tick(FPS)
	if update():
		sys.exit()
	handle_events()
	window.fill((0, 0, 0))
	draw()
	display_score()
	score_ia += 1
		
	pygame.display.update()
