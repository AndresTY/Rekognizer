import boto3
import json
import decimal

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
s3 = boto3.client('s3','us-east-1')
table = dynamodb.Table('photo-ducuara')


json_file = s3.get_object(Bucket='bigdata-ducuara', Key='dynamo.json')["Body"].read()

movies = json.loads(json_file, parse_float = decimal.Decimal)
for i in movies:
    print("Adding movie:", i['url'], i['info']['name'],i['day'])
    table.put_item(Item={'day': i['day'],'ruta': i['url'],'info': i['info'] } )
