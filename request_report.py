import json
from config.environment import settings
import requests
import yaml
import os
import urllib.parse
api_key = settings.crimecheck_api_key



def request_report(cin: str, companyName: str, compAddress: str):
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
        ('companyAddress', compAddress)
    ]


    # url_encoded_query = "searchTerm=" + urllib.parse.quote_plus(json.dumps(data2))+"&page=1&resultsPerPage=100&matchFlag=true&matchingCriteria=true&callbackUrl=http://api.altinfo.com/api/callback/crimecheck"
    response = requests.post('https://crime.getupforchange.com/api/v3/addReport', headers=headers, data=data,auth=(api_key, ''))
    print(response.status_code)
    return response.text


def report(CIN:str, companyName: str, companyAddress: str):
    with open(f'{settings.base_data_path}/response.json', 'w',encoding='utf-8') as response_file:
        response_json = json.loads(request_report(cin=CIN, companyName=companyName, compAddress=companyAddress))
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
                loaded_memory['reports'].append(response_json['requestId']  + " " + CIN)
                yaml.dump(loaded_memory, memory)
            else:
                print("request failed " + str(response_json) )

        json.dump(response_json, response_file, indent=4)

if __name__ == '__main__':
    orders = [
        {
            "cin": "AAQ-1061",
            "companyName": "IIPI GLOBAL LLP",
            "companyAddress": "B18 DLF PHASE I Faridabad Haryana 121003"
        },
        # {
        #     "cin": "U36990RJ2022PTC079282",
        #     "companyName": "ATSPACE INTERNATIONAL PRIVATE LIMITED",
        #     "companyAddress": "B-165 KAMAL NEHRU NAGAR EXTENSION II JODHPUR Rajasthan 342008"
        # },
        # {
        #     "cin": "U51909DL2021PTC379420",
        #     "companyName": "GENIEMODE GLOBAL PRIVATE LIMITED",
        #     "companyAddress": "C-2/83, Himalayan CGHS Sec-22,Plot No.10 Dwarka, Opposite Police Station, Delhi New Delhi 110077"
        # },
        # {
        #     "cin": "U72200TG2005PTC047831",
        #     "companyName": "DATUM CYBERTECH INDIA PRIVATE LIMITED",
        #     "companyAddress": "Flat No. 203 to 206, 1st Floor, KTC illumination, Image Hospital Lane, Madhapur. Hyderabad Telangana 500081"
        # }
    ]
    for order in orders :
        report(order['cin'], order['companyName'], order['companyAddress'])





