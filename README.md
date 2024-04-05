# The Summariser

## Summary:
This Summariser web-APP is designed to summarise the call logs and answer questions based on the questions asked by the user, along with a time navigation functionality.

## Key Functionalities:
### The UI: [Link](https://summary-logs-app.onrender.com/ui)
This app supports an extensive functionalities which is both user and developer friendly.
The App has two screens mainly, which allows the users to enter the documents through a URL and asks them for their approval on the facts.
Document Addition Screen: This screen allows the users to enter the documents through a URL and asks them for their approval on the facts.
Questions Answer Screen: This screen allows navigation through a date slider where the user can get the details based on the dates provided in the call logs.

### The API endpoint:
There are two major end points mainly :
1)  This for submitting the question and the URLs . The endpoint would be https://summary-logs-app.onrender.com/submit_question_and_documents
2)  This for retrieving the details submitted the question and the URLs . The endpoint would be https://summary-logs-app.onrender.com/get_question_and_facts

## Design and Approach:
### FastAPI
The main app is built using FastAPI framework, which supports both UI and the API endpoints. FastAPI was chosen becuase of the ease of incorporating multiple features.

### UI (Gradio)
The UI is built using Gradio. Gradio is an open-source Python library that enables to quickly create UIs for your machine learning models. This was again chosen because of its high compatability with the FastAPI components.

### Model (Mistral)
From Model Perspective, I chose to use the Hugging Face's Mistral_7B_Instruct_v0.2 [link](https://huggingface.co/mistralai/Mistral-7B-Instruct-v0.2) for getting the summaries of logs. The request with proper prompt is sent and the output is processed accroddingly

### Data Retrieval and Storage (SQLite)
The class summaryWriter, is responsible for receiving the urls and questions and interact with the LLM and finally store the values in a Database. The class contains multiple utilitarian modularised functions to enhance the functionality of the app. SQLite is chosen because of its light weighted nature, and incorporating a database could eventually help in scaling up.

### Tools and Technologies:
All scripts are in python language and its supported libraries have been used. 

## Demo of the implementation is as below:
![](others/demo.gif)

## Testing 
Development strategy was mainly using Test Driven Development, where use cases where predefine earlier.

Testing was done on test logs in the test_logs. With multiple questions, and to check whether the app handles all errors effectively.

### Note
Please ensure the URLS end with the format "call_log_20240314_104111.txt", where the last characters denotes the timestamp of the call log.

## Limitations and Challenges:
Even though Mistral is the best in its LLM category, it is prone to hallucinate , even after a tuning the prompt very finely.This can lead to errors, while processing the outputs. 

One other limitation is the payload. In this solution we use the inference APIs to access model, which gives us less control over the size of the message sent.

To mitigate the above two problems, one can implement a self hosted LLM and finetune it according to the use case. However,the solution comes with a cost.