import unittest
import graphene
from main import Query

schema = graphene.Schema(query=Query)

class TestHelloQuery(unittest.TestCase):
    def test_hello(self):
        result = schema.execute('''
            query {
                hello(name: "jerome")
            }
        ''')
        self.assertEqual(result.data['hello'], "Hello jerome")

if __name__ == '__main__':
    unittest.main()
