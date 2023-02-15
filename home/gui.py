import sys
import config

try:
    import pygame
except ImportError:
    print("Error: 'pygame' module is not installed.")
    sys.exit(1)

green = (0, 255, 0)
gold = (255, 215, 0)
blue = (0, 0, 128)
offset = lambda x,y: (x[0]+y, x[1]+y)

class GUI:
    def __init__(self, width, height):
        self.width = width
        self.height = height

        pygame.init()

        self.screen = pygame.display.set_mode([self.width, self.height])
        pygame.display.set_caption(config.game_name)

        self.font = pygame.font.Font('resources/fonts/PressStart2P-vaV7.ttf', 20)
        self.bg_image = pygame.image.load('resources/img/background.jpeg').convert()
        self.bg_image = pygame.transform.scale(self.bg_image, (self.width, self.height))
        self.ship_icon = pygame.image.load('resources/img/spaceship.png').convert_alpha()
        self.ast_sm_icon = pygame.image.load('resources/img/asteroid-small.png').convert_alpha()
        self.ast_lg_icon = pygame.image.load('resources/img/asteroid-large.png').convert_alpha()

        self.set_background("-", "-")
        pygame.display.update()

    def set_background(self, score, fuel):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print("Error: User closed the window")
                sys.exit(1)
        self.screen.blit(self.bg_image, [0, 0])

        score_text = self.font.render("Score {}".format(score), True, green, blue)
        score_text_rect = score_text.get_rect()
        score_text_rect.topleft = (15, 15)
        self.screen.blit(score_text, score_text_rect)

        fuel_text = self.font.render("Fuel {}".format(fuel), True, green, blue)
        fuel_text_rect = fuel_text.get_rect()
        fuel_text_rect.topleft = (15, 35)
        self.screen.blit(fuel_text, fuel_text_rect)


    def rot_center(self, image, angle):
        """
        rotate an image while keeping its center and size
        Thanks to https://www.pygame.org/wiki/RotateCenter?parent=CookBook
        """
        orig_rect = image.get_rect()
        rot_image = pygame.transform.rotate(image, angle)
        rot_rect = orig_rect.copy()
        rot_rect.center = rot_image.get_rect().center
        rot_image = rot_image.subsurface(rot_rect).copy()
        return rot_image


    def update_frame(self, spaceship, asteroid_ls, bullet_ls, score, fuel):
        self.set_background(score, fuel)

        # Display Player
        spaceship_image = self.rot_center(self.ship_icon, spaceship.angle)
        spaceship_pos = offset(spaceship.get_xy(), -spaceship.radius)
        self.screen.blit(spaceship_image, spaceship_pos)

        # Display Asteroid
        for asteroid in asteroid_ls:
            ast_pos = offset(asteroid.get_xy(), -asteroid.radius)

            if asteroid.obj_type == "asteroid_small":
                self.screen.blit(self.ast_sm_icon, ast_pos)
            elif asteroid.obj_type == "asteroid_large":
                self.screen.blit(self.ast_lg_icon, ast_pos)

        # Display Bullet
        for bullet in bullet_ls:
            pygame.draw.circle(self.screen, gold, bullet.get_xy(), bullet.radius)

        pygame.display.update()
        pygame.time.wait(int(config.frame_delay * 1000))

    def finish(self, score):
        self.set_background(score, 0)

        score_text = self.font.render("Final Score {}".format(score), True, green, blue)
        score_text_rect = score_text.get_rect()
        score_text_rect.center = (self.width // 2, self.height // 2)
        self.screen.blit(score_text, score_text_rect)

        pygame.display.update()

        pygame.time.wait(3000)
        pygame.quit()

