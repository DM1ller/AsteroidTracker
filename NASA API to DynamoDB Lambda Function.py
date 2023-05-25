import json
import requests
import boto3

client = boto3.client('dynamodb')


def get_asteroids():
    response = requests.get('https://api.nasa.gov/neo/rest/v1/feed?start_date=2023-05-11&end_date=2023-05-11&api_key=7m6UK6aibw2jHOAvKOAgF6T9AJvMKK21zduo4ZhY')
    data = response.json()
    shortData = data['near_earth_objects']['2023-05-11']

    for asteroid in range(len(shortData)):
        asteroid_id = shortData[asteroid]['id']
        asteroid_name = shortData[asteroid]['name']
        hazardous = shortData[asteroid]['is_potentially_hazardous_asteroid']
        minSize = shortData[asteroid]['estimated_diameter']['meters']['estimated_diameter_min']
        maxSize = shortData[asteroid]['estimated_diameter']['meters']['estimated_diameter_max']
        averageSize = str((maxSize + minSize)//2)
        close_approach_date = shortData[asteroid]['close_approach_data'][0]['close_approach_date']
        orbiting_body = shortData[asteroid]['close_approach_data'][0]['orbiting_body']
        relative_velocity = str(int(float(shortData[asteroid]['close_approach_data'][0]['relative_velocity']['kilometers_per_hour'])//1))
        
        

        print (f'Asteroid ID: {asteroid_id} \nSize:{averageSize}\nIs Hazardous:{hazardous}\n Close Approach Date:{close_approach_date} \n  \n')
        print(type(close_approach_date))
        
        data = client.put_item(TableName = 'Asteroids_DynamoDB', Item={'ID':{'S':asteroid_id}, 'Name':{'S':asteroid_name}, 'Size (Meters)': {'N':averageSize}, 'Relative Velocity (KPH)': {'S':relative_velocity}, 'Orbiting Body':{'S':orbiting_body}, 'Is Hazardous': {'BOOL':hazardous}})

   
   


def lambda_handler(event, context):
    get_asteroids()
