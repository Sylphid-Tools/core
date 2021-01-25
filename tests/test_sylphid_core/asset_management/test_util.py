import pytest

from sylphid_core.asset_management import util


class TestSerialise:
    def test_serialise_string(self):
        assert util.serialise("test") == '"test"'

    def test_serialise_int(self):
        assert util.serialise(1) == "1"

    def test_serialise_float(self):
        assert util.serialise(1.0) == "1.0"

    def test_serialise_dict_single(self):
        assert util.serialise({"a": "b"}) == '{a:"b"}'

    def test_serialise_dict_multiple(self):
        assert util.serialise({"a": "b", "c": "d"}) == '{a:"b",c:"d"}'

    def test_serialise_dict_mixed(self):
        assert util.serialise({"a": 1, "b": "c"}) == '{a:1,b:"c"}'

    def test_serialise_dict_nested(self):
        assert util.serialise({"a": {"b": "c"}}) == '{a:{b:"c"}}'

    def test_serialise_unknown_type(self):
        with pytest.raises(RuntimeError):
            util.serialise(set())


class TestGenerateMutation:
    def test_basic(self):
        expected = 'mutation name {method(input: {key:"value"}){type {id}}}'
        result = util.generate_mutation(
            "name", "method", {"key": "value"}, "type", ["id"]
        )
        assert result == expected

    def test_multiple_fields(self):
        expected = 'mutation name {method(input: {key:"value"}){type {field,field1}}}'
        result = util.generate_mutation(
            "name", "method", {"key": "value"}, "type", ["field", "field1"]
        )
        assert result == expected

    def test_multiple_inputs(self):
        expected = (
            'mutation name {method(input: [{key:"value"},{key1:"value1"}]){type {id}}}'
        )
        result = util.generate_mutation(
            "name", "method", [{"key": "value"}, {"key1": "value1"}], "type", ["id"]
        )
        assert result == expected
