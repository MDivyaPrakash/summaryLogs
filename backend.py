## This function acts as a middle layer, interacting with the LLM and the database which stores the details.
## The summaryWriter class, contains the functions to get the response from the LLM, publish to the UI and API.
## The APP also uses a SQLite DB to temporarily store and update the values, for efficient retrievals.

import requests
from credentials import *
from datetime import datetime
import json
from db_Ops import *

db_obj = DatabaseClass()

class RequestError(Exception):
    pass
class summaryWriter():
    def __init__(self):
        self.dateResponse = {}
        self.question = ''
    
    def make_request(self, url):
        try:
            response = requests.get(url)
            response.raise_for_status()  
            return response.text  
        except requests.exceptions.HTTPError as e:
            raise RequestError(f"HTTP error occurred: {e}")
        except requests.exceptions.RequestException as e:
            raise RequestError(f"An error occurred: {e}")

    def get_call_logs(self,url_list):
        call_logs = []
        for urlVal in url_list:
            urlVal = urlVal.strip()
            call_log_date = urlVal.split("/")[-1].split("_")[2]
            try:
                call_log = self.make_request(urlVal)
            except RequestError as e:
                 raise Exception(f"Invalid URL Provided")
                
            call_log = "\n".join([item.strip() for item in call_log.split("\n") if len(item.strip()) and not item.strip()[0].isdigit()])
            call_logs.append((call_log_date, call_log))
        return call_logs
    
    def query(self, payload):
        json= {"inputs": payload, "parameters": {"max_new_tokens":512, "top_p":0.95, "temperature":0.75}}
        response = requests.post(API_URL, headers=HEADERS, json=json)
        return response.json()
        
    def get_response_wrapper(self,urls,question):
        self.question = question
        
        url_list = sorted([val.strip() for val in urls.split(',')]) if isinstance(urls,str) else sorted([val.strip() for val in urls])
        print(url_list)
        call_logs = self.get_call_logs(url_list)
        response = self.get_response(self.question, call_logs)
        print(response)

        start = response.find('{')
        end = response.rfind('}') + 1
        json_str = response[start:end]

        return self.load_details(json_str)

    def get_response(self, question, call_logs):
        summary = ''
        current_message = ''

        for call_log in call_logs:
            call_log_date, call_log_transcript = call_log
            print(call_log_date)
            current_message += f"[INST] {call_log_date} {call_log_transcript} [/INST]" 
        question = f"[INST]{question}[/INST]" 
        input = PROMPT + current_message + question
        output = self.query(input)
        summary= output[-1]['generated_text'].split("[/INST]")[-1]
        return summary
    
    def load_details(self,response):
        if not response:
            return
        print(response)
        self.dateResponse = json.loads(response)
        print(self.dateResponse)
        self.db_wrapper_function(self.dateResponse,'CREATE')
        return "Done",sorted(self.dateResponse.keys())
    
    def get_api_dict(self):
        apiDict = {}
        for key,values in self.dateResponse.items():
            for val in values:
                print(key,val["message"])
                if key not in apiDict:
                    apiDict[key] = [val["message"]]
                else:
                    apiDict[key].append(val["message"])
        return apiDict

    def db_wrapper_function(self,dict,action='CREATE'):
        now = datetime.now()
        dt_string = now.strftime("%Y-%m-%d %H:%M:%S")
        if action == 'CREATE':
            inputlist = []
            for key,values in dict.items():
                for val in values:
                    sample_dict = {
                        "date": key,
                        "message": val["message"],
                        "suggest_nd": val["tag"],
                        "approve_nd": True,
                        "update_dt": dt_string
                            }
                    inputlist.append(sample_dict)
            db_obj.create_db_details(inputlist)
        elif action == 'UPDATE':
            db_obj.update_table(dict)
        elif action == "GETALL":
            return db_obj.get_allvalues()
            