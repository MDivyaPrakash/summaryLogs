API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2"
HEADERS = {"Authorization": "Bearer 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"}

INSTRUCTION = """As a professional meeting summarizer, your objective is to answer question based on the summary of a provided call log. 
The call log for a given day will consists of multiple conversations of team members. Your job is to summarise the logs, day by day, understand the context and answer the question. Make
If you find logs for multiple dates, you should you should check whether the answers to the same question has changed from the previous date.
    If the answer to the question has changed then you should include that new point. If not changed, just include the previous point.
The output should be in JSON Format. No need of any additional notes"""

EXAMPLE_CALL_LOG = """ For a sample log like this "'20240314' Alex: Let's choose our app's color scheme today. Jordan: I suggest blue for a calm feel. Casey: We need to make sure it's accessible to all users." '20240315' Alex: Let's change our app's color scheme today. Jordan: I suggest orange for a calm feel. Casey: We need to make sure it's accessible to all users. Lets wait on the color scheme, as it may take time" """

EXAMPLE_QUESTION = """ And for a question, like this " What product design decisions did the team make?" """

EXAMPLE_ANSWER = """ The example answer in json format would be "'{'2024-03-14': ['The team has decided to use blue for the color scheme of the app', 'The team has decided go with accessible design'] , '2024-03-15': ['The team has decided to use blue for the color scheme of the app', 'The team will go with accessible design']}. Use this only as a reference. """

PROMPT = '[INST]' + INSTRUCTION + '[/INST]' + EXAMPLE_CALL_LOG + EXAMPLE_QUESTION + EXAMPLE_ANSWER