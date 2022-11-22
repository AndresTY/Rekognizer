import boto3

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')

table = dynamodb.create_table(
            TableName='photo-ducuara',
                KeySchema=[
                            {
                                            'AttributeName': 'day',
                                                        'KeyType': 'HASH'  #Partition key
                                                                },
                                    {
                                                    'AttributeName': 'ruta',
                                                                'KeyType': 'RANGE'  #Sort key
                                                                        }
                                        ],
                    AttributeDefinitions=[
                                {
                                                'AttributeName': 'day',
                                                            'AttributeType': 'N'
                                                                    },
                                        {
                                                        'AttributeName': 'ruta',
                                                                    'AttributeType': 'S'
                                                                            },

                                            ],
                        ProvisionedThroughput={
                                    'ReadCapacityUnits': 10,
                                            'WriteCapacityUnits': 10
                                                }
                        )

print("Table status:", table.table_status)
