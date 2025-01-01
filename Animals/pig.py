from .animal import Animal


class Omnivore(Animal):
    def __init__(self, pos: tuple, preys: dict, genoms: dict, population: dict, map: list, key: int, sprite: str, group) -> None:
        super().__init__(pos, genoms, population, map, key, sprite, group)
        self.huntable = preys
        self.prey = None
        self.prey_pos = None
        self.last_hunt_success = 0  # Track successful hunts
        self.hunting_cooldown = 0   # Add hunting cooldown

    def __find_food__(self) -> None:
        """Balanced food-seeking behavior for omnivores"""
        # If recently successful in hunting, prefer berries
        if self.last_hunt_success > 0:
            self.__find_berry__()
            if self.food_found:
                self.last_hunt_success -= 1
                return

        # If very hungry, try hunting
        if self.hunger > 500 and self.hunting_cooldown <= 0:
            self.__find_prey__()
            if self.food_found:
                self.last_hunt_success = 5  # Will prefer berries for next 3 food searches
                self.hunting_cooldown = 60  # Add cooldown after successful hunt
                return

        # Default to berries if hunting failed or not very hungry
        if not self.food_found:
            self.__find_berry__()

    def alive(self):
        """Updated alive check with hunting cooldown"""
        if value := super().alive():
            if self.hunting_cooldown > 0:
                self.hunting_cooldown -= 1
            return value
        self.__cleanup_on_death__()
        return value