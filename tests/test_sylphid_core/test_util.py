from sylphid_core import util


class TestDictMerge:
    def test_non_nested_join(self):
        a = {"a": 1}
        b = {"b": 2}
        expected = {"a": 1, "b": 2}
        assert util.dict_merge(a, b) == expected

    def test_non_nested_overlay(self):
        a = {"a": 1}
        b = {"a": 2}
        assert util.dict_merge(a, b) == {"a": 2}

    def test_nested_join(self):
        a = {"b": {"c": 1}}
        b = {"b": {"d": 2}}
        assert util.dict_merge(a, b) == {"b": {"c": 1, "d": 2}}

    def test_nested_overlay(self):
        a = {"b": {"c": 1}}
        b = {"b": {"c": 2}}
        assert util.dict_merge(a, b) == {"b": {"c": 2}}

    def test_dict_over_primitive(self):
        a = {"a": 1}
        b = {"a": {"b": 1}}
        assert util.dict_merge(a, b) == {"a": {"b": 1}}

    def test_in_place_enabled(self):
        a = {}
        b = {"a": 1}
        util.dict_merge(a, b, in_place=True)
        assert a == {"a": 1}

    def test_in_place_disabled(self):
        a = {}
        b = {"a": 1}
        util.dict_merge(a, b)
        assert a == {}
