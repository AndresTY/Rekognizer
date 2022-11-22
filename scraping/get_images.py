import boto3
import requests
from bs4 import BeautifulSoup

S3_BUCKET = 'bigdata-ducuara'
s3 = boto3.client('s3')

def upload_file(file_name, bucket, object_name=None):
    if object_name is None:
        object_name = os.path.basename(file_name)
    try:
        response = s3.upload_file(file_name, bucket, object_name)
    except ClientError as e:
        logging.error(e)
        return False
    return True

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


object_key = "page.txt"
file_content = str(s3.get_object(Bucket=S3_BUCKET, Key=object_key)["Body"].read().decode('utf-8')).split('\n')
for i in file_content:
    url=extract_images_url(i)
    for j in url:
        print(j)
        f = open('/tmp/page_img.txt','a+')
        f.write(j+'\n')

with open("/tmp/page_img.txt", "rb") as f:
            s3.upload_fileobj(f, S3_BUCKET, 'page_img.txt')