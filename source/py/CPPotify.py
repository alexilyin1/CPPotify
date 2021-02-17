import sys
import os
import json
import warnings
from datetime import datetime

sys.path.insert(0, os.path.join(os.path.abspath('../../'), 'build/'))
import pybind11module
from auth import oAuth


class CPPotify:
    """
    Python wrapper for C++ Spotify API class. This class calls methods built in a C++ class

    For additional details on Spotify API functionality and function arguments, visit the official Spotify API web reference:
    https://developer.spotify.com/documentation/web-api/reference

    Example Client Credentials flow:

        cpp = CPPotify('your client id', 'your client secret')
        cpp.get_albums('spotify id for album you want to request', 'tracks')

    Example oAuth 2.0 flow:

        cpp = CPPotify('your client id', 'your client secret', 'your redirect URI as set in your Spotify API profile', 'state', 'scope', True/False)
        cpp.oAuth_flow() <- Warning: This method will open a URL in your default browser. See source/py/oAuth for additional details
        cpp.oAuth_set_token('url after enabling auth') 
        cpp.get_albums('spotify id for album you want to request', 'tracks')

    get_albums: Get Spotify Album tracks/attributes
    get_artists: Get Spotify Artist details
    get_episodes: Get Spotify Episode attributes
    get_playlists: Get Spotify Playlist tracks/images/details
    get_profiles: Get Spotify Profile information 
    get_shows: Get Spotify Show attributes
    get_tracks: Get Spotify Track features/attributes
    get_player: Get Spotify Player information. To interfact with the player, refer to other _player methods
    search: Use the Spotify API search functionality 
    browse: View information from the Spotify 'Browse' page

    _token_check: Spotify API tokens are currently set to expire after 60 mintues - this function will auto-renew tokens 
    """

    def __init__(self, CLIENT_ID, CLIENT_SECRET, REDIRECT_URI = "", STATE = "", SCOPE = "", SHOW_DIALOG: bool = False):
        self.CLIENT_ID = CLIENT_ID 
        self.CLIENT_SECRET = CLIENT_SECRET
        self.REDIRECT_URI = REDIRECT_URI 
        self.STATE = STATE
        self.SCOPE = SCOPE 
        self.SHOW_DIALOG = SHOW_DIALOG
        self.TOKEN = None
        self.oAuth = None
        self.oAuthToken = None

        if REDIRECT_URI != "" and STATE != "" and SCOPE != "":
            self.oAuth = oAuth(self.CLIENT_ID, self.CLIENT_SECRET, self.REDIRECT_URI, self.STATE, self.SCOPE, self.SHOW_DIALOG)
            self.oAuth.set_client()
            self._cpp_obj = None
        else:
            self._cpp_obj = pybind11module.CPPotify(self.CLIENT_ID, self.CLIENT_SECRET)
        
        self.TOKEN_start = datetime.now()

    def open_browser(self):
        if self.oAuth:
            self.oAuth.open_auth_url()

    def oAuth_flow(self, url):
        if not self.oAuth:
            return "CPPotify object initialized with Client Credentials authorization. Initialize the object with necessary oAuth arguments before proceeding"
        
        self.oAuth.set_oAuth_token(url)
        self.oAuth.set_token()

        self.oAuthToken = self.oAuth.auth_token
        self.TOKEN = self.oAuth.TOKEN
        
        self._cpp_obj = pybind11module.CPPotify(self.CLIENT_ID, self.CLIENT_SECRET, self.oAuthToken, self.TOKEN, self.REDIRECT_URI, self.STATE, self.SCOPE, self.SHOW_DIALOG)

    def get_albums(self, album_id: [list, str], album_obj = '', limit = 50, offset = 0):
        """
        Return information about Spotify albums

        :param album_id: Spotify album ID for the album that information will be returned from. Can be a list object containing up to 20 IDs 
        :param album_obj: Album object, must be set to 'tracks'. Takes no value if returning playlist objects
        :param limit: Limit the amount of results returned, min 0, max 50, default 50
        :param offset: Offset results based on popularity, i.e. offset of 5 will list the 6th most popular results onwards, default 0. 
                       Can be used with the limit argument to parse search result pages

        :returns Call to relevant C++ class method 
    
        :raises ValueError if album_obj is not 'tracks'
        :raises ValueError if length of multiple album_id's is greater than 50
        """
        self._token_check()
        
        if type(album_id) == list:
            call = self._cpp_obj.getAlbums(",".join([id for id in album_id]), album_obj, limit, offset)
        else:
            call = self._cpp_obj.getAlbums(album_id, album_obj, limit, offset)

        return self._parse_errors(
            json.loads(call[1]),
            'albums',
            call[0],
            datetime.now() 
        )
        
    def get_artists(self, artist_id: [list, str], artist_obj = '', include_groups = '', limit = 50, offset = 0):
        """
        Return information about Spotify artists

        :param artist_id: Spotify artist ID for the artist that information will be returned from. Can be a list object containing up to 50 IDs  
        :param artist_obj: Artist object, must be albums, top-tracks or related-tracks. Takes no value if returning playlist objects
        :param include_groups: When returning an artists' albums, use this to filter for the type of albums to return i.e. pass the string 'album,single'
                               to only return an artists albums and singles
        :param limit: When returning an artists' albums, limit the amount of results returned. Min 1, max 50, default 50
        :param offset: When returning an artists' albums, offset results based on popularity, i.e. offset of 5 will list the 6th most popular results onwards, default 0, max 100. 
                       Can be used with the limit argument to parse search result pages
        
        :returns Call to relevant C++ class method

        :raises ValueError if artist_obj is not 'albums', 'top-tracks' or 'related-tracks'
        :raises ValueError if length of mulitple artist_id's is greater than 50
        """
        self._token_check()
        
        if type(artist_id) == list:
            call = self._cpp_obj.getArtists(",".join([id for id in artist_id]), artist_obj, include_groups, limit, offset)
        else:
            call = self._cpp_obj.getArtists(artist_id, artist_obj, include_groups, limit, offset)

        return self._parse_errors(
            json.loads(call[1]),
            'artists',
            call[0],
            datetime.now() 
        ) 

    def get_episodes(self, episode_id: [list, str]):
        """
        Return information about Spotify Playlist Episodes

        :param episode_id: Episode ID for the episode that information will be returned be returned from. Can be a list object containing up to 50 IDs 

        :returns Call to relevant C++ class method

        :raises ValueError if length of multiple episode_id's is greater than 50      
        """
        self._token_check()

        if type(episode_id) == list:
            call = self._cpp_obj.getEpisodes(",".join([id for id in episode_id]))
        else:            
            call = self._cpp_obj.getEpisodes(episode_id)

        return self._parse_errors(
            json.loads(call[1]),
            'episodes',
            call[0],
            datetime.now() 
        ) 

    def get_player(self, player_obj = ''):
        """
        Return information about Spotify songs/tracks

        :param Audio_analysis: Bool, set to True if you returning audio analysis and features. Audio analysis/features for one 
                               song is returned as a nested Json
        :param track_id: Identifies the song/track for which information will be requested. If requesting for multiple tracks, input a 
                       list of IDs

        :returns Call to relevant C++ class method

        :raises ValueError if player_obj is not 'devices', 'currently-playing' or 'recently-played'
        """
        self._token_check()
        
        call = self._cpp_obj.getPlayer(player_obj)

        return self._parse_errors(
            json.loads(call[1]),
            'player',
            call[0],
            datetime.now()
        )

    def get_playlists(self, get_own_playlists: bool, user_id = '', playlist_id = '', playlist_obj = '', fields = '', limit = 50, offset = 0):
        """
        Return information about Spotify playlists

        :param get_own_playlists: Bool, set to True if returning information about the playlists on the account to which the
                                  Spotify API was assigned to, set to False if returning information about another users 
                                  playlists 
        :param user_id: Spotify user _id for the account that playlist infomration will be returned from
        :param playlist_id: Spotify playlist _id for the playlist information will be returned from. Can not be used in concurrency
                           with the user_id variable. Takes no value if returning playlist objects
        :param playlist_obj: Playlist object, either tracks or images. Takes no value if returning playlist objects
        :param fields: Can be used to filter the either the playlist object or the tracks in the playlist. Must be inputted as a string following 
                       format 'total,limit', which will return the total number of items and the request limit. For more information on the
                       format of the fields parameter, visit the Spotify Web API reference:
                       https://developer.spotify.com/documentation/web-api/reference-beta/#category-playlists
                       Note that this parameter will only be valid when returning a playlist object or a playlist's tracks
        :param limit: Limit the amount of results returned. For returning a playlists' tracks: min 1, max 100, default 100.
                      For all other playlist queries, min 1, max 50, default 50
        :param offset: Offset results based on popularity, i.e. offset of 5 will list the 6th most popular results onwards, default 0, max 100. 
                       Can be used with the limit argument to parse search result pages
                       
        :returns Call to relevant C++ class method 

        :raises ValueError if playlist_obj is not 'tracks' or 'images'
        :raises ValueError if get_own_playlists is True and any Spotify IDs
        """
        self._token_check()

        call = self._cpp_obj.getPlaylists(get_own_playlists, user_id, playlist_id, playlist_obj, fields, limit, offset)

        return self._parse_errors(
            json.loads(call[1]),
            'playlists',
            call[0],
            datetime.now() 
        )

    def get_profiles(self, get_own_profile: bool, user_id = ''):
        """
        Return information about a Spotify User's Profile

        :param get_own_profile: Boolean to select the profile of the user to which the API key was assigned
        :param user_id: If not selecting own profile, the profile for this user will be returned

        :returns Call to relevant C++ class method
        """
        self._token_check()

        return self._parse_errors(
            json.loads(self._cpp_obj.getProfiles(get_own_profile, user_id)[1]),
            'profiles',
            self._cpp_obj.getProfiles(get_own_profile, user_id)[0],
            datetime.now()
        ) 

    def get_shows(self, show_id: [list, str], show_obj):
        """
        Return information about Spotify Shows

        :param show_id: Show ID for the show that information will be returned be returned from. Can be a list object containing up to 50 IDs       
        :param show_obj: Used if returning a show's episodes, enter the value 'episodes' which will replace the default value of null

        :returns Call to relevant C++ class method

        :raises ValueError if length of multiple show_id's is greater than 50
        """
        self._token_check()

        if type(show_id) == list:
            call = self._cpp_obj.getShows(",".join([id for id in show_id]), show_obj)
        else:
            call = self._cpp_obj.getShows(show_id, show_obj)

        return self._parse_errors(
            json.loads(call[1]),
            'shows',
            call[0],
            datetime.now()
        ) 

    def get_tracks(self, track_id: [list, str], track_obj):
        """
        Return information about Spotify songs/tracks

        :param Audio_analysis: Bool, set to True if you returning audio analysis and features. Audio analysis/features for one 
                               song is returned as a nested Json
        :param track_id: Identifies the song/track for which information will be requested. If requesting for multiple tracks, input a 
                       list of IDs

        :returns Call to relevant C++ class method

        :raises ValueError if track_obj is not 'audio-analysis', 'audio-features' or 'tracks'
        :raises ValueError if length of multiple track_id's is greater than 50
        """
        self._token_check()

        if type(track_id) == list:
            call = self._cpp_obj.getTracks(",".join([id for id in track_id]), track_obj)
        else:
            call = self._cpp_obj.getTracks(track_id, track_obj)

        return self._parse_errors(
            json.loads(call[1]),
            'tracks',
            call[0],
            datetime.now()
        ) 

    def browse(self, browse_category, category_id = '', category_obj = '', timestamp: datetime = datetime.now(), limit = 50, offset=0):
        """
        Use the Spotify API browse feature
        
        :param browse_category: Category of the browse page to parse. Accepts 'categories', 'featured-playlists', 'new-releases'
        :param timestamp: Timestamp for snapshot of the browse page. Must be passes as a datetime object i.e. datetime.datetime(2018, 12, 25, 1, 27, 53)
        :param category_id: If viewing categories, Spotify category ID to parse 
        :param category_obj: If viewing categories, object to return from a category. Must be 'playlists'
        :param limit: Limit the amount of results returned, min 0, max 50, default 50
        :param offset: Offset results based on popularity, i.e. offset of 5 will list the 6th most popular results onwards, default 0,
                       max 2000. Can be used with the limit argument to parse search result pages
        """
        self._token_check()

        call = self._cpp_obj.browse(browse_category, category_id, category_obj, str(timestamp).replace(' ', 'T').replace(':', '%3A').split('.')[0], limit, offset)

        return self._parse_errors(
            json.loads(call[1]),
            'browse',
            call[0],
            datetime.now()
        ) 

    def search(self, query, obj_type, filt:dict = {}, limit = 50, offset = 0):
        """
        Use the Spotify API search function 

        :param query: The query used for the search inputted as a string i.e. "Classic Rock". Set to '' if only search with filters 
        :param obj_type: The type of objects to be returned from the search. Can be one of album, artist, playlist, track, show and episode 
                         If performing a search with multiple result types, input the types as a list i.e. ["playlists", "track"]
        :param filt: Optional filters to add to a search, must be a dictionary object. Can be used in place of a search query
                     i.e. {'album': 'python', 'year': '2008'} will filter your search results to albums containing the word 'python'
                     released in 2008. Can use date range i.e. '2008-2010'. To use as main search query, input '' as first argument
        :param limit: Limit the amount of results returned, min 0, max 50, default 50
        :param offset: Offset results based on popularity, i.e. offset of 5 will list the 6th most popular results onwards, default 0,
                       max 2000. Can be used with the limit argument to parse search result pages

        :returns Call to relevant C++ class method

        :raises ValueError if filt dictionary keys not 'album', 'artist', 'track' or 'year'
        :raises ValueError if both query and filt are empty
        :raises ValueError if obj_type values are not 'album', 'artist', 'playlist', 'track', 'show', or 'episode'
        """
        self._token_check()

        if type(obj_type) == list:
            call = self._cpp_obj.search(query, ",".join([typ for typ in obj_type]), filt, limit, offset)
        else:
            call = self._cpp_obj.search(query, obj_type, filt, limit, offset)

        return self._parse_errors(
            json.loads(call[1]),
            'search',
            call[0],
            datetime.now()
        ) 

    def post_player(self, player_action, song_uri = '', device_id = ''):
        """
        Send commands to the Spotify Player
        
        :param player_action: Action for the Spotify Player to complete. Must be set to 'next', 'previous', or 'queue'
        :param song_uri: If adding a song to the queue, enter the song URI here. NOTE: this must be a Spotify URI NOT an ID
        :param device_id: If modifying the Player on a certain device, enter the device ID here

        :returns Call to relevant C++ class method

        :raises ValueError if player_action is not 'next', 'previous', or 'queue'
        """
        if not self.oAuth:
            warnings.warn(
                "This operation will not complete with the current level of user authentication. Visit the Spotify developer documentation for more information",
                category=RuntimeWarning
            )

        self._token_check()

        call = self._cpp_obj.postPlayer(player_action, song_uri, device_id)

        return self._parse_errors(
            json.loads(call[1]),
            'player',
            call[0],
            datetime.now()
        )
            
    def _token_check(self):
        """
        Auto regenerate Spotify tokens after 1 hour, use the "TOKEN_start" class variable
        """
        if not self.oAuth:
            seconds_after_start = (datetime.now() - self.TOKEN_start).seconds
            if seconds_after_start >= 3000 and seconds_after_start < 3600:
                warnings.warn(
                    "Spotify token nearing expiration. This class will generate a new Spotify token when the token expires"
                )
            elif seconds_after_start >= 3600:
                warnings.warn(
                    "Spotify token has expired. No action needed, generating new token..."
                )
                self._cpp_obj.ac.auth()
                self.TOKEN_start = datetime.now()

                warnings.warn("New Spotify token created")
        else:
            seconds_after_start = (datetime.now() - self.TOKEN_start).seconds
            if seconds_after_start >= 3000 and seconds_after_start < 3600:
                warnings.warn(
                    "Spotify token nearing expiration. This class will generate a new Spotify token when the token expires"
                )
            elif seconds_after_start >= 3600:
                warnings.warn(
                    "Spotify token has expired. No action needed, generating new token..."
                )
                self.oAuth.new_token()
                self.TOKEN_start = datetime.now()

                warnings.warn("New Spotify token created")

    def _parse_errors(self, response: dict, obj, request_url, timestamp: datetime):
        """
        Returns a more detailed error object

        :param response: The response being parse for an error
        :param obj: Spotify object that generated the response
        :param timestamp: Timestamp of the request 
        
        :return error_obj: Detailed error object containing error code, error reason, error message, Spotify object, Spotify request URL and timestamp
        """
        response_map = {
            '200': 'OK',
            '201': 'Created',
            '202': 'Accepted',
            '204': 'No Content',
            '304': 'Not Modified',
            '400': 'Bad Request',
            '401': 'Unauthorized',
            '403': 'Forbidden',
            '404': 'Not Found',
            '429': 'Too Many Requests - Rate limiting has been applied.',
            '500': 'Internal Server Error',
            '502': 'Bad Gateway',
            '503': 'Service Unavailable'
        }
        try:
            if 'error' in response.keys():
                try:
                    print("""Found error in response. \n
                             URL: {} \n
                             Code: {} \n
                             Reason: {} \n
                             Message: {} \n """.\
                        format(request_url,
                            str(response['error']['status']), 
                            response_map[str(response['error']['status'])],
                            response['error']['message']))

                    return {'error': str(response['error']['status']),
                            'reason': response_map[str(response['error']['status'])],
                            'message': response['error']['message'],
                            'request_obj': obj,
                            'request_url': request_url, 
                            'time': str(timestamp)}
                except:
                    warnings.warn("Unexpected error occured")
                    return response 
            else:
                return response
        except:
            return response