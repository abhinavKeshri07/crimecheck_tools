import json
from config.environment import settings
import requests
import yaml
import os
import time
import urllib.parse
api_key = settings.crimecheck_api_key



def request_report(query: dict) -> str:
    headers = {
        'content-type': 'application/x-www-form-urlencoded',
    }

    data = [
        # ('searchTearm', json.dumps(query)),
        ('name', query['name']),
        ('fatherName', query['fatherName']),
        ('address', query['address']),
        ('panNumber', query['panNumber']),
        ('apiKey', api_key),
        ('callbackUrl', settings.callback_url) # this field is necessary for making callback
    ]
    response = requests.post('https://crime.getupforchange.com/api/v3/addReport', headers=headers, data=data,auth=(api_key, ''))
    print(response.status_code)
    return response.text


def report_individual(query: dict):
    with open(f'{settings.base_data_path}/response.json', 'w',encoding='utf-8') as response_file:
        response_json = json.loads(request_report(query=query))
        loaded_memory = {}
        memory_file_name = f'{settings.base_data_path}/memory_individual.yml'
        if(not os.path.isfile(memory_file_name)):
            memory_file = open(memory_file_name, 'w')
            memory_file.close()
        with open(f'{settings.base_data_path}/memory_individual.yml', 'r') as memory:
            memory_from_file = yaml.safe_load(memory)
            if memory_from_file:
                loaded_memory.update(memory_from_file)
            if( not 'reports' in loaded_memory.keys()):
                loaded_memory['reports'] = []

        with open(f'{settings.base_data_path}/memory_individual.yml', 'w') as memory:
            if "requestId" in response_json.keys():
                loaded_memory['reports'].append(response_json['requestId']  + " " + query['name'])
                yaml.dump(loaded_memory, memory)
            else:
                print("request failed " + str(response_json) )

        json.dump(response_json, response_file, indent=4)

if __name__ == '__main__':
    orders = [
        {
            "name": "Rajesh Verma",
            "fatherName": "SURESHCHANDRA VERMA",
            "address": "1504 Elecia Bldg, Dosti Imperia, Godhbandar Road,Manpada, Thane West, opp R mall, Sandozbaugh, Maharashtra 400607",
            "panNumber": "ABQPV4771N"
        },
        {
            "name": "FIROZ KARUMANNIL",
            "fatherName": "ABDULLAKUTTY",
            "address": "FLT NO 713, AL NAKHEEL, DUBAI 030930",
            "panNumber": "ASHPK1802B"
        },
        {
            "name": "VYOMESH RAMESHCHANDRAN THAKKER",
            "fatherName": "RAMESHCHANDRA THAKKER",
            "address": "709, Burj Al Nahda Building, Al Nahda First, DUBAI 78029",
            "panNumber": "AAIPV3121D"
        },
        {
            "name": "ZAMEER AKHTAR",
            "fatherName": "ZAMEER AHMED SHARIFF",
            "address": "Flat no 113, Zakhir Towers 1 ,Near Al Twaun Mall , PO Box UAE, Sharjah 0000",
            "panNumber":"CRXPA6044A"
        }
    ]
    for order in orders :
        report_individual(query=order)
        time.sleep(2)





