from Algorithms.csp import CSP

class GameTheory:
    def __init__(self):
        pass

    def predator_prey_game(self, predator_count, prey_count):
        """
        Simulates a predator-prey game using CSP.
        Args:
            predator_count (int): Number of predators.
            prey_count (int): Number of prey.
        Returns:
            tuple: (predator_strategy, prey_strategy)
        """
        variables = ['predator', 'prey']
        domains = {
            'predator': ['Hunt', 'Rest'],
            'prey': ['Hide', 'Graze']
        }

        def predator_constraint(var, value, assignment):
            if var == 'predator' and 'prey' in assignment:
                if value == 'Hunt' and assignment['prey'] == 'Hide':
                    return False
            return True

        def prey_constraint(var, value, assignment):
            if var == 'prey' and 'predator' in assignment:
                if value == 'Hide' and assignment['predator'] == 'Hunt':
                    return False
            return True

        constraints = [predator_constraint, prey_constraint]

        csp = CSP(variables, domains, constraints)
        solution = csp.solve()

        predator_strategy = solution['predator']
        prey_strategy = solution['prey']

        return predator_strategy, prey_strategy