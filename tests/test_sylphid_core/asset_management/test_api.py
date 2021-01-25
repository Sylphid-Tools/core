import sys
import pytest
import mock

import sylphid_core.errors as syl_errors


@pytest.fixture()
def patched_api_module(monkeypatch):
    monkeypatch.setitem(sys.modules, "requests", mock.MagicMock())
    from sylphid_core.asset_management import api

    yield api


class TestClient:
    class TestMutate:
        def test_http_error(self, monkeypatch, patched_api_module):
            monkeypatch.setattr(patched_api_module, "requests", mock.MagicMock())
            monkeypatch.setattr(patched_api_module, "util", mock.MagicMock())

            response = patched_api_module.requests.post.return_value
            response.status_code = 400
            response.json.return_value = {}

            with pytest.raises(syl_errors.AssetManagementError):
                client = patched_api_module.Client("")
                client._mutate("", "", {}, "", [])

        def test_asset_management_error(self, monkeypatch, patched_api_module):
            monkeypatch.setattr(patched_api_module, "requests", mock.MagicMock())
            monkeypatch.setattr(patched_api_module, "util", mock.MagicMock())

            response = patched_api_module.requests.post.return_value
            response.status_code = 200
            response.json.return_value = {"errors": ["error"]}

            with pytest.raises(syl_errors.AssetManagementError):
                client = patched_api_module.Client("")
                client._mutate("", "", {}, "", [])

        def test_data(self, monkeypatch, patched_api_module):
            monkeypatch.setattr(patched_api_module, "requests", mock.MagicMock())
            monkeypatch.setattr(patched_api_module, "util", mock.MagicMock())

            response = patched_api_module.requests.post.return_value
            response.status_code = 200
            expected = {"key": "value"}
            response.json.return_value = {"data": {"name": {"type": expected}}}

            client = patched_api_module.Client("")
            assert client._mutate("name", "", {}, "type", []) == expected
