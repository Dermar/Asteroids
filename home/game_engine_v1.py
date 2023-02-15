import config
from space_object import SpaceObject

class Engine:
    def __init__(self, game_state_filename, player_class, gui_class):
        
        self.import_state(game_state_filename)
        self.player = player_class()
        self.GUI = gui_class(self.width, self.height)

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
        asteroid_counter = 0
        asteroid_sets = 0
        incomp_check = []
        correct_key_check = []

        # These are lists which I'll use to compare to all the needed keys, thus allowing me to determine which keys are missing or incorrect
        keys_with_float_val = ['width', 'height', 'score', 'fuel', 'asteroids_count', 'bullets_count', 'upcoming_asteroids_count']
        keys_with_ls_val = ['spaceship', 'asteroid_small', 'asteroid_large', 'upcoming_asteroid_large', 'upcoming_asteroid_small']
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

            # Errors if there's an unexpected key
                # 1. If the key just isn't one that's possible:
            if key_val[0] not in keys_with_ls_val and key_val[0] not in keys_with_float_val:
                raise ValueError(f"Error: unexpected key: {key_val[0]} in line {line_count}")

                # 2. If the key isn't in the correct order; which I do by cross-referencing the correct key order with the key order in the file (but without the asteroids since those are so changeable)
            if key_val[0] != 'asteroid_large' and key_val[0] != 'asteroid_small' and key_val[0] != 'upcoming_asteroid_small' and key_val[0] != 'upcoming_asteroid_large':
                correct_key_check.append(key_val[0])
                if correct_key_check != correct_key_order[:len(correct_key_check)]:
                    raise ValueError(f"Error: unexpected key: {key_val[0]} in line {line_count}")

                # 3. If the key is supposed to be another asteroid info line but it's not:
            # Asteroid info lines are preceded by an asteroid_count line so use that as the basis for this check
            if key_val[0] == 'upcoming_asteroids_count' or key_val[0] == 'asteroids_count':
                asteroid_counter = 0
                asteroid_called = True
                try:
                    asteroid_goal = int(key_val[1])
                except ValueError:
                    raise ValueError(f"Error: invalid data type in line {line_count}")
            
            # If there's an extra asteroid line
            elif asteroid_called == False and key_val[0] in asteroids:
                raise ValueError(f"Error: unexpected key: {key_val[0]} in line {line_count}")
            
            # Now count how many asteroids there are after the asteroid_count line and check that against how many there should be
            elif asteroid_called and key_val[0] in asteroids:
                asteroid_counter += 1
                
                if asteroid_counter == asteroid_goal:
                    asteroid_called = False
                    asteroid_sets += 1 # If the file is complete then we should have 2 complete sets of asteroids. I perform this check outside of the loop
            
            # If we've hit an asteroid_count line but a line after that isn't an asteroid line when there's still supposed to be more asteroids
            elif asteroid_called and not key_val[0] in asteroids:
                raise ValueError(f"Error: unexpected key: {key_val[0]} in line {line_count}")

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

            # Error if the file is incomplete or not- Set up check that there are entries for all of the different objects
            if key_val[0] not in incomp_check:
                incomp_check.append(key_val[0]) # I check whether this list is the same as a list with all the required keys outside of this loop
            
        
        # Now I'm outside of the loop so I'm going to check if all of the keys that we needed were actually there
        if set(incomp_check) != set(keys_with_float_val + keys_with_ls_val):
            raise ValueError("Error: game state incomplete")

        # And I'm going to check if there were 2 complete sets of asteroids
        if asteroid_sets != 2:
            print("not enough sets asteroids")
            raise ValueError("Error: game state incomplete")

        # Now I'm going to actually bring in the file's content. For clarity, I'm doing this outside the exception loop
        f = open(game_state_filename, 'r')
        while True:
            line = f.readline()
            if line == '':
                break
            if len(line) == 1:
                continue
            key_val = line.strip().split(' ')

            # Now assign the attributes as needed
            if key_val[0] == 'width':
                self.width = int(key_val[1])
            if key_val[0] == 'height':
                self.height = int(key_val[1])

        f.close()

    def export_state(self, game_state_filename):
        
        f = open(game_state_filename, 'w')
        # writes the game state data to f (file)

    def run_game(self):

        while True:
            # 1. Receive player input
            
            # 2. Process game logic

            # 3. Draw the game state on screen using the GUI class
            # self.GUI.update_frame(???)

            # Game loop should stop when:
            # - the spaceship runs out of fuel, or
            # - no more asteroids are available

            break

        # Display final score
        # self.GUI.finish(???)


