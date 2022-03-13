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
            loaded_memory['reports'].append(response_json['requestId']  + " " + CIN)
            yaml.dump(loaded_memory, memory)

        json.dump(response_json, response_file, indent=4)

if __name__ == '__main__':
    orders = [
        {
            "cin": "U40104MH2014PTC259254",
            "companyName": "ECHANDA URJA PRIVATE LIMITED",
            "companyAddress": "618, Maker Chambers V Nariman Point Mumbai Mumbai City Maharashtra 400021"
        },
        # {
        #     "cin": "U74999HR2018PTC075474",
        #     "companyName": "R.J. WAREHOUSING PRIVATE LIMITED",
        #     "companyAddress": "PLOT NO. 31P SECTOR-38 Gurgaon Haryana 122001"
        # },
        # {
        #     "cin": "U74999HR2018PTC076202",
        #     "companyName": "P.R.J. WAREHOUSING PRIVATE LIMITED",
        #     "companyAddress": "PLOT NO. 31P SECTOR-38 Gurgaon Haryana 122001"
        # }
    ]
    for order in orders :
        report(order['cin'], order['companyName'], order['companyAddress'])





