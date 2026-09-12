<picture>
  <source media="(prefers-color-scheme: dark)" srcset="./assets/Catppuccin-Banner-dark.png">
  <source media="(prefers-color-scheme: light)" srcset="./assets/Catppuccin-Banner-light.png">
  <img alt="Catppuccin-Banner" src="./assets/Catppuccin-Banner-dark.png">
</picture>

----------------------------------------------------

### Requirements
|  Library   |          version        |     Required      |                 Purpose                |
|------------|-------------------------|-------------------|----------------------------------------|
|   `PIL`    |   Recommended:`10.1.0`  |        True       |             Image processing           |
|`catppuccin`|       `>=2.5.0,<3`      |        True       |       Provide catppuccin palettes      |
| `libraqm`  |           `Any`         |      Optional     |    To use `--text-direction` option    |

install requirements `pip`

* install catppuccin with `pip`

```bash
$ pip install "catppuccin>=2.5,<3" pillow
```

Further resources : 
* [Official Catppuccin Palette](https://github.com/catppuccin/python/tree/main?tab=readme-ov-file)
* [Official Pillow Installation Guide](https://pillow.readthedocs.io/en/latest/installation.html#python-support)

### Usage
The Python code utilizes the argparse library, allowing for various configurations of the image through the terminal. 


| Option              | Type   | Role                                                                        | Default Value   |
|---------------------|--------|-----------------------------------------------------------------------------|-----------------|
| `--path`            | str    | Path to save the generated banner image                                     | "Banner.png"    |
| `--format`          | str    | File format for the output image                                            | (None)          |
| `--text`            | str    | Text to be displayed on the banner                                          | "Catppuccin"    |
| `--text-position`   | str    | Starting position (x,y) of the text on the banner                           | (Auto)          |
| `--text-align`      | str    | Alignment of the text                                                       | "left"          |
| `--text-direction`  | str    | Direction of the text                                                       | (None)          |
| `--flavour`         | str    | Catppuccin color theme                                                      | "mocha"         |
| `--base-image`      | str    | Path to a base image for the banner background                              | (None)          |
| `--font`            | str    | Path to the '.ttf' font file for the text                                   | (Required)      |
| `--font-size`       | int    | Font size for the text                                                      | 0 (Auto)        |
| `--image-size`      | str    | Size of the banner image                                                    | "1600x600"      |
| `--text-color`      | str    | Color of the text                                                           | "text"          |
| `--text-bdr-color`  | str    | Color of the text border                                                    | "mauve"         |
| `--image-bdr-color` | str    | Color of the image border                                                   | "mauve"         |
| `--text-bdr-size`   | int    | Size of the text border                                                     | -1 (Auto)       |
| `--image-bdr-size`  | int    | Size of the image border                                                    | -1 (Auto)       |
| `--image-bdr-radius`| int    | Radius of the image border corners                                          | (None)          |
| `--bg-opacity`      | int    | Alpha (transparency) level of the background                                | 255             |


### Catppuccin Flavours and colors

```python
flavour_choice = [
    "latte", "frappe",
    "macchiato", "mocha",
]

color_choice = [
    "rosewater", "flamingo", "pink", "mauve", "red",
    "maroon", "peach", "yellow", "green", "teal",
    "sky", "sapphire", "blue", "lavender", "text",
    "subtext1", "subtext0", "overlay2", "overlay1",
    "overlay0", "surface2", "surface1", "surface0",
    "base", "mantle", "crust",
]
```

### Examples

Below are commands to create Dark/Light theme banner images for this repository. Check out the [Mocha theme image](./assets/Catppuccin-Banner-dark.png) and the [Latte theme image](./assets/Catppuccin-Banner-light.png)

1. Dark theme banner

```bash
$ python banner.py \ 
    --path="./assets/Catppuccin-Banner-dark.png" \ 
    --text="Catppuccin\nBanner" \ 
    --flavour=mocha \ 
    --text-color=sky \ 
    --text-border-color=text \ 
    --image-border-color=lavender \ 
    --font="/path/to/your/font.ttf" \ 
    --image-border-radius=20 \ 
    --text-align=left \ 
    --text-geometry="40,40" 
```

2. Light theme banner

```bash
$ python banner.py\ 
    --path="./assets/Catppuccin-Banner-light.png" \
    --text="Catppuccin\nBanner" \
    --flavour=latte \
    --text-color=lavender \
    --text-border-color=text \
    --image-border-color=sky \
    --font="/path/to/your/font.ttf" \
    --image-border-radius=20 \
    --text-align=left \
    --text-geometry="40,40"
```

### Fonts

Fonts are not bundled with this project. Provide the path to a font that you are
licensed to use with the `--font` option.
