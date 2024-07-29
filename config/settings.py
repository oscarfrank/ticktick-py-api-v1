import os
from dotenv import load_dotenv

load_dotenv()

AUTH_URL = "https://ticktick.com/oauth/authorize"
TOKEN_URL = "https://ticktick.com/oauth/token"
TASK_URL = "https://api.ticktick.com/open/v1/task"

CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')

REDIRECT_URI = "http://localhost:8321"
SERVER_PORT = 8321

TOKEN_FILE = "ticktick_token.json"