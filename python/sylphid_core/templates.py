"""
"""

import re
import copy

from sylphid_core import errors, constants


def _expand_template(name, templates):
    """get the named template, and resolve all nested template references.

    WARNING: this method modifies the templates dictionary in place.

    Args:
        name(str): the name of the template.
        templates(dict[str,str]): source of template references.

    Returns:
        str: the resolved template

    Raises:
        errors.TemplateError

    """
    try:
        template = templates[name]
    except KeyError:
        raise errors.TemplateError("referenced template :'{}' not found.".format(name))

    for reference in re.findall(constants.PATH_REFERENCE_REGEX, template):
        value = _expand_template(reference, templates)
        template = template.replace("<{}>".format(reference), value)
        templates[name] = template

    return template


def resolve_references(templates):
    """Takes a templates dictionary and resolves all template references.
    Args:
        templates(dict[str,str]): a dictionary of path templates

    Returns:
        dict[str,str]: the resolved template dictionary.

    Raises:
        errors.TemplateError

    """
    templates = copy.deepcopy(templates)
    for name in templates:
        _expand_template(name, templates)
    return templates
