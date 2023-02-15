import math
import config

class SpaceObject:
    id = 0
    def __init__(self, x, y, width, height, angle, obj_type, id):
        
        self.angle = int(angle)
        self.x = float(x)
        self.y = float(y)
        self.obj_type = obj_type
        self.id = int(id)
        self.width = int(width)
        self.height = int(height)
        self.radius = int(config.radius[self.obj_type])

    # Turns the spaceship right or left, but with no change to its position
    def turn_left(self):
        
        if self.obj_type == 'spaceship':
            self.angle += config.angle_increment
            if self.angle >= 360:
                self.angle -= 360

    def turn_right(self):
        
        if self.obj_type == 'spaceship':
            self.angle -= config.angle_increment
            if self.angle < 0:
                self.angle += 360
    
    # Moves the object forward according to its speed constant while maintaining its direction (angle)
    def move_forward(self):
        
        # Retrieve the speed of the object from config
        speed = config.speed[self.obj_type]

        # Calculate the change in the x and y values
        self.x += math.cos(math.radians(self.angle)) * speed
        self.y -= math.sin(math.radians(self.angle)) * speed
        
        # Now handle how the spaceobject will wrap-around
        self.x %= self.width
        self.y %= self.height

    # Returns a tuple of the object's x and y coordinates
    def get_xy(self):    
        return (self.x, self.y)

    # Checks if two objects have collided with each other
    def collide_with(self, other):
        # First check the non wraparound distance
        dir_x = abs(self.x - other.x)
        dir_y = abs(self.y - other.y)
            
        # Then the wraparound distance
        wrap_x = self.width - dir_x
        wrap_y = self.height - dir_y

        # Take whichever difference that's the lowest - either the wraparound distance or the direct distance
        low_x = min(dir_x, wrap_x)
        low_y = min(dir_y, wrap_y)
        # Now find the euclidean distance between the two objects
        diff_x_squared = pow(low_x, 2)
        diff_y_squared = pow(low_y, 2) 
        euc_d = math.sqrt(diff_x_squared + diff_y_squared)
        
        # Return whether they're going to collide or not
        if euc_d <= (self.radius + other.radius):
            return True
        return False
        
    # Returns a formatted string with the spaceobject's attributes during the frame    
    def __repr__(self):
        x_one_dp = round(self.x, 1)
        y_one_dp = round(self.y, 1)
        return f"{self.obj_type} {x_one_dp},{y_one_dp},{self.angle},{self.id}"
