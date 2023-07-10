import numpy as np
from pulp import LpMinimize, LpProblem, LpVariable, lpSum
from scipy.optimize import linear_sum_assignment


def assign_rooms(people, prefs_by_person):
    '''Applies Hungarian algorithm to come up with optimal room allocation'''
    # Initialize cost matrix (negative of prefs because cost is minimized)
    prefs = np.array([prefs for prefs in prefs_by_person.values()])
    cost = np.zeros((len(people),) * 2) - prefs

    # Apply Hungarian algorithm to find optimal assignment
    row_indices, col_indices = linear_sum_assignment(cost)

    # Initialize structures
    assignment = {}
    for row, col in zip(row_indices, col_indices):
        assignment[people[row]] = col

    return assignment


def solve_lp(people, total_rent, prefs_by_person, assignment):
    '''Solves a linear program to minimize max pettiness'''
    # Set up linear program
    model = LpProblem(name="room-assignment", sense=LpMinimize)

    # Initialize variables
    y = LpVariable(name="Maximum Pettiness", lowBound=0)
    price_vars = {}
    for name in people:
        var = LpVariable(name=f'{name}\'s Rent', lowBound=0)
        price_vars[name] = var

    # Set up constraints
    for name in people:
        for name_ in people:
            if name_ == name:
                continue

            # Minimize pettiness
            happiness = prefs_by_person[name][assignment[name]] - price_vars[name]
            happiness_ = prefs_by_person[name_][assignment[name_]] - price_vars[name_]
            model += (happiness - happiness_ <= y,
                      f'{name_} pettiness for {name}')

            # Ensure envy-freeness
            model += (happiness >= (prefs_by_person[name][assignment[name_]] - price_vars[name_]),
                      f'{name} envy for {name_}')

    # Ensure sum of prices is equal to rent
    model += (lpSum(list(price_vars.values())) == total_rent, "total rent")

    # Add the objective function to the model
    model += y

    # Solve the problem
    model.solve()

    return model.variables()


def set_rent(people, total_rent, prefs_by_person, assignment):
    '''Determines how much each person should pay for their room'''
    variables = solve_lp(people, total_rent, prefs_by_person, assignment)

    # Initialize price and happiness maps
    price = {}
    happiness = {}
    for var in variables:
        if 'Rent' in var.name:
            name, val = var.name.split('\'')[0], round(var.value(), 2)
            price[name] = val
            happiness[name] = round(prefs_by_person[name][assignment[name]] - val, 2)

    return price, happiness


def assert_desiderata(people, prefs_by_person, assignment, price, happiness, total_rent):
    '''Make sure the results are valid——i.e. rent is made and no one is envious'''
    # Assert rent is made
    assert(abs(sum(price.values()) - total_rent) < 0.01 * len(people))

    # Assert envy-freeness
    for name in people:
        for name_ in people:
            if name_ == name:
                continue
            assert(happiness[name] - (prefs_by_person[name][assignment[name_]] - price[name_]) > -1)


def execute(people, total_rent, prefs_by_person):
    '''Executes the Spliddit algorithm'''
    assignment = assign_rooms(people, prefs_by_person)
    price, happiness = set_rent(people, total_rent, prefs_by_person, assignment)
    assert_desiderata(people, prefs_by_person, assignment, price, happiness, total_rent)
    return assignment, price, happiness
