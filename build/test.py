from datetime import datetime
import ast
import sys
import json
import warnings
import pybind11module

import logging 
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
log = logging.getLogger('CPPotify-logger')


class CPPotify:
    """
    Python wrapper for C++ Spotify API class

    get_playlists: Get playlist information
    get_albums: Get album information
    get_artists: Get artist information
    get_tracks: Get track features/attributes
    search: Use the Spotify API search feature 
    browse: Use the Spotify API browse feature, parses the Spotify 'Browse' page

    _token_check: Spotify API tokens are currently set to expire after 60 mintues - this function will auto-renew tokens 
    """

    def __init__(self, CLIENT_ID, CLIENT_SECRET):
        self.CLIENT_ID = CLIENT_ID 
        self.CLIENT_SECRET = CLIENT_SECRET
        
        self._cpp_obj = pybind11module.CPPotify(self.CLIENT_ID, self.CLIENT_SECRET)
        self.TOKEN_start = datetime.now()

    def request_get(self, spotify_obj: str, get_own_values: bool, user_id: str = '', spotify_id: [str, list] = '', item_obj: str = '', fields: str = '', limit: int = 50, offset: int = 0):
        """
        Use the linked PyBind11 C++ class to make HTTP requests using the C++ library 'libcurl'

        @param spotify_obj: The Spotify object to be returned. A list of Spotify objects and their descriptions can be found in Spotify's official API documentation
                            https://developer.spotify.com/documentation/web-api/
        @param get_own_values: Set to True if you want to return values from the account associated with the current API keys. Possible queries can be found in the API documentation
        @param user_id: Use this argument to return information from a particular user
        @param spotify_id: The ID of the Spotify object information will be returned from
        @param item_obj: The object to be returned from the specified Spotify Object i.e. set to 'tracks' with spotify_obj set to 'playlist' to return tracks of a particular playlist
        @param fields: Used to filter fields from returned objects. Only valid with playlist tracks queries 
        @param limit: Limit the count of results returned. Different default/maximum values based on the Spotify object 
        @param offset: Offsets the first result of the query i.e. set offset to 5 to return the last 15 results from a request response with length 20. Can be used in tandem with the 
                       limit parameter to objects past the maximum limit values
        
        @returns error_obj: If query returns an error, will call the parse_error function to return a custom error object
        @returns response: If query succesful, returns the results of the query
        """
        response = self._cpp_obj.curlGET(spotify_obj, get_own_values, user_id, spotify_id, item_obj, fields, limit, offset)

        if 'error' in json.loads(response[1]).keys():
            return self._parse_errors(json.loads(response[1]), spotify_obj, response[0], datetime.now())
        return json.loads(response[1])

    def request_post(self, spotify_obj: str, use_own_profile: bool, spotify_id: str = '', item_obj: str = ''):
        response = self._cpp_obj.curlPOST(spotify_obj, use_own_profile, spotify_id, item_obj)

        if 'error' in json.loads(response[1]).keys():
            return self._parse_errors(json.loads(response[1]), spotify_obj, response[0], datetime.now())
        return json.loads(response[1])

    def get_playlists(self, get_own_playlists: bool, user_id = '', playlist_id = '', playlist_obj = '', fields = '', limit = 50, offset = 0):
        """
        Return information about Spotify playlists

        @param get_own_playlists: Bool, set to True if returning information about the playlists on the account to which the
                                  Spotify API was assigned to, set to False if returning information about another users 
                                  playlists 
        @param user_id: Spotify user _id for the account that playlist infomration will be returned from
        @param playlist_id: Spotify playlist _id for the playlist information will be returned from. Can not be used in concurrency
                           with the user_id variable. Takes no value if returning playlist objects
        @param playlist_obj: Playlist object, either tracks or images. Takes no value if returning playlist objects
        @param fields: Can be used to filter the either the playlist object or the tracks in the playlist. Must be inputted as a string following 
                       format 'total,limit', which will return the total number of items and the request limit. For more information on the
                       format of the fields parameter, visit the Spotify Web API reference:
                       https://developer.spotify.com/documentation/web-api/reference-beta/#category-playlists
                       Note that this parameter will only be valid when returning a playlist object or a playlist's tracks
        @param limit: Limit the amount of results returned. For returning a playlists' tracks: min 1, max 100, default 100.
                      For all other playlist queries, min 1, max 50, default 50
        @param offset: Offset results based on popularity, i.e. offset of 5 will list the 6th most popular results onwards, default 0, max 100. 
                       Can be used with the limit argument to parse search result pages
        """
        self._token_check()
        
        if playlist_obj != '' and (playlist_obj != 'tracks' and playlist_obj != 'images'):
            raise ValueError(
                    "Spotify API returns only track and image information from playlists. Argument {} is not a valid option".\
                        format(playlist_obj))
        
        if get_own_playlists and (user_id != '' or playlist_id != '' or playlist_obj != ''):
            raise ValueError(
                    "Spotify API only supports listing playlists for your linked account. Try again without populating the user_id, playlist_id and playlist_obj arguments"
                    )
        
        if playlist_id != '' and (limit != 100 or offset != 0):
            warnings.warn(
                "Limit and Offset arguments can will be ignored when returning a single playlist object"
                )

        return self.request_get('playlists', get_own_playlists, user_id, playlist_id, playlist_obj, fields.replace(',', '%2C'), limit, offset)

    def get_albums(self, album_id: [list, str], album_obj = '', limit = 50, offset = 0):
        """
        Return information about Spotify albums

        @param album_id: Spotify album ID for the album that information will be returned from. Can be a list object containing up to 20 IDs 
        @param album_obj: Album object, must be set to 'tracks'. Takes no value if returning playlist objects
        @param limit: Limit the amount of results returned, min 0, max 50, default 50
        @param offset: Offset results based on popularity, i.e. offset of 5 will list the 6th most popular results onwards, default 0. 
                       Can be used with the limit argument to parse search result pages
        """
        self._token_check()
        
        if album_obj != '' and album_obj != 'tracks':
            raise ValueError(
                    "Spotify API returns only trac information from albums. Argument {} is not a valid option".\
                        format(album_obj))
        
        if album_obj == '' and (limit != 50 or offset != 0):
            warnings.warn(
                "Limit and Offset arguments can only be used when returning a playlist's tracks. Arguments will be ignored for other calls"
                )

        if type(album_id) == list:
            if len(album_id) > 20:
                raise ValueError(
                        "Spotify API limits length of multiple song requests to 50, split up requests by length of multiples of 50"
                        )
            return self.request_get('albums', False, '', ",".join([id for id in album_id]), album_obj, '', limit, offset)
        else:
            return self.request_get('albums', False, '', album_id, album_obj, '', limit, offset)

    def get_artists(self, artist_id: [list, str], artist_obj = '', include_groups = '', limit = 50, offset = 0):
        """
        Return information about Spotify artists

        @param artist_id: Spotify artist ID for the artist that information will be returned from. Can be a list object containing up to 50 IDs  
        @param artist_obj: Artist object, must be albums, top-tracks or related-tracks. Takes no value if returning playlist objects
        @param include_groups: When returning an artists' albums, use this to filter for the type of albums to return i.e. pass the string 'album,single'
                               to only return an artists albums and singles
        @param limit: When returning an artists' albums, limit the amount of results returned. Min 1, max 50, default 50
        @param offset: When returning an artists' albums, offset results based on popularity, i.e. offset of 5 will list the 6th most popular results onwards, default 0, max 100. 
                       Can be used with the limit argument to parse search result pages
        """
        self._token_check()
        
        if artist_obj != '' and (artist_obj != 'albums' and artist_obj != 'top-tracks' and artist_obj != 'related-artists'):
            raise ValueError(
                    "Spotify API returns only albums, top-tracks and related-tracks information from artists. Argument {} is not a valid option".\
                        format(artist_obj))
        
        if type(artist_id) == list:
            if len(artist_id) > 50:
                raise ValueError(
                        "Spotify API limits length of multiple song requests to 50, split up requests by length of multiples of 50"
                        )
            return self.request_get('artists', False, '', ",".join([id for id in artist_id]), artist_obj, include_groups, limit, offset)
        else:
            return self.request_get('artists', False, '', artist_id, artist_obj, include_groups, limit, offset)  

    def get_episodes(self, episode_id: [list, str]):
        """
        Return information about Spotify Playlist Episodes

        @param episode_id: Episode ID for the episode that information will be returned be returned from. Can be a list object containing up to 50 IDs       
        """
        self._token_check()

        if type(episode_id) == list:
            if len(episode_id) > 50:
                raise ValueError(
                        "Spotify API limits length of multiple episode requests to 50, split up requests by length of multiples of 50"
                        )
            return self.request_get('episodes', False, '', ",".join([id for id in episode_id]))
        else:
            return self.request_get('episodes', False, '', episode_id)

    def get_shows(self, show_id: [list, str], show_obj):
        """
        Return information about Spotify Shows

        @param show_id: Show ID for the show that information will be returned be returned from. Can be a list object containing up to 50 IDs       
        @param show_obj: Used if returning a show's episodes, enter the value 'episodes' which will replace the default value of null
        """
        self._token_check()

        if type(show_id) == list:
            if len(show_id) > 50:
                raise ValueError(
                        "Spotify API limits length of multiple episode requests to 50, split up requests by length of multiples of 50"
                        )
            return self.request_get('shows', False, '', ",".join([id for id in show_id]), show_obj)
        else:
            return self.request_get('shows', False, '', show_id, show_obj)

    def get_profiles(self, get_own_profile: bool, user_id = ''):
        """
        Return information about a Spotify User's Profile

        @param get_own_profile: Boolean to select the profile of the user to which the API key was assigned
        @param user_id: If not selecting own profile, the profile for this user will be returned
        """
        self._token_check()

        if get_own_profile and user_id != '':
            warnings.warn(
                "Cannot use 'get_own_profile' and 'user_id' variables concurrenctly, user_id inputted will be ignored"
            )

        return self.request_get('', get_own_profile, user_id)
            
    def get_tracks(self, track_id: [list, str], track_obj):
        """
        Return information about Spotify songs/tracks

        @param Audio_analysis: Bool, set to True if you returning audio analysis and features. Audio analysis/features for one 
                               song is returned as a nested Json
        @param track_id: Identifies the song/track for which information will be requested. If requesting for multiple tracks, input a 
                       list of IDs
        """
        self._token_check()
        
        if track_obj != 'audio-analysis' and track_obj != 'audio-features' and track_obj != 'tracks':
            raise ValueError(
                    "Not an acceptable query for the Spotify track object. Options are 'audio-analysis', 'audio-features' or 'tracks'. Argument {} is not a valid option".\
                        format(track_obj))

        if type(track_id) == list:
            if len(track_id) > 50:
                raise ValueError(
                        "Spotify API limits length of multiple song requests to 50, split up requests by length of multiples of 50"
                        )
            if track_obj == 'audio-analysis':
                raise ValueError(
                        "Cannot return audio analysis for multiple tracks"
                        )
            return self.request_get(track_obj, False, '', ",".join([id for id in track_id]))
        else:
            return self.request_get(track_obj, False, '', track_id)

    def get_player(self, player_obj = ''):
        self._token_check()
        
        if player_obj != '' and player_obj != 'devices' and player_obj != 'currently-playing' and player_obj != 'recently-played':
            raise ValueError(
                    "Spotify Player requests are limited to 'devices' or 'currently-playing'. {} is not a valid option".\
                        format(player_obj))
        
        return self.request_get('player', True, '', '', player_obj)

    def post_player(self, player_action):
        self._token_check()

        if player_action != 'next' and player_action != 'previous':
            raise ValueError(
                    "Spotify Player POST requests are limited to 'next' and 'previous' for cycling through tracks. {} is not a valid command for the player".\
                        format(player_action))
            
        return self.request_post('player', True, '', player_action)

    def search(self, query, obj_type, filt:dict = {}, limit = 50, offset = 0):
        """
        Use the Spotify API search function 

        @param query: The query used for the search inputted as a string i.e. "Classic Rock". Set to '' if only search with filters 
        @param obj_type: The type of objects to be returned from the search. Can be one of album, artist, playlist, track, show and episode 
                         If performing a search with multiple result types, input the types as a list i.e. ["playlists", "track"]
        @param filt: Optional filters to add to a search, must be a dictionary object. Can be used in place of a search query
                     i.e. {'album': 'python', 'year': '2008'} will filter your search results to albums containing the word 'python'
                     released in 2008. Can use date range i.e. '2008-2010'. To use as main search query, input '' as first argument
        @param limit: Limit the amount of results returned, min 0, max 50, default 50
        @param offset: Offset results based on popularity, i.e. offset of 5 will list the 6th most popular results onwards, default 0,
                       max 2000. Can be used with the limit argument to parse search result pages
        """
        self._token_check()
        
        if len([key for key in filt.keys() if key not in ['album', 'artist', 'track', 'year']]) > 0:
            raise ValueError(
                    "Spotify API search function accepts 'album', 'artist', 'track' or 'year' as search filters'"
                    )

        if query == '' and filt == {}:
            raise ValueError(
                    "If not using a query search, a filter dictionary must be passed"
                    )

        if type(obj_type) == list:
            if len([obj for obj in obj_type if obj not in ['album', 'artist', 'playlist', 'track', 'show', 'episode']]) > 0:
                raise ValueError(
                        "Spotify object type must be one of 'album', 'artist', 'playlist', 'track', 'show' or 'episode'. Arguments {} not a valid option".\
                            format([obj for obj in obj_type if obj not in ['album', 'artist', 'playlist', 'track', 'show', 'episode']]))
            response = self._cpp_obj.search(query.replace(' ', '%20'), ",".join([id for id in obj_type]), filt, limit, offset)
        else:
            if obj_type not in ['album', 'artist', 'playlist', 'track', 'show', 'episode']:
                raise ValueError(
                        "Spotify object type must be one of 'album', 'artist', 'playlist', 'track', 'show' or 'episode'. Argument {} not a valid option".\
                            format(obj_type))
            response = self._cpp_obj.search(query.replace(' ', '%20'), obj_type, filt, limit, offset)
            
        if 'error' in json.loads(response[1]).keys():
            return self._parse_errors(json.loads(response[1]), 'search', response[0], datetime.now())
        return json.loads(response[1])

    def browse(self, browse_category, category_id = '', category_obj = '', timestamp: datetime = datetime.now(), limit = 50, offset=0):
        """
        Use the Spotify API browse feature
        
        @param browse_category: Category of the browse page to parse. Accepts 'categories', 'featured-playlists', 'new-releases'
        @param timestamp: Timestamp for snapshot of the browse page. Must be passes as a datetime object i.e. datetime.datetime(2018, 12, 25, 1, 27, 53)
        @param category_id: If viewing categories, Spotify category ID to parse 
        @param category_obj: If viewing categories, object to return from a category. Must be 'playlists'
        @param limit: Limit the amount of results returned, min 0, max 50, default 50
        @param offset: Offset results based on popularity, i.e. offset of 5 will list the 6th most popular results onwards, default 0,
                       max 2000. Can be used with the limit argument to parse search result pages
        """
        self._token_check()

        if browse_category != 'categories' and (browse_category != 'featured-playlists' and browse_category != 'new-releases'):
            raise ValueError(
                    "Spotify browse category must be one of 'categories', 'featured-playlists', or 'new-releases', Argument {} is not a valid option".\
                        format(browse_category))

        if category_obj != '' and category_obj != 'playlists':
            raise ValueError(
                    "Spotify browse category object must be 'playlists'. Argument {} is not a valid option".\
                        format(category_obj))

        response = self._cpp_obj.browse(browse_category, str(timestamp).replace(' ', 'T').replace(':', '%3A').split('.')[0], category_id, category_obj, limit, offset)

        if 'error' in json.loads(response[1]).keys():
            return self._parse_errors(json.loads(response[1]), 'browse', response[0], datetime.now())
        return json.loads(response[1])

    def _token_check(self):
        """
        Auto regenerate Spotify tokens after 1 hour, use the "TOKEN_start" class variable
        """
        seconds_after_start = (datetime.now() - self.TOKEN_start).seconds
        if seconds_after_start >= 3000 and seconds_after_start < 3600:
            warnings.warn(
                'Spotify token nearing expiration. This class will generate a new Spotify token when the token expires'
                )
        elif seconds_after_start >= 3600:
            warnings.warn(
                'Spotify token has expired. No action needed, generating new token...'
                )
            self._cpp_obj.ac.setToken()
            self.TOKEN_start = datetime.now()

            warnings.warn('New Spotify token created')

    def _parse_errors(self, response: dict, obj, request_url, timestamp: datetime):
        """
        Returns a more detailed error object

        @param response: The response being parse for an error
        @param obj: Spotify object that generated the response
        @param timestamp: Timestamp of the request 
        @return error_obj: Detailed error object containing error code, error reason, error message, Spotify object, Spotify request URL and timestamp
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
            warnings.warn("""Found error in response. \n
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


cpp = CPPotify(CLIENT_ID, CLIENT_SECRET)
# print(cpp.post_player('next'))
print(cpp.get_tracks('7EgBk5LLR', 'tracks'))



