import requests
import gradio as gr
from glob import glob
from datetime import datetime, timedelta
from llm import *
obj = summaryWriter()

def document_addition_screen(question,urls):
    output,dates = obj.get_response_wrapper(urls,question,ui_nd=True,date=None)
    return output,'\n'.join(dates)

def qa_display_screen(date):
    question ,output = obj.get_response_wrapper(None,None,ui_nd=True,date=date)
    return question, output

def populate_slider(dates):
    newDates = dates.split('\n')
    new_slider = gr.Slider(value=1, minimum=1, maximum=len(newDates), step=1)
    return new_slider,newDates[0]

def populate_text_box(slider_value,dates):
    newDates = dates.split('\n')
    return newDates[slider_value-1]

with gr.Blocks() as demo:
        
        gr.Markdown( """  # The Summariser  """)

        with gr.Tab("Document Addition Screen"):
            with gr.Column():
                qn_input = gr.Textbox(label="Question")
                url_input = gr.Textbox(label="URLs (separated by comma)")
                doc_submit = gr.Button("Submit")
            text_output = gr.Textbox(label="Answer", lines = 10)
            with gr.Accordion("Submitted Dates", open=False):
                date_text = gr.Textbox(label="Dates",lines=5)
        doc_submit.click(document_addition_screen, inputs=[qn_input,url_input], outputs=[text_output,date_text])

        with gr.Tab("Question and Answers Display Screen"):
            with gr.Column():
                with gr.Row():
                    data_slider = gr.Slider(label="Time Slider")
                    date_text2 = gr.Textbox(label="Date") 
                date_submit = gr.Button("Submit")
            filter_question = gr.Textbox(label="Question")
            filer_output = gr.Textbox(label="Answer", lines = 10)
        
        date_text.change(populate_slider,[date_text],[data_slider,date_text2])
        data_slider.change(populate_text_box,[data_slider,date_text],[date_text2])
        date_submit.click(qa_display_screen, inputs=date_text2, outputs=[filter_question,filer_output])

if __name__ == "__main__":
    demo.queue().launch()
