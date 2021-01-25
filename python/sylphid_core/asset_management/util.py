import six
import string


def _serialise_dict(value, factory):
    elements = [
        '{}:{}'.format(k, factory(v)) for k, v in value.items()
    ]
    return ",".join(elements)


def serialise_dict(value, factory):
    return "{{{}}}".format(_serialise_dict(value, factory))


def serialise_list(value, factory):
    elements = [
        factory(v) for v in value
    ]
    return "[{}]".format(",".join(elements))


def serialise(value):
    if isinstance(value, (int, float)):
        return str(value)
    elif isinstance(value, six.string_types):
        return '"{}"'.format(value)
    elif isinstance(value, dict):
        return serialise_dict(value, serialise)
    elif isinstance(value, list):
        return serialise_list(value, serialise)
    else:
        raise RuntimeError("unknown type: {}".format(value.__class__))


def generate_mutation(name, method, input_data, type_, fields):
    template = string.Template("mutation $name {$method(input: $input){$type_ {$fields}}}")
    return template.substitute(
        name=name,
        method=method,
        input=serialise(input_data),
        fields=",".join(fields),
        type_=type_
    )
