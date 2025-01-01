import random as rnd

class GeneticAlgorithm:
    def __init__(self):
        pass

    def generate_genomes(self, genomes1: dict, genomes2: dict) -> dict:
        """Generates a new set of genomes based on the ones passed into the function.

        Args:
            genomes1 (dict): genomes from animal 1
            genomes2 (dict): genomes from animal 2

        Returns:
            dict: contains the genome values
        """
        genomes_f = genomes1
        genomes_m = genomes2

        inheritance_values = [0 for _ in range(6)]

        for i in range(0, 5, 2):
            t = rnd.randint(0, 1)
            r = rnd.randint(0, 3)
            if i == 0:  # age values
                if t == 0 and r >= 1:  # male dominant stays dominant
                    inheritance_values[i] = genomes_m["max_age_d"]
                    inheritance_values[i + 1] = genomes_f["max_age_r"]
                elif t == 0 and r == 0:  # male dominant becomes recessive
                    inheritance_values[i + 1] = genomes_m["max_age_d"]
                    inheritance_values[i] = genomes_f["max_age_r"]
                elif t == 1 and r >= 1:  # female dominant stays dominant
                    inheritance_values[i] = genomes_f["max_age_d"]
                    inheritance_values[i + 1] = genomes_m["max_age_r"]
                else:  # female dominant becomes recessive
                    inheritance_values[i + 1] = genomes_f["max_age_d"]
                    inheritance_values[i] = genomes_m["max_age_r"]
            elif i == 2:  # hunger values
                if t == 0 and r >= 1:  # male dominant stays dominant
                    inheritance_values[i] = genomes_m["hunger_rate_d"]
                    inheritance_values[i + 1] = genomes_f["hunger_rate_r"]
                elif t == 0 and r == 0:  # male dominant becomes recessive
                    inheritance_values[i + 1] = genomes_m["hunger_rate_d"]
                    inheritance_values[i] = genomes_f["hunger_rate_r"]
                else:  # female dominant stays dominant
                    inheritance_values[i] = genomes_f["hunger_rate_d"]
                    inheritance_values[i + 1] = genomes_m["hunger_rate_r"]
            # thirst values
            elif t == 0 and r >= 1:  # male dominant stays dominant
                inheritance_values[i] = genomes_m["thirst_rate_d"]
                inheritance_values[i + 1] = genomes_f["thirst_rate_r"]
            elif t == 0 and r == 0:  # male dominant becomes recessive
                inheritance_values[i + 1] = genomes_m["thirst_rate_d"]
                inheritance_values[i] = genomes_f["thirst_rate_r"]
            elif t == 1 and r >= 0:  # female dominant stays dominant
                inheritance_values[i] = genomes_f["thirst_rate_d"]
                inheritance_values[i + 1] = genomes_m["thirst_rate_r"]
            else:  # female dominant becomes recessive
                inheritance_values[i + 1] = genomes_f["thirst_rate_d"]
                inheritance_values[i] = genomes_m["thirst_rate_r"]

        if rnd.randint(1, 20) == 1:
            inheritance_values = self.mutate_genes(inheritance_values)

        return {
            "animal_type": genomes_m["animal_type"],
            "max_age_d": inheritance_values[0],
            "max_age_r": inheritance_values[1],
            "hunger_rate_d": inheritance_values[2],
            "hunger_rate_r": inheritance_values[3],
            "thirst_rate_d": inheritance_values[4],
            "thirst_rate_r": inheritance_values[5],
        }

    def mutate_genes(self, inh_val: list) -> list:
        """Mutation process of genomes.

        Args:
            inh_val (list): contains all inheritable values

        Returns:
            list: the changed inheritable values
        """
        new_values = inh_val

        for i in range(0, 5, 2):
            mut = round((rnd.uniform(new_values[i], new_values[i + 1]) / 4), 2)
            x = rnd.randint(0, 1)
            new_values[i] += mut if x == 0 else (-1) * mut
            new_values[i + 1] += mut if x == 0 else (-1) * mut

        return new_values