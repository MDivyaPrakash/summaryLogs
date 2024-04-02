import requests
import gradio as gr
from glob import glob
from datetime import datetime, timedelta
from llm import *
obj = summaryWriter()

def document_addition_screen(question,urls):
    output = obj.get_response_wrapper(urls,question,ui_nd=True,date=None)
    return output

def qa_display_screen(date):
    question ,output = obj.get_response_wrapper(None,None,ui_nd=True,date=date)
    return question, output

## Interface
qa_screen = gr.Interface(
    fn=qa_display_screen,
    inputs=[gr.Textbox(label="Date (YYYY-MM-DD)")],
    outputs=[gr.Textbox(label="Question"), gr.Textbox(label="Answer", lines = 10)],
    title="Question and Answers Display Screen",
    allow_flagging='auto'
)

document_screen = gr.Interface(
    fn=document_addition_screen,
    inputs=[gr.Textbox(label="Question"),
            gr.Textbox(label="URLs (separated by comma)")],
    outputs=[gr.Textbox(label="Answer", lines = 10)],
    title="Document Addition Screen",
    allow_flagging='manual'
)

with gr.Blocks(theme=gr.themes.Base()) as demo:
    gr.TabbedInterface([qa_screen, document_screen], ["QA Screen", "Document Screen"])
    gr.themes.Base()

if __name__ == "__main__":
    demo.queue().launch()
