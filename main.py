import os
import sys

libdir = "./lib/e-Paper/RaspberryPi_JetsonNano/python/lib"
if os.path.exists(libdir):
    sys.path.append(libdir)

import logging
import requests
from waveshare_epd import epd7in3f
from PIL import Image
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.DEBUG)

try:
    response = requests.get(os.getenv("DAILY_PHOTO_API_URL")).json()
    print(response)
    image_response = requests.get(response['activeImage'], stream=True)
    image = Image.open(image_response.raw)

    epd = epd7in3f.EPD()
    epd.init()
    epd.Clear()
    
    logging.info("1.Drawing on the image...")
    Himage = Image.new('RGB', (epd.width, epd.height), epd.WHITE)  # 255: clear the frame
    epd.display(epd.getbuffer(Himage))
    epd.display(epd.getbuffer(image.resize((800, 480))))
    epd.sleep()

except IOError as e:
    logging.info(e)
    
except KeyboardInterrupt:    
    logging.info("ctrl + c:")
    epd7in3f.epdconfig.module_exit(cleanup=True)
    exit()
