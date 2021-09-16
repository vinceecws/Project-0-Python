import unittest
from main import extract_input
from weather.util import format_wind_deg, format_visibility


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


class FormatVisibilityTestCase(unittest.TestCase):
    def test_low_visibility(self):
        self.assertFalse(format_visibility(999).endswith("km"), "Ends with km")
        self.assertTrue(format_visibility(999) == "999m", "Wrong format")
        self.assertTrue(format_visibility(0) == "0m", "Wrong format")
        self.assertTrue(format_visibility(500) == "500m", "Wrong format")

    def test_high_visibility(self):
        self.assertTrue(format_visibility(1000).endswith("km"), "Ends with km")
        self.assertTrue(format_visibility(5020) == "5.0km", "Wrong format")
        self.assertTrue(format_visibility(10000) == "10.0km", "Wrong format")
        self.assertTrue(format_visibility(2100) == "2.1km", "Wrong format")


class FormatWindDegTestCase(unittest.TestCase):
    def test_nsew_only_true(self):
        self.assertTrue(format_wind_deg(359, nsew_only=True) == "NW")
        self.assertTrue(format_wind_deg(180, nsew_only=True) == "S")
        self.assertTrue(format_wind_deg(0, nsew_only=True) == "N")
        self.assertTrue(format_wind_deg(136, nsew_only=True) == "SE")

    def test_nsew_only_false(self):
        self.assertTrue(format_wind_deg(143) == "8° SE")
        self.assertTrue(format_wind_deg(228) == "3° SW")
        self.assertTrue(format_wind_deg(93) == "3° E")
        self.assertTrue(format_wind_deg(7) == "7° N")


if __name__ == '__main__':
    unittest.main()

