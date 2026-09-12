from flavourlib import CatppuccinColor
from PIL import Image, ImageDraw, ImageFont
import argparse

parser = argparse.ArgumentParser(prog="banner.py", 
                                 description="Creates a banner image with Catppuccin color themes and customizable typography.")

parser.add_argument("--path",                   type=str,   default="Banner.png",   help="Path to save the generated banner image. Default is 'Banner.png'.")
parser.add_argument("--format",                 type=str,                           help="File format for the output image. Automatically detected from the file extension if not specified.")
parser.add_argument("--text",                   type=str,   default="Catppuccin",   help="Text to be displayed on the banner. Default is 'Catppuccin'.")
parser.add_argument("--text-position",          type=str,                           help="Specifies the starting position (x,y) of the text on the banner. Format: 'x,y'. If not specified, defaults to an automatically calculated position.")
parser.add_argument("--text-align",             type=str,   default="left",         choices=["left", "center", "right"], help="Alignment of the text. Choices are 'left', 'center', 'right'. Default is 'left'.")
parser.add_argument("--text-direction",         type=str,                           choices=["ltr", "rtl", "ttb"], help="Direction of the text. Choices are 'ltr' (left-to-right), 'rtl' (right-to-left), 'ttb' (top-to-bottom). Requires libraqm to use this option.")
parser.add_argument("--flavour",                type=str,   default="mocha",        choices=CatppuccinColor.flavour_choice, help="Catppuccin color theme. Default is 'mocha'.")
parser.add_argument("--base-image",             type=str,                           help="Path to a base image to be used as the banner background. If not specified, a solid color background is used.")
parser.add_argument("--font",                   type=str,   required=True,          help="Path to the '.ttf' font file to be used for the text.")
parser.add_argument("--font-size",              type=int,   default=0,              help="Font size for the text. If not specified, automatically calculated based on image height.")
parser.add_argument("--image-size",             type=str,   default="1600x600",     help="Size of the banner image. Format: 'widthxheight'. Default is '1600x600'.")
parser.add_argument("--text-color",             type=str,   default="text",         choices=CatppuccinColor.color_choice, help="Color of the text. Default is 'text'.")
parser.add_argument("--text-bdr-color",         type=str,   default="mauve",        choices=CatppuccinColor.color_choice, help="Color of the text border. Default is 'mauve'.")
parser.add_argument("--image-bdr-color",        type=str,   default="mauve",        choices=CatppuccinColor.color_choice, help="Color of the image border. Default is 'mauve'.")
parser.add_argument("--text-bdr-size",          type=int,   default=-1,             help="Size of the text border. If not specified or below 0, automatically calculated.")
parser.add_argument("--image-bdr-size",         type=int,   default=-1,             help="Size of the image border. If not specified or below 0, automatically calculated.")
parser.add_argument("--image-bdr-radius",       type=int,                           help="Radius of the image border corners. If not specified, a rectangle is drawn.")
parser.add_argument("--bg-opacity",             type=int,   default=255,            help="Sets the alpha (transparency) level of the background. Accepts a value from 0 (fully transparent) to 255 (fully opaque). Default is 255 (fully opaque).")

def parse_geometry(geometry:str, sep:str) -> tuple[int, int]:
    if len(sep) > 1:
        raise RuntimeError("Invalid separator")
    g = geometry.split(sep)
    return (int(g[0]), int(g[1]))

def textpos_calculate(imgsz:tuple[int, int]) -> tuple[int, int]:
    return (imgsz[0]//8, imgsz[1]//8)

def mask_alpha(image_A: Image, image_B: Image) -> Image:
    alpha_A = image_A.split()[3]
    r, g, b, _ = image_B.split()
    result = Image.merge("RGBA", (r, g, b, alpha_A))
    return result


option = parser.parse_args()
# --------------- basic settings ---------------
savepath = option.path # str
colorset = CatppuccinColor(option.flavour)
# -------------------- size --------------------
image_W, image_H = parse_geometry(option.image_size, 'x') # int, int
fontsize = option.font_size if option.font_size > 0 else image_H // 3 # int
# ---------------- text && font ----------------
text = option.text.replace(r"\n", "\n") # str
font = ImageFont.truetype(option.font, fontsize)
# ----- Border color && size configuration -----
text_color = colorset.crgba(option.text_color)
textborder_color = colorset.crgba(option.text_bdr_color)
imgborder_color = colorset.crgba(option.image_bdr_color)
textborder_size = option.text_bdr_size if option.text_bdr_size >= 0 else fontsize // 40 # int
imgborder_size = option.image_bdr_size if option.image_bdr_size >= 0 else fontsize // 20 # int
# ------------------- Image --------------------
mask = Image.new("RGBA", (image_W, image_H), color=(0, 0, 0, 0))
mask_canvas = ImageDraw.Draw(mask)
# --------------- text position ----------------
text_X = None
text_Y = None
if option.text_position is None:
    text_X, text_Y = textpos_calculate(imgsz=(image_W, image_H))
else:
    text_X, text_Y = parse_geometry(option.text_position, ',')
# -------------- Draw mask rectangle -------------
if option.image_bdr_radius is None:
    mask_canvas.rectangle([(imgborder_size // 2, imgborder_size // 2), 
                                (mask.size[0] - imgborder_size // 2 - 1, mask.size[1] - imgborder_size // 2 - 1)], 
                                width=imgborder_size,
                                fill=(0, 0, 0, option.bg_opacity))
else:
    mask_canvas.rounded_rectangle([(imgborder_size // 2, imgborder_size // 2), 
                                (mask.size[0] - imgborder_size // 2 - 1, mask.size[1] - imgborder_size // 2 - 1)], 
                                radius=option.image_bdr_radius, 
                                width=imgborder_size,
                                fill=(0, 0, 0, option.bg_opacity))        
# ------------- Draw base image to mask ----------
image = Image.new("RGBA", (image_W, image_H), color=colorset.crgba("base")) if option.base_image is None else Image.open(option.base_image).convert("RGBA")
result = mask_alpha(mask, image)
canvas = ImageDraw.Draw(result)

# --------------- Draw image border --------------
if imgborder_size > 0:
    if option.image_bdr_radius is None:
        canvas.rectangle([(imgborder_size // 2, imgborder_size // 2), 
                                (mask.size[0] - imgborder_size // 2 - 1, mask.size[1] - imgborder_size // 2 - 1)], 
                                outline=imgborder_color, 
                                width=imgborder_size)
    else:
        canvas.rounded_rectangle([(imgborder_size // 2, imgborder_size // 2), 
                                (mask.size[0] - imgborder_size // 2 - 1, mask.size[1] - imgborder_size // 2 - 1)], 
                                radius=option.image_bdr_radius, 
                                outline=imgborder_color, 
                                width=imgborder_size)    

# ---------------- Draw text border --------------
if textborder_size > 0: # if size is 0, not drawing border
    for dx in range(-textborder_size, textborder_size + 1):
        for dy in range(-textborder_size, textborder_size + 1):
            canvas.text((text_X + dx, text_Y + dy), text=text, font=font, fill=textborder_color, align=option.text_align, direction=option.text_direction)
# ----------------- write text -----------------
canvas.text((text_X, text_Y), text, font=font, fill=text_color, align=option.text_align, direction=option.text_direction) # edit this part

# ----------------- Save Image -----------------
result.save(savepath, format=option.format)
