import json
import base64
import requests
import webbrowser
from rauth import OAuth2Service

class oAuth:

    def __init__(self, CLIENT_ID, CLIENT_SECRET, REDIRECT_URI, STATE, SCOPE, SHOW_DIALOG): 
        self.CLIENT_ID = CLIENT_ID
        self.CLIENT_SECRET = CLIENT_SECRET
        self.REDIRECT_URI = REDIRECT_URI 
        self.STATE = STATE
        self.SCOPE = SCOPE
        self.SHOW_DIALOG = SHOW_DIALOG
        self.auth_token = None
        self.TOKEN = None
        self.REFRESH_TOKEN = None
        self.params = None
        self.auth_url = None

        self.set_client()

    def set_client(self):
        self.auth_url = "https://accounts.spotify.com/authorize?"

        params = {
            'client_id': self.CLIENT_ID,
            'response_type': 'code',
            'redirect_uri': self.REDIRECT_URI,
            'state': self.STATE,
            'scope': self.SCOPE,
            'show_dialog': str(self.SHOW_DIALOG)
        }

        for k in params:
            self.auth_url += k + '=' + params[k]
            if list(params.keys())[-1] != k:
                self.auth_url += '&'
        
    def open_auth_url(self):
        if not self.TOKEN:
            webbrowser.open(self.auth_url)
        else:
            return self.auth_token
    
    def set_oAuth_token(self, url):
        try:
            if not self.REDIRECT_URI in url:
                return "Invalid URL provided, must use valid redirect URL containing access code"
            
            if 'error' in url:
                return "Error when authorizing user. Try again and check your credentials"

            code = url.split('code=')[1].split('&')[0]
            self.auth_token = code
        except:
            return "Invalid redirect URL"

    def set_token(self):
        if not self.auth_token:
            return "oAuth token not set, call open_auth_url() method or navigate to set auth_url to receive auth token before continuing"

        base_url = 'https://accounts.spotify.com/api/token'

        payload ={
            'redirect_uri': self.REDIRECT_URI,
            'code': self.auth_token,
            'grant_type': 'authorization_code'
        }

        headers = {
            'Authorization': 'Basic %s' % base64.b64encode((self.CLIENT_ID + ':' + self.CLIENT_SECRET).encode('ascii')).decode('ascii')
        }

        response = json.loads(
            requests.post(base_url, data=payload, headers=headers).text
        )

        try:
            self.TOKEN = response['access_token']
            self.REFRESH_TOKEN = response['refresh_token']
        except KeyError:
            raise KeyError("Invalid oAuth token request response: " + response)
        
    def new_token(self):
        if not self.auth_token:
            return "oAuth token not set, call open_auth_url() method or navigate to set auth_url to receive auth token before continuing"

        base_url = 'https://accounts.spotify.com/api/token'

        payload ={
            'refresh_token': self.REFRESH_TOKEN,
            'grant_type': 'refresh_token'
        }

        headers = {
            'Authorization': 'Basic %s' % base64.b64encode((self.CLIENT_ID + ':' + self.CLIENT_SECRET).encode('ascii')).decode('ascii')
        }

        response = json.loads(
            requests.post(base_url, data=payload, headers=headers).text
        )
        
        try:
            self.TOKEN = response['access_token']
        except KeyError:
            raise KeyError("Invalid oAuth token request response: " + response)
        



