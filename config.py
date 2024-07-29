import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# API endpoints
AUTH_URL = "https://ticktick.com/oauth/authorize"
TOKEN_URL = "https://ticktick.com/oauth/token"
TASK_URL = "https://api.ticktick.com/open/v1/task"

# Client credentials
CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')

# Server settings
REDIRECT_URI = "http://localhost:8321"
SERVER_PORT = 8321

# Token file
TOKEN_FILE = "ticktick_token.json"