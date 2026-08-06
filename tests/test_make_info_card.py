import tempfile
import unittest
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

import make_info_card


class MakeInfoCardTests(unittest.TestCase):
    def test_escapes_xml_special_characters_in_svg_text(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            out_path = Path(tmpdir) / "info-card.svg"
            make_info_card.make_svg([("Now", "A & B")], out_path, static=True)
            content = out_path.read_text(encoding="utf-8")
            self.assertIn("A &amp; B", content)

    def test_renders_bullet_points_with_indented_svg_lines(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            out_path = Path(tmpdir) / "info-card.svg"
            make_info_card.make_svg([("Highlights", "• Built a quantitative research operating system.\n• Created Hermes")], out_path, static=True)
            content = out_path.read_text(encoding="utf-8")
            self.assertIn("• Built a quantitative research operating system.", content)
            self.assertIn("x=\"120\"", content)

    def test_wraps_long_bullets_across_multiple_svg_lines(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            out_path = Path(tmpdir) / "info-card.svg"
            make_info_card.make_svg([("Highlights", "• This is a very long bullet that should wrap onto another line because it exceeds the available width.")], out_path, static=True)
            content = out_path.read_text(encoding="utf-8")
            self.assertGreaterEqual(content.count('<text x="120"'), 2)


if __name__ == "__main__":
    unittest.main()
