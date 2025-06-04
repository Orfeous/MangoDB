from typing import Any, Dict

def validate_document(doc: Dict[str, Any]) -> bool:
    """Validate that a document is a dictionary with string keys"""
    if not isinstance(doc, dict):
        return False
    return all(isinstance(k, str) for k in doc.keys())

def is_valid_collection_name(name: str) -> bool:
    """Validate that a collection name is a non-empty string"""
    return isinstance(name, str) and len(name) > 0

def is_valid_query(query: Dict[str, Any]) -> bool:
    """Validate that a query is a dictionary with string keys"""
    if not isinstance(query, dict):
        return False
    return all(isinstance(k, str) for k in query.keys())
