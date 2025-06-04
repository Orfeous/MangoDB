# MangoDB API Documentation

## Core Features

### Initialization
```python
db = MangoDB(file_path: str)
```
Creates a new database instance with the specified JSON file path.

### Basic Operations

#### Insert
```python
doc_id = db.insert(collection: str, document: dict) -> str
```
- Inserts a single document into a collection
- Returns a UUID string as document ID
- Thread-safe operation
- Document is automatically assigned an '_id' field

#### Batch Insert
```python
doc_ids = db.batch_insert(collection: str, documents: List[dict]) -> List[str]
```
- Inserts multiple documents in a single atomic operation
- Returns a list of UUID strings as document IDs
- More efficient than multiple single inserts
- Thread-safe operation

#### Find
```python
results = db.find(collection: str, query: Optional[dict] = None) -> List[dict]
```
- Returns a list of documents matching the query
- Returns all documents if query is None
- Thread-safe, allows concurrent reads
- Returns deep copies of documents to prevent external modifications

#### Update
```python
count = db.update(collection: str, query: dict, update: dict) -> int
```
- Updates documents matching the query
- Returns number of documents updated
- Thread-safe operation

#### Batch Update
```python
count = db.batch_update(collection: str, operations: List[Dict[str, dict]]) -> int
```
- Performs multiple updates in a single atomic operation
- Each operation should contain 'query' and 'update' dictionaries
- Returns total number of documents updated
- More efficient than multiple single updates

#### Delete
```python
count = db.delete(collection: str, query: dict) -> int
```
- Deletes documents matching the query
- Returns number of documents deleted
- Thread-safe operation

### Version Control

```python
db.version_control(enable: bool) -> None
```
- Enable or disable automatic backups before modifications
- Creates timestamped backup files: `<filename>.<timestamp>.bak`

### Custom Type Support

```python
db.register_type(cls: Type) -> None
```
- Register custom Python classes for serialization
- Allows storing and retrieving custom objects

## Thread Safety

The library implements a two-tier locking mechanism:
- Read Lock: Allows concurrent reads
- Write Lock: Exclusive access for modifications

All operations are thread-safe and can be used in concurrent environments.

## Performance Considerations

- Use batch operations when possible for better performance
- Concurrent reads are supported and efficient
- Version control adds overhead due to file copying
- Each write operation triggers a file save