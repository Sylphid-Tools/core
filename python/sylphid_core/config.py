import json
import os
from sylphid_core import util


class ConfigProviderBase(object):
    def get_config(self, fields):
        raise NotImplementedError


def default_json_loader(filepath):
    with open(filepath, mode="r") as json_file:
        data = json.load(json_file)
        return data


class FileSystemConfigProvider(ConfigProviderBase):
    """
    The filesystem config provider takes a list of location templates, formats them with
    the fields provided and then searches each resulting path in order to find configs.

    Example:
        Given the following templates:
            1: /{project}/configs/{config}.json
            2: /{project}/{sequence}/configs/{config}.json

        Format them with the following fields:
            {"project": myProject", "sequence": "sq0010", "config": "resolutions"}

        To get the following paths:
            1: /myProject/configs/resolutions.json
            2: /myProject/sq0010/configs/resolutions.json

        Which we load to get the following configs:
            1: {"default": "1920x1080", "preview":"1280x720"}
            2: {"default": "2560x1440"}

        We then merge them in order of discovery to get a collapsed config:
            {"default": "2560x1440", "preview": "1280x720"}

        In the above example sq0010 has a custom default resolution but uses the preview
        resolution defined on the project.

    """

    def __init__(self, template_list, loader=None):
        """
        Args:
            template_list(list[str]): each template defines a location to
            loader(callable): a custom function for loading different config formats.

        """
        self._template_list = template_list
        self._loader = loader or default_json_loader

    def _iter_paths(self, fields):
        """Iterate over the providers templates and yield the paths the given fields
        can format. Templates with missing fields will be skipped.

        Args:
            fields(dict): the fields to be used for template formatting

        Yields
            str: a config path.

        """
        for template in self._template_list:
            try:
                yield template.format(**fields)
            except KeyError:
                continue

    def _iter_configs(self, paths):
        """Iterate over the given paths and yield their contents if they exist on disk.

        Args:
            paths(List|Generator[str]): the paths to load.

        Yields:
            dict: a config.
        """
        for path in paths:
            if os.path.exists(path):
                yield self._loader(path)

    def get_config(self, fields):
        """
        Get config from filesystem using given fields.
        Args:
            fields(dict): the fields used to describe the config.

        Returns:
            dict: the config

        """
        result = {}
        for config in self._iter_configs(self._iter_paths(fields)):
            util.dict_merge(result, config, in_place=True)

        return result


class RezConfigProvider(ConfigProviderBase):
    """
    Every Rez package defines an environment variable REZ_{PACKAGE_NAME}_ROOT which we
    can use to get the currently resolved version of that packages root directory.

    Using this we can easily extract config data from rez packages.

    """

    default_template = "$REZ_{package_name}_ROOT/config/{config}.json"

    def __init__(self, template=None, loader=None):
        self._loader = loader or default_json_loader
        self._template = template or self.default_template

    def get_config(self, fields):
        """
        Get Rez package configuration.

        Args:
            fields(dict): the fields used to describe the config being searched for.

        Required Fields:
            package_name: the name of the rez package, this package must be resolved.
            config: the name of the config being searched for.

        Returns:
            dict: the config.

        """
        fields["package_name"] = fields["package_name"].upper()
        path = os.path.expandvars(self._template.format(**fields))

        if os.path.exists(path):
            return self._loader(path)

        return {}
