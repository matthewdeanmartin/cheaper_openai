import tiktoken


def count_tokens(prompt):
    # gpt2 (or r50k_base) 	Most GPT-3 models
    # p50k_base 	Code models, text-davinci-002, text-davinci-003
    # cl100k_base 	text-embedding-ada-002
    enc = tiktoken.get_encoding("p50k_base")
    tokens = enc.encode(prompt)
    print(len(tokens))
    prompt_tokens = len(tokens)
    return prompt_tokens


def permitted_tokens(prompt, maximum):
    if maximum > 4000:
        maximum = 4000
