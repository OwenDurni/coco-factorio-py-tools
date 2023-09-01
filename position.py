"""Position related functions."""
import draftsman.utils
from draftsman.classes.entity import Entity


def sort_top_to_bottom_left_to_right(entities: list[Entity]):
    """Sorts entities by (y,x) coordinate."""
    return entities.sort(key=lambda e: (e.position.y, e.position.x))


def aabb_for_tile_position(x: int, y: int) -> draftsman.utils.AABB:
    """Returns a 1x1 area covering the tile at the specified tile_position."""
    return draftsman.utils.AABB(x, y, x+1, y+1)
