"""Lookup information from factorio data."""

from draftsman.data import recipes

import logging


def raw_item_name(o) -> str:
    return o[0] if isinstance(o, list) else o['name']


def raw_item_quantity(o) -> int:
    return int(o[1] if isinstance(o, list) else o['amount'])


def raw_recipe_get_results(o) -> list[str]:
    if 'normal' in o:
        o = o['normal']
    if 'result' in o:
        return [o['result']]
    else:
        return o['results']


def raw_signal_name(s) -> str:
    return s['signal']['name']


def raw_signal_count(s) -> int:
    return int(s['count'])


def raw_signal_type(s) -> str:
    return s['signal']['type']


def raw_signal_index(s) -> int:
    return int(s['index'])


def get_recipe_ingredients(recipe_name: str) -> dict[str, int]:
    """Returns ingredients in a recipe as a map of (item-name, quantity)."""
    # Assumes "normal" mode rather than "expensive" mode.
    recipe = (
        recipes.raw[recipe_name]['ingredients']
        if 'ingredients' in recipes.raw[recipe_name]
        else recipes.raw[recipe_name]['normal']['ingredients'])
    return {
        raw_item_name(part): raw_item_quantity(part)
        for part in recipe
    }


def guess_recipe_primary_output(recipe_name: str) -> str:
    """Guesses the primary output for a recipe."""
    r = recipes.raw.get(recipe_name, None)
    assert r, f'failed to find recipe with name "{recipe_name}"'

    results = raw_recipe_get_results(r)

    # For now just guess the first item in the list. Better might be to guess the item with the name closest to the
    # name of the recipe.
    g = results[0]

    if isinstance(g, str):
        guess = g
    elif isinstance(g, list):
        guess = g[0]
    else:
        guess = g['name']

    if guess != recipe_name:
        logging.warning(f'guessed recipe primary output was different than recipe name. "{recipe_name}" -> "{guess}"')
    return guess
