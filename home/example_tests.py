import sys
from game_engine import Engine
from space_object import SpaceObject
from gui import GUI


class ExamplePlayer:
    """
    Issues Player commands based on *.in files
    """

    def __init__(self):
        self.i = 0
        with open(f"examples/{sys.argv[1]}.in", "r") as f:
            self.cmd = f.read().splitlines()
        print("Detailed Test Output Format")
        print("Frame <id> :: spaceship_pos :: asteroid_pos_ls :: bullet_pos_ls :: fuel :: score")

    def action(self, spaceship_pos, asteroid_pos_ls, bullet_pos_ls, fuel, score):
        print(f"Frame {self.i} :: {spaceship_pos} :: {asteroid_pos_ls} :: {bullet_pos_ls} :: {fuel} :: {score}")
        self.i += 1

        try:
            return [bool(int(i)) for i in list(self.cmd.pop(0))]
        except IndexError:
            print("Game engine calling Player.action() after game has ended")

        sys.exit()


def example_spaceobject_1():
    obj = SpaceObject(12.0, 56.0, 100, 200, 45, "spaceship", 0)
    print(obj)


def example_spaceobject_2():
    obj = SpaceObject(12.0, 56.0, 100, 200, 45, "spaceship", 0)
    print(obj)
    for _ in range(20):
        obj.turn_left()
        obj.move_forward()
        print(obj)


def example_spaceobject_3():
    spaceship = SpaceObject(30.0, 60.0, 100, 200, 45, "spaceship", 0)
    asteroid_small = SpaceObject(32.0, 50.0, 100, 200, 30, "asteroid_small", 3)
    print(spaceship)
    print(asteroid_small)
    print("Will spaceship collide with asteroid_small?")
    print(spaceship.collide_with(asteroid_small))
    print(asteroid_small.collide_with(spaceship))


def example_game_basic():
    game = Engine('examples/basic_state.txt', ExamplePlayer, GUI)
    game.run_game()


TESTCASES = {"example_spaceobject_1": example_spaceobject_1,
             "example_spaceobject_2": example_spaceobject_2,
             "example_spaceobject_3": example_spaceobject_3,
             "example_game_basic_1": example_game_basic,
             "example_game_basic_2": example_game_basic,
             "example_game_basic_3": example_game_basic}

if len(sys.argv) != 2:
    sys.exit("Usage: python3 example_tests.py <test case name>")

if sys.argv[1] not in TESTCASES:
    sys.exit(f"Invalid test case: {sys.argv[1]}")

TESTCASES[sys.argv[1]]()
