import openai

from chats.client_utils import create_client
from chats.io_utils import dump_response, read_config, read_prompt
from chats.markdown_utils import cleanup_markdown
from chats.name_this_cheap import create_name
from chats.spelling_utils import check_document
from chats.token_utils import count_tokens

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
            exit()

    is_code = False

    for temperature in [
        0.9,
    ]:
        for max_tokens in [
            4000,
        ]:
            args = {
                "model": "text-davinci-003",
                "prompt": prompt,
                "temperature": temperature,
                "max_tokens": max_tokens - prompt_tokens,
                "top_p": 1,
                "frequency_penalty": 0,
                "presence_penalty": 0,
            }
            if is_code:
                args["model"] = "code-davinci-002"
                args["max_tokens"] = 4000 - prompt_tokens

            response = openai.Completion.create(**args)

            choices = list(x["text"] for x in response["choices"])
            file_name = create_name(response["choices"][0]["text"])
            dump_response(prompt, choices, file_name, output_folder)


if __name__ == "__main__":
    run()
