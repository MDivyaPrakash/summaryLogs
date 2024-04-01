## This file contains the LLMS functionalities required
import requests
from credentials import *
from datetime import datetime
import json

class summaryWriter():
    def __init__(self):
        self.datalogs = {}
        self.dateResponse = {}
        self.question = ''
        
    def getResponseWrapper(self,urls,question,ui_nd=False, date=None):
        if self.question == '':
            self.question = question
        print(self.question)

        if not urls and not question and ui_nd and date:
             return self.serve_UI_1(date)

        url_list = sorted(urls.split(','))
        CALL_LOGS = []
        print(url_list)
        for urlVal in url_list:
            print(urlVal)
            CALL_LOG_DATE = urlVal.split("/")[-1].split("_")[2]
            CALL_LOG = requests.get(urlVal).text
            CALL_LOG = "\n".join([item.strip() for item in CALL_LOG.split("\n") if len(item.strip()) and not item.strip()[0].isdigit()])
            CALL_LOGS.append((CALL_LOG_DATE, CALL_LOG))

        response = self.getResponse(self.question, CALL_LOGS)
        if ui_nd:
            return self.serve_UI_2(response)
        else:
            return self.serveAPI(response)


    def getResponse(self, question, call_logs):
        summary = ''
        current_message = ''

        for call_log in call_logs:
            call_log_date, call_log_transcript = call_log
            print(call_log_date)
            current_message += f"[INST] {call_log_date} {call_log_transcript} {question} [/INST]"
        input = PROMPT + current_message
        output = self.query(input)
        summary= output[-1]['generated_text'].split("[/INST]")[-1]
        return summary
    
    def query(self, payload):
        json= {"inputs": payload, "parameters": {"max_new_tokens":256, "top_p":0.9, "temperature":0.7}}
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
    
    def serve_UI_2(self,response):
        if not response:
            return
        newResponse = response.split('```')[1].split('json')
        self.dateResponse = json.loads(newResponse[1])
        responseList = []
        for key,val in self.dateResponse.items():
                strVal = f"The facts at the end of the day {key} are below:" 
                responseList.append(strVal)
                responseList.append("\n".join(val))
        return "\n \n".join(responseList)
    
    def serveAPI(self,response):
        newResponse = response.split('```')[1].split('json')
        jsonResponse = json.loads(newResponse[1])
        return jsonResponse
