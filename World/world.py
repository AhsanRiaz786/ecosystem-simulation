import pygame as pg
import random as rnd
from settings import *
from World.tile import Tile
from Animals.rabbit import Herbivore
from Animals.fox import Carnivore
from Animals.pig import Omnivore
from generator import generate_map
from Algorithms.game_theory import GameTheory


class World:
    """Handles the actual simulated world"""

    def __init__(self, map: list = None) -> None:
        self.display_surface = pg.display.get_surface()
        self.font = pg.font.SysFont("arial", 20, True)

        self.world_sprites = pg.sprite.Group()
        self.alive_sprites = pg.sprite.Group()
        self.dead_sprites = pg.sprite.Group()

        # Season tracking
        self.current_tick = 0
        self.current_season = 0  # Index into SEASONS list
        
        self.map = generate_map() if map is None else map

        # dictionaries containing all alive instances of their respective animal type
        self.rabbits = {}
        self.foxes = {}
        self.pigs = {}

        # key values corresponding to the dictionaries
        self.rabbit_key = 1
        self.fox_key = 1
        self.pig_key = 1

        # paths to all the sprites
        self.images = {
            "grass": "World/tileset/grass.png",
            "berry": "World/tileset/berry.png",
            "water": "World/tileset/water.png",
            "rabbit": "World/tileset/rabbit.png",
            "fox": "World/tileset/fox.png",
            "pig": "World/tileset/pig.png",
        }

        # map setup
        self.__create_map__()

        # Initialize Game Theory
        self.game_theory = GameTheory()

    # MAKE ANIMAL SECTION

    def __make_fox__(self, pos: tuple, passed_genomes: dict = None) -> None:
        """Creates a new fox with either a random or a passed set of genomes.

        Args:
            pos (tuple): The position at which the animal will be spawned in.
            passed_genomes (dict, optional): Passed on genomes in case of mating. Defaults to None so that if no genomes are passed, a random set gets generated.
        """
        if passed_genomes:
            self.foxes[self.fox_key] = Carnivore(
                pos,
                self.rabbits,
                passed_genomes,
                self.foxes,
                self.map,
                self.fox_key,
                self.images["fox"],
                [self.alive_sprites],
            )
        else:
            genomes = {
                "animal_type": "fox",
                "max_age_d": rnd.randint(700, 800),
                "max_age_r": rnd.randint(700, 800),
                "hunger_rate_d": round(rnd.uniform(8, 14), 2),
                "hunger_rate_r": round(rnd.uniform(8, 14), 2),
                "thirst_rate_d": round(rnd.uniform(8, 14), 2),
                "thirst_rate_r": round(rnd.uniform(8, 14), 2),
            }

            self.foxes[self.fox_key] = Carnivore(
                pos,
                self.rabbits,
                genomes,
                self.foxes,
                self.map,
                self.fox_key,
                self.images["fox"],
                [self.alive_sprites],
            )

        self.fox_key += 1

    def __make_rabbit__(self, pos: tuple, passed_genomes: dict = None) -> None:
        """Creates a new rabbit with either a random or a passed set of genomes.

        Args:
            pos (tuple): The position at which the animal will be spawned in.
            passed_genomes (dict, optional): Passed on genomes in case of mating. Defaults to None so that if no genomes are passed, a random set gets generated.
        """
        if passed_genomes:
            self.rabbits[self.rabbit_key] = Herbivore(
                pos,
                passed_genomes,
                self.rabbits,
                self.map,
                self.rabbit_key,
                self.images["rabbit"],
                [self.alive_sprites],
            )
        else:
            genomes = {
                "animal_type": "rabbit",
                "max_age_d": rnd.randint(500, 600),
                "max_age_r": rnd.randint(500, 600),
                "hunger_rate_d": round(rnd.uniform(5, 10), 2),
                "hunger_rate_r": round(rnd.uniform(5, 10), 2),
                "thirst_rate_d": round(rnd.uniform(5, 10), 2),
                "thirst_rate_r": round(rnd.uniform(5, 10), 2),
            }

            self.rabbits[self.rabbit_key] = Herbivore(
                pos,
                genomes,
                self.rabbits,
                self.map,
                self.rabbit_key,
                self.images["rabbit"],
                [self.alive_sprites],
            )

        self.rabbit_key += 1

    def __make_pig__(self, pos: tuple, passed_genomes: dict = None) -> None:
        """Creates a new pig with balanced survival characteristics"""
        if passed_genomes:
            self.pigs[self.pig_key] = Omnivore(
                pos,
                self.rabbits,
                passed_genomes,
                self.pigs,
                self.map,
                self.pig_key,
                self.images["pig"],
                [self.alive_sprites],
            )
        else:
            # Adjusted values for more balanced pig characteristics
            genomes = {
                "animal_type": "pig",
                "max_age_d": rnd.randint(600, 750),  # Reduced max age
                "max_age_r": rnd.randint(600, 750),
                "hunger_rate_d": round(rnd.uniform(10, 15), 2),  # Increased hunger rate
                "hunger_rate_r": round(rnd.uniform(10, 15), 2),
                "thirst_rate_d": round(rnd.uniform(8, 14), 2),
                "thirst_rate_r": round(rnd.uniform(8, 14), 2),
            }
            
            self.pigs[self.pig_key] = Omnivore(
                pos,
                self.rabbits,
                genomes,
                self.pigs,
                self.map,
                self.pig_key,
                self.images["pig"],
                [self.alive_sprites],
            )

        self.pig_key += 1

    # END OF MAKE ANIMAL SECTION

    def __create_map__(self) -> None:
        """Creates the map from the array the generator module created."""

        # converts array to positions and draws the corresponding tile
        for row_index, row in enumerate(self.map):
            for col_index, col in enumerate(row):
                x = col_index * TILESIZE
                y = row_index * TILESIZE
                if col == 2.0:  # grass tiles
                    Tile((x, y), self.images["grass"], [self.world_sprites])
                elif col == 0.0:  # berry tiles
                    # there needs to be a grass tile placed under the berry bush
                    Tile((x, y), self.images["grass"], [self.world_sprites])
                    Tile((x, y), self.images["berry"], [self.world_sprites])
                elif col == 5.0:  # water tiles
                    Tile((x, y), self.images["water"], [self.world_sprites])
                elif col == 1.0:  # fox
                    # there needs to be a grass tile placed under the animal
                    Tile((x, y), self.images["grass"], [self.world_sprites])
                    self.__make_fox__((x, y))
                elif col == 3.0:  # rabbit
                    # see above
                    Tile((x, y), self.images["grass"], [self.world_sprites])
                    self.__make_rabbit__((x, y))
                elif col == 4.0:  # pig
                    Tile((x, y), self.images["grass"], [self.world_sprites])
                    self.__make_pig__((x, y))
                else:  # this shouldn't happen
                    print(
                        f"Error: Unknown value in array at: {(x, y)}. Exiting program."
                    )
                    exit(1)

    def __update_graphics__(self):
        """Updates the sprites on screen and the animal counters."""
        self.world_sprites.draw(self.display_surface)
        self.alive_sprites.draw(self.display_surface)

        # Season info with color coding
        season = SEASONS[self.current_season]
        season_colors = {
            "Winter": (200, 200, 255),  # Light blue
            "Spring": (144, 238, 144),  # Light green
            "Summer": (255, 255, 153),  # Light yellow
            "Fall": (255, 165, 0)       # Orange
        }
        
        season_text = self.font.render(
            f"Season: {season} (Day {self.current_tick}/{SEASON_LENGTH})", 
            True, 
            season_colors[season]
        )
        
        # Population counts
        live_rabbits = self.font.render(
            f"Rabbits: {len(self.rabbits)}", True, (255, 255, 255)
        )
        live_foxes = self.font.render(
            f"Foxes: {len(self.foxes)}", True, (255, 255, 255)
        )
        live_pigs = self.font.render(
            f"Pigs: {len(self.pigs)}", True, (255, 255, 255)
        )
        
        # Draw all text
        self.display_surface.blit(season_text, (10, 990))
        self.display_surface.blit(live_rabbits, (10, 1015))
        self.display_surface.blit(live_foxes, (10, 1040))
        self.display_surface.blit(live_pigs, (10, 1065))

    def __remove_animal(self, animal) -> None:
        """Removes the specified animal from the corresponding animal type dictionary and kills the animal.

        Args:
            animal: The animal to be removed.
        """
        if animal.type == "rabbit":
            self.rabbits.pop(animal.key)
        elif animal.type == "fox":
            self.foxes.pop(animal.key)
        elif animal.type == "pig":
            self.pigs.pop(animal.key)
        else:  # this shouldn't happen
            print(
                "Error: Animal of unknown type encountered during removal process. Exiting program."
            )
            exit(1)
        animal.kill()  # removes sprite from all groups

    def __handle_mating__(self, genomes: list) -> None:
        """Handles the mating process based on the given genomes to create specific types of animals.

        Args:
            genomes (list): List containing genetic information for mating.
        """
        if genomes[0] == "rabbit":
            self.__make_rabbit__(genomes[1], genomes[2])
        elif genomes[0] == "fox":
            self.__make_fox__(genomes[1], genomes[2])
        elif genomes[0] == "pig":
            self.__make_pig__(genomes[1], genomes[2])
        else:  # this shouldn't happen
            print(
                "Error: Animal of unknown type encountered during creation process. Exiting program."
            )
            exit(1)
    
    def get_season_effects(self):
        """Returns current season modifiers for animal behavior"""
        season = SEASONS[self.current_season]
        effects = {
            "hunger_mult": 1.0,
            "thirst_mult": 1.0,
            "breeding_mult": 1.0,
            "berry_mult": 1.0
        }
        
        if season == "Winter":
            effects["hunger_mult"] = WINTER_HUNGER_MULTIPLIER
            effects["thirst_mult"] = WINTER_THIRST_MULTIPLIER
            effects["berry_mult"] = WINTER_FOOD_MULTIPLIER
            effects["breeding_mult"] = WINTER_BREEDING_MULTIPLIER
        elif season == "Spring":
            effects["breeding_mult"] = SPRING_BREEDING_MULTIPLIER
            effects["berry_mult"] = SPRING_FOOD_MULTIPLIER
            effects["thirst_mult"] = SPRING_THIRST_MULTIPLIER
        elif season == "Summer":
            effects["thirst_mult"] = SUMMER_THIRST_MULTIPLIER
            effects["berry_mult"] = SUMMER_FOOD_MULTIPLIER
            effects["breeding_mult"] = SUMMER_BREEDING_MULTIPLIER
        elif season == "Fall":
            effects["berry_mult"] = FALL_FOOD_MULTIPLIER
            effects["breeding_mult"] = FALL_BREEDING_MULTIPLIER
            effects["thirst_mult"] = FALL_THIRST_MULTIPLIER
        
        return effects
    
    def update_season(self):
        """Updates the current season based on tick count"""
        self.current_tick += 1
        if self.current_tick >= SEASON_LENGTH:
            self.current_tick = 0
            self.current_season = (self.current_season + 1) % len(SEASONS)
            self.__seasonal_map_update__()

    def __seasonal_map_update__(self):
        """Updates map elements based on season"""
        season = SEASONS[self.current_season]
        
        # Clear existing berry tiles and update sprites
        berry_positions = []
        for y in range(MAPSIZE):
            for x in range(MAPSIZE):
                if self.map[y][x] == 0.0:  # Berry tile
                    self.map[y][x] = 2.0  # Convert to grass
                    berry_positions.append((x, y))
        
        # Get season multiplier
        berry_mult = 1.0
        if season == "Winter":
            berry_mult = WINTER_FOOD_MULTIPLIER
        elif season == "Spring":
            berry_mult = SPRING_FOOD_MULTIPLIER
        elif season == "Summer":
            berry_mult = SUMMER_FOOD_MULTIPLIER
        elif season == "Fall":
            berry_mult = FALL_FOOD_MULTIPLIER
        
        # Find valid grass tiles for new berries
        land_tiles = [(y,x) for y in range(MAPSIZE) for x in range(MAPSIZE) 
                    if self.map[y][x] == 2.0]
        
        # Calculate new berry count
        berries_to_spawn = int(len(land_tiles) * B_PERCENT * berry_mult)
        
        # Spawn new berries
        for _ in range(berries_to_spawn):
            if not land_tiles:
                break
            coord = rnd.choice(land_tiles)
            land_tiles.remove(coord)
            self.map[coord[0]][coord[1]] = 0.0
            x, y = coord[1] * TILESIZE, coord[0] * TILESIZE
            
            # Update sprites
            Tile((x, y), self.images["grass"], [self.world_sprites])
            Tile((x, y), self.images["berry"], [self.world_sprites])

    def run(self, r_state: bool, t_state: bool) -> None:
        """Runs the simulation with season updates"""
        self.__update_graphics__()

        if not (r_state and t_state):
            return
            
        self.update_season()
        season_effects = self.get_season_effects()
        
        for animal in self.alive_sprites:
            # Apply season effects
            animal.hunger_rate *= season_effects["hunger_mult"]
            animal.thirst_rate *= season_effects["thirst_mult"]
            if animal.cooldown:
                animal.cooldown *= season_effects["breeding_mult"]
                
            value = animal.alive()
            if type(value) == bool:
                if not value:
                    self.__remove_animal(animal)
            else:
                self.__handle_mating__(value)
                
            # Reset rates after applying effects
            animal.hunger_rate /= season_effects["hunger_mult"]
            animal.thirst_rate /= season_effects["thirst_mult"]