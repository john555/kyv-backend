# Bring your packages onto the path
import sys, os, json
sys.path.append(os.path.abspath(os.path.join("..", "vms")))

import unittest
from vms.validation import is_empty

class VMSTestCase (unittest.TestCase):
    def test_is_empty(self):
        self.assertEqual(is_empty(), True)
        self.assertEqual(is_empty(None), True)
        self.assertEqual(is_empty(''), True)
        self.assertEqual(is_empty(2), False)
        self.assertEqual(is_empty('string'), False)

if __name__ == "__main__":
    unittest.main()
