import os

from dotenv import load_dotenv
load_dotenv()


# Get API key from environment variable
openai_api_key = os.getenv("OPENAI_API_KEY")

