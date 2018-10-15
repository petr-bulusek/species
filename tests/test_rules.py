import context
from species.world import World


def test_survive():
    assert 1 == World.apply_rules_to_cell(current_species=1,
                                          adjacent_species={1: 2})

    assert 1 == World.apply_rules_to_cell(current_species=1,
                                          adjacent_species={1: 3})


def test_isolated():
    assert 0 == World.apply_rules_to_cell(current_species=1,
                                          adjacent_species={1: 1})

    assert 0 == World.apply_rules_to_cell(current_species=1,
                                          adjacent_species={1: 0})


def test_overcrowded():
    assert 0 == World.apply_rules_to_cell(current_species=1,
                                          adjacent_species={1: 4})

    assert 0 == World.apply_rules_to_cell(current_species=1,
                                          adjacent_species={1: 5})


def test_birth():
    assert 1 == World.apply_rules_to_cell(current_species=0,
                                          adjacent_species={1: 3})

    assert 2 == World.apply_rules_to_cell(current_species=0,
                                          adjacent_species={2: 3})
