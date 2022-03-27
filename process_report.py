import json
import traceback

from config.environment import settings
import requests
from aws.download_json import download_all_jsons
import yaml
import os
import re
ILLEGAL_CHARACTERS_RE = re.compile(r'[\000-\010]|[\013-\014]|[\016-\037]|[\x00-\x1f\x7f-\x9f]|[\uffff]')
import re
import openpyxl
from openpyxl import  Workbook




def process(reportId:str, cin: str):
    # loaded_data = json.loads(f'{settings.base_data_path}chrimecheck/1643556523684.json')
    # print(loaded_data)
    json_path = f'{settings.base_data_path}/chrimecheck/{reportId}.json'
    if not os.path.exists(json_path):
        print(f"JSON not available for {reportId} {cin}. Wait for crimecheck to hit Callback URL.")
        return

    if(not os.path.isdir(f'{settings.base_data_path}/output/{cin}_{reportId}')):
    # if (True):
        base_path = f'{settings.base_data_path}/output/{cin}_{reportId}'
        caseDetailDir = f'{base_path}/caseDetail'
        judgement = f'{base_path}/judgement'
        caseFlow  = f'{base_path}/caseFlow'
        if( not os.path.exists(base_path)):
            os.makedirs(base_path)
        if(not os.path.exists(caseDetailDir)):
            os.makedirs(caseDetailDir)
        if(not os.path.exists(judgement)):
            os.makedirs(judgement)
        if(not os.path.exists(caseFlow)):
            os.makedirs(caseFlow)


        with open(json_path) as report:
            load = json.load(report)
            wb= Workbook()

            ws_data = wb.active
            ws_data['A1'] = "CompanyCIN"
            ws_data['B1'] = cin

            ws_data['A2'] = "Number of Cases: "
            ws_data['B2'] = load['numberOfCases']

            ws_data['A3'] = "Case Details"

            ws_data['A4'] = "Serial No"
            ws_data['B4'] = "Petitionar"
            ws_data["C4"] = "Respondent"
            ws_data["D4"] = "Case Type"
            ws_data["E4"] = "Hearing Date"
            ws_data["F4"] = "Court Number and Judge"
            ws_data["G4"] = "Court Name"
            ws_data["H4"] = "State"
            ws_data["I4"] = "District"
            ws_data["J4"] = "Petitionar Address"
            ws_data["K4"] = "Respondent Address"
            ws_data["L4"] = "Case Number"
            ws_data['M4'] = "Case Year"
            ws_data["N4"] = "Under Act"
            ws_data["O4"] = "Section"
            ws_data["P4"] = "Under Section"
            ws_data['Q4'] = "Case Status"
            # fetch JudgementLink
            ws_data["R4"] = "FIR Link"
            ws_data["S4"] = "Case Link"
            ws_data["T4"] = "Case Type"
            ws_data["U4"] = "Nature of Disposal"
            ws_data["V4"] = "Risk Type"
            ws_data["W4"] = "Risk Summary"
            ws_data["X4"] = "Severity"
            ws_data["Y4"] = "Judgement Summary"
            ws_data["Z4"] = "Case Registeration Date"
            ws_data["AA4"] = "Registration Number"
            ws_data["AB4"] = "Filing Date"
            ws_data["AC4"] = "Filing Number"
            ws_data["AD4"] = "Court Type"
            ws_data["AE4"] = "Matching Address"
            # fetch caseDetailLink
            row = 5
            if int(load['numberOfCases']) > 0:
                for caseDetail in load['caseDetails']:
                    ws_data[f'A{row}'] = caseDetail['slNo']
                    ws_data[f'B{row}'] = caseDetail['petitioner']
                    ws_data[f'C{row}'] = ILLEGAL_CHARACTERS_RE.sub("", caseDetail['respondent'])
                    # ws_data[f"C{row}"] = caseDetail['respondent'].encode("ascii",errors="ignore")
                    ws_data[f"D{row}"] = caseDetail['caseTypeName']
                    ws_data[f"E{row}"] = caseDetail['hearingDate']
                    ws_data[f"F{row}"] = caseDetail['courtNumberAndJudge']
                    ws_data[f"G{row}"] = caseDetail['courtName']
                    ws_data[f"H{row}"] = caseDetail['state']
                    ws_data[f"I{row}"] = caseDetail['district']
                    ws_data[f"J{row}"] = caseDetail['petitionerAddress']
                    ws_data[f"K{row}"] = caseDetail['respondentAddress']
                    ws_data[f"L{row}"] = caseDetail['caseNumber']
                    ws_data[f'M{row}'] = caseDetail['caseYear']
                    ws_data[f"N{row}"] = caseDetail['underAct']
                    ws_data[f"O{row}"] = caseDetail['section']
                    ws_data[f"P{row}"] = caseDetail['underSection']
                    ws_data[f'Q{row}'] = caseDetail['caseStatus']

                    try:
                        judgementLink = caseDetail['judgementLink']
                        r = requests.get(judgementLink, allow_redirects=True)
                        open(f'{judgement}/{caseDetail["slNo"]}.pdf', "wb").write(r.content)
                    except Exception as e:
                        print(e)
                        pass

                    caseFlows = caseDetail['caseFlow']
                    if len(caseFlows) > 0:
                        caseflow_dir = f'{caseFlow}/{caseDetail["slNo"]}'
                        if (not os.path.exists(caseflow_dir)):
                            os.makedirs(caseflow_dir)
                        caseflow_file_no = 1
                        for caseflow in caseFlows:
                            orderLink = caseflow['orderLink']
                            try:
                                r = requests.get(orderLink, allow_redirects=True)
                                open(f'{caseflow_dir}/{caseflow_file_no}_{caseflow["gfc_OrderType"]}_{caseflow["orderDate"]}.pdf', "wb").write(r.content)
                            except Exception as e:
                                print(e)
                                pass
                            print(caseflow)
                            caseflow_file_no = caseflow_file_no + 1
                        pass

                    ws_data[f"R{row}"] = caseDetail['firLink']
                    ws_data[f"S{row}"] = caseDetail['caseLink']
                    ws_data[f"T{row}"] = caseDetail['caseType']
                    ws_data[f"U{row}"] = caseDetail['natureOfDisposal']
                    ws_data[f"V{row}"] = caseDetail['riskType']
                    ws_data[f"W{row}"] = caseDetail['riskSummary']
                    ws_data[f"X{row}"] = caseDetail['severity']
                    ws_data[f"Y{row}"] = caseDetail['judgementSummary']
                    ws_data[f"Z{row}"] = caseDetail['caseRegDate']
                    ws_data[f"AA{row}"] = caseDetail['regNumber']
                    ws_data[f"AB{row}"] = caseDetail['filingDate']
                    ws_data[f"AC{row}"] = caseDetail['filingNumber']
                    ws_data[f"AD{row}"] = caseDetail['courtType']
                    ws_data[f"AE{row}"] = caseDetail['matchingAddress']

                    try:

                        caseDetailLink = caseDetail['caseDetailsLink']
                        r = requests.post("http://127.0.0.1:8050/render.html",json={"url": caseDetailLink})
                        open(f'{caseDetailDir}/{caseDetail["slNo"]}.html', "wb").write(r.content)
                    except Exception as e:
                        traceback.print_exec()
                        pass

                    row = row +1

            ws_data[f'A{row}'] = "Disclaimer"
            ws_data[f'B{row}'] = "This report contains information about the Subject in question which has been compiled using data collected from the public domain. This report was generated from a database which contains 21 Crore crime records from all courts, Tribunals & Defaulters List across India. To that effect, the correctness, accuracy, and completeness of this report are directly related to the data available online in the public domain at the time of report generation. This report is not to be treated as an advice in any form and the users are advised to carry out necessary due diligence/ verification or to seek proper professional advice as may be necessary on the information provided in this report before taking any decision."


            wb.save(f'{base_path}/test.xlsx')
    print("done", reportId, cin)
    pass

# /Volumes/samsung_usb/code_data/chrimecheck/1647849476843.json


if __name__ == "__main__":
    download_all_jsons()
    with open(f'{settings.base_data_path}/memory.yml', 'r') as memory:
        loaded_memory = yaml.safe_load(memory)
        for entry in loaded_memory['reports']:
            report_id, cin = entry.split(' ')
            print(report_id, cin)
            process(report_id, cin)
            # process("1647849476843", "U45400MH2011PTC222160")











