import json
from config.environment import settings
import requests
import yaml
import os
import time
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
        # {
        #     "cin": "L92199MH1999PLC353754",
        #     "companyName": "INOX LEISURE LIMITED",
        #     "companyAddress": "5th Floor, Viraj Towers, Next to Andheri Flyover, Western Express Highway, Andheri (East) Mumbai City Maharashtra 400093"
        # },
        # {
        #     "cin": "U50404TG2020PTC141082",
        #     "companyName": "TRUE BLUE M2M PRIVATE LIMITED",
        #     "companyAddress": "GNR RV INSIGNIA, PLOT NO. 28 29 30 SILICON VALLEY LAYOUT, MADHAPUR Hyderabad Telangana 500034"
        # },
        # {
        #     "cin": "U51909TG2021PTC153617",
        #     "companyName": "HORNBILLE MACHINES AND RENTALS PRIVATE LIMITED",
        #     "companyAddress": "PLOT NO 28 29 30, GNR RV INSIGNIA SILICON VALLEY LAYOUT,MADHAPUR Hyderabad Telangana 500034"
        # },
        # {
        #     "cin": "U74999MH2015PTC266456",
        #     "companyName": "FLIPSPACES TECHNOLOGY LABS PRIVATE LIMITED",
        #     "companyAddress": "Unit Nos. 801B, 801C and 802A, 8th Floor, Eureka Tower,Mindspace , Link Road, Malad (West), Mumbai City Maharashtra 400064"
        # },
        # {
        #     "cin": "U45400MH2011PTC222160",
        #     "companyName": "GLOOB INTERIOR DESIGN PRIVATE LIMITED",
        #     "companyAddress": "Unit Nos. 801B, 801C and 802A, 8th Floor, Eureka Tower,Mindspace , Link Road, Malad (West), Mumbai City Maharashtra 400064"
        # }
    ]
    for order in orders :
        report(order['cin'], order['companyName'], order['companyAddress'])
        time.sleep(2)





