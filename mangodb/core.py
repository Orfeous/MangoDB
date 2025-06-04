import json
import os
import uuid
from threading import RLock
from datetime import datetime
from typing import Any, Dict, List, Optional, Type
from .encoder import JSONEncoder
from .decoder import JSONDecoder

class MangoDB:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.read_lock = RLock()
        self.write_lock = RLock()
        self.version_control_enabled = True
        self.data: Dict[str, List[Dict]] = {}
        self._load_data()

    def _load_data(self) -> None:
        """Load data from the JSON file"""
        if not os.path.exists(self.file_path):
            self.data = {}
            return

        with self.write_lock:
            try:
                with open(self.file_path, 'r') as f:
                    content = f.read()
                    self.data = json.loads(content, cls=JSONDecoder) if content else {}
            except json.JSONDecodeError:
                self.data = {}

    def _save_data(self) -> None:
        """Save data to the JSON file"""
        if self.version_control_enabled:
            self._create_backup()

        with self.write_lock:
            with open(self.file_path, 'w') as f:
                json.dump(self.data, f, cls=JSONEncoder, indent=2)

    def _create_backup(self) -> None:
        """Create a timestamped backup of the current data"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = f"{self.file_path}.{timestamp}.bak"
        with self.write_lock:
            with open(self.file_path, 'r') as src, open(backup_path, 'w') as dst:
                dst.write(src.read())

    def insert(self, collection: str, document: Dict) -> str:
        """Insert a document into a collection"""
        with self.write_lock:
            if collection not in self.data:
                self.data[collection] = []
            doc_id = str(uuid.uuid4())
            document['_id'] = doc_id
            self.data[collection].append(document)
            self._save_data()
            return doc_id

    def batch_insert(self, collection: str, documents: List[Dict]) -> List[str]:
        """Insert multiple documents in a single operation"""
        with self.write_lock:
            if collection not in self.data:
                self.data[collection] = []
            
            doc_ids = []
            for document in documents:
                doc_id = str(uuid.uuid4())
                document['_id'] = doc_id
                self.data[collection].append(document)
                doc_ids.append(doc_id)
            
            self._save_data()
            return doc_ids

    def find(self, collection: str, query: Optional[Dict] = None) -> List[Dict]:
        """Find documents matching the query"""
        with self.read_lock:
            if collection not in self.data:
                return []
            
            if not query:
                return self.data[collection].copy()
                
            return [doc.copy() for doc in self.data[collection] 
                    if all(doc.get(k) == v for k, v in query.items())]

    def update(self, collection: str, query: Dict, update: Dict) -> int:
        """Update documents matching the query"""
        with self.write_lock:
            if collection not in self.data:
                return 0
                
            count = 0
            for doc in self.data[collection]:
                if all(doc.get(k) == v for k, v in query.items()):
                    doc.update(update)
                    count += 1
            if count > 0:
                self._save_data()
            return count

    def batch_update(self, collection: str, operations: List[Dict[str, Dict]]) -> int:
        """Perform multiple updates in a single operation"""
        with self.write_lock:
            if collection not in self.data:
                return 0
            
            count = 0
            for op in operations:
                query = op.get('query', {})
                update = op.get('update', {})
                for doc in self.data[collection]:
                    if all(doc.get(k) == v for k, v in query.items()):
                        doc.update(update)
                        count += 1
            
            if count > 0:
                self._save_data()
            return count

    def delete(self, collection: str, query: Dict) -> int:
        """Delete documents matching the query"""
        with self.write_lock:
            if collection not in self.data:
                return 0
            
            initial_count = len(self.data[collection])
            self.data[collection] = [doc for doc in self.data[collection]
                                   if not all(doc.get(k) == v for k, v in query.items())]
            deleted = initial_count - len(self.data[collection])
            if deleted > 0:
                self._save_data()
            return deleted

    def version_control(self, enable: bool) -> None:
        """Enable or disable version control"""
        self.version_control_enabled = enable

    def register_type(self, cls: Type) -> None:
        """Register a custom type for serialization"""
        JSONEncoder.register_type(cls)
        JSONDecoder.register_type(cls)
