import algo


def test_basic():
    people = ['A', 'B']
    rooms = ['a', 'b']
    total_rent = 700
    prefs_by_person = {
        'A': [400, 300],
        'B': [300, 400],
    }

    assignment, price, happiness = algo.execute(people, total_rent, prefs_by_person)
    assert(rooms[assignment['A']] == 'a')
    assert(rooms[assignment['B']] == 'b')
    for name in people:
        assert(round(happiness[name], 2) == 50)
        assert(price[name] == 350)

    algo.assert_desiderata(people, prefs_by_person, assignment, price, happiness, total_rent)


def test_irrational():
    people = ['A', 'B', 'C']
    rooms = ['a', 'b', 'c']
    total_rent = 1000
    prefs_by_person = {
        'A': [400, 300, 300],
        'B': [300, 400, 300],
        'C': [300, 300, 400],
    }

    assignment, price, happiness = algo.execute(people, total_rent, prefs_by_person)
    assert(rooms[assignment['A']] == 'a')
    assert(rooms[assignment['B']] == 'b')
    assert(rooms[assignment['C']] == 'c')
    for name in people:
        assert(round(happiness[name], 2) == 66.67)
        assert(round(price[name], 2) == 333.33)
        
    algo.assert_desiderata(people, prefs_by_person, assignment, price, happiness, total_rent)

def test_asymmetric():
    people = ['A', 'B', 'C', 'D']
    rooms = ['a', 'b', 'c', 'd']
    total_rent = 1200
    prefs_by_person = {
        'A': [350, 250, 400, 200],
        'B': [355, 245, 400, 200],
        'C': [360, 250, 390, 200],
        'D': [320, 250, 420, 210],
    }
    assignment, price, happiness = algo.execute(people, total_rent, prefs_by_person)
    assert(rooms[assignment['A']] == 'b')
    assert(rooms[assignment['B']] == 'd')
    assert(rooms[assignment['C']] == 'a')
    assert(rooms[assignment['D']] == 'c')
    assert(price['A'] == 246.25)
    assert(price['B'] == 196.25)
    assert(price['C'] == 351.25)
    assert(price['D'] == 406.25)
    assert(happiness['A'] == 3.75)
    assert(happiness['B'] == 3.75)
    assert(happiness['C'] == 8.75)
    assert(happiness['D'] == 13.75)

    algo.assert_desiderata(people, prefs_by_person, assignment, price, happiness, total_rent)
