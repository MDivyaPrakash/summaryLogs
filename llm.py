## This file contains the LLMS functionalities required
import requests
from credentials import *
from datetime import datetime
import json

class summaryWriter():
    def __init__(self):
        self.dateResponse = {}
        self.question = ''
        
    def get_response_wrapper(self,urls,question,ui_nd=False, date=None,api_nd=False):
       
        if not date:
            self.question = question
        print(self.question)

        if not urls and not question and ui_nd and date:
             return self.serve_UI_1(date)
        
        url_list = sorted(urls.split(',')) if isinstance(urls, str) else sorted(urls)

        print(url_list)
        CALL_LOGS = []
        for urlVal in url_list:
            CALL_LOG_DATE = urlVal.split("/")[-1].split("_")[2]
            CALL_LOG = requests.get(urlVal).text
            CALL_LOG = "\n".join([item.strip() for item in CALL_LOG.split("\n") if len(item.strip()) and not item.strip()[0].isdigit()])
            CALL_LOGS.append((CALL_LOG_DATE, CALL_LOG))

        response = self.get_response(self.question, CALL_LOGS)

        return self.serve_UI_2(response,api_nd)

    def get_response(self, question, call_logs):
        summary = ''
        current_message = ''

        for call_log in call_logs:
            call_log_date, call_log_transcript = call_log
            print(call_log_date)
            current_message += f"[INST] {call_log_date} {call_log_transcript}  {question}[/INST]" 
        input = PROMPT + current_message
        output = self.query(input)
        summary= output[-1]['generated_text'].split("[/INST]")[-1]
        return summary
    
    def query(self, payload):
        json= {"inputs": payload, "parameters": {"max_new_tokens":256, "top_p":0.9, "temperature":0.75}}
        response = requests.post(API_URL, headers=HEADERS, json=json)
        return response.json()
    
    def serve_UI_1(self,date):
        responseList = []
        if date not in self.dateResponse.keys() :
            return self.question, "The given date is not in range"
        for key,val in self.dateResponse.items():
            if key == date:
                strVal = f"The facts at the end of the day {key} are below:" 
                responseList.append(strVal)
                responseList.append("\n".join(val))
        return self.question, "\n \n".join(responseList)
    
    def serve_UI_2(self,response,api_nd):
        if not response:
            return
        print(response)
        #newResponse = response.split('```')[1].split('json')[1]
        self.dateResponse = json.loads(response)
        if api_nd:
            return self.dateResponse
        
        responseList = []
        for key,val in self.dateResponse.items():
                strVal = f"The facts at the end of the day {key} are below:" 
                responseList.append(strVal)
                responseList.append("\n".join(val))
        return "\n \n".join(responseList)