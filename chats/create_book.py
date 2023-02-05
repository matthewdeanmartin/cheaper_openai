import time

import openai
import yaml

from chats.client_utils import create_client
from chats.io_utils import dump_response, read_config, read_prompt, read_yaml_toc_prompt

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


def make_the_toc() -> None:
    # get output folder from config file
    output_folder = config["output"]["output_folder"]

    prompt = read_prompt(output_folder)
    # prompt = cleanup_markdown(prompt)

    temperature = 0.9
    max_tokens = 250
    response = basic_request(max_tokens, prompt, temperature)

    choices = list(x["text"] for x in response["choices"])
    dump_response(prompt, choices, "book.yml", output_folder)

    likely_yaml = "".join(choices)
    yaml.safe_load(likely_yaml)


def run_the_toc():
    temperature = 0.9
    max_tokens = 4000

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
                prompt = f"Please write the exposition for '{section}:{chapter}'"

                response = basic_request(max_tokens, prompt, temperature, sleep=5)

                choices = list(x["text"] for x in response["choices"])
                dump_response(prompt, choices, f"{section}_{chapter_count}", output_folder)

                prompt = f"Please write code samples for '{section}:{chapter}'"
                response = basic_request(max_tokens, prompt, temperature, sleep=5)

                choices = list(x["text"] for x in response["choices"])
                dump_response(prompt, choices, f"{section}_{chapter_count}", output_folder)


def basic_request(max_tokens, prompt, temperature, sleep=0):
    print(prompt)
    time.sleep(sleep)
    args = {
        "model": "text-davinci-003",
        "prompt": prompt,
        "temperature": temperature,
        "max_tokens": max_tokens,
        "top_p": 1,
        "frequency_penalty": 0,
        "presence_penalty": 0,
    }
    response = openai.Completion.create(**args)
    return response


if __name__ == "__main__":
    run_the_toc()
