import requests
import base64

from PIL import Image
from io import BytesIO


def getPosterImage(posterData):
    url = 'http://cloud.mattes.cc:3000/poster'
    img_data = requests.post(url, data = posterData)

    f = open("sample.txt", "wb")
    f.write(img_data.content)
    f.close()

    f = open("sample.txt", "r").read()

    img_data = str(f).replace("data:image/png;base64,", "")


    img = Image.open(BytesIO(base64.b64decode(img_data)))
    #return img
    img.save('image.png', 'PNG')



