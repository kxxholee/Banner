import unittest

from catppuccin.models import Color, Flavor

from flavourlib import CatppuccinColor


class CatppuccinColorTest(unittest.TestCase):
    def test_all_flavours_and_colors_are_available(self):
        self.assertEqual(
            CatppuccinColor.flavour_choice,
            ("latte", "frappe", "macchiato", "mocha"),
        )
        self.assertEqual(len(CatppuccinColor.color_choice), 26)

        for flavour_name in CatppuccinColor.flavour_choice:
            flavour = CatppuccinColor.get_flavour(flavour_name)
            self.assertIsInstance(flavour, Flavor)
            for color_name in CatppuccinColor.color_choice:
                self.assertIsInstance(
                    CatppuccinColor.get_color(flavour, color_name), Color
                )

    def test_pillow_color_formats(self):
        colors = CatppuccinColor("mocha")

        self.assertEqual(colors.chex("mauve"), "#cba6f7")
        self.assertEqual(colors.chex("mauve", prefix="0x"), "0xcba6f7")
        self.assertEqual(colors.crgb("mauve"), (203, 166, 247))
        self.assertEqual(colors.crgba("mauve"), (203, 166, 247, 255))

    def test_invalid_flavour_has_a_helpful_error(self):
        with self.assertRaisesRegex(ValueError, "macchiato"):
            CatppuccinColor("macchiatto")

    def test_invalid_color_has_a_helpful_error(self):
        with self.assertRaisesRegex(ValueError, "mauve"):
            CatppuccinColor("mocha").crgb("purple")

    def test_invalid_flavour_type_is_rejected(self):
        with self.assertRaisesRegex(TypeError, "Flavor"):
            CatppuccinColor.get_color(object(), "mauve")


if __name__ == "__main__":
    unittest.main()
