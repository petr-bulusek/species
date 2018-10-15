import context
import numpy
import os
import lxml.etree
from species.world import World
from species.main import read_world_simulation_from_xml
from species.helpers import parse_num_val, species_generator_from_xml_el


def test_read_input():
    world, num_species, num_iterations =\
        read_world_simulation_from_xml('test_input.xml')
    a = world.as_numpy_array()
    b = numpy.array([[1, 2],
                     [3, 4]])
    assert numpy.array_equal(a, b)
    assert num_species == 4
    assert num_iterations == 10


def test_write_xml():
    w = World(world_dim=2, num_species=4)
    a = numpy.array([[1, 2],
                     [3, 4]])
    w.populate_from_numpy_array(a)
    test_out_file = 'test_out.xml'
    w.write_to_xml(test_out_file)

    tree = lxml.etree.parse(test_out_file)
    root = tree.getroot()
    world_el = root.find('world')
    cells_el = world_el.find('cells')
    species = world_el.find('species')
    world_dim = parse_num_val(cells_el)
    assert world_dim == 2
    num_species = parse_num_val(species)
    assert num_species == 4

    organisms_el = root.find('organisms')
    species_iter = species_generator_from_xml_el(organisms_el)
    species_list = list(species_iter)
    assert len(species_list) == 4
    assert (0, 0, 1) in species_list
    assert (0, 1, 2) in species_list
    assert (1, 0, 3) in species_list
    assert (1, 1, 4) in species_list
    os.remove('test_out.xml')
