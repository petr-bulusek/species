import context
import numpy
from species.world import World


def test_adjacent():
    w = World(world_dim=2, num_species=4)
    a = numpy.array([[1, 2, 3],
                     [1, 2, 1],
                     [3, 1, 0]])
    w.populate_from_numpy_array(a)
    assert w.count_adjacent_species(0, 0) == {1: 1, 2: 2, 3: 0}
    assert w.count_adjacent_species(0, 1) == {1: 3, 2: 1, 3: 1}
    assert w.count_adjacent_species(0, 2) == {1: 1, 2: 2, 3: 0}
    assert w.count_adjacent_species(1, 0) == {1: 2, 2: 2, 3: 1}
    assert w.count_adjacent_species(1, 1) == {1: 4, 2: 1, 3: 2}
    assert w.count_adjacent_species(1, 2) == {1: 1, 2: 2, 3: 1}
    assert w.count_adjacent_species(2, 0) == {1: 2, 2: 1, 3: 0}
    assert w.count_adjacent_species(2, 1) == {1: 2, 2: 1, 3: 1}
    assert w.count_adjacent_species(2, 2) == {1: 2, 2: 1, 3: 0}
