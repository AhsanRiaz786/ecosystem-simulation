from Animals.animal import Animal


class Herbivore(Animal):

    def __init__(self, pos: tuple, genoms: dict, population: dict, map: list, key: int, sprite: str, group) -> None:
        super().__init__(pos, genoms, population, map, key, sprite, group)

        self.hunted = False
        self.hunter = None

    def __cleanup_on_death__(self) -> None:
        super().__cleanup_on_death__()
        if self.hunted:
            self.hunter.food_found = False
            self.hunter.food_point = None
            self.hunter.prey = None
            self.hunter.queued_movements = []
            self.hunter.path_length = None

    def alive(self) -> bool or list:
        if self.hunted:
            self.hunter.queued_movements.append(self.__convert_pos__(self.pos))
            self.hunter.food_point = self.__convert_pos__(self.pos)
            if self.hunter.pos == self.pos:
                self.hunter.hunger -= 35*(2-self.hunter.hunger_rate)
                self.__cleanup_on_death__()
                return False
        
        value = super().alive()
        if not value:
            self.__cleanup_on_death__()
            return False
        else:
            return value

    def __find_food__(self) -> None:
        self.__find_berry__()