import types
import unittest

from fallback import Fallback


class TestFallback(unittest.TestCase):
    def setUp(self) -> None:
        self.test_dict = {"key_exists": "value_exists"}
        self.test_obj = types.SimpleNamespace()
        self.test_obj.attr_exists = "attr_exists_value"

    def test_objExists(self):
        wrapper = Fallback(obj="obj", fallback="fallback")
        self.assertEqual("obj", wrapper.get())

    def test_objDoesNotExists(self):
        wrapper = Fallback(obj=None, fallback="fallback")
        self.assertEqual("fallback", wrapper.get())

    def test_getitem(self):
        wrapper = Fallback(obj=self.test_dict, fallback=None)
        self.assertEqual("value_exists", wrapper["key_exists"].get())
        self.assertEqual(None, wrapper["key_does_not_exists"].get())

    def test_setitem(self):
        wrapper = Fallback(obj=self.test_dict, fallback="fallback")
        wrapper["new_attr"] = "new_attr_value"
        self.assertEqual("new_attr_value", wrapper["new_attr"].get())
        self.assertEqual("new_attr_value", self.test_dict["new_attr"])

    def test_delitem(self):
        wrapper = Fallback(obj=self.test_dict, fallback="fallback")
        self.assertEqual("value_exists", wrapper["key_exists"].get())
        del wrapper["key_exists"]
        self.assertEqual("fallback", wrapper["key_exists"].get())

    def test_setattributes(self):
        wrapper = Fallback(obj=self.test_obj, fallback="fallback")
        wrapper.new_attr = "new_attr_value"
        self.assertEqual("new_attr_value", wrapper.new_attr.get())
        self.assertEqual("new_attr_value", self.test_obj.new_attr)

    def test_getattributes(self):
        wrapper = Fallback(obj=self.test_obj, fallback="fallback")
        self.assertEqual("attr_exists_value", wrapper.attr_exists.get())
        self.assertEqual("fallback", wrapper.attr_does_not_exists.get())

    def test_func(self):
        func = Fallback(obj=lambda: "return_value", fallback="fallback")
        not_func = Fallback(obj=None, fallback="fallback")
        self.assertEqual("return_value", func().get())
        self.assertEqual("fallback", not_func().get())

    def test_iterSuccess(self):
        iterable = [1, 2, 3]
        wrapper = Fallback(iterable, fallback=[4, 5, 6])
        iterator = iter(wrapper)
        self.assertEqual(1, next(iterator).get())
        self.assertEqual(2, next(iterator).get())
        self.assertEqual(3, next(iterator).get())
        self.assertRaises(StopIteration, lambda: next(iterator))

    def test_iterFail(self):
        non_iterable = 123
        wrapper = Fallback(non_iterable, fallback=None)
        iterator = iter(wrapper)
        self.assertRaises(StopIteration, lambda: next(iterator))

    def test_iterFallback(self):
        non_iterable = 123
        wrapper = Fallback(non_iterable, fallback=[4, 5, 6])
        iterator = iter(wrapper)
        self.assertEqual(4, next(iterator).get())
        self.assertEqual(5, next(iterator).get())
        self.assertEqual(6, next(iterator).get())
        self.assertRaises(StopIteration, lambda: next(iterator))

    def test_str(self):
        wrapper = Fallback(123, fallback=456)
        self.assertEqual("123", str(wrapper))

        wrapper = Fallback(None, fallback=456)
        self.assertEqual("456", str(wrapper))

        wrapper = Fallback(None, fallback=None)
        self.assertEqual("None", str(wrapper))

    def test_repr(self):
        wrapper = Fallback(123, fallback=456)
        self.assertEqual("Fallback(obj=123, fallback=456)", repr(wrapper))

    def test_eq(self):
        wrapper1 = Fallback(123, fallback=456)
        self.assertNotEqual(123, wrapper1)
        wrapper2 = Fallback(123, fallback="fallback not same")
        self.assertEqual(wrapper1, wrapper2)

        wrapper3 = Fallback(None, fallback=123)
        wrapper4 = Fallback(None, fallback=123)
        self.assertEqual(wrapper3, wrapper4)

        wrapper5 = Fallback(None, fallback=678)
        self.assertNotEqual(wrapper4, wrapper5)

    def test_hash(self):
        wrapper = Fallback(123, fallback=456)
        self.assertEqual(hash(123), hash(wrapper))

        wrapper = Fallback(None, fallback=456)
        self.assertEqual(hash(456), hash(wrapper))

    def test_containsObj(self):
        set123 = {1, 2, 3}
        set456 = {4, 5, 6}
        wrapper = Fallback(set123, fallback=set456)
        self.assertTrue(1 in wrapper)
        self.assertTrue(2 in wrapper)
        self.assertTrue(3 in wrapper)
        self.assertFalse(4 in wrapper)
        self.assertFalse(5 in wrapper)
        self.assertFalse(6 in wrapper)

    def test_containsFallback(self):
        set456 = {4, 5, 6}
        wrapper = Fallback(None, fallback=set456)
        self.assertFalse(1 in wrapper)
        self.assertFalse(2 in wrapper)
        self.assertFalse(3 in wrapper)
        self.assertTrue(4 in wrapper)
        self.assertTrue(5 in wrapper)
        self.assertTrue(6 in wrapper)

    def test_containsFails(self):
        wrapper = Fallback(None, fallback=None)
        self.assertRaises(TypeError, lambda: 1 in wrapper)


if __name__ == "__main__":
    unittest.main()
