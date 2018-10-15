import click
import lxml.etree
from species.world import World
from species.helpers import logger, parse_num_val,\
    species_generator_from_xml_el, ProcessInputException


def read_world_simulation_from_xml(file_path):
    try:
        tree = lxml.etree.parse(file_path)
    except lxml.etree.ParseError as e:
        logger.error('Could not parse xml file.')
        logger.error(str(e))
        raise ProcessInputException

    root = tree.getroot()
    world_el = root.find('world')
    cells_el = world_el.find('cells')
    species = world_el.find('species')
    iterations_el = world_el.find('iterations')
    world_dim = parse_num_val(cells_el)
    num_species = parse_num_val(species)
    num_iterations = parse_num_val(iterations_el)

    organisms_el = root.find('organisms')
    species_iter = species_generator_from_xml_el(organisms_el)

    world = World(world_dim=world_dim, num_species=num_species)
    try:
        world.populate(species_iterator=species_iter)
    except IndexError as e:
        logger.error('Could not populate world.')
        logger.error(str(e))
        raise ProcessInputException

    return world, num_species, num_iterations


@click.command()
@click.argument('input_file_path', type=click.Path(exists=True))
@click.option('-o', '--output_file', default='out.xml')
@click.option('-p', '--print_debug', is_flag=True, default=False)
def run_simulation(input_file_path, output_file, print_debug):
    try:
        world, num_species, num_iterations = \
            read_world_simulation_from_xml(input_file_path)
    except ProcessInputException:
        logger.error('Could not load simulation from xml file.')
    except Exception as e:
        logger.error("Unexpected error in processing input: {}".format(str(e)))
        raise

    dim = world.get_dim()
    logger.info('Loaded world {}x{} with {} distinct species'
                .format(dim, dim, num_species))
    logger.info('Number iterations defined: {}'.format(num_iterations))

    world.simulate(num_iterations, print_debug=print_debug)
    world.write_to_xml(output_file)


if __name__ == '__main__':
    run_simulation()
