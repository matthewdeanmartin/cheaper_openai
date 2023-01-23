import mdformat


def cleanup_markdown(text):
    return mdformat.text(md=text)


# not sure where I was going with this.
# def merge_markdown(prompt:str, answer:str):
#     parsed = marko.parse(prompt)
#     answer_parsed = marko.parse(prompt)
#     print()
#
# if __name__ == '__main__':
#     config = read_config()
#     # get output folder from config file
#     output_folder = config["output"]["output_folder"]
#
#     prompt = read_prompt(output_folder)
#     merge_markdown(prompt, "## davinci\n\nNo I don't think I will")
