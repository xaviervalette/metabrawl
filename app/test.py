from PIL import Image
import glob
from dotenv import load_dotenv
import os
import errno

load_dotenv()

dataPath = os.environ["BRAWL_COACH_DATAPATH"]
frontPath = os.environ["BRAWL_COACH_FRONTPATH"]
backPath = os.environ["BRAWL_COACH_BACKPATH"]
logPath = os.environ["BRAWL_COACH_LOGPATH"]
token = os.environ["BRAWL_COACH_TOKEN"]
currentBattlePath = dataPath+"/battles/current"
allBattlePath = dataPath+"/battles/all"
webImgPath = frontPath+"/app/static/img"

imgList = []
imgNameList = {}
for filename in glob.glob(f"{webImgPath}/maps/*/*.png"):
    print(filename)
    mode = os.path.basename(os.path.dirname(str(filename)))
    map=os.path.basename(str(filename))
    print(os.path.basename(os.path.dirname(str(filename))))
    im=Image.open(filename)
    #imgList.append(im)

    alpha = im.getchannel('A')

    # Set the border and color
    borderSize = 20
    color = (207, 207, 207)

    # Create red image the same size and copy alpha channel across
    background = Image.new('RGBA', im.size, color=color)
    background.putalpha(alpha) 

    # Make the background bigger
    background=background.resize((background.size[0]+borderSize, background.size[1]+borderSize))

    # Merge the targeted image (foreground) with the background
    foreground = im
    background.paste(foreground, (int(borderSize/2), int(borderSize/2)), foreground.convert("RGBA"))
    imageWithBorder = background
    #imageWithBorder.show()
    filePath = f"{webImgPath}/maps/borderImg/{mode}/"
    if not os.path.exists(os.path.dirname(filePath)):
        try:
            os.makedirs(os.path.dirname(filePath))
        except OSError as exc: # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise
    imageWithBorder.save(f"{filePath}{map}")
