from argparse import ArgumentParser
import os
import csv
import requests
from requests.models import PreparedRequest
import json

APP_ID_KEY = 'SENDBIRD_APPLICATION_ID'
TOKEN_KEY = 'SENDBIRD_TOKEN'
ENV_FILE = '.env'

USER_ID = 'user_id'
NICKNAME = 'nickname'
PROFILE_URL = 'profile_url'

RANDOM_USERS_ENDPOINT = 'https://randomuser.me/api/'
# Sendbird endpoint is calculated by the getEndpoint() function b/c it depends on the application id

def configFile():
    # Append to existing
    f = open(ENV_FILE, 'a')
    if f is None:
        # Oop - create a new one!
        f = open(ENV_FILE, 'w+')
    return f


def newApplicationId():
    print(f'Sendbird application id:')
    aid = input()
    # TODO: Validation
    if aid is None or aid == '':
        print(f'Invalid application id')
        return newApplicationId()
    f = configFile()
    f.write(f"{APP_ID_KEY}='{aid}'\n")
    f.close()
    return aid


def newToken():
    print(f'Sendbird primary or secondary token:')
    token = input()
    # TODO: Validation
    if token is None:
        print(f'Invalid token')
        return newToken()
    f = configFile()
    f.write(f"{TOKEN_KEY}='{token}'\n")
    f.close()
    return token


def getEnvValue(target_key):
    if os.path.exists(ENV_FILE) == False:
        return None
    with open(ENV_FILE) as f:
        for line in f:
            if line.startswith('#') or not line.strip():
                continue
            key, value = line.strip().split('=', 1)
            if target_key != key:
                continue
            # Strip those quotes
            value = value[1:-1]
            return value


def getApplicationId():
    aid = getEnvValue(APP_ID_KEY)
    if aid is None:
        aid = newApplicationId()
    return aid


def getToken():
    token = getEnvValue(TOKEN_KEY)
    if token is None:
        token = newToken()
    return token


def specifySourceCSV():
    print('Enter a .csv file with user data to upload:')
    result = input()
    return result


def getEndpoint(app_id):
    return f'https://api-{app_id}.sendbird.com/v3'


def getHeaders(token):
    return {
        'Content-Type': 'application/json',
        'Api-Token': token
    }

def getRandomUsers(number, nationalities):
    params = {'results': number, 'nat': nationalities}
    r = PreparedRequest()
    r.prepare_url(RANDOM_USERS_ENDPOINT, params)
    response = requests.get(r.url, headers={'Content-Type': 'application/json'})
    json = response.json()
    if json is None:
        print(f'Random user service request: {response.status_code}:{response.message}')
        return None
    return json


def convertRandomUserToSendbirdUserData(data):
    fn = data['name']['first']
    ln = data['name']['last']

    result = {}
    result[USER_ID] = data['login']['uuid']
    result[NICKNAME] = f'{fn} {ln}'
    result[PROFILE_URL] = data['picture']['medium']
    return result

def createUser(data, app_id, token):
    if data[USER_ID] is None:
        print(f'Missing {USER_ID} from {data}')
        return
    if data[NICKNAME] is None:
        print(f'Missing {NICKNAME} from {data}')
        return
    if data[PROFILE_URL] is None:
        print(f'Missing {PROFILE_URL} from {data}')
        return
    endpoint = getEndpoint(app_id) + '/users'
    headers = getHeaders(token)
    # TODO: Validate data
    print(
        f'Sending create user request for user with nickname: {data[NICKNAME]}...')
    r = requests.post(url=endpoint, headers=headers, data=json.dumps(data))
    print(f'Response code: {r.status_code}: {r.reason}')


def main(count, nationalities):
    print()
    aid = getApplicationId()
    token = getToken()

    users = getRandomUsers(count, nationalities)['results']
    for user in users:
        sendbird_user_data = convertRandomUserToSendbirdUserData(user)
        createUser(sendbird_user_data, aid, token)

    return True


# Parse Args
parser = ArgumentParser()
parser.add_argument("-c", "--count",
                    dest="count", default=2,
                    help="Total count of random users to generate")
parser.add_argument("-n", "--nationalities",
                    dest="nationalities", default="US",
                    help="Nationalities of random users to generate. Options: AU, BR, CA, CH, DE, DK, ES, FI, FR, GB, IE, IR, NO, NL, NZ, TR, US. comma seperated option multiple options acceptable")

args = parser.parse_args()

# Run baby run
main(args.count, args.nationalities)
