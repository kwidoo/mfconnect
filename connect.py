import requests
from dotenv import load_dotenv
import os
from datetime import datetime, timedelta
import json
import logging
from rich.logging import RichHandler

logging.basicConfig(level=logging.ERROR, handlers=[RichHandler()])

load_dotenv()

url = os.getenv('API_URL')
mfHeaders = {
            'User-Agent': 'MyFitness/26 CFNetwork/1399 Darwin/22.1.0',
            'country-id': 'lv',
            'language-Id': 'lv',
        }
loginResponse = {}

def login():
    response = requests.post(
        url + '/oauth/token',
        data = {
            'username':os.getenv('USERNAME'),
            'password':os.getenv('PASSWORD'),
            'client_id':os.getenv('CLIENT_ID'),
            'client_secret':os.getenv('CLIENT_SECRET'),
            'grant_type':'password',
            'push_token':os.getenv('PUSH_TOKEN'),
        },
        headers=mfHeaders
    )
    return response.json()

def refresh(): 
    response = requests.post(
        url + '/oauth/token',
        data = {
            'refresh_token': loginResponse['refresh_token'],
            'client_id':os.getenv('CLIENT_ID'),
            'client_secret':os.getenv('CLIENT_SECRET'),
            'grant_type':'refresh_token',
        },
        headers=mfHeaders
    )
    return response.json()


def search_classes(when):
    response = requests.post(
        url + '/classes/search',
        data = json.dumps({ 
            'additional_service_ids': [],
            'club_ids': [
                '18'
            ],
            'country_ids': [
                'lv'
            ],
            'date_for': when.strftime('%Y-%m-%d 00:00:01+02:00'),
            'date_from': when.strftime('%Y-%m-%d 00:00:01+02:00'),
            'date_to': when.strftime('%Y-%m-%d 23:59:59+02:00'),
            'search_string': 'BOXBOX',
            'time_ids': [],
            'town_ids': [
                "1"
            ],
            'trainer_ids': [
                300
            ],
            'training_ids': [],
            'training_type_ids': []
        }, indent=4, sort_keys=True),
        headers = mfHeaders
    )
    return response.json()

def reserve(id):
    response = requests.post(
        url + '/reservations/' + str(id),
        headers = mfHeaders
    )
    return response.json()

def start():
    print('Myfitness reservation script')
    print('Logging in')
    login_response = login()
    if 'access_token' in login_response:
        print('Login successful')
        mfHeaders['Authorization'] = 'Bearer ' + login_response['access_token']
    else:
        print('Login failed')
        print(login_response)
        exit(2) 

def get_weedkday(day_number = 1):
    today = datetime.now().date()
    weekday = today.weekday()
    days_until_next_week = weekday - 1

    next_week = today + timedelta(days=days_until_next_week)  
    return next_week + timedelta(days=day_number)

def check_class_exists( trainings ):
    if 'classes' in trainings and trainings['classes'] is not None:
        if len(trainings['classes']) > 0:
            training_id = trainings['classes'][0]['id']
            if training_id > 0:
                print('Found training with id: ' + str(training_id))
                return training_id
    return False


def check_existing_reservation(trainings):
    if trainings['classes'][0]['reservation'] is not None:
        if len(trainings['classes'][0]['reservation']) > 1:
            print('Training already reserved')
            return True
    return False

def process_reservation():
    for week_day in (1,3):
        when = get_weedkday(week_day)
        print('Searching for training on next ' + when.strftime('%A') + ' ' + when.strftime('%Y-%m-%d'))
        trainings = search_classes(when)
        training_id = check_class_exists(trainings)
        if check_existing_reservation(trainings):
            continue
        print('Reserving training')
        response = reserve(training_id)
        if 'reservation_id' in response:
            print('Reservation successful')
        else:
            print('Reservation failed')

if __name__ == '__main__':
    start()
    process_reservation()
