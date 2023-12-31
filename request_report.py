import json
from config.environment import settings
import requests
import yaml
import os
import time
import urllib.parse
api_key = settings.crimecheck_api_key



def request_report(cin: str, companyName: str, compAddress: str, directors: list = None) -> str:
    headers = {
        'content-type': 'application/x-www-form-urlencoded',
    }

    """
    Possible values of companyType
    ------------------------------
    Private Limited => "PvtLtd"
    Public Limited => "Limited"
    Limited Liability Company => "LLC"
    Limited Liability Partnership => "LLP"
    Registered Firm => "RegFirm"
    Unregistered Firm => "UnregFirm"
    Proprietary => "Proprietary"
    """
    # data = [
    #     ('companyName', input("enter company name -> ")),
    #     ('cinNumber', input('cin number -> ')),
    #     ('callbackUrl', settings.callback_url)
    # ]

    data = [
        ('companyName', companyName),
        ('cinNumber', cin),
        ('callbackUrl',settings.callback_url),
        ('companyAddress', compAddress),
        ('apiKey', api_key)
    ]
    if directors:
        data.append(('directors', json.dumps(directors)))
    # url_encoded_query = "searchTerm=" + urllib.parse.quote_plus(json.dumps(data2))+"&page=1&resultsPerPage=100&matchFlag=true&matchingCriteria=true&callbackUrl=http://api.altinfo.com/api/callback/crimecheck"
    response = requests.post('https://crime.getupforchange.com/api/v3/addReport', headers=headers, data=data,auth=(api_key, ''))
    print(response.status_code)
    print(response.text)
    return response.text


def report(cin:str, companyName: str, companyAddress: str, directors: list = None):
    with open(f'{settings.base_data_path}/response.json', 'w',encoding='utf-8') as response_file:
        response_json = json.loads(request_report(cin=cin,
                                                  companyName=companyName,
                                                  compAddress=companyAddress,
                                                  directors=directors))
        loaded_memory = {}
        memory_file_name = f'{settings.base_data_path}/memory.yml'
        if(not os.path.isfile(memory_file_name)):
            memory_file = open(memory_file_name, 'w')
            memory_file.close()
        with open(f'{settings.base_data_path}/memory.yml', 'r') as memory:
            memory_from_file = yaml.safe_load(memory)
            if memory_from_file:
                loaded_memory.update(memory_from_file)
            if( not 'reports' in loaded_memory.keys()):
                loaded_memory['reports'] = []

        with open(f'{settings.base_data_path}/memory.yml', 'w') as memory:
            if "requestId" in response_json.keys():
                loaded_memory['reports'].append(response_json['requestId']  + " " + cin)
                yaml.dump(loaded_memory, memory)
            else:
                print("request failed " + str(response_json) )

        json.dump(response_json, response_file, indent=2)

if __name__ == '__main__':
    orders = [
        # {
        #     "cin": "U74899DL1983PTC017237",
        #     "companyName": "VIMAL PLAST (INDIA) PRIVATE LIMITED",
        #     "companyAddress": "PROPERTY NO. E-21, FIRST FLOOR, NARAINA VIHAR, NEW DELHI South West Delhi 110028",
        #     "directors": [
        #         {
        #             "name" : "Harish Batra",
        #             "fatherName": "Khushi Ram Batra",
        #             "dob": "",
        #             "address": "F-50 D, RADHE MOHAN DRIVE BANDH ROAD, VILLAGE- JAUNPUR, JONAPUR 110047",
        #             "panNumber": "AAGPB7869J"
        #         },
        #         {
        #             "name": "Saurabh Batra",
        #             "fatherName": "Harish Batra",
        #             "dob": "",
        #             "address": "F-50 D, RADHE MOHAN DRIVE BANDH ROAD, VILLAGE- JAUNPUR, JONAPUR 110047",
        #             "panNumber": "AFAPB4359Q"
        #         },
        #         {
        #             "name": "Anju Batra",
        #             "fatherName": "Sada Nand Grover",
        #             "dob": "",
        #             "address": "F-50 D, RADHE MOHAN DRIVE BANDH ROAD, VILLAGE- JAUNPUR, JONAPUR 110047",
        #             "panNumber": "AHNPB0173B"
        #         },
        #         {
        #             "name": "Sahil Batra",
        #             "fatherName": "Harish Batra",
        #             "dob": "",
        #             "address": "F-50 D, RADHE MOHAN DRIVE BANDH ROAD, VILLAGE- JAUNPUR, JONAPUR 110047",
        #             "panNumber": "AHNPB0146J"
        #         }
        #     ]
        # },
        {
            "cin": "U72300DL2006PTC154805",
            "companyName": "ELCOM SYSTEMS PRIVATE LIMITED",
            "companyAddress": "M-41/4&5 SPEED BIRD HOUSE CONNAUGHT CIRCUS NEW DELHI Central Delhi 110001"
        },
    ]
    for order in orders :
        report(cin=order['cin'],
               companyName=order['companyName'],
               companyAddress=order['companyAddress'],
               directors=order['directors'] if 'directors' in order.keys() else None)
        time.sleep(2)





