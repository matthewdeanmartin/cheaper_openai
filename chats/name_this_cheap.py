import openai

from chats.client_utils import create_client

create_client()

def create_name(full_text:str):
    prompt = f"""Please give a short title to this document 
    ```
    {full_text}
    ```
    """

    temperature= 0.5
    max_tokens= 250
    args = {
        "model":"text-davinci-003",
        "prompt":prompt,
        "temperature":temperature,
        "max_tokens":max_tokens,
        "top_p":1,
        "frequency_penalty":0,
        "presence_penalty":0
    }

    response = openai.Completion.create(
        **args
    )

    print(response)
    return response["choices"][0]["text"]
