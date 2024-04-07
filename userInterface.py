## This file has the user interace implementation.

import requests
import gradio as gr
from glob import glob
from datetime import datetime, timedelta
from backend import *

obj = summaryWriter()


def update_values_function(*argv):
    newOutput = obj.db_wrapper_function(None, "GETALL")
    now = datetime.now()
    dt_string = now.strftime("%Y-%m-%d %H:%M:%S")
    valList = []
    for i, val in enumerate(newOutput):
        innerList = []
        innerList.append(val["date"])
        innerList.append(val["message"])
        if str(argv[i]) == "Approve":
            innerList.append(True)
        else:
            innerList.append(False)
        innerList.append(dt_string)
        valList.append(innerList)
    obj.db_wrapper_function(valList, "UPDATE")
    gr.Info("Approval List Processed")
    return None


def getall_function():
    output_db = obj.db_wrapper_function(None, "GETALL")
    print("-->")
    visible = []
    for i, val in enumerate(output_db):
        keyval = f'For date {val["date"]} fact is: {val["message"]}'
        message_val = f" Choose to Approve or Deny "
        new_text = gr.Radio(
            ["Approve", "Deny"],
            value="Approve",
            label=keyval,
            info=message_val,
            visible=True,
        )
        visible.append(new_text)
    for j in range(i + 1, 100):
        dummyNode = gr.Radio(visible=False)
        visible.append(dummyNode)
    return visible


def document_addition_screen(question, urls):
    _, date = obj.get_response_wrapper(urls, question)
    # opList = getall_function()
    output_db = obj.db_wrapper_function(None, "GETALL")
    visible = []
    for i, val in enumerate(output_db):
        keyval = f'For date {val["date"]} fact is: {val["message"]}'
        message_val = f" Choose to Approve or Deny "
        new_text = gr.Radio(
            ["Approve", "Deny"],
            value="Approve",
            label=keyval,
            info=message_val,
            visible=True,
        )
        visible.append(new_text)
    for j in range(i + 1, 100):
        dummyNode = gr.Radio(visible=False)
        visible.append(dummyNode)
    date = "\n".join(date)
    visible.append(gr.Textbox(value=date))
    return visible


def qa_display_screen(date):
    question = obj.question
    output_db = obj.db_wrapper_function(None, "GETALL")
    oplist = []
    now = datetime.now()
    current_dt = now.strftime("%Y-%m-%d %H:%M:%S")
    FMT = "%Y-%m-%d %H:%M:%S"
    for val in output_db:
        update_dt = val["update_dt"]
        tdelta = datetime.strptime(current_dt, FMT) - datetime.strptime(update_dt, FMT)
        val["suggest_nd"] = "ADDED" if not val["suggest_nd"] else val["suggest_nd"]
        if val["date"] == date and val["approve_nd"] and tdelta < timedelta(hours=24):
            oplist.append((val["message"], val["suggest_nd"]))
    if not oplist:
        oplist.append(
            ("No matching approved facts found for the given date", "NO_DATA")
        )
    return question, oplist


def populate_slider(dates):
    newDates = dates.split("\n")
    new_slider = gr.Slider(value=1, minimum=1, maximum=len(newDates), step=1)
    return new_slider, newDates[0]


def populate_text_box(slider_value, dates):
    newDates = dates.split("\n")
    return newDates[slider_value - 1]


op_list = []

with gr.Blocks(theme=gr.themes.Default()) as demo:

    gr.Markdown("""  # The Summariser  """)
    with gr.Tab("Document Addition Screen"):
        with gr.Column():
            qn_input = gr.Textbox(label="Question")
            url_input = gr.Textbox(label="URLs (separated by comma)")
        text_box = gr.Textbox(visible=False)
        doc_submit = gr.Button("Document Submit")

        for i in range(100):
            dummyNode = gr.Radio(visible=False)
            op_list.append(dummyNode)
        approval_submit = gr.Button("Approve")
        with gr.Accordion("Submitted Dates", open=False):
            date_text = gr.Textbox(label="Dates")
            op_list.append(date_text)
        doc_submit.click(
            document_addition_screen, inputs=[qn_input, url_input], outputs=op_list
        )
        approval_submit.click(update_values_function, op_list, None)

    with gr.Tab("Question and Answers Display Screen"):
        with gr.Column():
            with gr.Row():
                data_slider = gr.Slider(label="Time Slider")
                date_text2 = gr.Textbox(label="Date")
            date_submit = gr.Button("Submit")
        filter_question = gr.Textbox(label="Question")
        filer_output = gr.HighlightedText(
            label="Facts by Choice",
            adjacent_separator="",
            show_legend=True,
            color_map={"REMOVED": "red", "ADDED": "green", "NO_DATA": "blue"},
        )
    date_text.change(populate_slider, [date_text], [data_slider, date_text2])
    data_slider.change(populate_text_box, [data_slider, date_text], [date_text2])
    date_submit.click(
        qa_display_screen, inputs=date_text2, outputs=[filter_question, filer_output]
    )

if __name__ == "__main__":
    demo.launch()
