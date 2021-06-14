import unittest
import serializer
import test1


class TestSerializer(unittest.TestCase):

    def test_json_string(self):

        json_str = serializer.dumps(test1.string, 'json')
        des_str = serializer.loads(json_str, 'json')

        self.assertEqual(test1.string, des_str)


    def test_json_list(self):

        json_list = serializer.dumps(test1.list, 'json')
        des_list = serializer.loads(json_list, 'json')

        self.assertEqual(test1.list, des_list)

    
    def test_json_dict(self):

        json_dict = serializer.dumps(test1.dict, 'json')
        des_dict = serializer.loads(json_dict, 'json')

        self.assertEqual(test1.dict, des_dict)


    def test_json_class(self):

        json_class = serializer.dumps(test1.MyClass, 'json')
        deserialized_class = serializer.loads(json_class, 'json')

        self.assertEqual(deserialized_class.a, test1.MyClass.a)
        self.assertEqual(deserialized_class.my_func(1), test1.MyClass.my_func(1))


    def test_json_func(self):

        json_func = serializer.dumps(test1.func, 'json')
        des_func = serializer.loads(json_func, 'json')

        self.assertEqual(test1.func(2), des_func(2))
        

    def test_json_lambda(self):

        json_lmbd = serializer.dumps(test1.lmbd, 'json')
        des_lmbd = serializer.loads(json_lmbd, 'json')

        self.assertEqual(test1.lmbd(1), des_lmbd(1))
