from .animal import Animal
from Algorithms.game_theory import GameTheory

class Carnivore(Animal):
    def __init__(
        self,
        pos: tuple,
        preys: dict,
        genoms: dict,
        population: dict,
        map: list,
        key: int,
        sprite: str,
        group,
    ) -> None:
        super().__init__(pos, genoms, population, map, key, sprite, group)
        self.huntable = preys
        self.prey = None
        self.prey_pos = None
        self.game_theory = GameTheory()

    def alive(self):
        if value := super().alive():
            return value
        self.__cleanup_on_death__()
        return False

    def __find_food__(self) -> None:
        predator_count = len(self.population)
        prey_count = len(self.huntable)

        predator_strategy, prey_strategy = self.game_theory.predator_prey_game(predator_count, prey_count)

        if predator_strategy == 'Hunt':
            self.__find_prey__()
        else:
            self.__rest__()

    def __rest__(self) -> None:
        """Resting behavior for the predator."""
        self.hunger -= 10  # Reduce hunger slightly while resting