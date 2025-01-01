class CSP:
    def __init__(self, variables, domains, constraints):
        self.variables = variables
        self.domains = domains
        self.constraints = constraints
        self.assignment = {}

    def is_consistent(self, var, value):
        for constraint in self.constraints:
            if not constraint(var, value, self.assignment):
                return False
        return True

    def select_unassigned_variable(self):
        for var in self.variables:
            if var not in self.assignment:
                return var
        return None

    def order_domain_values(self, var):
        return self.domains[var]

    def forward_checking(self, var, value):
        for neighbor in self.variables:
            if neighbor != var and neighbor not in self.assignment:
                for neighbor_value in self.domains[neighbor]:
                    if not self.is_consistent(neighbor, neighbor_value):
                        self.domains[neighbor].remove(neighbor_value)
                if not self.domains[neighbor]:
                    return False
        return True

    def backtrack(self):
        if len(self.assignment) == len(self.variables):
            return self.assignment

        var = self.select_unassigned_variable()
        for value in self.order_domain_values(var):
            if self.is_consistent(var, value):
                self.assignment[var] = value
                if self.forward_checking(var, value):
                    result = self.backtrack()
                    if result:
                        return result
                del self.assignment[var]

        return None

    def solve(self):
        return self.backtrack()