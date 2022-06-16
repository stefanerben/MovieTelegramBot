
import requests, base64
from PIL import Image
from io import BytesIO


def getPosterImage(posterData):
    url = 'insertYourAPIendpointHere'
    img_data = requests.post(url, data = posterData)

    f = open("sample.txt", "wb")
    f.write(img_data.content)
    f.close()

    f = open("sample.txt", "r").read()

    img_data = str(f).replace("data:image/png;base64,", "").replace('<img src="', '').replace('" />', '')

    img = Image.open(BytesIO(base64.b64decode(img_data)))
    img.save('image.png', 'PNG')
