import math
import config

class Player:
    def __init__(self):
        
        # Used to choose a target asteroid for the first time
        self.first_move = True
        # Used to choose an asteroid to shoot, and to shoot it once
        self.first_bullet = True
        self.has_shot = False

    # Moves a copy of the object forward twice to predict where that object will be in the future
    def predict_move(self, spaceobject):
        
        i = 0
        while i < 2:
            # Retrieve the speed of the object from config
            speed = config.speed[spaceobject.obj_type]

            # Calculate the change in the x and y values
            spaceobject.x += math.cos(math.radians(spaceobject.angle)) * speed
            spaceobject.y -= math.sin(math.radians(spaceobject.angle)) * speed
            
            # Now handle how the spaceobject will wrap-around
            spaceobject.x %= spaceobject.width
            spaceobject.y %= spaceobject.height
            
            i += 1

    # Checks whether two objects will collide with each other or not
    def collide_with(self, obj, other):
        
        #Check the non wraparound distance
        dir_x = abs(obj.x - other.x)
        dir_y = abs(obj.y - other.y)
            
        # Now find the euclidean distance between the two objects
        diff_x_squared = pow(dir_x, 2)
        diff_y_squared = pow(dir_y, 2) 
        euc_d = math.sqrt(diff_x_squared + diff_y_squared)
        
        obj_radius = config.radius[obj.obj_type]
        other_radius = config.radius[other.obj_type]
        # Return whether the objects are going to collide or not
        if euc_d <= (obj_radius + other_radius):
            return True
        return False
    
    # Returns the distance between the asteroids and the player
    def dist_to_ast(self, spaceship, asteroid):
        # First check the non wraparound distance
        dir_x = abs(spaceship.x - asteroid.x)
        dir_y = abs(spaceship.y - asteroid.y)
            
        # Then the wraparound distance
        wrap_x = spaceship.width - dir_x
        wrap_y = spaceship.height - dir_y

        # Take whichever difference that's the lowest - either the wraparound distance or the direct distance
        low_x = min(dir_x, wrap_x)
        low_y = min(dir_y, wrap_y)
        # Now find the euclidean distance between the two objects
        diff_x_squared = pow(low_x, 2)
        diff_y_squared = pow(low_y, 2) 
        euc_d = math.sqrt(diff_x_squared + diff_y_squared)

        return euc_d

    # Works out the angle that the spaceship or the bullet should be at to eventually collide with the asteorid
    def fut_col(self, spaceship, ast):
        # My formula works by measuring the angles clockwise from the x-axis, not counter-clockwise, so I'm making a variable that will hold the angle I need now.
        n_ast_angle = 360 - ast.angle
        
        # Distance between coords
        dir_x = abs(spaceship.x - ast.x)
        dir_y = abs(spaceship.y - ast.y)
            
        # Then the wraparound distance
        wrap_x = spaceship.width - dir_x
        wrap_y = spaceship.height - dir_y

        # Take whichever difference that's the lowest - either the wraparound distance or the direct distance
        low_x = min(dir_x, wrap_x)
        low_y = min(dir_y, wrap_y)

        # I have derived a formula from my own calculations, which I'm going to implement here
        step_one = (low_x* math.sin(math.radians(n_ast_angle))) - (low_y * math.cos(math.radians(n_ast_angle)))
        step_two = step_one / math.sqrt(pow(low_y, 2) + pow(low_x, 2))
        step_three = step_two * (config.speed[ast.obj_type] / config.speed[spaceship.obj_type])
        angle = step_three - math.atan(low_x / low_y)
        return (360 - angle)

    # Calculates the angle that the spaceship should be at to get to the closest asteroid, and tells the spaceship to move accordingly
    def move_to_clos_ast(self, spaceship, asteroid_ls):
        # Return left and right to their original positions so the spaceship doesn't only go straight
        self.left = False
        self.right = False

        ast_dist = {}
        # I need to assign the first asteroid that the bot will shoot at. That will be the closest asteroid
        for asteroid in asteroid_ls:
            ast_dist[asteroid] = self.dist_to_ast(spaceship, asteroid)

        # Retrieve the asteroid closest to the spaceship
        min_ast = min(ast_dist, key = ast_dist.get)
        # For the first frame, I want to assign a variable self.current_ast which will store which asteroid the bot is aiming for
        if self.first_move:   
            self.first_move = False
            # Goal_angle is the angle calculated to collide with the closest asteroid
            goal_angle = self.fut_col(spaceship, min_ast)
            self.current_ast = min_ast
            if goal_angle > spaceship.angle:
                self.left = True
            if goal_angle < spaceship.angle:
                self.right = True
        
        #After the first frame, I only want to change my goal_angle if the asteroid that the bot is aiming for isn't the smallest asteroid any more
        if min_ast != self.current_ast:
            goal_angle = self.fut_col(spaceship, min_ast)
            self.current_ast = min_ast
            if goal_angle > spaceship.angle:
                self.left = True
            if goal_angle < spaceship.angle:
                self.right = True

    # Returns a boolean whether the spaceship is facing the asteroid or not. This is used in the next method to calculate whether the spaceship is facing the asteroid and should shoot it or not
    def is_facing_ast(self, spaceship, asteroid):
        # I'll find the dot product of the unit vectors given by the objects' positions
        spac_x = spaceship.x
        spac_y = spaceship.y
        ast_x = asteroid.x
        ast_y = asteroid.y
        
        # find their lengths
        length_spac = math.sqrt(pow(spac_x, 2) + pow(spac_y, 2))
        length_ast = math.sqrt(pow(ast_x, 2) + pow(ast_y, 2))

        # find the unit vectors given by the spaceship and the asteroid by dividing each of their values by the vector's length
        spac_x /= length_spac
        spac_y /= length_spac
        ast_x /= length_ast
        ast_y /= length_ast

        # find the dot product of the unit vectors 
        dot_product = spac_x * ast_x + spac_y * ast_y
        
        if dot_product > 0 and dot_product < 1:
            return True
        return False

    # Uses fut_col to see whether a bullet fired right now will successfully shoot an asteroid, and tells the spaceship to shoot accordingly 
    def shoot_ast(self, spaceship):
        
        self.bullet = False
        
        # I only want to fire if I'm in range of the closest asteroid
        if self.dist_to_ast(spaceship, self.current_ast) < (config.bullet_move_count * config.speed['bullet']) / 1.3:
            if self.first_bullet:
                self.new_goal_angle = self.fut_col(spaceship, self.current_ast)
                self.ast_shoot = self.current_ast
                self.first_bullet = False
            
            # I'm going to override the directions that the 'move_to_close_ast' method has given if the ship is close to an asteroid
            if not self.is_facing_ast(spaceship, self.current_ast):
                if self.new_goal_angle < spaceship.angle:
                    self.right = True
                if self.new_goal_angle > spaceship.angle:
                    self.left = True
            
            # Use the previous method to check if the spaceship is facing the asteroid and shoot if it is - also don't shoot at an asteroid more than once
            if self.is_facing_ast(spaceship, self.current_ast) and not self.has_shot:
                self.has_shot = True
                self.ast_shoot = self.current_ast
                self.bullet = True

            # If the target asteroid has changed then I should reset how the bullet should shoot the asteroid
            if self.current_ast != self.ast_shoot:
                self.new_goal_angle = self.fut_col(spaceship, self.current_ast)
                self.has_shot = False
                            
    def avoid_ast(self, spaceship, asteroid_ls, fuel):
        # Only avoid asteroids if the player can't shoot them any more
        if fuel <= config.shoot_fuel_threshold:
            # Create a copy of the spaceship and calculate the future x and y coordinates of the spaceship 2 frames from now
            fake_spaceship = self(spaceship.x, spaceship.y, spaceship.width, spaceship.height, spaceship.angle, spaceship.obj_type, spaceship.id)        
            self.predict_move(fake_spaceship)
            
            # Tells a spaceship to change its trajectory if it's about to hit an asteroid
            for asteroid in asteroid_ls:
                # Calculates the future x and y coordinates of the asteroid 2 frames from now
                fake_asteroid = self(asteroid.x, asteroid.y, spaceship.width, spaceship.height, asteroid.angle, asteroid.obj_type, asteroid.id)
                self.predict_move(fake_asteroid)
                
                # If the spaceship is going to collide with an asteroid, tell it to change its trajectory
                if self.collide_with(fake_spaceship, fake_asteroid):
                    if self.left == True:
                        self.left = False
                        self.right = True
                    if self.right == True:
                        self.right = False
                        self.left = True
                    else:
                        self.right = True

    def action(self, spaceship, asteroid_ls, bullet_ls, fuel, score):
        self.move_to_clos_ast(spaceship, asteroid_ls)
        self.shoot_ast(spaceship)
        self.avoid_ast(spaceship, asteroid_ls, fuel)
        self.thrust = True
        return (self.thrust, self.left, self.right, self.bullet)