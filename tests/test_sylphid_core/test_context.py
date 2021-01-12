import pytest

from sylphid_core import context, errors


@pytest.fixture()
def patched_constants(monkeypatch):
    monkeypatch.setattr(context.constants, "CTX_ENV_KEY_ORDER", ["prj", "seq", "sht", "tsk"])
    monkeypatch.setattr(context.constants, "CTX_DICT_KEY_ORDER", ["prj", "seq", "sht", "tsk"])
    yield context.constants


class TestValidateContext:
    @pytest.mark.parametrize("fields", [
        {},  # No data at all.
        {"prj": ""},
        {"seq": "seq"},  # the first field, in this case prj, must always be populated
        {"prj": "prj", "seq": "seq", "tsk": "tsk"},  # tsk is dependant on sht which is unpopulated
        {"prj": "prj", "seq": "seq", "sht": None, "tsk": "tsk"},  # tsk is dependant on sht which is None
        {"prj": "prj", "seq": "seq", "sht": "", "tsk": "tsk"},  # tsk is dependant on sht which is empty
    ])
    def test_validation_fails(self, fields, patched_constants):
        with pytest.raises(errors.ContextError):
            context.validate_context(fields)

    @pytest.mark.parametrize("fields", [
        {"prj": "prj"},
        {"prj": "prj", "seq": "seq"},
        {"prj": "prj", "seq": "seq", "sht": "sht"},
        {"prj": "prj", "seq": "seq", "sht": "sht", "tsk": "tsk"},
    ])
    def test_validation_passes(self, fields, patched_constants):
        context.validate_context(fields)


class TestFromEnvironment:
    def test_extraction(self, monkeypatch, patched_constants):
        monkeypatch.setenv(patched_constants.CTX_ENV_KEY_ORDER[0], "a")
        monkeypatch.setenv(patched_constants.CTX_ENV_KEY_ORDER[1], "b")
        monkeypatch.setenv(patched_constants.CTX_ENV_KEY_ORDER[2], "c")
        monkeypatch.setenv(patched_constants.CTX_ENV_KEY_ORDER[3], "d")
        ctx = context.from_environment()
        assert ctx == {
            "prj": "a",
            "seq": "b",
            "sht": "c",
            "tsk": "d"
        }


class TestFromShortPath:
    @pytest.mark.parametrize("path, result", [
        ("/prj", {"prj": "prj"}),
        ("/prj/seq", {"prj": "prj", "seq": "seq"}),
        ("/prj/seq/sht/tsk", {"prj": "prj", "seq": "seq", "sht": "sht", "tsk": "tsk"}),
    ])
    def test_parser(self, path, result, patched_constants):
        assert context.from_short_path(path) == result

    @pytest.mark.parametrize("path", [
        "",  # empty string
        "/",  # no context
        "/a/b/c/d/e/f/g",  # too many members

    ])
    def test_failure_cases(self, path, patched_constants):
        with pytest.raises(errors.ContextError):
            context.from_short_path(path)
