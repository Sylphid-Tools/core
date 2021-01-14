import os
import pytest
import json
import mock
from pyfakefs.fake_filesystem_unittest import Patcher as FSPatcher

from sylphid_core import config as syl_config


@pytest.fixture(scope="function")
def fake_fs():
    with FSPatcher() as fs:
        yield fs.fs


class TestDefaultJsonLoader:
    def test_basic(self, fake_fs):  # keep coverage happy :P
        test_data = {"key": "value"}
        fake_fs.create_file("/test.json", contents=json.dumps(test_data))
        assert syl_config.default_json_loader("/test.json") == test_data


class TestBase:
    def test_base(self):
        base = syl_config.ConfigProviderBase()
        with pytest.raises(NotImplementedError):
            base.get_config({})


class TestFilesystemConfigProvider:
    def test_iter_paths_skip_on_missing_keys(self):
        """Ensure skip failed format operations and move to the next path."""
        templates = ["{prj}/{sht}", "/{prj}"]
        fields = {"prj": "prj1"}
        provider = syl_config.FileSystemConfigProvider(templates)
        assert list(provider._iter_paths(fields)) == ["/prj1"]

    def test_iter_paths_format(self):
        """Ensure templates are formatted."""
        templates = ["/{prj}/{seq}"]
        fields = {"prj": "prj1", "seq": "sht1"}
        provider = syl_config.FileSystemConfigProvider(templates)
        assert list(provider._iter_paths(fields)) == ["/prj1/sht1"]

    def test_iter_configs_skip_missing_file(self, fake_fs):
        """ensure configs that dont exist are handled without error"""
        provider = syl_config.FileSystemConfigProvider([])
        config = {"k": "v"}
        config_path = "/path/to/file.json"
        fake_fs.create_file(config_path, contents=json.dumps(config))
        result = list(provider._iter_configs(["/nothing.json", config_path]))
        assert result == [config]

    def test_get_config_ordered_merge(self, monkeypatch):
        provider = syl_config.FileSystemConfigProvider([])
        configs = [{"a": "a"}, {"b": "b"}]
        monkeypatch.setattr(
            provider, "_iter_configs", mock.MagicMock(return_value=configs)
        )
        monkeypatch.setattr(provider, "_iter_paths", mock.MagicMock())

        result = provider.get_config({})
        assert result == {"a": "a", "b": "b"}

    def test_custom_loader(self, monkeypatch, fake_fs):
        """ensure custom loader is used"""
        config_file = "/a/config_a.yml"

        fake_fs.create_file(config_file)

        loader = mock.MagicMock(return_value={})
        provider = syl_config.FileSystemConfigProvider([], loader=loader)
        monkeypatch.setattr(
            provider, "_iter_paths", mock.MagicMock(return_value=[config_file])
        )

        provider.get_config({})

        loader.assert_called_once_with(config_file)


class TestRezConfigProvider:
    def test_get_config(self, monkeypatch, fake_fs):
        package_root = "/rez/test/root"
        monkeypatch.setenv("REZ_TEST_PACKAGE_ROOT", package_root)
        config = {"key": "value"}
        fake_fs.create_file(
            os.path.join(package_root, "config", "test_package.json"),
            contents=json.dumps(config),
        )

        provider = syl_config.RezConfigProvider()
        assert (
            provider.get_config(
                {"package_name": "test_package", "config": "test_package"}
            )
            == config
        )

    def test_stop_on_missing_package_name(self):
        provider = syl_config.RezConfigProvider(template="{key_not_available}/{root}")
        with pytest.raises(KeyError):
            provider.get_config({"": "available"})

    def test_custom_loader(self, monkeypatch, fake_fs):
        """ensure custom loader is used"""
        config_file = "/a/config_a.yml"

        fake_fs.create_file(config_file)

        loader = mock.MagicMock(return_value={})
        provider = syl_config.RezConfigProvider(loader=loader)

        mock_expand_vars = mock.MagicMock(return_value=config_file)

        with monkeypatch.context() as patch:
            patch.setattr(os.path, "expandvars", mock_expand_vars)
            provider.get_config({"package_name": "dummy", "config": "dummy"})

        loader.assert_called_once_with(config_file)

    def test_no_file_exists(self, monkeypatch, fake_fs):
        """ensure custom loader is used"""
        config_file = "/a/config_a.json"

        provider = syl_config.RezConfigProvider()

        mock_expand_vars = mock.MagicMock(return_value=config_file)

        with monkeypatch.context() as patch:
            patch.setattr(os.path, "expandvars", mock_expand_vars)
            assert (
                provider.get_config({"package_name": "dummy", "config": "dummy"}) == {}
            )
