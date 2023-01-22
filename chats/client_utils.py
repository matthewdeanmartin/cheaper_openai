import os

from dotenv import load_dotenv
import openai

load_dotenv()

def create_client():
  openai.api_key = os.environ["OPENAI_API_KEY"]



