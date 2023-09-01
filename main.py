"""
Load a partially populated CastleVantress production scaffold and attempt to dynamically assign recipes and combinator
settings.
"""

from draftsman.blueprintable import Blueprint
from draftsman.data import mods

import cv
import order
import logging
import pyperclip

SCAFFOLD_BLUEPRINT_FILE = 'scaffold_blueprint.txt'


def read_file(path: str) -> str:
    with open(path, 'r') as f:
        return f.read()


def check_mods():
    assert len(mods.mod_list) > 5


def cv_extend():
    """Takes a cv block and guesses new recipes and populates combinators."""
    # Read blueprint
    # blueprint = Blueprint(read_file(SCAFFOLD_BLUEPRINT_FILE))  # from file
    blueprint = Blueprint(pyperclip.paste())  # from copy buffer
    # Find all py automated factories
    factories = cv.find_factories_grid(blueprint)
    # Guess recipes for factories below other factories (assumes mkN -> mkN+1)
    # Use cv.Direction.EAST to use the next recipe in the recipe list
    cv.guess_factory_recipes(factories, directions=[cv.Direction.SOUTH])
    # Set all the combinators.
    cv.set_all_combinators(blueprint)
    # Output the resulting blueprint to clipboard
    pyperclip.copy(blueprint.to_string())


def populate_combinators():
    blueprint = Blueprint(pyperclip.paste())
    cv.set_all_combinators(blueprint)
    pyperclip.copy(blueprint.to_string())


def main():
    logging.basicConfig(level=logging.INFO)
    check_mods()
    populate_combinators()


if __name__ == '__main__':
    main()
