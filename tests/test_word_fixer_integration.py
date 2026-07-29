import unittest

from chinjiin import word_fixer
from chinjiin.converter import cji_converter


class DefaultDictionaryIntegrationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        word_fixer.load_dict()

    def test_default_dictionary_aggregates_duplicate_source_frequencies(self):
        geu = cji_converter.convert("그")
        self.assertEqual(word_fixer.cji_dict[geu], 54868 + 196 + 3)
        self.assertEqual(word_fixer.max_freq, max(word_fixer.cji_dict.values()))

    def test_known_keyboard_typo_prefers_physically_closer_candidate(self):
        self.assertEqual(word_fixer.direct_fix("낭아지"), "강아지")

    def test_valid_compound_final_words_are_not_corrupted(self):
        for word in ("젊은", "않습니다", "삶을", "없습니다"):
            with self.subTest(word=word):
                self.assertEqual(word_fixer.direct_fix(word), word)


if __name__ == "__main__":
    unittest.main()
