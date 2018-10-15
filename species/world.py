import numpy
import random
import lxml.etree
from itertools import product
from species.helpers import logger


# reserved for empty cell, don't change, species types should be integers
EMPTY_CELL_TYPE = 0
# species can be born to empty cell by this count
# of same species in adjacent cells
BIRTH_REQUIRED_ADJACENT_COUNT = 3
# species in cell survives if surrounded by same species
# and their count is between following values
SURVIVE_ADJACENT_COUNT_MIN = 2
SURVIVE_ADJACENT_COUNT_MAX = 3
# species dies overcrowded by this count (or more) of same species
OVERCROWD_TRESHOLD = 4
# species dies isolated if surrounded by this count (or less) of same species
ISOLATION_TRESHOLD = 1


class World:
    """
    class representing n x n matrix with species in cells
    0 - means empty cell
    species are integers
    """
    def __init__(self, world_dim, num_species=0):
        self.world_dim = world_dim
        self.world = numpy.zeros((world_dim, world_dim), dtype=int)
        self.species_types = set()
        self.num_species = num_species

    def populate_from_numpy_array(self, matrix):
        assert matrix.shape[0] == matrix.shape[1], 'Matrix is not diagonal'
        self.world = matrix
        self.world_dim = matrix.shape[0]
        self.species_types = set(numpy.unique(matrix))
        if EMPTY_CELL_TYPE in self.species_types:
            self.species_types.remove(EMPTY_CELL_TYPE)

    def get_dim(self):
        return self.world_dim

    def as_numpy_array(self):
        return self.world

    def populate(self, species_iterator):
        for x, y, species_type in species_iterator:
            val = self.world[x, y]
            if val != EMPTY_CELL_TYPE:
                self.world[x, y] = random.choice([val, species_type])
            else:
                self.world[x, y] = species_type

            self.species_types.add(species_type)
        if EMPTY_CELL_TYPE in self.species_types:
            self.species_types.remove(EMPTY_CELL_TYPE)

        distinct_count = len(self.species_types)
        if distinct_count != self.num_species:
            logger.warning('{} distinct species count found in input file,'
                           ' but {} specified as num_species'
                           .format(distinct_count, self.num_species))

    def iterate(self, print_debug=False):
        new_world = numpy.zeros((self.world_dim, self.world_dim), dtype=int)
        world_changed = False
        for x in range(self.world_dim):
            for y in range(self.world_dim):
                new_val, changed = self._cell_iterate(x, y)
                new_world[x, y] = new_val
                if changed:
                    world_changed = True
        self.world = new_world
        if print_debug:
            print(self.world)
        return world_changed

    def simulate(self, num_iterations, print_debug=False):
        logger.info('Starting world simulation...')
        if print_debug:
            print(self.world)
        for i in range(1, num_iterations+1):
            logger.info('Iteration number: {}'.format(i))
            world_changed = self.iterate(print_debug)
            if not world_changed:
                logger.info('World did not change, simulation stopped.')
                return
        logger.info('Last iteration, simulation stopped.')

    def write_to_xml(self, out_file):
        logger.info('Writing world to xml file {}'.format(out_file))
        et = lxml.etree
        life_el = et.Element('life')
        world_el = et.SubElement(life_el, 'world')

        et.SubElement(world_el, 'cells').text = str(self.world_dim)
        et.SubElement(world_el, 'species').text = str(self.num_species)
        # et.SubElement(world_el, 'iterations').text = str(self.num_iterations)

        organisms_el = et.SubElement(life_el, 'organisms')
        for x in range(self.world_dim):
            for y in range(self.world_dim):
                species = self.world[x, y]
                if species != 0:
                    organism = et.SubElement(organisms_el, 'organism')
                    et.SubElement(organism, 'x_pos').text = str(x)
                    et.SubElement(organism, 'y_pos').text = str(y)
                    et.SubElement(organism, 'species').text = str(species)

        s = et.tostring(life_el, pretty_print=True, encoding='UTF8',
                        xml_declaration=True)
        with open(out_file, 'wb') as f:
            f.write(s)

    def count_adjacent_species(self, x, y):
        # dictionary holding adjacent species counts
        adjacent_species = dict.fromkeys(self.species_types, 0)

        # go through adjacent vertices
        steps = [-1, 0, 1]
        pairs = list(product(steps, steps))
        pairs.remove((0, 0))
        for i, j in pairs:
            # adjacent indices inside world
            if 0 <= x + i < self.world_dim and 0 <= y + j < self.world_dim:
                species_ij = self.world[x + i, y + j]
                if species_ij > 0:
                    adjacent_species[species_ij] += 1
        return adjacent_species

    @staticmethod
    def apply_rules_to_cell(current_species, adjacent_species):
        """
        params:
        current_species (int): current species type in the cell
        adjacent_species (dict): {"key" (int) - species_type,
         "value" (int) - count of adjacent cells with species_type}

        return: (int) new species type after applying organism rules to cell
        """
        if current_species == EMPTY_CELL_TYPE:
            birth_candidates = \
                [s for s in adjacent_species
                 if adjacent_species[s] == BIRTH_REQUIRED_ADJACENT_COUNT]
            if len(birth_candidates) > 0:
                return random.choice(birth_candidates)
            else:
                return EMPTY_CELL_TYPE

        if current_species != EMPTY_CELL_TYPE:
            same_type_count = adjacent_species[current_species]
            if SURVIVE_ADJACENT_COUNT_MIN <= same_type_count <= SURVIVE_ADJACENT_COUNT_MAX:
                return current_species  # survive
            if same_type_count >= OVERCROWD_TRESHOLD:
                return EMPTY_CELL_TYPE  # die, overcrowded
            if same_type_count <= ISOLATION_TRESHOLD:
                return EMPTY_CELL_TYPE  # die, isolation

    def _cell_iterate(self, x, y):
        adjacent_species = self.count_adjacent_species(x, y)
        cell_species = self.world[x, y]
        new_species = self.apply_rules_to_cell(cell_species, adjacent_species)
        changed = cell_species != new_species
        return new_species, changed
