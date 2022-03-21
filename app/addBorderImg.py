from PIL import Image, ImageOps

from PIL import Image

background = Image.open("bankshot.png")
background.paste((255,0,0), [0,0,background.size[0], background.size[1]])
foreground = Image.open("Brawlstars.png")

background.paste(foreground, (0, 0), foreground.convert("RGBA"))
background.show()