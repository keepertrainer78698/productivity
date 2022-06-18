import config
import requests
import json
import pandas as pd


class UploadFiles:
    def __init__(self, uploadcategory):
        if uploadcategory == 'Rechnungen':
            self.kdrive_url = config.kdrive_api + config.invoice_path
            self.airt_url = config.airtable_api + config.invoice_target
        elif uploadcategory == 'Goalkeeping':
            self.kdrive_url = config.kdrive_api + config.gk_path
            self.airt_url = config.airtable_api + config.gk_target
        else:
            'Not allowed Parameter, choose from "Rechnungen" or "Goalkeeping"'

        self.kdrive_headers = {'Content-Type': 'application/json', 'Authorization': f'Bearer ' + config.kdrive_key}
        self.airt_headers = {'Content-Type': 'application/json', 'Authorization': f'Bearer ' + config.airtable_key}


    def retrieve_new_files(self):
        # Get all kDrive Invoice Files

        self.kdrive_response = requests.get(url=self.kdrive_url, headers=self.kdrive_headers)

        self.kdrive_ids = []
        for i in self.kdrive_response.json()['data']:
            if i['type'] == 'file':
                self.kdrive_ids.append(i['id'])

        # Get List of Invoices already uploaded to Airtable
        airt_upload_view = self.airt_url + '?view=Upload'
        airt_response = requests.get(url=airt_upload_view, headers=self.airt_headers)

        airt_ids = []
        for k, v in airt_response.json().items():
            for i in v:
                airt_ids.append(i['fields']['kdrive_id'])

        upload_ids = []
        for i in self.kdrive_ids:
            if not i in airt_ids:
                upload_ids.append(i)

        return upload_ids
    
    def upload_to_airtable(self): 
        u = self.retrieve_new_files()
        result = []
        for i in self.kdrive_response.json()['data']:
            if i['id'] in u:
                output = {}
                output['kdrive_id'] = i['id']
                output['filename'] = i['name']
                fields = {'fields': output}
                result.append(fields)
        records = {'records': result}

        requests.post(url=self.airt_url, headers=self.airt_headers, data=json.dumps(records))
        for k, v in records.items():
            return str(len(v)) + " File Uploaded from kDrive to Airtable"