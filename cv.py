"""Functions specific to CastleVantress design."""

from collections.abc import Iterable
from draftsman.blueprintable import Blueprint
from draftsman.entity import AssemblingMachine, ConstantCombinator
from draftsman.utils import AABB
from enum import Enum

import factorio
import logging
import position
import pymod

CV_WIDTH = 10
CV_HEIGHT = 8
CV_HALF_HEIGHT = 4


def left(p):
    y, x = p
    # previous row
    if y > 0 and x == 0:
        return y - 1, CV_WIDTH - 1
    return None if x <= 0 else (y, x - 1)


def right(p):
    y, x = p
    # next row
    if y < CV_HEIGHT - 1 and x == CV_WIDTH - 1:
        return y + 1, 0
    return None if x >= CV_WIDTH - 1 else (y, x + 1)


def up(p):
    y, x = p
    return None if y <= 0 else (y - 1, x)


def down(p):
    y, x = p
    return None if y == CV_HALF_HEIGHT - 1 or y >= CV_HEIGHT - 1 else (y + 1, x)


def find_blue_recipe_combinator(blueprint: Blueprint, factory: AssemblingMachine) -> ConstantCombinator:
    x, y = factory.tile_position
    target: AABB = position.aabb_for_tile_position(x+7, y+6)
    cs = blueprint.find_entities_filtered(name='constant-combinator', area=target)
    assert len(cs) == 1
    c = cs[0]
    assert isinstance(c, ConstantCombinator)
    sig = c.get_signal(0)
    assert factorio.raw_signal_name(sig) == 'signal-cyan'
    return c


def set_all_blue_recipe_combinators(blueprint: Blueprint, factories: Iterable[AssemblingMachine]):
    for factory in factories:
        if not factory.recipe:
            continue
        c: ConstantCombinator = find_blue_recipe_combinator(blueprint, factory)
        ingredients = factorio.get_recipe_ingredients(factory.recipe)
        for i, (name, quantity) in enumerate(ingredients.items()):
            if i+1 >= 20:
                logging.warning(
                    f'"{factory.recipe}" recipe has more than 19 ingredients, some ingredients skipped.')
                continue
            c.set_signal(i+1, name, quantity)


def find_red_output_combinator(blueprint: Blueprint, factory: AssemblingMachine) -> ConstantCombinator:
    x, y = factory.tile_position
    target: AABB = position.aabb_for_tile_position(x+7, y+8)
    cs = blueprint.find_entities_filtered(name='constant-combinator', area=target)
    assert len(cs) == 1
    c = cs[0]
    assert isinstance(c, ConstantCombinator)
    sig = c.get_signal(0)
    assert factorio.raw_signal_name(sig) == 'signal-red'
    return c


def set_all_red_output_combinators(blueprint: Blueprint, factories: Iterable[AssemblingMachine]):
    for factory in factories:
        if not factory.recipe:
            continue
        c: ConstantCombinator = find_red_output_combinator(blueprint, factory)
        item_name = factorio.guess_recipe_primary_output(factory.recipe)
        index = 1
        sig = c.get_signal(index)
        assert factorio.raw_signal_name(sig) == 'signal-info' or factorio.raw_signal_name(sig) == item_name
        c.set_signal(index, item_name, 1)


def find_factories(blueprint: Blueprint) -> list[AssemblingMachine]:
    """Finds all factories in the blueprint."""
    factories: list[AssemblingMachine] = blueprint.find_entities_filtered(name='automated-factory-mk01')
    position.sort_top_to_bottom_left_to_right(factories)
    return factories


def set_all_combinators(blueprint: Blueprint):
    """Sets all CV-style logistics combinators adjacent to factories in the blueprint."""
    factories: list[AssemblingMachine] = find_factories(blueprint)
    set_all_red_output_combinators(blueprint, factories)
    set_all_blue_recipe_combinators(blueprint, factories)


def find_factories_grid(bp: Blueprint) -> dict[tuple[int, int], AssemblingMachine]:
    """
    Returns the 80 factories in a CastleVantress block by (y,x) index.

    Visually:
      (0,0) (0,1) (0,2) ..... (0,9)
      (1,0) (1,1) (1,2) ..... (1,9)
      ..... ..... ..... ..... .....
      (7,0) (7,1) (7,2) ..... (7,9)
    """
    factories: list[AssemblingMachine] = bp.find_entities_filtered(name='automated-factory-mk01')
    position.sort_top_to_bottom_left_to_right(factories)

    # Assumes 10x8 factories per CV block
    result = dict()
    assert len(factories) == 80
    x = 0
    y = 0
    for f in factories:
        result[(y, x)] = f
        x += 1
        if x == CV_WIDTH:
            x = 0
            y += 1
    return result


def guess_factory_recipes(factories: dict[tuple[int, int], AssemblingMachine], directions=None):
    """Attempts to guess CastleVantress recipes from nearby assemblers."""
    if directions is None:
        directions = [Direction.NORTH, Direction.SOUTH]

    if Direction.SOUTH in directions:
        for y in range(CV_HEIGHT):
            for x in range(CV_WIDTH):
                guess_adjacent_factory_recipes(factories, y, x, directions=[Direction.SOUTH])

    if Direction.NORTH in directions:
        for y in reversed(range(CV_HEIGHT)):
            for x in range(CV_WIDTH):
                guess_adjacent_factory_recipes(factories, y, x, directions=[Direction.NORTH])

    if Direction.EAST in directions:
        for y in range(CV_HEIGHT):
            for x in range(CV_WIDTH):
                guess_adjacent_factory_recipes(factories, y, x, directions=[Direction.EAST])

    if Direction.WEST in directions:
        for y in reversed(range(CV_HEIGHT)):
            for x in reversed(range(CV_WIDTH)):
                guess_adjacent_factory_recipes(factories, y, x, directions=[Direction.WEST])


class Direction(Enum):
    NORTH = (-1, 0)
    SOUTH = (1, 0)
    WEST = (0, -1)
    EAST = (0, 1)


def guess_adjacent_factory_recipes(
        factories: dict[tuple[int, int], AssemblingMachine], y: int, x: int, directions=None):
    """Attempts to guess the recipes of adjacent assemblers for CastleVantress factories."""
    if directions is None:
        directions = [e.value for e in Direction]
    p = (y, x)
    f = factories.get(p, None)
    if f is None or f.recipe is None:
        return
    recipe_index = f.recipes.index(f.recipe)

    north = Direction.NORTH in directions and up(p) and factories[up(p)]
    if north and north.recipe is None:
        guess = pymod.guess_downgraded_name(f.recipe)
        if guess in north.recipes:
            north.recipe = guess

    south = Direction.SOUTH in directions and down(p) and factories[down(p)]
    if south and south.recipe is None:
        guess = pymod.guess_upgraded_name(f.recipe)
        if guess in south.recipes:
            south.recipe = guess

    west = Direction.WEST in directions and left(p) and factories[left(p)]
    if west and west.recipe is None and recipe_index > 0:
        guess = f.recipes[recipe_index - 1]
        if guess in west.recipes:
            west.recipe = guess

    east = Direction.EAST in directions and right(p) and factories[right(p)]
    if east and east.recipe is None and recipe_index < len(f.recipes) - 1:
        guess = f.recipes[recipe_index + 1]
        if guess in east.recipes:
            east.recipe = guess
