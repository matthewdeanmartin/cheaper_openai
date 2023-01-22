# cheaper_openai
Recreate ChatGPT-Assistant, but with an IDE, CLI driven UI and the cheaper text-davinci-003 model

The audience is software developers who don't want to spend $42 a month yet.

I'm trying to layout this project to keep prompts and response out of github, for example, all .md
files are excluded.

Some people report a month of API usage as low as $2.

# installation

Go add a credit card and get an API key.
Put the API key into `.env`, copy the `.env.example`. Do not commit your key!

This workflow doesn't work well for pypi packages. 
```
git clone
# set an output folder
nano config.toml
```

Put a `current.md` file with your prompt in your output folder.

Open in pycharm and run create.

# usage
Open your output folder and the `chat` module in your favorite IDE. I suppose you could open one in Pycharm and the other in a good markdown editor like Obsidian.

Right now, it looks like the API has no concept of conversation. You can submit a document that looks like a move script and the chatbot will add the response, e.g.

```markdown
Please write the next response. You are davinci. You are a crazy wild comedian.

Me: Tell me a joke about chickens and roads.

davicni:
```

To keep the conversation going, tack on what Davinci said. I plan to try to automate this.

I ask Davinci to give a conversation a title to avoid `response_01.md`, `response_02.md` etc. I plan to make this controllable via `config.toml`

I will eventually ask Davinci to clean up prompts preflight (fix grammar, spelling) and to make this controllable via `config.toml` 

