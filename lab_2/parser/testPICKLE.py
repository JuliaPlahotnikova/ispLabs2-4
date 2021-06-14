import unittest
import serializer
import test1


class TestSerializer(unittest.TestCase):

    def test_pickle_string(self):

        pickle_str = serializer.dumps(test1.string, 'pickle')
        des_str = serializer.loads(pickle_str, 'pickle')

        self.assertEqual(test1.string, des_str)


    def test_pickle_list(self):

        pickle_list = serializer.dumps(test1.list, 'pickle')
        des_list = serializer.loads(pickle_list, 'pickle')

        self.assertEqual(test1.list, des_list)

    
    def test_pickle_dict(self):

        pickle_dict = serializer.dumps(test1.dict, 'pickle')
        des_dict = serializer.loads(pickle_dict, 'pickle')

        self.assertEqual(test1.dict, des_dict)


    def test_pickle_class(self):

        pickle_class = serializer.dumps(test1.MyClass, 'pickle')
        deserialized_class = serializer.loads(pickle_class, 'pickle')

        self.assertEqual(deserialized_class.a, test1.MyClass.a)
        self.assertEqual(deserialized_class.my_func(1), test1.MyClass.my_func(1))


    def test_pickle_func(self):

        pickle_func = serializer.dumps(test1.func, 'pickle')
        des_func = serializer.loads(pickle_func, 'pickle')

        self.assertEqual(test1.func(2), des_func(2))
        

    def test_pickle_lambda(self):

        pickle_lmbd = serializer.dumps(test1.lmbd, 'pickle')
        des_lmbd = serializer.loads(pickle_lmbd, 'pickle')

        self.assertEqual(test1.lmbd(1), des_lmbd(1))


    def test_pickle_func_with_defaults(self):

        pickle_func = serializer.dumps(test1.func_with_defaults, 'pickle')
        des_func = serializer.loads(pickle_func, 'pickle')

        self.assertEqual(test1.func_with_defaults(), des_func())