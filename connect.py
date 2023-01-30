import requests
from dotenv import load_dotenv
import os
from datetime import datetime, timedelta
import json

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
    loginResponse = login()
    if 'access_token' in loginResponse:
        print('Login successful')
        mfHeaders['Authorization'] = 'Bearer ' + loginResponse['access_token']
    else:
        print('Login failed')
        print(loginResponse)
        exit(2) 

def get_weedkday(day_number = 1):
    today = datetime.now().date()
    next_week = today + timedelta(weeks=1)  
    return next_week + timedelta((day_number - next_week.weekday()) % 7)

def process_reservation():
    for week_day in (1,3):
        when = get_weedkday(week_day)
        print('Searching for training on next ' + when.strftime('%A') + ' ' + when.strftime('%Y-%m-%d'))
        trainings = search_classes(when)
        if 'classes' in trainings and len(trainings['classes']) > 0:
                trainingId = trainings['classes'][0]['id']
                if trainingId > 0:
                    print('Found training with id: ' + str(trainingId))
                    if len(trainings['classes'][0]['reservation']) > 1:
                        print('Training already reserved')
                    else:
                        print('Reserving training')
                        response = reserve(trainingId)
                        if 'reservation_id' in response:
                            print('Reservation successful')
                        else:
                            print('Reservation failed')

if __name__ == '__main__':
    start()
    process_reservation()
