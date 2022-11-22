import boto3
from decimal import Decimal
from boto3.dynamodb.conditions import Key,Attr

dynamodb = boto3.resource('dynamodb', 'us-east-1')

print(list(dynamodb.tables.all()))

result_list=[]


table = dynamodb.Table('photo-ducuara')

# logos on 1669079603.6762888
print(table.query(KeyConditionExpression=Key('day').eq(Decimal('1669079603.6762888')),FilterExpression= Attr('info.name').contains('Logo')))

#all People
print(table.scan(FilterExpression= Attr('info.name').eq('People')| Attr('info.parents').contains('People')))
