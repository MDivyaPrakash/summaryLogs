## This python file contains the basic FastAPI documentation of the webapp.
## This file can be run using the command uvicorn or a main funtion can be included to execute the same.

from fastapi import FastAPI, HTTPException, Response
from pydantic import BaseModel
from typing import List, Dict
from datetime import date

import gradio as gr
from backend import *
from userInterface import demo

app = FastAPI()
obj = summaryWriter()


@app.get("/")
async def root():
    return (
        "The Web app is running at /ui. For GET questions use /get_question_and_facts and for POST use /submit_question_and_documents",
        200,
    )


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
@app.post("/submit_question_and_documents")
def submit_docs(payload: questionDocPayload):

    question = payload.question
    urls = payload.documents
    try:
        _ = obj.get_response_wrapper(urls, question)
        return Response(
            content="Question and documents submitted successfully", status_code=200
        )
    except:
        raise HTTPException(status_code=400, detail="No Data to be displayed")


## End point to handle the retrieval tasks
@app.get("/get_question_and_facts")
def get_docs():
    dayLogDict = obj.get_api_dict()
    question = obj.question
    if dayLogDict:
        return summaryResponse(question=question, factsByDay=dayLogDict, status="done")
    else:
        if obj.question:
            return {"question": obj.question, "status": "processing"}
        else:
            raise HTTPException(status_code=404, detail="No Data to be displayed")


## The WEB UI Implementation using gradio
app = gr.mount_gradio_app(app, demo, path="/ui")
