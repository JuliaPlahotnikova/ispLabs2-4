import unittest
import serializer
import test1

class TestSerializer(unittest.TestCase):
    def test_toml_string(self):
        toml_str = serializer.dumps(test1.string, 'toml')
        des_str = serializer.loads(toml_str, 'toml')

        self.assertEqual(test1.string, des_str)


    def test_toml_list(self):
        
        toml_list = serializer.dumps(test1.list, 'toml')
        des_list = serializer.loads(toml_list, 'toml')

        self.assertEqual(test1.list, des_list)


    def test_toml_dict(self):

        toml_dict = serializer.dumps(test1.dict, 'toml')
        des_dict = serializer.loads(toml_dict, 'toml')

        self.assertEqual(test1.dict, des_dict)


    def test_toml_class(self):

        toml_class = serializer.dumps(test1.MyClass, 'toml')
        deserialized_class = serializer.loads(toml_class, 'toml')

        self.assertEqual(deserialized_class.a, test1.MyClass.a)
        self.assertEqual(deserialized_class.my_func(1), test1.MyClass.my_func(1))


    def test_toml_func(self):

        toml_func = serializer.dumps(test1.func, 'toml')
        des_func = serializer.loads(toml_func, 'toml')

        self.assertEqual(test1.func(2), des_func(2))
        

    def test_toml_lambda(self):

        toml_lmbd = serializer.dumps(test1.lmbd, 'toml')
        des_lmbd = serializer.loads(toml_lmbd, 'toml')

        self.assertEqual(test1.lmbd(1), des_lmbd(1))


    def test_toml_func_with_defaults(self):

        toml_func = serializer.dumps(test1.func_with_defaults, 'toml')
        des_func = serializer.loads(toml_func, 'toml')

        self.assertEqual(test1.func_with_defaults(), des_func())
