import pygame
import random
import sys
import time
import os

import neat


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
		self.x = x
		self.top = random.randint(0 , 250)
		self.bottom = self.top + 150
		self.width = pipe_img.get_width()
		self.image = pipe_img

class Score:
	def __init__(self):
		self.score = 0
		self.font = pygame.font.SysFont('Arial', 20)

def draw(birds):
	window.blit(bg_img, (0, 0))
	for bird in birds:
		window.blit(bird.image, (bird.x, bird.y))
	for pipe in pipes:
		window.blit(pipe.image, (pipe.x, pipe.top - pipe.image.get_height()))
		window.blit(pipe.image, (pipe.x, pipe.bottom))

def update(bird):
	global ge

	bird.velocity += bird.gravity
	bird.y += bird.velocity

	if bird.y > WINDOW_HEIGHT or bird.y < 0:
		return True
 
	for pipe in pipes:
		if bird.x + bird.width - 5 > pipe.x and bird.x < pipe.x + pipe.width:
			if bird.y + 5 < pipe.top or bird.y + bird.height - 10 > pipe.bottom:
				return True

	return False

def handle_events(bird):
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_SPACE:
				bird.velocity = -10

def display_score():
	score_text = score.font.render(f"Score: {score.score}", True, (255, 255, 255))
	window.blit(score_text, (10, 10))



def main(genomes, config):
	global birds, pipes, score

	birds = []
	pipes = [Pipe(WINDOW_WIDTH), Pipe(WINDOW_WIDTH + ((WINDOW_WIDTH + pipe_img.get_width()) / 4)), Pipe(WINDOW_WIDTH + ((WINDOW_WIDTH + pipe_img.get_width()) / 4) * 2), Pipe(WINDOW_WIDTH + ((WINDOW_WIDTH + pipe_img.get_width()) / 4) * 3 )]
	score = Score()
	nets = []
	ge = []
 
	for _, g in genomes:
		net = neat.nn.FeedForwardNetwork.create(g, config)
		nets.append(net)
		birds.append(Bird())
		g.fitness = 0
		ge.append(g)
  
	
	time.sleep(1)
	run = True
	while run and len(birds) > 0:
		clock.tick(FPS)
		pipe_ind = 0
		if len(birds) > 0:
			if len(pipes) > 0 and birds[0].x > pipes[0].x + pipes[0].x + pipes[0].width:
				pipe_ind = 1
		else:
			run = False
			break

		for x, bird in enumerate(birds):
			ge[x].fitness += .1
			output = nets[x].activate((bird.y, abs(bird.y - pipes[pipe_ind].bottom), abs(bird.y - pipes[pipe_ind].top)))
			if output[0] > .5:
				bird.velocity = -10
			if update(bird):
				# sys.exit()
				ge[x].fitness -= .1
				birds.pop(x)
				nets.pop(x)
				ge.pop(x)
			if pipes[0].x < -pipe_img.get_width():
				for g in ge:
					g.fitness += 5
			handle_events(bird)
			window.fill((0, 0, 0))
			draw(birds)
	
		for pipe in pipes:
			pipe.x -= (score.score / 10) + 1 if score.score > 10 else 2

		if pipes[0].x < -pipe_img.get_width():
			pipes.pop(0)
			score.score += 1
			pipes.append(Pipe(WINDOW_WIDTH))
		display_score()
		pygame.display.update()


def run(config_file):
	config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_file)

	p = neat.Population(config)
 
	p.add_reporter(neat.StdOutReporter(True))
	stats = neat.StatisticsReporter()
	p.add_reporter(stats)
 
	winner = p.run(main, 50)

if __name__ == "__main__":
	local_dir = os.path.dirname(__file__)
	config_path = os.path.join(local_dir, "neat_config.txt")

	run(config_path)