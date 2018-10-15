import logging
import sys

logger = logging.getLogger()
logger.setLevel(logging.INFO)

stdout_handler = logging.StreamHandler(sys.stdout)
stdout_handler.setLevel(logging.INFO)
logger.addHandler(stdout_handler)


class ProcessInputException(Exception):
    pass


def parse_num_val(xml_element):
    try:
        return int(xml_element.text)
    except (TypeError, ValueError) as e:
        logger.error('Could not parse value {} from xml_el {}'
                     .format(xml_element.text, xml_element.tag))
        logger.error(str(e))
        raise ProcessInputException


def species_generator_from_xml_el(organisms_el):
    for organism in organisms_el:
        x = parse_num_val(organism.find('x_pos'))
        y = parse_num_val(organism.find('y_pos'))
        species = parse_num_val(organism.find('species'))
        yield x, y, species
