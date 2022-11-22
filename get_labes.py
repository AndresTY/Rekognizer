import boto3
import requests
from PIL import Image
from io import BytesIO
import mimetypes
import time
import json

def upload_file(file_name, bucket, object_name=None):
    if object_name is None:
        object_name = os.path.basename(file_name)
    try:
        response = s3.upload_file(file_name, bucket, object_name)
    except ClientError as e:
        logging.error(e)
        return False
    return True
 
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

def get_labels_json(files_in_S3):
    data = []
    for j,y in files_in_S3:
        response = rek_client.detect_labels(Image={'S3Object':{'Bucket':S3_BUCKET,'Name':j}})
    
        label_lst = []
    
        for label in response['Labels']:
            label_lst.append(label['Name'])
            for parents in label['Parents']:
                label_lst.append(parents['Name'])
        #data += f'{label_lst[0]}|{label_lst[1:]}|{y}'
        data.append({"url": y,"day": today,"info":{"name":label_lst[0],"parents":label_lst[1:]}})
        
    return data

def load_data(data):
    with open('/tmp/data_dynamo.json','a+') as f:
        f.write(json.dumps(data)) #escritura de los datos transformados
        f.close()
    with open("/tmp/data_dynamo.json", "rb+") as f:
        s3.upload_fileobj(f, S3_BUCKET, f"dynamo.json") #carge archivo JSON

today = time.time()
S3_BUCKET = 'bigdata-ducuara'

s3 = boto3.client('s3','us-east-1')
rek_client = boto3.client('rekognition','us-east-1')

object_key = "page_img.txt"
file_content = str(s3.get_object(Bucket=S3_BUCKET, Key=object_key)["Body"].read().decode('utf-8')).split('\n')

files_list = save_img(file_content)
labels = get_labels_json(files_list)
load_data(labels)


        