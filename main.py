## This python file contains the basic FastAPI documentation

from fastapi import FastAPI
import gradio as gr

from webapp import demo

app = FastAPI()

@app.get('/')
async def root():
    return 'My Gradio app is running at /gradio', 200

app = gr.mount_gradio_app(app, demo, path='/gradio')