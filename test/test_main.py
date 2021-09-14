import unittest
from main import *


class ExtractInputTestCase(unittest.TestCase):
    def test_extract_input(self):
        tests = [
            ("queens,ny", ("queens", "ny")),
            ("queens,nyc", ("", "")),
            ("palo alto,ca", ("palo alto", "ca")),
            ("boston,massachusetts", ("", "")),
            ("miami,fl,usa", ("", ""))
        ]
        for value, expected in tests:
            with self.subTest(value=value):
                self.assertTupleEqual(extract_input(value), expected)


if __name__ == '__main__':
    unittest.main()
