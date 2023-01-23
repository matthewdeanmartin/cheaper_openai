import os
import tomllib
from typing import Any


def read_config() -> dict[str, Any]:
    with open("../config.toml", "rb") as file:
        config = tomllib.load(file)
    return config


def read_prompt(output_folder: str) -> str:
    """Read the prompt from the file"""
    file_path = os.path.join(output_folder, "current.md")
    with open(file_path, encoding="utf-8") as file:
        return file.read()


def dump_response(prompt: str, choices: list[str], file_name: str, folder_path: str):
    """Dump the response to a file"""
    folder_path = os.path.join(folder_path, "output")
    file_count = len([f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))])
    # Create the new file name
    count = str(file_count + 1).zfill(4)
    file_name = (
        file_name.strip()
        .replace(" ", "_")
        .replace("\n", "")
        .replace("\t", "")
        .replace("\r", "")
        .replace("'", "")
        .replace('"', "")
    )
    new_file_name = f"{file_name}_{count}.md"
    full_name = os.path.join(folder_path, new_file_name)
    assert full_name.endswith(".md")
    with open(full_name, "w", encoding="utf-8") as file:
        file.write(prompt)
        file.write("\n\n")

        for choice in choices:
            file.write(choice)
            print(choice)
