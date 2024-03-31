## This file contains the LLMS functionalities required

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
import requests

INSTRUCTION = """You're a professional meeting summariser bot. Given a sample call log, your task is
to answer questions based on the summary of the call log. Read the call log below and answer the
question. The output should be a bulleted list."""

EXAMPLE_CALL_LOG = """Alex: Let's choose our app's color scheme today.
Jordan: I suggest blue for a calm feel.
Casey: We need to make sure it's accessible to all users."""

EXAMPLE_QUESTION = """What product design decisions did the team make?"""

EXAMPLE_ANSWER = """- The team will use blue for the color scheme of the app
- The team will make the app accessible to all users"""

def get_response(urlVal,question):

    CALL_LOGS = []
    CALL_LOG_DATE = urlVal.split("/")[-1].split("_")[2]
    CALL_LOG = requests.get(urlVal)
    CALL_LOG = "\n".join([item.strip() for item in CALL_LOG.split("\n") if len(item.strip()) and not item.strip()[0].isdigit()])
    CALL_LOGS.append((CALL_LOG_DATE, CALL_LOG))

    m = CustomLLM()
    return m.getResponse(question, CALL_LOGS),CALL_LOG_DATE


class CustomLLM:
    def __init__(self, model_id="mistralai/Mistral-7B-Instruct-v0.2"):
        self.model_id = model_id
        self.tokenizer = AutoTokenizer.from_pretrained(model_id)
        self.model = AutoModelForCausalLM.from_pretrained(model_id, torch_dtype=torch.float16, device_map="cuda")
        self.running_job_flag = False

    def __getStartMessage(self):
        USER_EXAMPLE_MESSAGE = "\n".join([INSTRUCTION, EXAMPLE_CALL_LOG, EXAMPLE_QUESTION])
        messages = [
            {"role": "user", "content": USER_EXAMPLE_MESSAGE},
            {"role": "assistant", "content": EXAMPLE_ANSWER}
        ]
        return messages

    def getResponse(self, question, call_logs):
        responses = []
        previous_call_log = ""
        for call_log in call_logs:
            messages = self.__getStartMessage()
            call_log_date, call_log_transcript = call_log
            USER_MESSAGE = INSTRUCTION + "\n" + previous_call_log + call_log_transcript + "\n" + question
            messages.append({"role": "user", "content": USER_MESSAGE})
            inputs = self.tokenizer.apply_chat_template(messages, return_tensors="pt").to("cuda")
            outputs = self.model.generate(inputs, max_new_tokens=100)
            output_text = self.tokenizer.decode(outputs[0], skip_special_tokens=True).split("[/INST]")[-1].strip()
            responses.append((call_log_date, output_text))
            print(output_text)
            previous_call_log += call_log_transcript + "\n"
        return responses