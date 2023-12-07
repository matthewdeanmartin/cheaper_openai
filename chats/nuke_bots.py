import asyncio
import traceback

import time

import dotenv
from openai.types import FunctionDefinition
from openai.types.beta.threads import run_create_params
from openai.types.beta.threads.run import ToolAssistantToolsFunction

from chats.bot_shell import BotConversation
from chats.bots import get_persistent_bot, get_persistent_bot_convo
from chats.chatroom import ChatroomLog
from chats.utils import show_json
from chats.inventory import InventoryClient

dotenv.load_dotenv()

if __name__ == "__main__":
    async def main():
        client = InventoryClient()
        # only handles first page.
        for key, assistants in await client.list_assistants():
            if key == "data":
                for assistant in assistants:
                    result = await client.delete_assistant(assistant)
                    print(result)
            else:
                print(key, assistants)

    # Python 3.7+
    asyncio.run(main())
