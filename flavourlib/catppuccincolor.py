from catppuccin import PALETTE
from catppuccin.models import Color, Flavor


class CatppuccinColor:
    """Expose Catppuccin colors in formats accepted by Pillow."""

    _flavours = {flavour.identifier: flavour for flavour in PALETTE}
    flavour_choice = tuple(_flavours)
    color_choice = tuple(color.identifier for color in PALETTE.mocha.colors)

    def __init__(self, flavour: str):
        self.flavour = self.get_flavour(flavour)
        self.flavour_name = self.flavour.identifier

    def chex(self, color: str, prefix: str = "#") -> str:
        return prefix + self.get_color(self.flavour, color).hex.removeprefix("#")

    def crgb(self, color: str) -> tuple[int, int, int]:
        rgb = self.get_color(self.flavour, color).rgb
        return rgb.r, rgb.g, rgb.b

    def crgba(self, color: str) -> tuple[int, int, int, int]:
        return (*self.crgb(color), 255)

    @classmethod
    def get_color(cls, flavour: str | Flavor, color: str) -> Color:
        if color not in cls.color_choice:
            choices = ", ".join(cls.color_choice)
            raise ValueError(
                f"Unknown Catppuccin color {color!r}. Choose from: {choices}"
            )

        if isinstance(flavour, str):
            flavour = cls.get_flavour(flavour)
        elif not isinstance(flavour, Flavor):
            raise TypeError("flavour must be a Catppuccin Flavor or its identifier")

        return getattr(flavour.colors, color)

    @classmethod
    def get_flavour(cls, flavour: str) -> Flavor:
        try:
            return cls._flavours[flavour]
        except KeyError:
            choices = ", ".join(cls.flavour_choice)
            raise ValueError(
                f"Unknown Catppuccin flavour {flavour!r}. Choose from: {choices}"
            ) from None


if __name__ == "__main__":
    colors = CatppuccinColor("mocha")
    print(colors.chex("base"))
