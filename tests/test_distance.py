import unittest

from chinjiin.converter import cji_converter
from chinjiin.measurer import edit_distance_calculater


class PhysicalEditDistanceTests(unittest.TestCase):
    def test_internal_separator_has_no_physical_key_cost(self):
        typo = cji_converter.convert("듣전")
        candidate = cji_converter.convert("듣던")

        self.assertEqual(
            edit_distance_calculater.calc_edit_dist(candidate, typo),
            1,
        )


if __name__ == "__main__":
    unittest.main()
