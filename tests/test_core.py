import unittest
import os
import tempfile
import concurrent.futures
from mangodb import MangoDB


class TestMangoDB(unittest.TestCase):
    def setUp(self):
        self.temp_file = tempfile.NamedTemporaryFile(delete=False)
        self.db = MangoDB(self.temp_file.name)

    def tearDown(self):
        self.temp_file.close()
        os.unlink(self.temp_file.name)

    def test_insert_find(self):
        doc_id = self.db.insert('test', {'name': 'Alice', 'age': 25})
        results = self.db.find('test', {'name': 'Alice'})
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['name'], 'Alice')
        self.assertEqual(results[0]['age'], 25)

    def test_update(self):
        self.db.insert('test', {'name': 'Bob', 'age': 30})
        updated = self.db.update('test', {'name': 'Bob'}, {'age': 31})
        self.assertEqual(updated, 1)
        results = self.db.find('test', {'name': 'Bob'})
        self.assertEqual(results[0]['age'], 31)

    def test_delete(self):
        self.db.insert('test', {'name': 'Charlie', 'age': 35})
        deleted = self.db.delete('test', {'name': 'Charlie'})
        self.assertEqual(deleted, 1)
        results = self.db.find('test', {'name': 'Charlie'})
        self.assertEqual(len(results), 0)

    def test_concurrent_writes(self):
        """Test concurrent write operations"""
        import concurrent.futures
        import time

        def insert_docs(db, collection, count, worker_id):
            for i in range(count):
                try:
                    db.insert(collection, {'id': f"{worker_id}-{i}"})
                    time.sleep(0.01)  # Add small delay to reduce contention
                except Exception as e:
                    print(f"Worker {worker_id} failed: {str(e)}")
                    raise

        # Create a new temporary file for this test
        with tempfile.NamedTemporaryFile() as temp_file:
            db = MangoDB(temp_file.name)

            # Use ThreadPoolExecutor with timeout
            with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
                futures = [
                    executor.submit(insert_docs, db, 'concurrent', 10, i)
                    for i in range(3)
                ]
                try:
                    # Wait with timeout to prevent hanging
                    for future in concurrent.futures.as_completed(futures, timeout=10):
                        future.result()
                except concurrent.futures.TimeoutError:
                    self.fail("Test timed out - possible deadlock")

            # Verify all documents were inserted
            docs = db.find('concurrent')
            self.assertEqual(len(docs), 30)
            # Verify no duplicates
            ids = [doc['id'] for doc in docs]
            self.assertEqual(len(ids), len(set(ids)))

    def test_batch_operations(self):
        """Test batch insert and update operations"""
        # Test batch insert
        documents = [
            {'name': 'Alice', 'age': 25},
            {'name': 'Bob', 'age': 30},
            {'name': 'Charlie', 'age': 35}
        ]
        doc_ids = self.db.batch_insert('test', documents)
        self.assertEqual(len(doc_ids), 3)

        # Verify all documents were inserted
        results = self.db.find('test')
        self.assertEqual(len(results), 3)

        # Test batch update
        operations = [
            {'query': {'name': 'Alice'}, 'update': {'age': 26}},
            {'query': {'name': 'Bob'}, 'update': {'age': 31}}
        ]
        updated = self.db.batch_update('test', operations)
        self.assertEqual(updated, 2)

        # Verify updates
        alice = self.db.find('test', {'name': 'Alice'})[0]
        self.assertEqual(alice['age'], 26)
        bob = self.db.find('test', {'name': 'Bob'})[0]
        self.assertEqual(bob['age'], 31)

    def test_concurrent_reads(self):
        """Test concurrent read operations"""
        # Insert test data
        self.db.batch_insert('test', [
            {'name': f'User{i}', 'value': i} for i in range(100)
        ])

        def read_docs(db, collection):
            for _ in range(10):
                results = db.find(collection)
                self.assertEqual(len(results), 100)

        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            futures = [
                executor.submit(read_docs, self.db, 'test')
                for _ in range(5)
            ]
            concurrent.futures.wait(futures, timeout=10)
            for future in futures:
                self.assertTrue(future.done())
                self.assertIsNone(future.exception())


if __name__ == '__main__':
    unittest.main()
