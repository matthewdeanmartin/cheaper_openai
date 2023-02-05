import openai
import tiktoken

from chats.client_utils import create_client
from chats.io_utils import dump_response, read_config, read_prompt
from chats.markdown_utils import cleanup_markdown
from chats.name_this_cheap import create_name
from chats.spelling_utils import check_document

config = read_config()
create_client()


def run() -> None:
    # get output folder from config file
    output_folder = config["output"]["output_folder"]

    prompt = read_prompt(output_folder)

    # gpt2 (or r50k_base) 	Most GPT-3 models
    # p50k_base 	Code models, text-davinci-002, text-davinci-003
    # cl100k_base 	text-embedding-ada-002
    enc = tiktoken.get_encoding("p50k_base")
    tokens = enc.encode(prompt)
    print(len(tokens))
    prompt_tokens = len(tokens)

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
