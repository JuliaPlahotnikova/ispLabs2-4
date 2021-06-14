import unittest
import serializer
import test1

class TestSerializer(unittest.TestCase):

    def test_yaml_string(self):

        yaml_str = serializer.dumps(test1.string, 'yaml')
        des_str = serializer.loads(yaml_str, 'yaml')

        self.assertEqual(test1.string, des_str)


    def test_yaml_list(self):
        
        yaml_list = serializer.dumps(test1.list, 'yaml')
        des_list = serializer.loads(yaml_list, 'yaml')

        self.assertEqual(test1.list, des_list)

    
    def test_yaml_dict(self):

        yaml_dict = serializer.dumps(test1.dict, 'yaml')
        des_dict = serializer.loads(yaml_dict, 'yaml')

        self.assertEqual(test1.dict, des_dict)


    def test_yaml_class(self):

        yaml_class = serializer.dumps(test1.MyClass, 'yaml')
        deserialized_class = serializer.loads(yaml_class, 'yaml')

        self.assertEqual(deserialized_class.a, test1.MyClass.a)
        self.assertEqual(deserialized_class.my_func(1), test1.MyClass.my_func(1))


    def test_yaml_func(self):

        yaml_func = serializer.dumps(test1.func, 'yaml')
        des_func = serializer.loads(yaml_func, 'yaml')

        self.assertEqual(test1.func(2), des_func(2))
        

    def test_yaml_lambda(self):

        yaml_lmbd = serializer.dumps(test1.lmbd, 'yaml')
        des_lmbd = serializer.loads(yaml_lmbd, 'yaml')

        self.assertEqual(test1.lmbd(1), des_lmbd(1))


    def test_yaml_func_with_defaults(self):

        yaml_func = serializer.dumps(test1.func_with_defaults, 'yaml')
        des_func = serializer.loads(yaml_func, 'yaml')

        self.assertEqual(test1.func_with_defaults(), des_func())