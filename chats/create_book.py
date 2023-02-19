import time

import marko
import openai
import yaml

from chats.client_utils import create_client
from chats.io_utils import dump_response, read_config, read_prompt, read_yaml_toc_prompt
from chats.token_utils import count_tokens

config = read_config()
create_client()

TITLE = "Powershell for Linux Users"
TEMPLATE = f"""Create a table of contents for a book named '{TITLE}' The output must be in yaml. 
e.g.

```yaml
---
- Chapter
  - Section
  - Another Section
- Another Chapter
  - Another Section
  - Another Section
```
It should not have anything about the Registry because Linux doesn't have a Windows Registry."""


def fulfill_the_promise():
    # get output folder from config file
    # output_folder = config["output"]["output_folder"]
    # prompt = read_prompt(output_folder)

    markdown_document = """
    # title

    ## subtitle first

    paragraph

    ## subtitle last

    paragraph one.

    paragraph two.
    """

    tree = marko.parse(markdown_document)

    # Find the last subtitle node in the tree
    last_subtitle = None
    for node in tree.children:
        if node.tag_name == "h2":
            last_subtitle = node

    # Extract the markdown under the last subtitle
    markdown_text = ""
    for node in last_subtitle.children:
        markdown_text += node.markdown

    return markdown_text


def make_the_toc() -> None:
    # get output folder from config file
    output_folder = config["output"]["output_folder"]

    prompt = read_prompt(output_folder)

    who_are_you = (
        "You are professional software developer and build master. You are enthusiastically "
        "teaching people how to use the fish shell, version 3.2."
    )

    temperature = 0.9
    max_tokens = 4000
    response = basic_request(max_tokens, prompt, temperature)

    choices = list(x["text"] for x in response["choices"])
    dump_response(f"{who_are_you} \n\n {prompt}", choices, "book.yml", output_folder)

    likely_yaml = "".join(choices)
    yaml.safe_load(likely_yaml)


def run_the_toc():
    temperature = 0.9
    max_tokens = 4000

    who_are_you = (
        "You are a Linux enthusiast showing Debian users how to use powershell on Linux."
        " You have a lot of ideas for how to run powershell on linux. You are writing a book. "
    )
    # get output folder from config file
    output_folder = config["output"]["output_folder"]
    toc = read_yaml_toc_prompt(output_folder)
    section_count = 0

    for inner in toc:
        for section, chapters in inner.items():
            section_count += 1
            chapter_count = 0
            for chapter in chapters:
                chapter_count += 1

                prompt = f"{who_are_you} Please write the exposition for '{section} : {chapter}'. Use markdown."
                response = basic_request(max_tokens, prompt, temperature, sleep=5)
                choices = list(x["text"] for x in response["choices"])
                dump_response(f"{section} : {chapter}", choices, f"{section}_{chapter_count}", output_folder)

                prompt = (
                    f"{who_are_you} Please write code samples for '{section} : {chapter}'. "
                    f"Use markdown and code blocks for code."
                )
                response = basic_request(max_tokens, prompt, temperature, sleep=5)
                choices = list(x["text"] for x in response["choices"])
                dump_response(f"{section} : {chapter}", choices, f"{section}_{chapter_count}", output_folder)


def basic_request(max_tokens, prompt, temperature, sleep=0):
    prompt_tokens = count_tokens(prompt)
    print(prompt)
    time.sleep(sleep)
    args = {
        "model": "text-davinci-003",
        "prompt": prompt,
        "temperature": temperature,
        "max_tokens": max_tokens - prompt_tokens,
        "top_p": 1,
        "frequency_penalty": 0,
        "presence_penalty": 0,
    }
    response = openai.Completion.create(**args)
    return response


if __name__ == "__main__":
    make_the_toc()
