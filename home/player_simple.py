import math
import config

class Player:
    def __init__(self):
        self.i = 1

    def action(self, spaceship, asteroid_ls, bullet_ls, fuel, score):        
        self.left = False
        self.right = False
        if self.i % 5 == 0:
            self.bullet = True
            self.left = True
        else:
            self.bullet = False
            self.right = True
            self.i += 1

        
        self.thrust = True
        self.bullet = True
        
        return (self.thrust, self.left, self.right, self.bullet)