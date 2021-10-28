import os
import json
import glob
import datetime
from PIL import ImageFont, ImageDraw, Image  #pip install Pillow
from pathlib import Path

commander="YANOSH"
imageQuality=95
ttffont = "Roboto-Bold.ttf"

userFolder = os.path.expanduser("~")
eliteLogFolder = userFolder+"\\Saved Games\\Frontier Developments\\Elite Dangerous"
elitePhotoFolder = userFolder+"\\Pictures\\Frontier Developments\\Elite Dangerous"
Path(elitePhotoFolder+"\\Converted").mkdir(parents=True, exist_ok=True)
list_of_files = glob.glob(eliteLogFolder+"\\*.log")

def add_years(d):
    try:
        return d.replace(year=d.year + 1286)
    except ValueError:
        return d + (datetime.date(d.year + 1286, 1, 1) - datetime.date(d.year, 1, 1))
def convert_image(imageTitle,imageText,inImage,outImage):
    print(imageTitle,inImage)
    image = Image.open(inImage)
    draw = ImageDraw.Draw(image)

    font = ImageFont.truetype(ttffont, 20)
    font2 = ImageFont.truetype(ttffont, 12)

    draw.text((12, image.size[1]-73), imageTitle, font=font, fill="#000")
    draw.text((12, image.size[1]-48), imageText,  font=font2, fill="#000")
    draw.text((10, image.size[1]-75), imageTitle, font=font, fill='#EDEE7F')
    draw.text((10, image.size[1]-50), imageText,  font=font2)
    image.save(outImage, "JPEG", quality=imageQuality)  # save it

for file in list_of_files:
    logfile = open(file, 'r', encoding="utf8")
    lines = logfile.readlines()
    for line in lines:
        linedata = json.loads(line)
        event = linedata['event'] if 'event' in linedata else ""
        if event == 'Screenshot':
            imageFileName=linedata['Filename'].replace("\\ED_Pictures\\","")
            timestamp = linedata['timestamp']
            timestamp_obj = add_years(datetime.datetime.strptime(timestamp, '%Y-%m-%dT%H:%M:%SZ'))
            system = linedata['System']
            body = linedata['Body'] if 'Body' in linedata else ""
            latitude = str(linedata['Latitude']) if 'Latitude' in linedata else ""
            longitude = str(linedata['Longitude']) if 'Longitude' in linedata else ""
            heading = str(linedata['Heading']) if "Heading" in linedata else ""
            imageTitle=system+" - "+body
            imageText="Lat: "+latitude+"   Lon:"+longitude+"   Head:"+heading+"\n"+str(timestamp_obj)+"\nCommander: "+commander
            inImage = elitePhotoFolder+"\\"+imageFileName
            outImage = elitePhotoFolder+"\\Converted\\"+imageFileName
            if os.path.isfile(inImage):
                convert_image(imageTitle,imageText,inImage,outImage)
