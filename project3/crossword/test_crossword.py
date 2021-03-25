import os

import pytest

from crossword import Crossword, Variable
from generate import CrosswordCreator


@pytest.fixture(scope='module')
def small_crossword(request):
    structure = 'data/structure0.txt'
    words = 'data/words0.txt'
    test_dir = 'test_results'
    # os.makedirs(test_dir, exist_ok=True)
    # output = os.path.join(test_dir, 'output0.png')
    # Generate crossword
    crossword = Crossword(structure, words)
    return crossword


def test_enforce_node_consistency(small_crossword):
    creator = CrosswordCreator(small_crossword)
    creator.enforce_node_consistency()
    expected = {
        Variable(0, 1, 'down', 5): {'SEVEN', 'THREE', 'EIGHT'},
        Variable(0, 1, 'across', 3): {
            'ONE',
            'SIX',
            'TEN',
            'TWO',
        },
        Variable(1, 4, 'down', 4): {'NINE', 'FIVE', 'FOUR'},
        Variable(4, 1, 'across', 4): {'NINE', 'FIVE', 'FOUR'}
    }
    assert creator.domains == expected


def test_revise_true(small_crossword):
    creator = CrosswordCreator(small_crossword)
    creator.enforce_node_consistency()
    # based on structure, the first var going across (0, 1) and first var going
    # down (0, 1) should *only* agree on TWO/TEN/SIX and THREE/SEVEN respectively
    revised = creator.revise(Variable(0, 1, 'down', 5),
                             Variable(0, 1, 'across', 3))
    assert revised
    assert creator.domains[Variable(0, 1, 'down', 5)] == {'SEVEN', 'THREE'}


def test_revise_false(small_crossword):
    creator = CrosswordCreator(small_crossword)
    creator.enforce_node_consistency()
    # based on structure, the first var going across (0, 1) and first var going
    # down (0, 1) should *only* agree on TWO/TEN/SIX and THREE/SEVEN respectively
    _ = creator.revise(Variable(0, 1, 'down', 5), Variable(0, 1, 'across', 3))
    # expect that this will not be revised after the first pass
    revised = creator.revise(Variable(0, 1, 'down', 5),
                             Variable(0, 1, 'across', 3))
    assert not revised
    assert creator.domains[Variable(0, 1, 'down', 5)] == {'SEVEN', 'THREE'}


def test_ac3_true(small_crossword):
    creator = CrosswordCreator(small_crossword)
    creator.enforce_node_consistency()
    consistent = creator.ac3()
    assert consistent


def test_ac3_false(small_crossword):
    creator = CrosswordCreator(small_crossword)
    creator.enforce_node_consistency()
    # remove a value that makes it all work
    creator.domains[Variable(0, 1, 'down', 5)].remove('SEVEN')
    consistent = creator.ac3()
    assert not consistent


def test_assignment_complete(small_crossword):
    creator = CrosswordCreator(small_crossword)
    dummy_assignment = {var: 'test' for var in creator.domains}
    complete = creator.assignment_complete(dummy_assignment)
    assert complete


def test_assignment_incomplete_partial(small_crossword):
    creator = CrosswordCreator(small_crossword)
    vars = [var for var in creator.domains]
    dummy_assignment = {vars[0]: 'test'}
    complete = creator.assignment_complete(dummy_assignment)
    assert not complete


def test_assignment_incomplete_none(small_crossword):
    creator = CrosswordCreator(small_crossword)
    dummy_assignment = {var: None for var in creator.domains}
    complete = creator.assignment_complete(dummy_assignment)
    assert not complete


def test_assignment_incomplete_empty(small_crossword):
    creator = CrosswordCreator(small_crossword)
    vars = [var for var in creator.domains]
    dummy_assignment = {var: '' for var in creator.domains}
    complete = creator.assignment_complete(dummy_assignment)
    assert not complete


def test_consistent(small_crossword):
    creator = CrosswordCreator(small_crossword)
    # manually generated assignment
    assignment = {
        Variable(0, 1, 'down', 5): 'SEVEN',
        Variable(0, 1, 'across', 3): 'SIX',
        Variable(4, 1, 'across', 4): 'NINE',
        Variable(1, 4, 'down', 4): 'FIVE'
    }
    assert creator.consistent(assignment)


def test_inconsistent_not_distinct(small_crossword):
    creator = CrosswordCreator(small_crossword)
    # manually generated assignment
    assignment = {
        Variable(0, 1, 'down', 5): 'SEVEN',
        Variable(0, 1, 'across', 3): 'SIX',
        Variable(4, 1, 'across', 4): 'NINE',
        Variable(1, 4, 'down', 4): 'NINE'
    }
    assert not creator.consistent(assignment)


def test_inconsistent_conflict(small_crossword):
    creator = CrosswordCreator(small_crossword)
    # manually generated assignment
    assignment = {
        Variable(0, 1, 'down', 5): 'SEVEN',
        Variable(0, 1, 'across', 3): 'TWO',
    }
    assert not creator.consistent(assignment)


def test_order_domain_values(small_crossword):
    creator = CrosswordCreator(small_crossword)
    creator.enforce_node_consistency()
    var = Variable(0, 1, 'across', 3)
    # partial assignment
    assignment = {Variable(4, 1, 'across', 4): 'NINE'}
    ordered_vals = creator.order_domain_values(var, assignment)
    # 'ONE' should have the most conflicts
    assert ordered_vals[-1] == 'ONE'

def test_order_domain_values_assignment(small_crossword):
    creator = CrosswordCreator(small_crossword)
    creator.enforce_node_consistency()
    var = Variable(0, 1, 'across', 3)
    # partial assignment
    assignment = {Variable(0, 1, 'down', 5): 'SEVEN'}
    ordered_vals = creator.order_domain_values(var, assignment)
    # all orderings equally likely - how to test?
    # assert ordered_vals == ['ONE', 'SIX', 'TEN', 'TWO']

def test_select_unassigned_variable(small_crossword):
    creator = CrosswordCreator(small_crossword)
    creator.enforce_node_consistency()
    # partial assignment
    assignment = {Variable(0, 1, 'down', 5): 'SEVEN'}
    next_var = creator.select_unassigned_variable(assignment)
    # manual inspection shows this should be the next var
    assert next_var == Variable(4, 1, 'across', 4)
