#ifndef CPPOTIFY_H
#define CPPOTIFY_H

#include "authControl.h"
#include <map>
#include <string>
#include <vector>

class CPPotify {
private:
    std::string CLIENT_ID;
    std::string CLIENT_SECRET;
    std::string oAuthToken;
    std::string REDIRECT_URI; 
    std::string STATE;
    std::string SCOPE; 
    bool SHOW_DIALOG;
    authControl ac;
    std::string TOKEN = "";
    
    static size_t WriteCallback(void *contents, size_t size, size_t nmemb, void *userp);

public:
    CPPotify(std::string ID, std::string SECRET);
    CPPotify(std::string ID, std::string SECRET, std::string oAuthToken, std::string REDIRECT_URI = "", std::string STATE = "34fFs29kd09", std::string SCOPE = "user-read-private user-read-email", bool SHOW_DIALOG = false);
    ~CPPotify();

    //std::vector<std::string> curlGET(std::string spotifyObj, bool self, std::string userID = "", std::string spotifyID = "", std::string itemObj = "", std::string fields = "", int limit = 50, int offset = 0);
    std::vector<std::string> curlGET(std::string spotifyObj, std::map<std::string, std::string> payload, std::string query = "");
    //std::vector<std::string> curlPOST(std::string spotifyObj, bool self, std::string spotifyID = "", std::string itemObj = "");
    
    std::vector<std::string> getAlbums(std::string albumID, std::string albumObj = "", int limit = 50, int offset = 0);
    std::vector<std::string> getArtists(std::string artistID, std::string artistObj = "", std::string include_groups = "", int limit = 50, int offset = 0);
    std::vector<std::string> getEpisodes(std::string episodeID);    
    std::vector<std::string> getPlaylists(bool getOwnPlaylists, std::string userID = "", std::string playlistID = "", std::string playlistObj = "", std::string fields = "", int limit = 50, int offset = 0);
    std::vector<std::string> getProfiles(bool getOwnProfile, std::string userID);    
    std::vector<std::string> getShows(std::string showID, std::string showObj = "");
    std::vector<std::string> getTracks(std::string trackID, std::string trackObj = "");
    std::vector<std::string> getPlayer(std::string playerObj = "");
    std::vector<std::string> search(std::string query, std::string objType = "", std::map<std::string, std::string> filt = std::map<std::string, std::string>(), int limit = 50, int offset = 0);
    std::vector<std::string> browse(std::string browseCategory, std::string categoryID = "", std::string categoryObj = "", std::string timestamp = "", int limit = 50, int offset = 0);

    /*
    void postPlayer(std::string playerAction);
    */

    std::string getClientID();
    std::string getClientSecret();
    std::string getAuthToken();
    std::string getRedirectURI();
    std::string getState();
    std::string getScope();
    bool getShowDialog();
    std::string getToken();
    
};
#endif