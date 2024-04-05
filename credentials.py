API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2"
HEADERS = {"Authorization": "Bearer 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"}

INSTRUCTION = """You are professional meeting summarizer and your objective is to answer a question based on the summary of the call logs.
The call log for a given day will consists of multiple conversations of team members. Your job is to summarise the call logs, then understand the context and answer the question. Answers should be presented as bulleted lists of facts, using simple and clear language. 
Keep a track of your facts, to check whether the fact to the question has changed, with respect to all previous dates. The dates checked should be in the provided in the inputs, else ignore. 
You should suggest facts to be added, removed, or changed, based on previous days facts, by mentioning in the tag"""


EXAMPLE_ANSWER = """ Do not include any explanations or extra data, only provide a RFC8259 compliant JSON response following this format without deviation.
"
{
  "YYYY-MM-DD": [
    {"message": "Answer to the question in a clear and simple sentence", "tag": "REMOVED"},
    {"message": "Answer to the question in a clear and simple sentence", "tag": "ADDED"}
  ]
}
" """

PROMPT = '[INST]' + INSTRUCTION  + EXAMPLE_ANSWER  + '[/INST]'