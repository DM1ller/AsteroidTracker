import json
import requests
import boto3

client = boto3.client('dynamodb')


def get_asteroids():
    response = requests.get('https://api.nasa.gov/neo/rest/v1/feed?start_date=2023-05-11&end_date=2023-05-11&api_key=ENTER KEY HERE')
    data = response.json()
    shortData = data['near_earth_objects']['2023-05-11']

    for asteroid in range(len(shortData)):
        asteroid_id = shortData[asteroid]['id']
        hazardous = shortData[asteroid]['is_potentially_hazardous_asteroid']
        minSize = shortData[asteroid]['estimated_diameter']['meters']['estimated_diameter_min']
        maxSize = shortData[asteroid]['estimated_diameter']['meters']['estimated_diameter_max']
        averageSize = str((maxSize + minSize)//2)

        print (f'Asteroid ID: {asteroid_id} \nSize:{averageSize}\nIs Hazardous:{hazardous}\n\n')
        
        data = client.put_item(TableName = 'Asteroids_DynamoDB', Item={'ID':{'S':asteroid_id}, 'Size (Meters)': {'N':averageSize}, 'Is Hazardous': {'BOOL':hazardous}})

   
   


def lambda_handler(event, context):
    get_asteroids()