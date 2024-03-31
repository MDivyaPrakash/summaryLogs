import requests
import gradio as gr
from glob import glob
#from llm import CustomLLM
from datetime import datetime, timedelta

## Function to get the response
# def get_response(urlVal,question):

#     CALL_LOGS = []
#     CALL_LOG_DATE = urlVal.split("/")[-1].split("_")[2]
#     CALL_LOG = requests.get(urlVal)
#     CALL_LOG = "\n".join([item.strip() for item in CALL_LOG.split("\n") if len(item.strip()) and not item.strip()[0].isdigit()])
#     CALL_LOGS.append((CALL_LOG_DATE, CALL_LOG))

#     m = CustomLLM()
#     return m.getResponse(question, CALL_LOGS),CALL_LOG_DATE

def display_screen(date,question):
    # Function to display the screen with the question and answers for a given date
    # data = get_daily_data(date)
    answers = "The API call answer"
    return f"Date: {date}\n\nQuestion:\n{question}\n\nAnswers:\n{answers}"

def document_addition_screen(question,urls):
    # Function to simulate the document addition screen
    urls = urls.split(',')
    newLine = '\n'
    newAns =  answers = []
    for i,urlVal in enumerate(urls):
        #answers.append(get_response(urlVal,question))
        answers.append(f"Date --> {i} {newLine} Answer")
    return "\n".join(answers)

## Interfaces 
qa_screen = gr.Interface(
    fn=display_screen,
    inputs=[gr.Textbox(label="Question"),
        gr.Textbox(label="Date (YYYY-MM-DD)")],
    outputs=[gr.Textbox(label="Answer", lines = 10)],
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
