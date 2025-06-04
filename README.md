# MangoDB

A lightweight, thread-safe document database that stores data in a single JSON file.

<a href="https://pypi.org/project/pymangodb/" target="_blank">![PyPI - Status](https://img.shields.io/pypi/status/pymangodb)</a>
<a href="https://pypi.org/project/pymangodb/" target="_blank">![PyPI - Format](https://img.shields.io/pypi/format/pymango)</a>



## Features

- Thread-safe operations with read-write locking
- Support for concurrent reads
- Batch operations for better performance
- Automatic version control with backup files
- Custom Python type serialization
- Platform independent (Linux, Windows, MacOS)
- No external dependencies

## Installation

```bash
pip install pymangodb
```

## Quick Start

```python
from mangodb import MangoDB

# Initialize database
db = MangoDB("data.json")

# Insert documents
doc_id = db.insert("users", {"name": "Alice", "age": 25})

# Batch insert
doc_ids = db.batch_insert("users", [
    {"name": "Bob", "age": 30},
    {"name": "Charlie", "age": 35}
])

# Find documents
results = db.find("users", {"age": {"$gt": 30}})

# Update documents
db.update("users", {"name": "Alice"}, {"age": 26})

# Batch update
db.batch_update("users", [
    {"query": {"name": "Bob"}, "update": {"age": 31}},
    {"query": {"name": "Charlie"}, "update": {"age": 36}}
])

# Delete documents
db.delete("users", {"name": "Charlie"})
```

## Thread Safety

All operations are thread-safe. The database uses a two-tier locking mechanism:
- Read operations can run concurrently
- Write operations are serialized

## Version Control

Enable automatic backups before modifications:

```python
db.version_control(True)  # Creates backup files before changes
```

## Custom Types

Register your custom classes for serialization:

```python
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age is age

db.register_type(Person)
db.insert("people", Person("Alice", 25))
```

See [API.md](API.md) for detailed documentation.

## Notice
The codebase may contain AI slop.

## License

MIT License
