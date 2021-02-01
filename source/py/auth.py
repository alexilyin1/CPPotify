from rauth import OAuth2Service
import oauth2


class CPPotifySiteAdapter(oauth2.web.AuthorizationCodeGrantSiteAdapter, oauth2.web.ImplicitGrantSiteAdapter):

    TEMPLATE = '''
                <html>
                    <body>
                        <p>
                            <a href="{url}&confirm=confirm">confirm</a>
                        </p>
                        <p>
                            <a href="{url}&deny=deny">deny</a>
                        </p>
                    </body>
                </html>
                '''

def authenticate(self, request, environ, scopes, client):
    if request.post_param("confirm") == "confirm":
        return {}
    
    raise oauth2.error.UserNotAuthenticated

def render_auth_page(self, request, response, environ, scopes, client):
    url = request.path + "?" + request.query_string
    response.body = self.TEMPLATE.format(url = url)
    return response

def user_has_denied_access(self, request):
    if request.post_param("deny") == "deny":
        return True
    
    return False


class oAuth:

    def __init__(self, CLIENT_ID, CLIENT_SECRET, REDIRECT_URI, STATE, SCOPE, SHOW_DIALOG): 
        self.CLIENT_ID = CLIENT_ID
        self.CLIENT_SECRET = CLIENT_SECRET
        self.REDIRECT_URI = REDIRECT_URI 
        self.STATE = STATE
        self.SCOPE = SCOPE
        self.SHOW_DIALOG = SHOW_DIALOG

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

        '''self.client_store = oauth2.store.memory.ClientStore()
        self.client_store.add_client(client_id = self.CLIENT_ID, 
                                     client_secret = self.CLIENT_SECRET,
                                     redirect_uris = [self.REDIRECT_URI])
        self.site_adapter = CPPotifySiteAdapter()'''

    def getAuthToken(self):
        return self.auth_url