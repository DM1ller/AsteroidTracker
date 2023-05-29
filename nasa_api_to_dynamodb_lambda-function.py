import json
import requests
import boto3
import datetime

client = boto3.client('dynamodb')

#Collects the current date and inserts the date into the start and end date of api_link
current_date = datetime.date.today()
current_date_str = current_date.strftime("%Y-%m-%d")
api_link = "https://api.nasa.gov/neo/rest/v1/feed?start_date=" + current_date_str + "&end_date=" + current_date_str + "&api_key=#########"

def get_asteroids():
    response = requests.get(api_link)
    data = response.json()
    short_data = data['near_earth_objects'][current_date_str]

    for asteroid in range(len(short_data)):
        asteroid_id = short_data[asteroid]['id']
        asteroid_name = short_data[asteroid]['name']
        hazardous = short_data[asteroid]['is_potentially_hazardous_asteroid']
        min_size = short_data[asteroid]['estimated_diameter']['meters']['estimated_diameter_min']
        max_size = short_data[asteroid]['estimated_diameter']['meters']['estimated_diameter_max']
        average_size = str((max_size + min_size)//2)
        close_approach_date = short_data[asteroid]['close_approach_data'][0]['close_approach_date']
        orbiting_body = short_data[asteroid]['close_approach_data'][0]['orbiting_body']
        relative_velocity = str(int(float(short_data[asteroid]['close_approach_data'][0]['relative_velocity']['kilometers_per_hour'])//1))
        
        #Write the data to the DynamoDB Table
        client.put_item(TableName = 'Asteroids_DynamoDB', Item={'ID':{'S':asteroid_id}, 'Name':{'S':asteroid_name}, 'Size (Meters)': {'N':average_size}, 'Relative Velocity (KPH)': {'S':relative_velocity}, 'Orbiting Body':{'S':orbiting_body}, 'Is Hazardous': {'BOOL':hazardous}})

def lambda_handler(event, context):
    get_asteroids()