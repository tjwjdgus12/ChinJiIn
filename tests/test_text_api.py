import tempfile
import unittest
from pathlib import Path

import chinjiin
from chinjiin import word_fixer


class TextApiTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp_dir = tempfile.TemporaryDirectory()
        dictionary_path = Path(cls.temp_dir.name) / "custom.txt"
        dictionary_path.write_text(
            "강아지: 20\n망아지: 2\n안녕: 10\n반가워요: 10\n",
            encoding="utf-8",
        )
        word_fixer.load_dict(dictionary_path)

    @classmethod
    def tearDownClass(cls):
        cls.temp_dir.cleanup()

    def test_fix_preserves_punctuation_whitespace_and_mixed_scripts(self):
        source = "낭아지,  안녕!\nhello안녕"
        self.assertEqual(chinjiin.fix(source), "강아지,  안녕!\nhello안녕")

    def test_direct_fix_leaves_mixed_tokens_unchanged(self):
        self.assertEqual(word_fixer.direct_fix("안녕!"), "안녕!")
        self.assertEqual(word_fixer.direct_fix("hello안녕"), "hello안녕")

    def test_fix_file_defaults_to_utf8_sibling_output(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            input_path = Path(temp_dir) / "input.txt"
            input_path.write_text("낭아지!\n  안녕", encoding="utf-8")

            output_path = chinjiin.fix_file(input_path)

            self.assertEqual(output_path, input_path.with_name("input.fixed.txt"))
            self.assertEqual(
                output_path.read_text(encoding="utf-8"),
                "강아지!\n  안녕",
            )

    def test_fix_dir_processes_only_matching_files(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            source_dir = Path(temp_dir)
            (source_dir / "one.txt").write_text("낭아지", encoding="utf-8")
            (source_dir / "ignore.md").write_text("낭아지", encoding="utf-8")

            outputs = chinjiin.fix_dir(source_dir)

            self.assertEqual(outputs, [source_dir / "fixed" / "one.txt"])
            self.assertEqual(outputs[0].read_text(encoding="utf-8"), "강아지")
            self.assertFalse((source_dir / "fixed" / "ignore.md").exists())


if __name__ == "__main__":
    unittest.main()
