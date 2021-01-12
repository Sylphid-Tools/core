import pytest

from sylphid_core import templates, errors


class TestResolveReferences:
    def test_single_reference(self):
        un_resolved = {"root": "/root", "branch": "<root>/branch"}
        expected = un_resolved.copy()
        expected["branch"] = "/root/branch"

        assert templates.resolve_references(un_resolved) == expected

    def test_nested_reference(self):
        un_resolved = {
            "root": "/root",
            "branch": "<root>/branch",
            "leaf": "<branch>/leaf",
        }
        expected = {
            "root": "/root",
            "branch": "/root/branch",
            "leaf": "/root/branch/leaf",
        }

        assert templates.resolve_references(un_resolved) == expected

    def test_missing_template(self):
        unresolved = {"branch": "<root>/branch"}
        with pytest.raises(errors.TemplateError):
            templates.resolve_references(unresolved)
