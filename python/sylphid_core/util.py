import collections
import copy


def dict_merge(under, over, in_place=False):
    """
    Merge 2 dictionaries into a composite of the 2.

    values from 'over' overwrite values from 'under'

    Args:
        under: default data
        over: data to write over default data
        in_place(bool): write changes directly into the under dict

    Returns:
        dict: dictionary composite of under and over

    """
    if not in_place:
        under = copy.deepcopy(under)

    for over_k, over_v in over.items():
        if issubclass(over_v.__class__, collections.Mapping):
            under_v = under.setdefault(over_k, {})
            if issubclass(under_v.__class__, collections.Mapping):
                under[over_k] = dict_merge(under_v, over_v)
            else:
                under[over_k] = over_v
        else:
            under[over_k] = over_v

    return under
