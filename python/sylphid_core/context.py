import os
from sylphid_core import constants, errors


def from_environment():
    """Build a Context object representing the current environments context.

    Returns:
        dict[str,str]: the context data.

    """
    fields = {
        field: os.environ.get(env)
        for field, env in zip(constants.CTX_DICT_KEY_ORDER, constants.CTX_ENV_KEY_ORDER)
    }
    validate_context(fields)
    return fields


def from_short_path(path):
    """Context can be represented by joining its ordered members into a path /project/sequence/shot/task

    Args:
        path(str): the path to parse.

    Returns:
        dict[str, str]: the context data.
    """
    if not path.startswith("/"):
        raise errors.ContextError("Context paths must start with '/'.")

    if path == "/":
        raise errors.ContextError("Context path is too short: '{}'.".format(path))

    elements = path.lstrip("/").rstrip("/").split("/")

    if len(elements) > len(constants.CTX_DICT_KEY_ORDER):
        raise errors.ContextError(
            "too many members in path: '{}'. expected at most: {}.".format(
                path, len(constants.CTX_DICT_KEY_ORDER)
            )
        )

    fields = {k: v for k, v in zip(constants.CTX_DICT_KEY_ORDER, elements)}

    validate_context(fields)
    return fields


def validate_context(fields):
    """Validate a set of context fields.

    Args:
        fields(dict[str,str]): the context fields to use
    """

    # At minimum a context must define a root field. (project)
    if constants.CTX_DICT_KEY_ORDER[0] not in fields or fields.get(
        constants.CTX_DICT_KEY_ORDER[0]
    ) in [None, ""]:
        raise errors.ContextError("No Context Found.")

    reversed_names = list(reversed(constants.CTX_DICT_KEY_ORDER))
    ordered = [fields.get(n) for n in reversed_names]

    # build a tuple of pairs containing each context field and their preceding field
    # for example:
    #   ("task","shot"), ("shot", "sequence"), ("sequence", "project")
    pairs = [(ordered[i - 1], ordered[i]) for i in range(len(ordered)) if i > 0]

    # each item in the pair has a child parent relationship, tasks must exist in a shot, and shots must exist in a
    # sequence. If the child is defined but the parent isn't this is an invalid context.
    for index, pair in enumerate(pairs):
        child, parent = pair
        if child and not parent:
            raise errors.ContextError(
                "{} requires: {} to be set".format(
                    reversed_names[index - 1], reversed_names[index]
                )
            )
