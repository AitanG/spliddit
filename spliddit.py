from collections import defaultdict
import random
import re
import sys
import time

import algo


fast_print = False


def pr(line, skip_a_line=False, eol=True, no_trailing_newline=False):
    '''Prints line with typing effect to prevent large jumps'''
    if fast_print:
        if skip_a_line:
            print()

        print(line)
        return

    if skip_a_line:
        time.sleep(0.2)
        sys.stdout.write('\n\r')
        time.sleep(0.2)
    else:
        time.sleep(0.4)


    for char in line:
        sys.stdout.write(char)
        time.sleep(random.random() / 20)
        sys.stdout.flush()

    if not no_trailing_newline:
        time.sleep(0.2)
        sys.stdout.write('\n\r')

    if eol:
        time.sleep(0.3)


def collect_input():
    '''Prints instructions and interactively collects algo inputs'''
    pr('Welcome to the Spliddit rent-splitting algorithm!')

    pr('Spliddit finds a room allocation and sets prices for each room to ensure', skip_a_line=True, eol=False)
    pr('everyone is happy with their assignment.')

    pr('Let\'s review the conditions required for the Spliddit algorithm to work:', skip_a_line=True)
    pr(' 1. Each participant is able to come up with values for each room such that:', eol=False)
    pr('    a. The values add up to the total rent', eol=False)
    pr('    b. The participant would be equally happy with any room at those prices', eol=False)
    pr('    c. The participant can afford any room at those prices.')
    pr(' 2. Participants can be trusted to report their preferences honestly and based', eol=False)
    pr('    only on personal preferences.')
    pr(' 3. Participants agree to accept the result of the algorithm without', eol=False)
    pr('    negotiation.',)
    pr(' 4. For N participants, the non-shared parts of the living space can be divided', eol=False)
    pr('    into N partitions that don\'t change based on who is assigned where.')

    pr('If any of these preconditions isn\'t met, specify which one(s), by number, for', skip_a_line=True, eol=False)
    pr('help on how to proceed (comma-separated). Press Enter to continue:')
    inp = input()

    issues = set(re.split(', | |,|[A-Za-z]', inp))
    if '1' in issues:
        pr('For precondition 1: If (total rent / 3) is over a participant\'s budget, the', skip_a_line=True, eol=False)
        pr('only way Spliddit can work is if everyone agrees beforehand that the', eol=False)
        pr('participant should get a particular room at a particular price. Then the', eol=False)
        pr('remaining participants can run Spliddit on the remaining rooms.')
    if '2' in issues:
        pr('For precondition 2: Any participant who misrepresents their preferences runs', skip_a_line=True, eol=False)
        pr('the risk of ending up with an allocation they don\'t like. More', eol=False)
        pr('importantly, participants should reconsider their choice to live with someone', eol=False)
        pr('who might act selfishly.')
    if '3' in issues:
        pr('For precondition 3: The Spliddit algorithm makes certain guarantees in order', skip_a_line=True, eol=False)
        pr('to be fair to everyone. If everyone has faithfully reported their preferences,', eol=False)
        pr('any deviation from the outcome will result in one party gaining at another\'s', eol=False)
        pr('expense. To mitigate against this, make sure everyone follows instructions and', eol=False)
        pr('agrees not to negotiate.')
    if '4' in issues:
        pr('For precondition 4: If there are contingencies like storage space, sharing of', skip_a_line=True, eol=False)
        pr('bathrooms, or special privileges or duties that depend on who gets which room,', eol=False)
        pr('Spliddit may not work. If possible, resolve these questions after executing', eol=False)
        pr('Spliddit, with agreements such as "person A agrees to pay persons B and C $50', eol=False)
        pr('each for the private bathroom".')

    pr('Before continuing, have on hand the following information:', skip_a_line=True)
    pr(' 1. Total rent owed to landlord')
    pr(' 3. Unique names for each room/partition (up to 20)')
    pr(' 2. Unique names for each participant')
    pr(' 4. Each participant\'s personal values for each room.')

    pr('(Press Enter when ready)', skip_a_line=True)
    inp = input()

    pr('How many rooms/participants?', skip_a_line=True)
    while True:
        inp = input()
        n = int(inp)
        if n < 2:
            pr('Spliddit requires at least two participants, try again:')
        elif n > 20:
            pr('This program works for a maximum of 20 participants, try again:')
        else:
            break

    pr('Enter names of rooms, each one on a new line. Enter when finished:', skip_a_line=True)
    rooms = []
    while len(rooms) < n:
        inp = input()
        if inp:
            if inp in rooms:
                pr('Room already provided, try another name for it:')
            else:
                rooms.append(inp)

    pr('Enter names of participants, each one on a new line:', skip_a_line=True)
    people = []
    while len(people) < len(rooms):
        inp = input()
        if inp:
            if inp in people:
                pr('Name already provided, try specifying a last name:')
            else:
                people.append(inp)

    pr('Enter total rent (e.g. 1234.56):', skip_a_line=True)
    inp = input()
    inp = re.sub(r'[^\.0-9]', '', inp)
    total_rent = float(inp)

    pr('Enter values by person...', skip_a_line=True)
    prefs_by_person = defaultdict(list)
    for person in people:
        while True:  # keep trying until values add up to total rent
            for room in rooms:
                pr(f'{person} values "{room}" at: ', no_trailing_newline=True)
                inp = input()
                inp = re.sub(r'[^\.0-9]', '', inp)
                prefs_by_person[person].append(float(inp))

            if sum(prefs_by_person[person]) != total_rent:
                pr(f'{person}\'s values don\'t add up to total rent. Try again...')
                prefs_by_person[person] = list()
                continue

            if max(prefs_by_person[person]) - min(prefs_by_person[person]) >= total_rent / (len(people) - 1):
                pr(f'Spliddit doesn\'t work if a person values a room at (total rent / {len(people) - 1}) or more. Try again...')
                prefs_by_person[person] = list()
                continue

            break

    return people, rooms, total_rent, prefs_by_person


def print_optimal_assignment(rooms, prefs_by_person, assignment):
    '''Prints information about who is assigned to which room'''
    pr('Socially optimal assignment:', skip_a_line=True)
    for person, room_index in assignment.items():
        pr(f'{person} -> {rooms[room_index]} (values at: ${prefs_by_person[person][assignment[person]]})')


def handle_rounding_issues(total_rent, price):
    '''
    In the case of irrational results, adds or subtracts pennies from a
    random selection of participants to make prices add up to total rent
    '''
    sum_prices = round(sum(price.values()), 2)
    amount_to_divide = round(total_rent - sum_prices, 2)
    n = round(amount_to_divide / 0.01)
    extra_rent = [0.01] * n + [0] * (len(price) - n)
    random.shuffle(extra_rent)
    i = 0
    price_ = {}
    for person, p in price.items():
        price_[person] = p + extra_rent[i]
        i += 1
    return price_, amount_to_divide


def print_final_rent(total_rent, price, assignment, rooms):
    '''Prints information about final prices'''
    price_ = price
    optional_note = ''
    if total_rent != sum(price.values()):
        price_, amount_to_divide = handle_rounding_issues(total_rent, price)
        optional_note = f' (difference of {amount_to_divide} distributed randomly)'

    pr(f'Final rent{optional_note}:', skip_a_line=True)
    for name, p in price_.items():
        pr(f"{name}: ${p} for {rooms[assignment[name]]}")


def print_envy_explanation(people, prefs_by_person, assignment, price, happiness):
    '''Prints explanation of how the results are envy-free'''
    for name in people:
        pr(f'{name} is envy-free. At these room prices, {name}\'s happiness is {happiness[name]}. In comparison:', skip_a_line=True)
        for name_ in assignment:
            if name_ == name:
                continue

            pr(f'If assigned {name_}\'s room, {name}\'s happiness would be {round(prefs_by_person[name][assignment[name_]] - price[name_], 2)}.')
            assert(happiness[name] - (prefs_by_person[name][assignment[name_]] - price[name_]) > -1)


def print_pettiness_explanation(happiness):
    '''Prints explanation of how the results are minimized'''
    min_happiness = min(happiness.values())
    max_happiness = max(happiness.values())
    if min_happiness == max_happiness:
        pr('Everyone has the same happiness, so pettiness is 0!', skip_a_line=True)
    else:
        pr(f'The lowest happiness is {min_happiness} and the highest happiness is {max_happiness}.', skip_a_line=True)
        pr(f'This means the minimum pettiness found by the model is {max_happiness - min_happiness}.')


def print_results(people, rooms, prefs_by_person, assignment, price, happiness, total_rent):
    '''Prints the results of the algorithm, including explanation'''
    print_optimal_assignment(rooms, prefs_by_person, assignment)
    print_final_rent(total_rent, price, assignment, rooms)
    print_envy_explanation(people, prefs_by_person, assignment, price, happiness)
    print_pettiness_explanation(happiness)


def main():
    '''Interactively executes the Spliddit algorithm and explains the results'''
    global fast_print
    fast_print = len(sys.argv) >= 2 and sys.argv[1] == 'fast'
    people, rooms, total_rent, prefs_by_person = collect_input()
    assignment, price, happiness = algo.execute(people, total_rent, prefs_by_person)
    print_results(people, rooms, prefs_by_person, assignment, price, happiness, total_rent)


if __name__ == '__main__':
    main()
