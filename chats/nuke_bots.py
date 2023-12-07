import asyncio

import dotenv

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
