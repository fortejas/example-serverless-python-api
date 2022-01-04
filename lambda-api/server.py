import os
import random
import datetime

import boto3

from fastapi import FastAPI
from mangum import Mangum

# Constants
AWS_REGION = os.environ.get('AWS_REGION')
TABLE_NAME = os.environ.get('TABLE_NAME')
PARTITION_KEY= "id"


ddb = boto3.client('dynamodb', region_name=AWS_REGION)


destinations = [
    'London',
    'Manchester',
    'Edinburgh'
]


def write_to_ddb():

    choice = random.choice(destinations)

    time = datetime.datetime.today()
    time_str = datetime.datetime.strftime(time, '%H:%M')

    print(f'Recording Train Departure: {choice} @ {time_str}')

    ddb.put_item(
        TableName=TABLE_NAME,
        Item={
            PARTITION_KEY: { 'S': 'last_departed' },
            'dest': { 'S': choice },
            'time': { 'S': time_str }
        }
    )

    return choice, time_str


def get_last_departed():
    result = ddb.get_item(TableName=TABLE_NAME, Key={'id': {'S': 'last_departed'}})

    dest = result['Item']['dest']['S']
    time = result['Item']['time']['S']

    return dest, time


app = FastAPI()


@app.get("/")
def read_root():
    return {"hello": "world"}


@app.post("/update")
def refresh_time():
    choice, time_str = write_to_ddb()
    return {'new_departure': choice, 'time': time_str}


@app.get('/last_departed')
def read_times():
    dest, time = get_last_departed()
    return {'last_departed': dest, 'departure_time': time}


handler = Mangum(app)
