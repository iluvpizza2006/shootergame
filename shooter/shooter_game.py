#Создай собственный Шутер!

from pygame import *
from random import randint
from time import time as timer

mixer.init()
mixer.music.load("space.ogg")
mixer.music.play()
fire_sound = mixer.Sound("fire.ogg")

font.init()
font1 = font.SysFont(None, 80)
vic = font1.render("YOU WIN!", True, (255, 255, 255))
lose = font1.render("YOU LOSE!", True, (100, 0, 0))
font2 = font.SysFont(None, 36)
life = 3
goal = 15

clock = time.Clock()

score = 0
lost = 0
max_lost = 3

class GameSprite(sprite.Sprite):
	def __init__(self, player_image, player_x, player_y, player_speed, size_x, size_y):
		super().__init__()
		self.image = transform.scale(image.load(player_image), (size_x, size_y))
		self.speed = player_speed
		self.rect = self.image.get_rect()
		self.rect.x = player_x
		self.rect.y = player_y
	def reset(self):
		window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
	def update(self):
		keys = key.get_pressed()
		if keys[K_LEFT] and self.rect.x > 5:
			self.rect.x -= self.speed 
		if keys[K_RIGHT] and self.rect.x < 700  - 80:
			self.rect.x += self.speed
	def fire(self):
		bullet = Bullet("bullet.png", self.rect.centerx, self.rect.top, -15, 20, 15)
		bullets.add(bullet)
class Enemy(GameSprite):
	def update(self):
		self.rect.y += self.speed
		global lost 
		if self.rect.y > 500:
			self.rect.x = randint(0, 620)
			self.rect.y = 0
			lost = lost + 1

class Bullet(GameSprite):
	def update(self):
		self.rect.y += self.speed
		if self.rect.y < 0:
			self.kill()

window = display.set_mode((700, 500))
display.set_caption("Shooter Game")
background = transform.scale(
    image.load("galaxy.jpg"),
    (700, 500)
)

FPS = 60


ship = Player("rocket.png", 5, 400, 10, 80, 100)

monsters = sprite.Group()
for i in range(1, 6):
	monster = Enemy("ufo.png", randint(80, 620), 0, 5, 80, 50)
	monsters.add(monster)


bullets = sprite.Group()


finish = False

run = True

rel_time = False

num_fire = 0

while run:
	for e in event.get():
		if e.type == QUIT:
			run = False
		elif e.type == KEYDOWN:
			if e.key == K_SPACE:
				if num_fire < 8  and rel_time == False:
					num_fire = num_fire + 1
					fire_sound.play()
					ship.fire()

				if num_fire >= 8  and rel_time == False:
					last_time = timer()
					rel_time = True
	
			
				
	if not finish:
		window.blit(background,(0, 0))
		
		text = font2.render("Счет: " + str(score), 1, (255, 255, 255))
		window.blit(text,(10,20))

		text_lose = font2.render("Пропущено: " + str(lost), 1,(255, 255, 255))
		window.blit(text_lose, (10, 50))


		ship.update()
		ship.reset()
		
		monsters.update()
		bullets.update()

		monsters.draw(window)
		bullets.draw(window)
	

		if rel_time == True:
			now_time = timer()

			if now_time - last_time < 3:
				reload = font2.render('Wait, reload...', 1, (150, 0, 0))
				window.blit(reload, (260,460))
			else:
				num_fire = 0
				rel_time = False


		hits = sprite.groupcollide(monsters, bullets, True, True)
		for c in hits:
			score += 1
			monster = Enemy("ufo.png", randint(80, 620), 0, 5, 80, 50)
			monsters.add(monster)
		
		if lost >= 30:
			finish = True
			window.blit(lose, (200, 200))
		if score >= 10:
			finish  = True
			window.blit(vic, (200, 200))
		if sprite.spritecollide(ship, monsters, False):
			
			life -= 1
			hits = sprite.spritecollide(ship, monsters, True)
			for c in hits:
				
				monster = Enemy("ufo.png", randint(80, 620), 0, 5, 80, 50)
				monsters.add(monster)
		if life == 0 or lost >= 30:
			finish = True
			window.blit(lose, (200, 200))
			
		if score >= goal:
			finish = True
			window.blit(win, (200, 200))
		if life == 3:
			life_color = (0, 150, 0)
		if life == 2:
			life_color = (150, 150, 0)
		if life == 1:
			life_color = (150, 0, 0)
		
	display.update()
	clock.tick(60)

	
	



    