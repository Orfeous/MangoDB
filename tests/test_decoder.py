import unittest
from mangodb import JSONDecoder

class TestJSONDecoder(unittest.TestCase):
    def test_custom_type_deserialization(self):
        class Person:
            def __init__(self, name, age):
                self.name = name
                self.age = age

        JSONDecoder.register_type(Person)
        decoder = JSONDecoder()
        
        data = {
            '__type__': 'Person',
            '__value__': {'name': 'Alice', 'age': 25}
        }
        
        result = decoder.object_hook(data)
        
        self.assertIsInstance(result, Person)
        self.assertEqual(result.name, 'Alice')
        self.assertEqual(result.age, 25)

if __name__ == '__main__':
    unittest.main()
