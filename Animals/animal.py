from World.tile import Tile
from settings import *
import pygame as pg
import random as rnd
import numpy as np
import Algorithms.astar as ast
from Algorithms.genetic_algorithm import GeneticAlgorithm


class Animal(Tile):
    def __init__(
        self,
        pos: tuple,
        genomes: dict,
        population: dict,
        map: list,
        key: int,
        sprite: str,
        group,
    ) -> None:
        """Initializes an Animal object with specific characteristics.

        Args:
            pos (tuple): The position of the Animal.
            genomes (dict): Dictionary of genetic information.
            population (dict): Dictionary of population data.
            map (list): The map configuration.
            key (int): Key value for the Animal.
            sprite (str): The sprite representing the Animal.
            group: The group the Animal belongs to.

        """
        super().__init__(pos, sprite, group)

        self.pos = pos
        self.genomes = genomes
        self.map = map
        self.population = population
        self.key = key

        self.age = 0
        self.type = self.genomes["animal_type"]
        self.max_age = self.genomes["max_age_d"]
        self.hunger = 0
        self.hunger_rate = self.genomes["hunger_rate_d"]
        self.thirst = 0
        self.thirst_rate = self.genomes["thirst_rate_d"]
        self.set_timer = 0

        # movement related variables
        self.queued_movements = []
        self.path_length = None

        # nutrient related variables
        self.food_found = False
        self.water_found = False
        self.food_point = None
        self.water_point = None

        # mating related variables
        self.mate = None  # gets set to the corresponding animal
        self.mate_pos = None  # only gets set for the searching animal
        self.cooldown = None  # mating cooldown

        # Initialize Genetic Algorithm
        self.genetic_algorithm = GeneticAlgorithm()

    def __direct_movement__(self) -> None:
        if not self.queued_movements:
            self.__normal_movement__()
            return

        new_pos = self.queued_movements.pop(0)
        new_pos = new_pos[0] * TILESIZE, new_pos[1] * TILESIZE
        direction = tuple(np.subtract(self.pos, new_pos))
        self.rect.center -= pg.math.Vector2(direction[0], direction[1])
        self.pos = new_pos

    def __cleanup_on_death__(self) -> None:
        if self.mate:
            self.mate.mate = None
            self.mate.mate_pos = None
            self.mate.queued_movements = []

    def alive(self):
        self.age += 1

        if self.set_timer:
            self.set_timer -= 1
            return self.hunger < 1000 and self.thirst < 1000 and self.age < self.max_age

        if self.cooldown:
            if self.cooldown >= 100:
                self.cooldown = None
            else:
                self.cooldown += 1

        try:
            if not self.queued_movements:
                self.__normal_movement__()
            else:
                if (
                    self.path_length
                    and len(self.queued_movements) <= self.path_length / 2
                    and self.path_length > 4
                ):
                    self.queued_movements = ast.find_path(
                        self.map,
                        self.__convert_pos__(self.pos),
                        self.queued_movements[-1]
                    )
                    self.path_length = len(self.queued_movements)
                self.__direct_movement__()
        except Exception as e:
            self.__normal_movement__()

        if self.__convert_pos__(self.pos) == self.food_point:
            self.food_found = False
            self.food_point = None
            self.hunger -= 350 * (20 - self.hunger_rate)
            self.set_timer = 10
        elif self.__convert_pos__(self.pos) == self.water_point:
            self.water_found = False
            self.water_point = None
            self.thirst -= 350 * (20 - self.thirst_rate)
            self.set_timer = 10

        if self.mate:
            if not self.mate_pos:
                self.mate.queued_movements.append(self.__convert_pos__(self.pos))
                self.mate.mate_pos = self.__convert_pos__(self.pos)
            elif self.mate_pos == self.__convert_pos__(self.pos):
                self.set_timer = 10
                return self.__mating_process__(self.genomes, self.mate.genomes)

        self.hunger += self.hunger_rate
        self.thirst += self.thirst_rate

        if not self.queued_movements:
            self.__resolve_needs__()

        return self.hunger < 1000 and self.thirst < 1000 and self.age < self.max_age

    def __inside_range__(self, start: tuple, end: tuple, point: tuple) -> bool:
        return (
            (point[0] >= start[0])
            and (point[0] <= end[1])
            and (point[1] >= start[1])
            and (point[1] <= end[1])
        )

    def __water_tile__(self, pos: tuple) -> bool:
        coords = self.__convert_pos__(pos)
        return self.map[coords[1]][coords[0]] == 5.0

    def __check_bounds__(self, direction: int) -> bool:
        if direction == 1 and self.pos[1] != 0:
            return True
        elif direction == 2 and self.pos[0] != (MAPSIZE - 1) * TILESIZE:
            return True
        elif direction == 3 and self.pos[1] != (MAPSIZE - 1) * TILESIZE:
            return True
        elif direction == 4 and self.pos[0] != 0:
            return True
        else:
            return False

    def __convert_pos__(self, pos: tuple) -> tuple:
        x = int(pos[0] / TILESIZE)
        y = int(pos[1] / TILESIZE)
        return x, y

    def __normal_movement__(self) -> None:
        direction = rnd.randint(1, 4)

        if direction == 1 and self.__check_bounds__(direction):  # Move Up
            if not self.__water_tile__((self.pos[0], self.pos[1] - TILESIZE)):
                self.rect.center -= pg.math.Vector2(0, TILESIZE)
                self.pos = tuple(np.subtract(self.pos, (0, TILESIZE)))
        elif direction == 2 and self.__check_bounds__(direction):  # Move Right
            if not self.__water_tile__((self.pos[0] + TILESIZE, self.pos[1])):
                self.rect.center += pg.math.Vector2(TILESIZE, 0)
                self.pos = tuple(np.add(self.pos, (TILESIZE, 0)))
        elif direction == 3 and self.__check_bounds__(direction):  # Move Down
            if not self.__water_tile__((self.pos[0], self.pos[1] + TILESIZE)):
                self.rect.center += pg.math.Vector2(0, TILESIZE)
                self.pos = tuple(np.add(self.pos, (0, TILESIZE)))
        elif direction == 4 and self.__check_bounds__(direction):  # Move Left
            if not self.__water_tile__((self.pos[0] - TILESIZE, self.pos[1])):
                self.rect.center -= pg.math.Vector2(TILESIZE, 0)
                self.pos = tuple(np.subtract(self.pos, (TILESIZE, 0)))

    def __direct_movement__(self) -> None:
        new_pos = self.queued_movements.pop(0)
        new_pos = new_pos[0] * TILESIZE, new_pos[1] * TILESIZE
        direction = tuple(np.subtract(self.pos, new_pos))
        self.rect.center -= pg.math.Vector2(direction[0], direction[1])
        self.pos = new_pos

    def __resolve_needs__(self) -> None:
        if self.thirst > 500 and not self.water_found:
            self.__find_water__()
        elif self.hunger > 350 and not self.food_found:
            self.__find_food__()
        elif not self.mate and self.age > 100 and not self.cooldown:
            self.__find_mate__()

    def __find_prey__(self) -> None:
        start_point = self.__convert_pos__(self.pos)
        end_point = self.__convert_pos__(self.pos)

        for _ in range(41):
            if start_point[0] > 0:
                start_point = (start_point[0] - 1, start_point[1])
            if start_point[1] > 0:
                start_point = (start_point[0], start_point[1] - 1)
            if end_point[0] < (MAPSIZE - 1):
                end_point = (end_point[0] + 1, end_point[1])
            if end_point[1] < (MAPSIZE - 1):
                end_point = (end_point[0], end_point[1] + 1)

            for entry in self.huntable:
                prey_pos_conv = self.__convert_pos__(self.huntable[entry].pos)
                if (
                    self.__inside_range__(start_point, end_point, prey_pos_conv)
                    and not self.huntable[entry].hunted
                ):
                    self.huntable[entry].hunted = True
                    self.huntable[entry].hunter = self
                    self.food_point = prey_pos_conv
                    self.food_found = True
                    self.prey = self.huntable[entry]
                    break

            if self.food_found:
                break

        if self.food_found:
            self.queued_movements = ast.find_path(
                self.map, self.__convert_pos__(self.pos), self.food_point
            )
            self.path_length = len(self.queued_movements)

    def __find_berry__(self) -> None:
        start_point = self.__convert_pos__(self.pos)
        end_point = self.__convert_pos__(self.pos)
        for _ in range(31):
            if start_point[0] > 0:
                start_point = (start_point[0] - 1, start_point[1])
            if start_point[1] > 0:
                start_point = (start_point[0], start_point[1] - 1)
            if end_point[0] < (MAPSIZE - 1):
                end_point = (end_point[0] + 1, end_point[1])
            if end_point[1] < (MAPSIZE - 1):
                end_point = (end_point[0], end_point[1] + 1)

            for y in range(start_point[1], end_point[1]):
                for x in range(start_point[0], end_point[0]):
                    if self.map[y][x] == 0:
                        self.food_found = True
                        self.food_point = (x, y)
                        break
                if self.food_found:
                    break

            if self.food_found:
                break

        if self.food_found:
            self.queued_movements = ast.find_path(
                self.map, self.__convert_pos__(self.pos), self.food_point
            )

    def __find_water__(self) -> None:
        start_point = self.__convert_pos__(self.pos)
        end_point = self.__convert_pos__(self.pos)
        for _ in range(31):
            if start_point[0] > 0:
                start_point = (start_point[0] - 1, start_point[1])
            if start_point[1] > 0:
                start_point = (start_point[0], start_point[1] - 1)
            if end_point[0] < (MAPSIZE - 1):
                end_point = (end_point[0] + 1, end_point[1])
            if end_point[1] < (MAPSIZE - 1):
                end_point = (end_point[0], end_point[1] + 1)

            for y in range(start_point[1], end_point[1]):
                for x in range(start_point[0], end_point[0]):
                    if self.map[y][x] == 5 and self.__valid_tile__(x, y):
                        self.water_found = True
                        self.water_point = (x, y)
                        break
                if self.water_found:
                    break

            if self.water_found:
                break

        if self.water_found:
            self.queued_movements = ast.find_path(
                self.map, self.__convert_pos__(self.pos), self.water_point
            )

    def __valid_tile__(self, x: int, y: int) -> bool:
        c = 0
        if y == 0 or self.map[y - 1][x] == 5.0:
            c += 1
        if y == (MAPSIZE - 1) or self.map[y + 1][x] == 5.0:
            c += 1
        if x == 0 or self.map[y][x - 1] == 5.0:
            c += 1
        if x == (MAPSIZE - 1) or self.map[y][x + 1] == 5.0:
            c += 1

        return c != 4

    def __find_mate__(self) -> None:
        start_point = self.__convert_pos__(self.pos)
        end_point = self.__convert_pos__(self.pos)
        for _ in range(31):
            if start_point[0] > 0:
                start_point = (start_point[0] - 1, start_point[1])
            if start_point[1] > 0:
                start_point = (start_point[0], start_point[1] - 1)
            if end_point[0] < (MAPSIZE - 1):
                end_point = (end_point[0] + 1, end_point[1])
            if end_point[1] < (MAPSIZE - 1):
                end_point = (end_point[0], end_point[1] + 1)

            for entry in self.population:
                mate_pos_conv = self.__convert_pos__(self.population[entry].pos)
                if (
                    self.__inside_range__(start_point, end_point, mate_pos_conv)
                    and not self.population[entry].mate
                    and self.population[entry].key != self.key
                    and self.population[entry].type == self.type
                ):
                    self.mate = self.population[entry]
                    self.mate.mate = self
                    self.mate_pos = mate_pos_conv
                    self.queued_movements = ast.find_path(
                        self.map, self.__convert_pos__(self.pos), self.mate_pos
                    )
                    self.path_length = len(self.queued_movements)
                    break

            if self.mate:
                break

    def __mating_process__(self, genomes1: dict, genomes2: dict) -> list:
        new_genomes = self.genetic_algorithm.generate_genomes(genomes1, genomes2)
        self.cooldown = 1
        self.mate.cooldown = 1
        self.mate = None
        self.mate_pos = None
        self.queued_movements = []
        return [new_genomes["animal_type"], self.__convert_pos__(self.pos), new_genomes]