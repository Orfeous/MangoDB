import unittest
from mangodb import JSONEncoder

class TestJSONEncoder(unittest.TestCase):
    def test_custom_type_serialization(self):
        class Person:
            def __init__(self, name, age):
                self.name = name
                self.age = age

        encoder = JSONEncoder()
        JSONEncoder.register_type(Person)
        
        person = Person('Alice', 25)
        result = encoder.default(person)
        
        self.assertEqual(result['__type__'], 'Person')
        self.assertEqual(result['__value__']['name'], 'Alice')
        self.assertEqual(result['__value__']['age'], 25)

if __name__ == '__main__':
    unittest.main()
