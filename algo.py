import numpy as np
from pulp import LpMinimize, LpProblem, LpVariable, lpSum
from scipy.optimize import linear_sum_assignment


def assign_rooms(people, prefs_by_person):
    # Initialize cost matrix (negative of prefs because cost is minimized)
    prefs = np.array([prefs for prefs in prefs_by_person.values()])
    cost = np.zeros((3, 3)) - prefs

    # Apply Hungarian algorithm to find optimal assignment
    row_indices, col_indices = linear_sum_assignment(cost)

    # Initialize structures
    value = {}
    assignment = {}
    for row, col in zip(row_indices, col_indices):
        value[people[row]] = prefs[row, col]
        assignment[people[row]] = col

    return value, assignment


def solve_lp(people, total_rent, values, prefs_by_person, assignment):
    # TODO: get rid of values variable, instead use prefs_by_person and assignments
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
            model += ((values[name] - price_vars[name]) - (values[name_] - price_vars[name_]) <= y,
                      f'{name_} pettiness for {name}')

            # Ensure envy-freeness
            model += ((values[name] - price_vars[name]) >= (prefs_by_person[name][assignment[name_]] - price_vars[name_]),
                      f'{name} envy for {name_}')

    # Ensure sum of prices is equal to rent
    model += (lpSum(list(price_vars.values())) == total_rent, "total rent")

    # Add the objective function to the model
    model += y

    # Solve the problem
    model.solve()

    return model.variables()


def set_rent(people, total_rent, prefs_by_person, value, assignment):
    variables = solve_lp(people, total_rent, value, prefs_by_person, assignment)

    # Initialize price and happiness maps
    price = {}
    happiness = {}
    for var in variables:
        if 'Rent' in var.name:
            name, value = var.name.split('\'')[0], round(var.value(), 2)
            price[name] = value
            happiness[name] = round(prefs_by_person[name][assignment[name]] - value, 2)

    return price, happiness


def assert_desiderata(people, prefs_by_person, assignment, price, happiness, total_rent):
    # Assert rent is made
    assert(abs(sum(price.values()) - total_rent) < 0.01 * len(people))

    # Assert envy-freeness
    for name in people:
        for name_ in people:
            if name_ == name:
                continue
            assert(happiness[name] - (prefs_by_person[name][assignment[name_]] - price[name_]) > -1)


def execute(people, total_rent, prefs_by_person):
    value, assignment = assign_rooms(people, prefs_by_person)
    price, happiness = set_rent(people, total_rent, prefs_by_person, value, assignment)
    assert_desiderata(people, prefs_by_person, assignment, price, happiness, total_rent)
    return value, assignment, price, happiness
