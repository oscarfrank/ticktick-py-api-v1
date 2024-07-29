import requests
import json
import datetime
import webbrowser
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlencode, parse_qs
import threading
from config.settings import AUTH_URL, TOKEN_URL, CLIENT_ID, CLIENT_SECRET, REDIRECT_URI, SERVER_PORT, TOKEN_FILE

# Global variable to store the authorization code
authorization_code = None

class OAuthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        global authorization_code
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        query = parse_qs(self.path.split('?', 1)[-1])
        authorization_code = query.get('code', [None])[0]
        self.wfile.write(b"Authorization successful! You can close this window.")

def start_server():
    httpd = HTTPServer(('localhost', SERVER_PORT), OAuthHandler)
    thread = threading.Thread(target=httpd.handle_request)
    thread.start()
    return httpd

def save_token(token_data):
    with open(TOKEN_FILE, 'w') as f:
        json.dump(token_data, f)

def load_token():
    try:
        with open(TOKEN_FILE, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return None

def get_new_access_token(refresh_token=None):
    global authorization_code
    
    if refresh_token:
        data = {
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
            "refresh_token": refresh_token,
            "grant_type": "refresh_token"
        }
    else:
        httpd = start_server()
        auth_url = get_authorization_url()
        webbrowser.open(auth_url)
        while authorization_code is None:
            pass
        httpd.server_close()
        
        data = {
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
            "code": authorization_code,
            "grant_type": "authorization_code",
            "redirect_uri": REDIRECT_URI
        }
    
    response = requests.post(TOKEN_URL, data=data)
    if response.status_code == 200:
        token_data = response.json()
        token_data['expiry_time'] = datetime.datetime.now().timestamp() + token_data['expires_in']
        save_token(token_data)
        return token_data['access_token']
    else:
        raise Exception(f"Failed to obtain access token: {response.text}")

def get_access_token():
    token_data = load_token()
    if token_data:
        expiry_time = token_data.get('expiry_time', 0)
        if expiry_time > datetime.datetime.now().timestamp():
            return token_data['access_token']
        else:
            return get_new_access_token(token_data.get('refresh_token'))
    else:
        return get_new_access_token()

def get_authorization_url():
    params = {
        "client_id": CLIENT_ID,
        "scope": "tasks:write",
        "response_type": "code",
        "redirect_uri": REDIRECT_URI
    }
    return f"{AUTH_URL}?{urlencode(params)}"