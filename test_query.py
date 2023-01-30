import unittest
import graphene
import graphene.test

class TestHelloQuery(unittest.TestCase):
    def test_hello(self):
        schema = graphene.Schema(query=HelloQuery)
        result = schema.execute('''
            query {
                hello(name: "jerome")
            }
        ''')
        self.assertEqual(result.data['hello'], "Hello jerome")

if __name__ == '__main__':
    unittest.main()
