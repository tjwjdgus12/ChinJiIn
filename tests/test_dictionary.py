import tempfile
import unittest
from pathlib import Path

from chinjiin import word_fixer
from chinjiin.converter import cji_converter, del_converter


class DictionaryTests(unittest.TestCase):
    def test_duplicate_frequencies_are_aggregated(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            dictionary_path = Path(temp_dir) / "custom.txt"
            dictionary_path.write_text(
                "강아지: 10\n강아지: 5\n망아지: 2\n",
                encoding="utf-8",
            )

            loaded = cji_converter.load_cji_dict(dictionary_path)

        self.assertEqual(loaded[cji_converter.convert("강아지")], 15)
        self.assertEqual(loaded[cji_converter.convert("망아지")], 2)

    def test_custom_dictionary_drives_dynamic_frequency_ranking(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            dictionary_path = Path(temp_dir) / "custom.txt"
            dictionary_path.write_text(
                "강아지: 10\n강아지: 5\n망아지: 2\n",
                encoding="utf-8",
            )
            word_fixer.load_dict(dictionary_path)

            self.assertEqual(word_fixer.max_freq, 15)
            self.assertEqual(word_fixer.direct_fix("낭아지"), "강아지")

    def test_delete_index_deduplicates_candidates(self):
        index = del_converter.build_delete_index(["가", "가"])
        self.assertTrue(all(isinstance(candidates, list) for candidates in index.values()))
        self.assertTrue(all(candidates == ["가"] for candidates in index.values()))


if __name__ == "__main__":
    unittest.main()
