## This python file contains the basic FastAPI documentation of the webapp.
## This file can be run using the command uvicorn or a main funtion can be included to execute the same.

from fastapi import FastAPI, HTTPException, Response
from pydantic import BaseModel
from typing import List, Dict
from datetime import date

import gradio as gr
from llm import *
from webapp import demo

app = FastAPI()
app.mainResponse = {}
app.mainQuestion = ''

@app.get('/')
async def root():
    return 'The Web app is running at /ui. For GET questions use /get_question_and_facts and for POST use /submit_question_and_documents', 200

## The API Implementation using gradio
class questionDocPayload(BaseModel):
    question: str
    documents: List[str]
    autoApprove: bool

class summaryResponse(BaseModel):
    question: str
    factsByDay: Dict[date, List[str]]
    status: str

## End point to submit questions and documents
@app.post('/submit_question_and_documents')
def submit_docs(payload: questionDocPayload):

    obj = summaryWriter()
    question = payload.question
    urls = payload.documents
    responseAPI = obj.get_response_wrapper(urls,question,ui_nd=True,api_nd=True)
    app.mainQuestion = question
    app.mainResponse = responseAPI
    if responseAPI:
        return Response(content="Question and documents submitted successfully", status_code=200)
    else:
        raise HTTPException(status_code=404, detail="File not processed as desired")

## End point to handle the retrieval tasks
@app.get('/get_question_and_facts')
def get_docs():
    if app.mainResponse:
        dayLogDict = app.mainResponse
        return summaryResponse(question= app.mainQuestion, factsByDay=dayLogDict, status="done")
    else:
        return {"question": app.mainQuestion, "status": "processing"}


## The WEB UI Implementation using gradio
app = gr.mount_gradio_app(app, demo, path='/ui')