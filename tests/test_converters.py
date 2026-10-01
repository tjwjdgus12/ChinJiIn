import unittest

from chinjiin.converter import cji_converter, han_converter


class HangulRoundTripTests(unittest.TestCase):
    def assert_round_trip(self, text):
        converted = cji_converter.convert(text)
        self.assertEqual(han_converter.convert(converted), text)

    def test_all_modern_hangul_syllables_round_trip(self):
        for codepoint in range(0xAC00, 0xD7A4):
            with self.subTest(codepoint=hex(codepoint)):
                self.assert_round_trip(chr(codepoint))

    def test_compound_final_before_next_syllable_round_trips(self):
        for word in ("젊은", "않습니다", "삶을", "없습니다", "읽고", "맑고"):
            with self.subTest(word=word):
                self.assert_round_trip(word)


if __name__ == "__main__":
    unittest.main()
