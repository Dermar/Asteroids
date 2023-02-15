game_name = "INFO1110-Cosmic-Warrior"
frame_delay = 0.03  # seconds between each frame (0.03 = ~33 fps)

radius = {"spaceship": 12,
          "bullet": 3,
          "asteroid_small": 16,
          "asteroid_large": 32}

angle_increment = 15

speed = {"spaceship": 10,
          "bullet": 30,
          "asteroid_small": 3,
          "asteroid_large": 3}

bullet_move_count = 5

shoot_small_ast_score = 150
shoot_large_ast_score = 100
collide_score = -100
shoot_fuel_threshold = 10
fuel_warning_threshold = (75, 50, 25)

spaceship_fuel_consumption = 1
bullet_fuel_consumption = 2
