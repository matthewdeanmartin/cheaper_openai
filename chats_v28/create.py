import os
import sys

from chats.ai_utils.client_utils import create_client
from chats.ai_utils.io_utils import read_config, read_prompt, dump_response
from chats.ai_utils.token_utils import count_tokens
from chats.md_utils.markdown_utils import cleanup_markdown
from chats.preprompt.spelling_utils import check_document
from chats.workflow.name_this_cheap import create_name

os.environ["OPENAI_API_BASE"] = "https://api.openai.com/v1/chat"

import openai



config = read_config()
create_client()

TOC_PROMPT = """Create a table of contents for a book named 'Powershell for Linux Users' The output should be in yaml"""


def run() -> None:
    # get output folder from config file
    output_folder = config["output"]["output_folder"]

    prompt = read_prompt(output_folder)

    prompt_tokens = count_tokens(prompt)

    prompt = cleanup_markdown(prompt)
    all_right, assistance = check_document(prompt)
    if not all_right:
        print("Spelling")
        print(assistance)
        keep = input("Keep? ")
        if keep.lower() == "y":
            pass
        else:
            sys.exit()

    is_code = False

    model_max_tokens = {"text-davinci-003": 4000, "curie": 2049, "gpt-3.5-turbo-0301": 4000}
    model_name = "gpt-3.5-turbo-0301"
    for temperature in [
        0.9,
    ]:
        for max_tokens in [
            model_max_tokens[model_name],
        ]:
            args = {
                "model": model_name,
                # "prompt": prompt,
                "messages": [{"role": "user", "content": prompt}],
                "temperature": temperature,
                "max_tokens": max_tokens - prompt_tokens - 15,
                "top_p": 1,
                "frequency_penalty": 0,
                "presence_penalty": 0,
            }
            if is_code:
                args["model"] = "code-davinci-002"
                args["max_tokens"] = 4000 - prompt_tokens

            response = openai.Completion.create(**args)
            if model_name == "gpt-3.5-turbo-0301":
                choices = list(x["message"]["content"] for x in response["choices"])
                file_name = create_name(choices[0], model_name)
            else:
                choices = list(x["text"] for x in response["choices"])
                file_name = create_name(response["choices"][0]["text"], model_name)
            dump_response(prompt, choices, file_name, output_folder)


if __name__ == "__main__":
    run()
