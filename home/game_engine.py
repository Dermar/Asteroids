import config
from space_object import SpaceObject

class Engine:
    def __init__(self, game_state_filename, player_class, gui_class):
        # This is a list that I'm using to store the SpaceObjects from the game_state_filename
        self.SpaceObject_ls = [] 
        self.bullet_ls = []
        self.import_state(game_state_filename)
        self.player = player_class()
        self.GUI = gui_class(self.width, self.height)
        
    # Checks for errors in the given file and assigns the file's contents to their relevant class attributes
    def import_state(self, game_state_filename):

        # This will stop the game if the given file does not exist
        try:
            f = open(game_state_filename, 'r')
        except FileNotFoundError:
            raise FileNotFoundError(f"Error: unable to open {game_state_filename}")
        
        # Now I'm going to iterate over the file to see if there's anything wrong with its contents
        line_count = 0
        # The below initialised variables are to check whether the file is incomplete or not
        asteroid_called = False
        asteroid_counter = -1
        correct_key_check = []
        bullet_called = False

        # These are lists which I'll use to compare to all the needed keys, thus allowing me to determine which keys are missing or incorrect
        keys_with_float_val = ['width', 'height', 'score', 'fuel', 'asteroids_count', 'bullets_count', 'upcoming_asteroids_count']
        keys_with_ls_val = ['spaceship', 'asteroid_small', 'asteroid_large', 'bullet', 'upcoming_asteroid_large', 'upcoming_asteroid_small']
        correct_key_order = ['width', 'height', 'score', 'spaceship', 'fuel', 'asteroids_count', 'bullets_count', 'upcoming_asteroids_count']
        asteroids = ['asteroid_small', 'asteroid_large', 'upcoming_asteroid_large', 'upcoming_asteroid_small']
        while True:
            line = f.readline()
            line_count += 1
            if line == '':
                break

            # Skip a line if it's empty
            if len(line) == 1:
                continue
            
            key_val = line.strip().split(' ')

            # Error if the line doesn't have a key-value pair
            if len(key_val) != 2:
                raise ValueError(f"Error: expecting a key and value in line {line_count}")

            # Error if the value is an invalid data type
            if key_val[0] in keys_with_float_val:
                try:
                    key_val[1] = float(key_val[1])
                except ValueError:
                    raise ValueError(f"Error: invalid data type in line {line_count}")

            if key_val[0] in keys_with_ls_val:
                val_ls = key_val[1].split(',')
                if len(val_ls) != 4:
                    raise ValueError(f"Error: invalid data type in line {line_count}")

            # Errors if there's an unexpected key
                # 1. If the key just isn't one that's possible:
            if key_val[0] not in keys_with_ls_val and key_val[0] not in keys_with_float_val:
                raise ValueError(f"Error: unexpected key: {key_val[0]} in line {line_count}")

                # 2. If the key isn't in the correct order; which I do by cross-referencing the correct key order with the key order in the file (but without the asteroids and the bullets since those are so changeable)
            if key_val[0] not in asteroids and key_val[0] != 'asteroid_large' and key_val[0] != 'bullet':
                correct_key_check.append(key_val[0])
                if correct_key_check != correct_key_order[0:len(correct_key_check)]:
                    raise ValueError(f"Error: unexpected key: {key_val[0]} in line {line_count}")

                # 3. If the key is supposed to be another asteroid info line but it's not:
            # Asteroid info lines are preceded by an asteroid_count line so use that as the basis for this check
            if key_val[0] == 'upcoming_asteroids_count' or key_val[0] == 'asteroids_count':
                asteroid_called = True
                asteroid_goal = int(key_val[1]) + asteroid_counter
            
            # If there's an extra asteroid line
            elif asteroid_called == False and key_val[0] in asteroids:
                raise ValueError(f"Error: unexpected key: {key_val[0]} in line {line_count}")
            
            # Now count how many asteroids there are after the asteroid_count line and check that against how many there should be
            elif asteroid_called and key_val[0] in asteroids:
                asteroid_counter += 1
                id_of_asteroid = int(key_val[1].split(',')[3])

                if asteroid_counter != id_of_asteroid:
                    raise ValueError(f"Error: unexpected key: {key_val[0]} in line {line_count}")
                
                if asteroid_counter == asteroid_goal:
                    asteroid_called = False
            
            # If we've hit an asteroid_count line but a line after that isn't an asteroid line when there's still supposed to be more asteroids
            elif asteroid_called and not key_val[0] in asteroids:
                raise ValueError(f"Error: unexpected key: {key_val[0]} in line {line_count}")
            
            if not bullet_called and key_val[0] == 'bullet':
                raise ValueError(f"Error: unexpected key: {key_val[0]} in line {line_count}")

            # If there's a bullet_count line and there aren't enough bullet infos after it
            if key_val[0] == 'bullets_count':
                needed_bullets = key_val[1]
                current_bullets = 0.0
                bullet_called = True
                
            elif bullet_called:
                if key_val[0] == 'bullet':
                    print(f"needed bullets: {needed_bullets}  current_bullets: {current_bullets}")
                    current_bullets += 1
                if current_bullets == needed_bullets:
                    bullet_called = False
                
                if bullet_called and current_bullets > needed_bullets:
                    raise ValueError(f"Error: unexpected key: {key_val[0]} in line {line_count}")
                    
                elif bullet_called and key_val[0] != 'bullet':
                    raise ValueError(f"Error: unexpected key: {key_val[0]} in line {line_count}")
            
          
        # Now I'm outside of the loop so I'm going to check if all of the keys that we needed were actually there
        if correct_key_check != correct_key_order:
            raise ValueError("Error: game state incomplete")

        # Now I'm going to actually bring in the file's content. For clarity, I'm doing this outside the exception loop
        f = open(game_state_filename, 'r')
        
        while True:
            line = f.readline()
            if line == '':
                break
            if len(line) == 1:
                continue
            obj_attrib = line.strip().split(' ')

            obj = obj_attrib[0]
            attrib = obj_attrib[1]

            # Now assign the attributes as needed
            if obj == 'width':
                self.width = int(attrib)
            if obj == 'height':
                self.height = int(attrib)
            if obj == 'score':
                self.score = int(attrib)
            if obj == 'fuel':
                self.fuel = int(attrib)
            if obj == 'asteroids_count':
                self.asteroids_count = int(attrib)
            if obj == 'bullets_count':
                self.bullets_count = int(attrib)
            
            # Now assign the bullets to self.bullet_ls
            if obj == 'bullet':
                attrib_ls = attrib.split(',')
                my_bullet = SpaceObject(attrib_ls[0], attrib_ls[1], self.width, self.height, attrib_ls[2],obj,attrib_ls[3])
                self.bullet_ls.append(my_bullet)

            if obj == 'upcoming_asteroids_count':
                self.upcom_asteroids_count = int(attrib)
            
            # This assigns the data of those objects which have lists as their values- the SpaceObjects (without the bullets)
            if obj in keys_with_ls_val:
                # First take out the 'upcoming_' from the upcoming asteroid names since that's not a valid obj_type name
                obj = obj.lstrip('upcoming_')
                # Then just assign the SpaceObject to a list to be used in export_state
                attrib_ls = attrib.split(',')
                my_SpaceObject = SpaceObject(attrib_ls[0], attrib_ls[1], self.width, self.height, attrib_ls[2],obj,attrib_ls[3])  
                self.SpaceObject_ls.append(my_SpaceObject)    
                
        f.close()

    # Exports all of the game's attributes to a file
    def export_state(self, game_state_filename):
        
        # Write the lines to the export file one by one
        ex = open(game_state_filename, 'w')
        ex.write('width ' + str(self.width) + '\n')
        ex.write('height ' + str(self.height) + '\n')
        ex.write('score ' + str(self.score) + '\n')
        ex.write(self.SpaceObject_ls[0].__repr__() + '\n')
        ex.write('fuel ' + str(self.fuel) + '\n')
        ex.write('asteroids_count ' + str(self.asteroids_count) + '\n')
        
        # Current asteroids
        k = 1
        while k <= self.asteroids_count:
            ex.write(self.SpaceObject_ls[k].__repr__() + '\n')
            
            k += 1

        # Bullets count
        ex.write('bullets_count ' + str(self.bullets_count) + '\n')

        # Bullets
        j = 0
        while j < self.bullets_count:
            ex.write(self.bullet_ls[j].__repr__() + '\n')
            
            j += 1

        # Upcoming asteroids count
        ex.write('upcoming_asteroids_count ' + str(self.upcom_asteroids_count) + '\n')
        
        # Upcoming asteroids
        while k <= (self.asteroids_count + self.upcom_asteroids_count):
            ex.write('upcoming_' + self.SpaceObject_ls[k].__repr__() + '\n')
            
            k += 1

        ex.close()

    # Actually runs the game
    def run_game(self):
        id_num = -1 # this is for the ids of the bullets
        # The below are the variables to be given to Player and processed while running the game
        spaceship = self.SpaceObject_ls[0]
        asteroid_ls = self.SpaceObject_ls[1:self.asteroids_count + 1]
        upcom_asteroid_ls = self.SpaceObject_ls[self.asteroids_count + 1:]
        og_fuel = self.fuel
        bullet_ls = []
        
        j = 0 # this is a variable used to iterate over the fuel warning threshold in config

        while True:
            self.GUI.update_frame(spaceship, asteroid_ls, bullet_ls, self.score, self.fuel)
            ast_to_replenish = 0

            # Check collisions between the spaceship and asteroids for frame 0: the frame before the player has actually moved:
            space_ast_col = []
            # Process collisions between the spaceship and asteroids
            for asteroid in asteroid_ls:
                if spaceship.collide_with(asteroid) == True:
                    space_ast_col.append(asteroid)
                    ast_to_replenish += 1
                    # update the score
                    self.score += config.collide_score

                    print(f"Score: {self.score} \t [Spaceship collided with asteroid {asteroid.id}]")

            # Delete the collided asteroids
            for asteroid in space_ast_col:
                asteroid_ls.remove(asteroid)
            # 1. Manoeuvre the spaceship as per the Player's input
            actions = self.player.action(spaceship, asteroid_ls, bullet_ls, self.fuel, self.score)   
             
            if actions[1] == True and not (actions[1] == True and actions[2] == True):
                spaceship.turn_left()
            if actions[2] == True and not (actions[1] == True and actions[2] == True):
                spaceship.turn_right()
            if actions[0] == True:
                spaceship.move_forward()
            
            # 2. Update positions of asteroids by calling move_forward() for each asteroid
            i = 0
            while i < len(asteroid_ls):
                asteroid_ls[i].move_forward()          
                i += 1

            # 3. Update positions of bullets:
            # launch a new bullet if instructed by Player and if it's 
            if actions[3] == True:
                if self.fuel < config.shoot_fuel_threshold:
                    print("Cannot shoot due to low fuel")
                else:
                    self.fuel -= config.bullet_fuel_consumption # deduct the fuel for the launched bullet
                    id_num += 1
                    new_bullet = SpaceObject(spaceship.x, spaceship.y, self.width, self.height, spaceship.angle, 'bullet', id_num)
                    new_bullet.move_count = 0 # assign the new_bullet how many frames it's been 
                    bullet_ls.append(new_bullet)
                    

            # Go through the bullet list and check which bullets have expired
            bullet_del = []
            for bullet in bullet_ls:
                if bullet.move_count >= config.bullet_move_count:
                    bullet_del.append(bullet)
                # Update positions of bullets by calling move_forward() for each bullet
                bullet.move_forward()
                # Update the move_count for each bullet
                bullet.move_count += 1
            
            # Now delete the expired bullets
            for bullet in bullet_del:
                bullet_ls.remove(bullet)

            # 4. Deduct fuel for spaceship
            self.fuel -= config.spaceship_fuel_consumption
            
            # Calculate percentage of fuel consumed
            fuel_percent = (self.fuel/og_fuel) * 100
            # Calculate whether that fuel percent is on or below the next warning threshold
            if j != len(config.fuel_warning_threshold): # This condition is to make sure that j never goes beyond the length of the warning threshold tuple
                if fuel_percent <= config.fuel_warning_threshold[j]:
                    print(f"{config.fuel_warning_threshold[j]}% fuel warning: {self.fuel} remaining")
                    j += 1
                    
            # 5. Detect collisions
            asteroid_del = []
            bullet_hit_del = []
            # Process collisions between bullets and asteroids
            for asteroid in asteroid_ls:
                for bullet in bullet_ls:
                    if bullet.collide_with(asteroid) == True:
                        
                        if bullet not in bullet_hit_del:
                            bullet_hit_del.append(bullet)
                        if asteroid not in asteroid_del:
                            asteroid_del.append(asteroid)
                        
                        # update the score according to what type of asteroid was shot
                        if asteroid.obj_type == 'asteroid_large':
                            self.score += config.shoot_large_ast_score
                        if asteroid.obj_type == 'asteroid_small':
                            self.score += config.shoot_small_ast_score
                        
                        print(f"Score: {self.score} \t [Bullet {bullet.id} has shot asteroid {asteroid.id}]")
            
            # Delete the hit asteroid/s and bullet/s if they exist
            for bullet in bullet_hit_del:
                bullet_ls.remove(bullet)
            for asteroid in asteroid_del:
                ast_to_replenish += 1
                asteroid_ls.remove(asteroid)

            space_ast_col = []
            # Process collisions between the spaceship and asteroids
            for asteroid in asteroid_ls:
                if spaceship.collide_with(asteroid) == True:
                    space_ast_col.append(asteroid)
                    ast_to_replenish += 1
                    # update the score
                    self.score += config.collide_score

                    print(f"Score: {self.score} \t [Spaceship collided with asteroid {asteroid.id}]")

            # Delete the collided asteroids
            for asteroid in space_ast_col:
                asteroid_ls.remove(asteroid)

            # After processing all collisions, replenish as many asteroids as there were destroyed
            if len(upcom_asteroid_ls) != 0:
                m = 0
                while m < ast_to_replenish:
                    asteroid_ls.append(upcom_asteroid_ls[0])
                    added_ast = upcom_asteroid_ls.pop(0)
                    print(f"Added asteroid {added_ast.id}")
                    m += 1
            
            # Re-update the variables for export state
            self.SpaceObject_ls = [spaceship] + asteroid_ls + upcom_asteroid_ls
            self.asteroids_count = len(asteroid_ls)
            self.upcom_asteroids_count = len(upcom_asteroid_ls)
            self.bullets_count = len(bullet_ls)
            self.bullet_ls = bullet_ls

            # Check the stop conditions:
            if self.fuel <= 0 or len(upcom_asteroid_ls) == 0:
                if len(upcom_asteroid_ls) == 0:
                    print("Error: no more asteroids available")
                break