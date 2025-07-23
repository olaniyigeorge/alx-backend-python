#!/usr/bin/env python3

from utils import access_nested_map


nested_map={"x": {"y": {"z": 10}}}

path=["x", "y"]


print(access_nested_map(nested_map, path)) 







class TestAccessNestedMap(unittest.TestCase):

    def test_access_nested_map(self):
        nested_map={"x": {"y": {"z": 10}}}
        path=["x", "y"]
        self.assertEqual(access_nested_map(nested_map, path), 1)

