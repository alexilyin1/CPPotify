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

    std::vector<std::string> curlGET(std::string spotifyObj, bool self, std::string userID = "", std::string spotifyID = "", std::string itemObj = "", std::string fields = "", int limit = 50, int offset = 0);
    std::vector<std::string> curlPOST(std::string spotifyObj, bool self, std::string spotifyID = "", std::string itemObj = "");
    std::vector<std::string> search(std::string searchQuery, std::string type, std::map<std::string, std::string> filter = std::map<std::string, std::string>(), int limit = 50, int offset = 0);
    std::vector<std::string> browse(std::string browseCategory, std::string timestamp, std::string categoryID = "", std::string categoryObj = "", int limit = 50, int offset = 0);

    std::string getRequestToken();
};
#endif