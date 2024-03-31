## This python file contains the basic FastAPI documentation

from fastapi import FastAPI
import gradio as gr

from webapp import demo

app = FastAPI()

@app.get('/')
async def root():
    return 'The Gradio app is running at /ui', 200

## End point to submit questions and documents
@app.post('/submit_question_and_documents')
async def root():
    return 'Reached the post endpoint', 200

## End point to handle the retrieval tasks
@app.post('/get_question_and_facts')
async def root():
    return 'Reached the get Qns endpoint', 200

app = gr.mount_gradio_app(app, demo, path='/ui')