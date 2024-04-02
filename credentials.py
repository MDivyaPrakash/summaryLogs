API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2"
HEADERS = {"Authorization": "Bearer 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"}

INSTRUCTION = """You are professional meeting summarizer and your objective is to answer a question based on the summary of the call log.
The call log for a given day will consists of multiple conversations of team members. Your job is to summarise the call logs, then understand the context and answer the question. The answers should be in a detailed sentences, presented as bulleted points.
Analyse the only call log and return the answer for the only the dates, in inputs. Keep a track of decisions, if changed make sure the answer is updated. No additional results required. Generate the output as JSON object. """

EXAMPLE_CALL_LOG = """ For a sample log like this "'YYYYMMDD' Alex: Let's choose our app's color scheme today. Jordan: I suggest blue for a calm feel. Casey: We need to make sure it's accessible to all users." '20990315' Alex: Let's change our app's color scheme today. Jordan: I suggest orange for a calm feel. Casey: We need to make sure it's accessible to all users. Lets wait on the color scheme, as it may take time" """

EXAMPLE_QUESTION = """ For a sample question, like this " What product design decisions did the team make?" """

EXAMPLE_ANSWER = """ The output JSON object should be formatted as "{"YYYY-MM-DD": ["Detailed answer to the question", "Detailed answer to the question"] , "YYYY-MM-DD": ["Detailed answer to the question", "Detailed answer to the question"]}" """

PROMPT = '[INST]' + INSTRUCTION  + EXAMPLE_ANSWER  + '[/INST]' #EXAMPLE_CALL_LOG + EXAMPLE_QUESTION + EXAMPLE_ANSWER +

# If any logs for previous dates are present, you should check whether the current answers to the same question has changed from the previous date. 
# If the answer to the question has changed then you should include that new point. If not changed, just include the previous point.