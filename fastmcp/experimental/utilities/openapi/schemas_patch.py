"""Schema patching utilities for OpenAPI operations."""

from typing import Any


def add_schema_definitions_and_prune_unused(
    schema: dict[str, Any], schema_definitions: dict[str, Any] | None = None
) -> dict[str, Any]:
    """
    Add schema definitions to a schema and remove unused definitions.

    This function performs lightweight compression by:
    1. Adding schema definitions if available
    2. Removing unused definitions by checking recursive $ref usage
    3. Pruning additionalProperties if False

    The function recursively follows $ref chains to ensure that if schema A
    references schema B, and schema B references schema C, then all three
    schemas (A, B, C) are considered "used" and retained in the final $defs.

    Args:
        schema: The schema to add definitions to (will be modified in place)
        schema_definitions: Optional schema definitions to include

    Returns:
        The modified schema (same object as input)
    """
    # Use lightweight compression - prune additionalProperties and unused definitions
    if schema.get("additionalProperties") is False:
        schema.pop("additionalProperties")

    # Add schema definitions if available
    if schema_definitions:
        schema["$defs"] = schema_definitions.copy()

    # Remove unused definitions (recursive approach - check transitive $ref usage)
    if "$defs" in schema:
        used_refs = set()

        def find_refs_in_value(value):
            if isinstance(value, dict):
                if "$ref" in value and isinstance(value["$ref"], str):
                    ref = value["$ref"]
                    if ref.startswith("#/$defs/"):
                        used_refs.add(ref.split("/")[-1])
                for v in value.values():
                    find_refs_in_value(v)
            elif isinstance(value, list):
                for item in value:
                    find_refs_in_value(item)

        # Find refs in the main schema (excluding $defs section)
        for key, value in schema.items():
            if key != "$defs":
                find_refs_in_value(value)

        # Recursively find transitive references within definitions
        # Keep adding until no new references are found
        previous_size = 0
        while len(used_refs) > previous_size:
            previous_size = len(used_refs)
            # Check for references within each currently used definition
            for ref_name in list(
                used_refs
            ):  # Convert to list to avoid modification during iteration
                if ref_name in schema["$defs"]:
                    find_refs_in_value(schema["$defs"][ref_name])

        # Remove unused definitions
        if used_refs:
            schema["$defs"] = {
                name: def_schema
                for name, def_schema in schema["$defs"].items()
                if name in used_refs
            }
        else:
            schema.pop("$defs")

    return schema


# Export public symbols
__all__ = [
    "add_schema_definitions_and_prune_unused",
]
