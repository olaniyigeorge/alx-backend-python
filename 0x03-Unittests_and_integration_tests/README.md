# Unit Testing: `access_nested_map` Function

This module contains unit tests for the `access_nested_map` function defined in `utils.py`. The tests are written using Python’s built-in `unittest` framework and `parameterized` for test case expansion.

## ✅ What was implemented

- Created a test class `TestAccessNestedMap` inheriting from `unittest.TestCase`.
- Used the `@parameterized.expand` decorator to test multiple input/output combinations.
- Verified that `access_nested_map(nested_map, path)` returns the expected value for various nested structures.

## 🧪 Test Cases Covered

| Nested Map                   | Path         | Expected Value |
|-----------------------------|--------------|----------------|
| `{"a": 1}`                  | `("a",)`     | `1`            |
| `{"a": {"b": 2}}`           | `("a",)`     | `{"b": 2}`     |
| `{"a": {"b": 2}}`           | `("a", "b")` | `2`            |

## 🧰 Dependencies

Install the `parameterized` library if not already installed:

```bash
pip install parameterized





## 🚨 Exception Testing

The `test_access_nested_map_exception` test ensures that a `KeyError` is raised when accessing missing keys in the nested map.

### ❗ Test Cases Covered

| Nested Map       | Path         | Expected Exception |
|------------------|--------------|--------------------|
| `{}`             | `("a",)`     | `KeyError: 'a'`    |
| `{"a": 1}`       | `("a", "b")` | `KeyError: 'b'`    |

### ✅ What it does

- Uses `@parameterized.expand` to provide multiple invalid paths.
- Uses `with self.assertRaises(KeyError)` context manager to verify an exception is raised.
- Asserts that the exception message matches the missing key (`repr(path[-1])`).
