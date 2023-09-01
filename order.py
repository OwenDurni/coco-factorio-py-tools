"""Load factorio groups and ordering."""

import draftsman.data.items


def item_group(m: str) -> str:
    """Returns the group for an item with name `m`."""
    return _subgroup_to_group[item_subgroup(m)]


def item_subgroup(m: str) -> str:
    """Returns the subgroup for an item with name `m`."""
    item = draftsman.data.items.raw[m]
    return item['subgroup']


def item_order(m: str) -> str:
    """Returns the factorio `order` string for an item with name `m`."""
    return draftsman.data.items.raw[m]['order']


def item_is_hidden(m: str) -> bool:
    """Returns whether the item is flagged as hidden in factorio data."""
    item = draftsman.data.items.raw[m]
    return 'hidden' in item.get('flags', {})


#
# Module static initialization below here
#

# dictionary from group-name to index among all ordered groups (used in sorting)
_group_index = {
    group: index
    for index, group in enumerate(draftsman.data.items.groups)
}

# dictionary from subgroup-name to index among all ordered subgroups (used in sorting)
_subgroup_index = {
    subgroup: index
    for index, subgroup in enumerate(draftsman.data.items.subgroups)
}

# dictionary from subgroup-name to group-name
_subgroup_to_group = {}
for group, group_dict in draftsman.data.items.groups.items():
    for subgroup in group_dict['subgroups']:
        _subgroup_to_group[subgroup] = group

# dictionary from item-name to (group-index, subgroup-index, order, item-name)
_item_to_sort_index = {
    m: (_group_index[item_group(m)], _subgroup_index[item_subgroup(m)], item_order(m), m)
    for m in draftsman.data.items.raw if not item_is_hidden(m)
}
_all_items_sorted = sorted(_item_to_sort_index.values())

# dictionary from item-name to index in _all_items_sorted (used to find adjacent items)
_item_index = {}
for i, x in enumerate(_all_items_sorted):
    _, _, _, item_name = x
    _item_index[item_name] = i
