import openai

from chats.client_utils import create_client
from chats.io_utils import dump_response, read_prompt
from chats.name_this_cheap import create_name
import toml
config = toml.load("../config.toml")

# get output folder from config file
output_folder = config["output_folder"]

create_client()

prompt = read_prompt(output_folder)
is_code= False

for temperature in [0.9,]:
    for max_tokens in [250,]:
        args = {
            "model":"text-davinci-003",
            "prompt":prompt,
            "temperature":temperature,
            "max_tokens":max_tokens,
            "top_p":1,
            "frequency_penalty":0,
            "presence_penalty":0
        }
        if is_code:
            args["model"] = "code-davinci-002"
            args["max_tokens"] = 4000

        response = openai.Completion.create(
            **args
        )
        choices = list(x["text"] for x in response["choices"])
        file_name =  create_name(response["choices"][0]["text"])
        print(response)
        dump_response(prompt, choices, file_name,output_folder)
