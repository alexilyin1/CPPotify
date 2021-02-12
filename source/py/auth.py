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
        self.TOKEN = null

        self.spotify_client = OAuth2Service(client_id = self.CLIENT_ID,
                                            client_secret = self.CLIENT_SECRET,
                                            name = "spotify",
                                            authorize_url = "https://accounts.spotify.com/authorize",
                                            access_token_url = "https://accounts.spotify.com/api/token",
                                            base_url = "https://accounts.spotify.com/"
                                        )

        params = {'response_type': 'code',
                  'redirect_uri': self.REDIRECT_URI,
                  'state': self.STATE,
                  'scope': self.SCOPE,
                  'show_dialog': str(self.SHOW_DIALOG)
                }

        self.auth_url = self.spotify_client.get_authorize_url(**params)

    def get_auth_url(self):
        return self.auth_url

    def open_auth_url(self):
        webbrowser.open(self.auth_url)

    def set_token(self, token_url):
        pass