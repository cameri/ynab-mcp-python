"""Tests for schema patching utilities."""

from .schemas_patch import add_schema_definitions_and_prune_unused


class TestAddSchemaDefinitionsAndPruneUnused:
    """Test cases for add_schema_definitions_and_prune_unused function."""

    def test_no_schema_definitions(self):
        """Test that function works correctly when no schema definitions are provided."""
        schema = {
            "type": "object",
            "properties": {"name": {"type": "string"}, "age": {"type": "integer"}},
            "required": ["name"],
        }

        result = add_schema_definitions_and_prune_unused(schema, None)

        # Should return the same schema object
        assert result is schema
        assert "$defs" not in result
        assert result["type"] == "object"
        assert result["properties"]["name"]["type"] == "string"

    def test_prune_additional_properties_false(self):
        """Test that additionalProperties=False is removed."""
        schema = {
            "type": "object",
            "properties": {"name": {"type": "string"}},
            "additionalProperties": False,
        }

        result = add_schema_definitions_and_prune_unused(schema, None)

        assert "additionalProperties" not in result
        assert result["type"] == "object"

    def test_keep_additional_properties_true(self):
        """Test that additionalProperties=True is kept."""
        schema = {
            "type": "object",
            "properties": {"name": {"type": "string"}},
            "additionalProperties": True,
        }

        result = add_schema_definitions_and_prune_unused(schema, None)

        assert result["additionalProperties"] is True
        assert result["type"] == "object"

    def test_add_schema_definitions(self):
        """Test that schema definitions are added correctly."""
        schema = {"type": "object", "properties": {"user": {"$ref": "#/$defs/User"}}}

        definitions = {
            "User": {
                "type": "object",
                "properties": {"name": {"type": "string"}, "email": {"type": "string"}},
            },
            "UnusedType": {
                "type": "object",
                "properties": {"unused": {"type": "string"}},
            },
        }

        result = add_schema_definitions_and_prune_unused(schema, definitions)

        assert "$defs" in result
        assert "User" in result["$defs"]
        assert "UnusedType" not in result["$defs"]  # Should be pruned
        assert result["$defs"]["User"]["type"] == "object"

    def test_nested_ref_detection(self):
        """Test that references in nested structures are detected."""
        schema = {
            "type": "object",
            "properties": {
                "users": {"type": "array", "items": {"$ref": "#/$defs/User"}},
                "metadata": {
                    "type": "object",
                    "properties": {"creator": {"$ref": "#/$defs/User"}},
                },
            },
        }

        definitions = {
            "User": {"type": "object", "properties": {"name": {"type": "string"}}},
            "UnusedType": {
                "type": "object",
                "properties": {"unused": {"type": "string"}},
            },
        }

        result = add_schema_definitions_and_prune_unused(schema, definitions)

        assert "$defs" in result
        assert "User" in result["$defs"]
        assert "UnusedType" not in result["$defs"]

    def test_anyof_allof_oneof_refs(self):
        """Test that references in anyOf, allOf, oneOf are detected."""
        schema = {
            "type": "object",
            "properties": {
                "value": {
                    "anyOf": [
                        {"$ref": "#/$defs/StringValue"},
                        {"$ref": "#/$defs/NumberValue"},
                    ]
                }
            },
        }

        definitions = {
            "StringValue": {"type": "string"},
            "NumberValue": {"type": "number"},
            "UnusedType": {"type": "object"},
        }

        result = add_schema_definitions_and_prune_unused(schema, definitions)

        assert "$defs" in result
        assert "StringValue" in result["$defs"]
        assert "NumberValue" in result["$defs"]
        assert "UnusedType" not in result["$defs"]

    def test_no_refs_removes_all_defs(self):
        """Test that all definitions are removed when no references are found."""
        schema = {
            "type": "object",
            "properties": {"name": {"type": "string"}, "age": {"type": "integer"}},
        }

        definitions = {
            "UnusedType1": {"type": "string"},
            "UnusedType2": {"type": "number"},
        }

        result = add_schema_definitions_and_prune_unused(schema, definitions)

        assert "$defs" not in result

    def test_schema_modification_in_place(self):
        """Test that the original schema object is modified in place."""
        original_schema = {
            "type": "object",
            "properties": {"name": {"type": "string"}},
            "additionalProperties": False,
        }

        result = add_schema_definitions_and_prune_unused(original_schema, None)

        # Should be the same object
        assert result is original_schema
        # Original should be modified
        assert "additionalProperties" not in original_schema

    def test_definitions_copy_not_mutated(self):
        """Test that the original definitions dict is not mutated."""
        schema = {"type": "object", "properties": {"user": {"$ref": "#/$defs/User"}}}

        original_definitions = {
            "User": {"type": "object"},
            "UnusedType": {"type": "string"},
        }
        definitions_copy = original_definitions.copy()

        add_schema_definitions_and_prune_unused(schema, original_definitions)

        # Original definitions should be unchanged
        assert original_definitions == definitions_copy

    def test_complex_nested_structure(self):
        """Test with a complex nested structure with multiple reference types."""
        schema = {
            "type": "object",
            "properties": {
                "data": {
                    "allOf": [
                        {"$ref": "#/$defs/BaseType"},
                        {
                            "type": "object",
                            "properties": {
                                "items": {
                                    "type": "array",
                                    "items": {
                                        "oneOf": [
                                            {"$ref": "#/$defs/TypeA"},
                                            {"$ref": "#/$defs/TypeB"},
                                        ]
                                    },
                                }
                            },
                        },
                    ]
                }
            },
            "additionalProperties": False,
        }

        definitions = {
            "BaseType": {"type": "object", "properties": {"id": {"type": "string"}}},
            "TypeA": {"type": "string"},
            "TypeB": {"type": "number"},
            "UnusedType": {"type": "boolean"},
        }

        result = add_schema_definitions_and_prune_unused(schema, definitions)

        assert "$defs" in result
        assert "BaseType" in result["$defs"]
        assert "TypeA" in result["$defs"]
        assert "TypeB" in result["$defs"]
        assert "UnusedType" not in result["$defs"]
        assert "additionalProperties" not in result

    def test_empty_schema(self):
        """Test with an empty schema."""
        schema = {}
        definitions = {"Type": {"type": "string"}}

        result = add_schema_definitions_and_prune_unused(schema, definitions)

        # Should remove all definitions since no refs found
        assert "$defs" not in result

    def test_transitive_refs_are_included(self):
        """Test that transitive references within definitions are correctly included."""
        schema = {"type": "object", "properties": {"user": {"$ref": "#/$defs/User"}}}

        definitions = {
            "User": {
                "type": "object",
                "properties": {
                    "profile": {"$ref": "#/$defs/Profile"}  # User references Profile
                },
            },
            "Profile": {"type": "object"},
            "UnusedType": {"type": "string"},
        }

        result = add_schema_definitions_and_prune_unused(schema, definitions)

        assert "$defs" in result
        assert "User" in result["$defs"]
        # Profile SHOULD be included because User references it
        assert "Profile" in result["$defs"]
        assert "UnusedType" not in result["$defs"]

    def test_transitive_references_in_definitions(self):
        """Test that definitions that reference other definitions are both kept (should fail initially)."""
        schema = {"type": "object", "properties": {"user": {"$ref": "#/$defs/User"}}}

        definitions = {
            "User": {
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "address": {"$ref": "#/$defs/Address"},  # User references Address
                },
            },
            "Address": {
                "type": "object",
                "properties": {
                    "street": {"type": "string"},
                    "city": {"type": "string"},
                    "country": {
                        "$ref": "#/$defs/Country"
                    },  # Address references Country
                },
            },
            "Country": {
                "type": "object",
                "properties": {"name": {"type": "string"}, "code": {"type": "string"}},
            },
            "UnusedType": {
                "type": "object",
                "properties": {"unused": {"type": "string"}},
            },
        }

        result = add_schema_definitions_and_prune_unused(schema, definitions)

        assert "$defs" in result
        assert "User" in result["$defs"]
        # These should be included because User -> Address -> Country
        # but will currently fail because the function doesn't check transitively
        assert (
            "Address" in result["$defs"]
        ), "Address should be kept because User references it"
        assert (
            "Country" in result["$defs"]
        ), "Country should be kept because Address references it"
        # This should definitely not be included
        assert "UnusedType" not in result["$defs"]

    def test_circular_references_handled(self):
        """Test that circular references don't cause infinite loops."""
        schema = {"type": "object", "properties": {"node": {"$ref": "#/$defs/Node"}}}

        definitions = {
            "Node": {
                "type": "object",
                "properties": {
                    "value": {"type": "string"},
                    "parent": {"$ref": "#/$defs/Node"},  # Circular reference to itself
                    "children": {
                        "type": "array",
                        "items": {"$ref": "#/$defs/Node"},  # Another circular reference
                    },
                },
            },
            "UnusedType": {"type": "string"},
        }

        result = add_schema_definitions_and_prune_unused(schema, definitions)

        assert "$defs" in result
        assert "Node" in result["$defs"]
        assert "UnusedType" not in result["$defs"]
        # Verify the circular references are preserved in the definition
        assert result["$defs"]["Node"]["properties"]["parent"]["$ref"] == "#/$defs/Node"
        assert (
            result["$defs"]["Node"]["properties"]["children"]["items"]["$ref"]
            == "#/$defs/Node"
        )
