import sys
import os
import json
import warnings
from datetime import datetime

sys.path.insert(0, os.path.join(os.path.abspath('../../'), 'build/'))
import pybind11module


class CPPotify:
    """
    Python wrapper for C++ Spotify API class

    getPlaylists: Get playlist information
    getTracks: Get track features/attributes
    _token_check: Spotify API tokens are currently set to expire after 60 mintues - this function will auto-renew your token
    """

    def __init__(self, CLIENT_ID, CLIENT_SECRET):
        self.CLIENT_ID = CLIENT_ID 
        self.CLIENT_SECRET = CLIENT_SECRET
        
        self._cpp_obj = pybind11module.CPPotify(self.CLIENT_ID, self.CLIENT_SECRET)
        self.TOKEN_start = datetime.now()

    def getPlaylists(self, get_own_playlists: bool, userID = '', playlistID = '', playlistObj = ''):
        """
        Return information about Spotify playlists

        @param get_own_playlists: Bool, set to True if returning information about the playlists on the account to which the
                                  Spotify API was assigned to, set to False if returning information about another users 
                                  playlists 
        @param userID: Spotify user ID for the account that playlist infomration will be returned from
        @param playlistID: Spotify playlist ID for the playlist information will be returned from. Can not be used in concurrency
                           with the userID variable. Takes no value if returning playlist objects
        @param playlistObj: Playlist object, either tracks or images. Takes no value if returning playlist objects
        """
        self._token_check()
        
        if playlistObj != '' and playlistObj != 'tracks' or playlistObj != 'images':
            raise ValueError("Spotify API returns only track and image information from playlists. Argument {} is not a valid option".format(playlistObj))
        if get_own_playlists and userID != '' or playlistID != '' or playlistObj != '':
            raise ValueError("Spotify API only supports listing playlists for your linked account. Try again without populating the userID, playlistID and playlistObj arguments")
        
        return json.loads(self._cpp_obj.getPlaylists(get_own_playlists, userID))

    def getTracks(self, audio_analysis: bool, songID):
        """
        Return information about Spotify songs/tracks

        @param Audio_analysis: Bool, set to True if you returning audio analysis and features. Audio analysis/features for one 
                               song is returned as a nested Json
        @param songID: Identifies the song/track for which information will be requested. If requesting for multiple tracks, input a 
                       list of IDs
        """
        self._token_check()
        
        if type(songID) == list:
            if (len(songID)) > 50:
                raise ValueError("Spotify API limits length of multiple song requests to 50, split up requests by length of multiples of 50 instead of lists with lengths greater than 50")
            return json.loads(self._cpp_obj.getTracks(audio_analysis, ",".join([id for id in songID]))[0])
        else:
            if audio_analysis:
                content = {}
                res = self._cpp_obj.getTracks(audio_analysis, songID)
                
                content['audio_analysis'] = json.loads(res[0])
                content['audio_features'] = json.loads(res[1])
                return content
            else:
                return json.loads(self._cpp_obj.getTracks(audio_analysis, songID)[0])

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
                       max 2000. Can bse used with the limit argument to parse search result pages
        """
        self._token_check()
        
        if len([key for key in filt.keys() if key not in ['album', 'artist', 'track', 'year']]) > 0:
            raise ValueError("Spotify API search function accepts 'album', 'artist', 'track' or 'year' as search filters'")
        if query == '' and filt == {}:
            raise ValueError("If not using a query search, a filter dictionary must be passed")

        if type(obj_type) == list:
            if len([obj for obj in obj_type if obj not in ['album', 'artist', 'playlist', 'track', 'show', 'episode']]) > 0:
                raise ValueError("Spotify object type must be one of 'album', 'artist', 'playlist', 'track', 'show' or 'episode'. Arguments {} not a valid option".format([obj for obj in obj_type if obj not in ['album', 'artist', 'playlist', 'track', 'show', 'episode']]))
            return json.loads(self._cpp_obj.search(query.replace(' ', '%20'), ",".join([id for id in obj_type]), filt, limit, offset))
        else:
            if obj_type not in ['album', 'artist', 'playlist', 'track', 'show', 'episode']:
                raise ValueError("Spotify object type must be one of 'album', 'artist', 'playlist', 'track', 'show' or 'episode'. Argument {} not a valid option".format(obj_type))
            return json.loads(self._cpp_obj.search(query.replace(' ', '%20'), obj_type, filt, limit, offset))

    def _token_check(self):
        """
        Auto regenerate Spotify tokens after 1 hour, use the "TOKEN_start" class variable
        """
        seconds_after_start = (datetime.now() - self.TOKEN_start).seconds
        if seconds_after_start >= 3000 and seconds_after_start < 3600:
            warnings.warn('Spotify token nearing expiration. This class will generate a new Spotify token when the token expires')
        elif seconds_after_start >= 3600:
            warnings.warn('Spotify token has expired. No action needed, generating new token...')
            self._cpp_obj.tokenAuth()
            self.TOKEN_start = datetime.now()

            warnings.warn('New Spotify token created')