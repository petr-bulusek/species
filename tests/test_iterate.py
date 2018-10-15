import context
import numpy
from species.world import World


def test_birth_isolation():
    w = World(world_dim=2, num_species=4)
    a_0 = numpy.array([[1, 1, 1],
                       [0, 0, 0],
                       [0, 0, 0]])
    w.populate_from_numpy_array(a_0)
    w.iterate()
    a_1 = numpy.array([[0, 1, 0],
                       [0, 1, 0],
                       [0, 0, 0]])
    assert numpy.array_equal(w.as_numpy_array(), a_1)
    a_2 = numpy.array([[0, 0, 0],
                       [0, 0, 0],
                       [0, 0, 0]])
    w.iterate()
    assert numpy.array_equal(w.as_numpy_array(), a_2)


def test_overcrowded():
    w = World(world_dim=2, num_species=4)
    a_0 = numpy.array([[1, 1, 1],
                       [1, 1, 1],
                       [1, 1, 1]])
    w.populate_from_numpy_array(a_0)
    w.iterate()
    a_1 = numpy.array([[1, 0, 1],
                       [0, 0, 0],
                       [1, 0, 1]])

    assert numpy.array_equal(w.as_numpy_array(), a_1)
    a_2 = numpy.array([[0, 0, 0],
                       [0, 0, 0],
                       [0, 0, 0]])
    w.iterate()
    assert numpy.array_equal(w.as_numpy_array(), a_2)
