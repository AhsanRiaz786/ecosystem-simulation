from astar import Astar
from World.tile import Tile
from settings import *
import pygame as pg
import random as rnd
import numpy as np


class Animal(Tile):

    def __init__(self, pos: tuple, genoms: dict, population: dict, map: list, key: int, sprite: str, group) -> None:
        super().__init__(pos, sprite, group)

        self.pos = pos
        self.genoms = genoms
        self.map = map
        self.population = population # all currently alive animals of the same type
        self.key = key # the animals population key

        self.age = 0
        self.type = self.genoms['animal_type']
        self.max_age = self.genoms['max_age_d']
        self.hunger = 0
        self.hunger_rate = self.genoms['hunger_rate_d']
        self.thirst = 0
        self.thirst_rate = self.genoms['thirst_rate_d']

        # movement related variables
        self.queued_movements = []
        self.path_length = None
        
        # nutrient related variables
        self.food_found = False
        self.water_found = False
        self.food_point = None
        self.water_point = None

        # mating related variables
        self.mate = None # gets set to the corresponding animal
        self.mate_pos = None # only gets set for the searching animal
        self.cooldown = None # mating cooldown

    # cleanup function
    def __cleanup_on_death__(self) -> None:
        if self.mate:
            self.mate.mate = None
            self.mate.mate_pos = None
            self.mate.queued_movements = []

    # general process
    def alive(self) -> bool or list:
        self.age += 1

        # mating cooldown
        if self.cooldown:
            if self.cooldown >= 100:
                self.cooldown = None
            else:
                self.cooldown += 1

        if not self.queued_movements:
            self.__normal_movement__()
        else:
            if self.path_length:
            # searches for a more optimal path to a moving target after half the path has been traversed
                if len(self.queued_movements) <= self.path_length/2:
                    pathfinder = Astar()
                    self.queued_movements = pathfinder.find_path(self.map, self.__convert_pos__(
                        self.pos), self.queued_movements[len(self.queued_movements)-1])
                    self.path_length = len(self.queued_movements)
                    self.__direct_movement__()
                else:
                    self.__direct_movement__()
            else:
                self.__direct_movement__()

        # checks if either the food or water point has been reached
        if self.__convert_pos__(self.pos) == self.food_point:
            self.food_found = False
            self.food_point = None
            self.hunger -= 35*(2-self.hunger_rate)
        elif self.__convert_pos__(self.pos) == self.water_point:
            self.water_found = False
            self.water_point = None
            self.thirst -= 35*(2-self.thirst_rate)

        if self.mate and not self.mate_pos:
            # this triggers only if a animal wants to mate with this animal
            self.mate.queued_movements.append(self.__convert_pos__(self.pos))
            self.mate.mate_pos = self.__convert_pos__(self.pos)
        elif self.mate and self.mate_pos:
            if self.mate_pos == self.__convert_pos__(self.pos):
                # HERE BE MATING
                new_genoms = self.__generate_genoms__(self.genoms, self.mate.genoms)
                self.mate_pos = None
                self.mate.cooldown = 1
                self.mate.mate = None
                self.mate = None
                self.cooldown = 1
                return [self.type, self.pos, new_genoms]

        # increasing hunger and thirst
        self.hunger += self.hunger_rate
        self.thirst += self.thirst_rate

        if not self.queued_movements:
            if self.thirst > 50 and not self.water_found:
                self.__find_water__()
            elif self.hunger > 35 and not self.food_found:
                self.__find_food__()
            elif not self.mate and self.age > 100 and not self.cooldown:
                self.__find_mate__()

        if self.hunger >= 100 or self.thirst >= 100 or self.age >= self.max_age:
            return False
        else:
            return True

    # checks if a point is inside the rectangle made by two points
    def __inside_range__(self, start: tuple, end: tuple, point: tuple) -> bool:
        return (point[0] >= start[0]) and (point[0] <= end[1]) and (point[1] >= start[1]) and (point[1] <= end[1])

    # checks if a given point is a water tile
    def __check_water__(self, pos: tuple) -> bool:
        x, y = self.__convert_pos__(pos)[0], self.__convert_pos__(pos)[1]
        if self.map[y][x] == 5.0:
            return True
        else:
            return False

    # checks if movement in a given direction would lead out of bounds
    def __check_bounds__(self, direction: int) -> bool:
        if direction == 1 and self.pos[1] != 0:
            return True
        elif direction == 2 and self.pos[0] != 199*TILESIZE:
            return True
        elif direction == 3 and self.pos[1] != 199*TILESIZE:
            return True
        elif direction == 4 and self.pos[0] != 0:
            return True
        else:
            return False

    # converts a given map position into coordinates
    def __convert_pos__(self, pos: tuple) -> tuple:
        x = int(pos[0] / TILESIZE)
        y = int(pos[1] / TILESIZE)
        return tuple((x, y))

    # normal (random) movement 
    def __normal_movement__(self) -> None:
        direction = rnd.randint(1, 4)

        if direction == 1 and self.__check_bounds__(direction):  # Move Up
            if not self.__check_water__(tuple(np.subtract(self.pos, (0, TILESIZE)))):
                self.rect.center -= pg.math.Vector2(0, TILESIZE)
                self.pos = tuple(np.subtract(self.pos, (0, TILESIZE)))
        elif direction == 2 and self.__check_bounds__(direction):  # Move Right
            if not self.__check_water__(tuple(np.add(self.pos, (TILESIZE, 0)))):
                self.rect.center += pg.math.Vector2(TILESIZE, 0)
                self.pos = tuple(np.add(self.pos, (TILESIZE, 0)))
        elif direction == 3 and self.__check_bounds__(direction):  # Move Down
            if not self.__check_water__(tuple(np.add(self.pos, (0, TILESIZE)))):
                self.rect.center += pg.math.Vector2(0, TILESIZE)
                self.pos = tuple(np.add(self.pos, (0, TILESIZE)))
        elif direction == 4 and self.__check_bounds__(direction):  # Move Left
            if not self.__check_water__(tuple(np.subtract(self.pos, (TILESIZE, 0)))):
                self.rect.center -= pg.math.Vector2(TILESIZE, 0)
                self.pos = tuple(np.subtract(self.pos, (TILESIZE, 0)))

    # direct movement 
    def __direct_movement__(self) -> None:
        new_pos = self.queued_movements.pop(0)
        new_pos = tuple((new_pos[0]*TILESIZE, new_pos[1]*TILESIZE))
        direction = tuple(np.subtract(self.pos, new_pos))
        self.rect.center -= pg.math.Vector2(direction[0], direction[1])
        self.pos = new_pos

    def __find_food__(self) -> None:
        pass

    def __find_meat__(self) -> None:
        start_point = self.__convert_pos__(self.pos)
        end_point = self.__convert_pos__(self.pos)

        for i in range(0, 41):
            # checking if the points are still in range and then
            # increasing the range of the search radius every iteration
            if start_point[0] > 0:
                start_point = (start_point[0]-1, start_point[1])
            if start_point[1] > 0:
                start_point = (start_point[0], start_point[1]-1)
            if end_point[0] < 199:
                end_point = (end_point[0]+1, end_point[1])
            if end_point[1] < 199:
                end_point = (end_point[0], end_point[1]+1)

            # iterating through all huntable animals
            for entry in self.huntable:
                prey_pos_conv = self.__convert_pos__(self.huntable[entry].pos)
                if self.__inside_range__(start_point, end_point, prey_pos_conv) and not self.huntable[entry].hunted:
                    self.huntable[entry].hunted = True
                    self.huntable[entry].hunter = self
                    self.food_point = prey_pos_conv
                    self.food_found = True
                    self.prey = self.huntable[entry]
                    break

            if self.food_found:
                break

        if self.food_found:
            pathfinder = Astar()
            self.queued_movements = pathfinder.find_path(
                self.map, self.__convert_pos__(self.pos), self.food_point)
            self.path_length = len(self.queued_movements)

    def __find_berry__(self) -> None:
        start_point = self.__convert_pos__(self.pos)
        end_point = self.__convert_pos__(self.pos)
        for i in range(0, 31):
            # checking if the points are still in range and then
            # increasing the range of the search radius every iteration
            if start_point[0] > 0:
                start_point = (start_point[0]-1, start_point[1])
            if start_point[1] > 0:
                start_point = (start_point[0], start_point[1]-1)
            if end_point[0] < 199:
                end_point = (end_point[0]+1, end_point[1])
            if end_point[1] < 199:
                end_point = (end_point[0], end_point[1]+1)

            for y in range(start_point[1], end_point[1]):
                for x in range(start_point[0], end_point[0]):
                    if self.map[y][x] == 0: # checks for berry entry
                        self.food_found = True
                        self.food_point = (x, y)
                        break
                if self.food_found:
                    break

            if self.food_found:
                break

        if self.food_found:
            pathfinder = Astar()
            self.queued_movements = pathfinder.find_path(
                self.map, self.__convert_pos__(self.pos), self.food_point)

    def __find_water__(self) -> None:
        start_point = self.__convert_pos__(self.pos)
        end_point = self.__convert_pos__(self.pos)
        for i in range(0, 31):
            # checking if the points are still in range and then
            # increasing the range of the search radius every iteration
            if start_point[0] > 0:
                start_point = (start_point[0]-1, start_point[1])
            if start_point[1] > 0:
                start_point = (start_point[0], start_point[1]-1)
            if end_point[0] < 199:
                end_point = (end_point[0]+1, end_point[1])
            if end_point[1] < 199:
                end_point = (end_point[0], end_point[1]+1)

            for y in range(start_point[1], end_point[1]):
                for x in range(start_point[0], end_point[0]):
                    if self.map[y][x] == 5: # checks for water entry
                        self.water_found = True
                        self.water_point = (x, y)
                        break
                if self.water_found:
                    break

            if self.water_found:
                break

        if self.water_found:
            pathfinder = Astar()
            self.queued_movements = pathfinder.find_path(
                self.map, self.__convert_pos__(self.pos), self.water_point)

    def __find_mate__(self) -> None:
        start_point = self.__convert_pos__(self.pos)
        end_point = self.__convert_pos__(self.pos)
        for i in range(0, 31):
            if start_point[0] > 0:
                start_point = (start_point[0]-1, start_point[1])
            if start_point[1] > 0:
                start_point = (start_point[0], start_point[1]-1)
            if end_point[0] < 199:
                end_point = (end_point[0]+1, end_point[1])
            if end_point[1] < 199:
                end_point = (end_point[0], end_point[1]+1)

            for entry in self.population:
                mate_pos_conv = self.__convert_pos__(
                    self.population[entry].pos)
                # checks if the entry:
                # 1. is in range 
                # 2. doesn't have a mate 
                # 3. is not itself
                # 4. if the animal has reached mating age
                if self.__inside_range__(start_point, end_point, mate_pos_conv) and not self.population[entry].mate and not self.population[entry].key == self.key and self.population[entry].age > 100:
                    self.mate_pos = mate_pos_conv
                    self.population[entry].mate = self
                    self.mate = self.population[entry]
                    break

            if self.mate_pos:
                break

        if self.mate_pos:
            pathfinder = Astar()
            self.queued_movements = pathfinder.find_path(
                self.map, self.__convert_pos__(self.pos), self.mate_pos)
            self.path_length = len(self.queued_movements)


    def __generate_genoms__(self, genoms1: dict, genoms2: dict) -> dict:
        genoms_f = genoms1
        genoms_m = genoms2

        inheritance_values = [0 for x in range(6)] 

        for i in range(0,5,2):
            r = rnd.randint(0,1)
            t = rnd.randint(0,1)
            if i == 0: # age values
                if t == 0: # take male dominant
                    if r == 0: # stays dominant 
                        inheritance_values[i] = genoms_m['max_age_d']
                        inheritance_values[i+1] = genoms_f['max_age_r']
                    else: # becomes recessive
                        inheritance_values[i+1] = genoms_m['max_age_d']
                        inheritance_values[i] = genoms_f['max_age_r']
                else: # take female dominant
                    if r == 0: # stays dominant 
                        inheritance_values[i] = genoms_f['max_age_d']
                        inheritance_values[i+1] = genoms_m['max_age_r']
                    else: # becomes recessive
                        inheritance_values[i+1] = genoms_f['max_age_d']
                        inheritance_values[i] = genoms_m['max_age_r']
            elif i == 1: # hunger values
                if t == 0: # take male dominant
                    if r == 0: # stays dominant 
                        inheritance_values[i] = genoms_m['hunger_rate_d']
                        inheritance_values[i+1] = genoms_f['hunger_rate_r']
                    else: # becomes recessive
                        inheritance_values[i+1] = genoms_m['hunger_rate_d']
                        inheritance_values[i] = genoms_f['hunger_rate_r']
                else: # take female dominant
                    if r == 0: # stays dominant 
                        inheritance_values[i] = genoms_f['hunger_rate_d']
                        inheritance_values[i+1] = genoms_m['hunger_rate_r']
                    else: # becomes recessive
                        inheritance_values[i] = genoms_f['hunger_rate_d']
                        inheritance_values[i+1] = genoms_m['hunger_rate_r']
            else: # thirst values
                if t == 0: # take male dominant
                    if r == 0: # stays dominant 
                        inheritance_values[i] = genoms_m['thirst_rate_d']
                        inheritance_values[i+1] = genoms_f['thirst_rate_r']
                    else: # becomes recessive
                        inheritance_values[i+1] = genoms_m['thirst_rate_d']
                        inheritance_values[i] = genoms_f['thirst_rate_r']
                else: # take female dominant
                    if r == 0: # stays dominant 
                        inheritance_values[i] = genoms_f['thirst_rate_d']
                        inheritance_values[i+1] = genoms_m['thirst_rate_r']
                    else: # becomes recessive
                        inheritance_values[i+1] = genoms_f['thirst_rate_d']
                        inheritance_values[i] = genoms_m['thirst_rate_r']

        if rnd.randint(1,4) == 4:
            inheritance_values = self.__mutate_genes__(inheritance_values)


        new_genoms = {'animal_type': genoms_m['animal_type'],
                  'max_age_d': inheritance_values[0],
                  'max_age_r': inheritance_values[1],
                  'hunger_rate_d': inheritance_values[2],
                  'hunger_rate_r': inheritance_values[3],
                  'thirst_rate_d': inheritance_values[4],
                  'thirst_rate_r': inheritance_values[5]}
        
        return new_genoms
    
    def __mutate_genes__(self, inh_val: list) -> list:
        new_values = inh_val

        for i in range(0,5,2):
            mut = round((rnd.uniform(new_values[i],new_values[i+1])/4),2)
            x = rnd.randint(0,1)
            new_values[i] += mut if x == 0 else (-1)*mut
            new_values[i+1] += mut if x == 0 else (-1)*mut

        return new_values

        