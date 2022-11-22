import requests
from PIL import Image
from io import BytesIO
import mimetypes
import time
import json
import requests
from bs4 import BeautifulSoup

def save_img(file_content, tester=False, char = ''):
    files_in_S3=[]
    for e,i in enumerate(file_content):
        if "svg" not in i:
            try:
                if tester:
                    response=requests.get(i,stream=True)
                    img=Image.open(BytesIO(response.content))
                    name = f'{e}.png'
                    img.save(name)
                else:
                    imageResponse = requests.get(i, stream = True).raw
                    content_type = imageResponse.headers['content-type']
                    extension = mimetypes.guess_extension(content_type)
                    name = f'image/{str(today)}/{e}{extension}'
                    s3.upload_fileobj(imageResponse, S3_BUCKET, name)
                files_in_S3.append((name,i))
            except Exception as E:
                print('Casual error',E)
    return files_in_S3

def extract_images_url(URL):

    page = requests.get(URL)
    imgurls = []
    soup = BeautifulSoup(page.content, "html.parser")
    for i in set(soup.find_all("img")):

        if (URL not in i.get("src",None)) and ("https" not in i.get("src",None)):
            imgurls.append(URL+i["src"])
        else:
            imgurls.append(i["src"])
    return imgurls