#include "CPPotify.h"
#include <regex>
#include <typeinfo>
#include <curl/curl.h>
#include <nlohmann/json.hpp>
#include <pybind11/stl.h>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace std;

CPPotify::CPPotify(std::string ID, std::string SECRET) : CLIENT_ID(ID), CLIENT_SECRET(SECRET) {
    clientCredentials ac(this->CLIENT_ID, this->CLIENT_SECRET);
    this->TOKEN = ac.auth();
    this->ac = ac;
}

CPPotify::CPPotify(std::string ID, std::string SECRET, std::string oAuthToken, std::string REDIRECT_URI, std::string STATE, std::string SCOPE, bool SHOW_DIALOG) : CLIENT_ID(ID), CLIENT_SECRET(SECRET), oAuthToken(oAuthToken), REDIRECT_URI(REDIRECT_URI), STATE(STATE), SCOPE(SCOPE), SHOW_DIALOG(SHOW_DIALOG) {    
    oAuth ac(this->CLIENT_ID, this->oAuthToken, this->REDIRECT_URI, this->STATE, this->SCOPE, this->SHOW_DIALOG);
    this->TOKEN = ac.auth(this->oAuthToken);
    this->ac = ac;
}

CPPotify::~CPPotify() {}

size_t CPPotify::WriteCallback(void *contents, size_t size, size_t nmemb, void *userp) {
    ((std::string*)userp)->append((char*)contents, size * nmemb);
    return size * nmemb;
}

std::vector<std::string> CPPotify::curlGET(std::string spotifyObj, bool self, std::string userID, std::string spotifyID, std::string itemObj, std::string fields, int limit, int offset) {
    std::string targetURL;
    if (!self) {
        if ((spotifyObj == "audio-features" || spotifyObj == "tracks" || spotifyObj == "albums" || spotifyObj == "artists" || spotifyObj == "episodes" || spotifyObj == "shows") && spotifyID.size() > 25) {
            targetURL = "https://api.spotify.com/v1/" + spotifyObj + "/?ids=" + spotifyID;
        }
        else if (spotifyObj == "albums" && itemObj != "") {
            targetURL = "https://api.spotify.com/v1/" + spotifyObj + "/" + spotifyID + "/" + itemObj + "?limit=" + to_string(limit) + "&offset=" + to_string(offset);
        } 
        else if (spotifyObj == "playlists" && itemObj != "") {
            targetURL = "https://api.spotify.com/v1/" + spotifyObj + "/" + spotifyID + "/" + itemObj + "?fields=" + fields + "&limit=" + to_string(limit) + "&offset=" + to_string(offset);
        }
        else if (spotifyObj == "playlists" && spotifyID != "") {
            targetURL = "https://api.spotify.com/v1/" + spotifyObj + "/" + spotifyID + "?fields=" + fields;
        }
        else if (spotifyObj == "artists" && itemObj == "albums") {
            targetURL = "https://api.spotify.com/v1/" + spotifyObj + "/" + spotifyID + "/" + itemObj + "?include_groups=" + fields + "&limit=" + to_string(limit) + "&offset" + to_string(offset);
        }
        else if (userID == "") {
            targetURL = "https://api.spotify.com/v1/" + spotifyObj + "/" + spotifyID + "/" + itemObj;
        }
        else {
            targetURL = "https://api.spotify.com/v1/users/" + userID + "/" + spotifyObj + "?limit=" + to_string(limit) + "&offset=" + to_string(offset);
        }
    }
    else {
        if (spotifyObj != "player") {
            targetURL = "https://api.spotify.com/v1/me/" + spotifyObj + "?limit=" + to_string(limit) + "&offset=" + to_string(offset);
        }
        else {
            targetURL = "https://api.spotify.com/v1/me/" + spotifyObj + "/" + itemObj;
        }
    }
    /* Logging  */
    std::cout << targetURL << std::endl;

    CURL *curl;
    std::string res;
    
    curl = curl_easy_init();
    if(curl) {
        try {
            curl_easy_setopt(curl, CURLOPT_TCP_NODELAY, 0);
            curl_easy_setopt(curl, CURLOPT_URL, targetURL.c_str());
            curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, this->WriteCallback);
            curl_easy_setopt(curl, CURLOPT_WRITEDATA, &res);

            std::string bearer = "Content-Type: application/json"; 
            struct curl_slist *bearerChunk = nullptr;
            bearerChunk = curl_slist_append(bearerChunk, bearer.c_str());
            bearerChunk = curl_slist_append(bearerChunk, ("Authorization: Bearer " + regex_replace(this->TOKEN, regex("\""), "")).c_str());
            curl_easy_setopt(curl, CURLOPT_HTTPHEADER, bearerChunk);

            curl_easy_perform(curl);
            curl_easy_cleanup(curl);
        }
        catch (const char* Exception) {
            cerr << Exception << std::endl;
        }
    }
    
    return std::vector<std::string> {targetURL, res};
}

std::vector<std::string> CPPotify::curlPOST(std::string spotifyObj, bool self, std::string spotifyID, std::string itemObj) {
    std::string targetURL;
    std::string POSTFIELDS = "";

    if (!self) {
        if ((spotifyObj == "audio-features" || spotifyObj == "tracks" || spotifyObj == "albums" || spotifyObj == "artists") && spotifyID.size() > 25) {
            targetURL = "https://api.spotify.com/v1/" + spotifyObj + "/?ids=" + spotifyID;
        }
        if ((spotifyObj == "albums" || spotifyObj == "playlists") && itemObj != "") {
            targetURL = "https://api.spotify.com/v1/" + spotifyObj + "/" + spotifyID + "/" + itemObj + "?limit=";
        } 
    }
    else {
        targetURL = "https://api.spotify.com/v1/me/" + spotifyObj + "/" + itemObj;
    }
    /* Logging  */
    std::cout << targetURL << std::endl;

    CURL *curl;
    std::string res;
    
    curl = curl_easy_init();
    if(curl) {
        try {
            curl_easy_setopt(curl, CURLOPT_TCP_NODELAY, 0);
            curl_easy_setopt(curl, CURLOPT_URL, targetURL.c_str());
            curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, this->WriteCallback);
            curl_easy_setopt(curl, CURLOPT_WRITEDATA, &res);
            curl_easy_setopt(curl, CURLOPT_POSTFIELDS, POSTFIELDS.c_str());

            std::string bearer = "Content-Type: application/json"; 
            struct curl_slist *bearerChunk = nullptr;
            bearerChunk = curl_slist_append(bearerChunk, bearer.c_str());
            bearerChunk = curl_slist_append(bearerChunk, ("Authorization: Bearer " + regex_replace(this->TOKEN, regex("\""), "")).c_str());
            curl_easy_setopt(curl, CURLOPT_HTTPHEADER, bearerChunk);

            curl_easy_perform(curl);
            curl_easy_cleanup(curl);
        }
        catch (const char* Exception) {
            cerr << Exception << std::endl;
        }
    }

    return std::vector<std::string> {targetURL, res};
}

std::vector<std::string> CPPotify::search(std::string searchQuery, std::string type, std::map<std::string, std::string> filter, int limit, int offset) {
    std::string targetURL;
    std::string filterQuery;
    
    if (searchQuery != "" and filter.size() > 0) {
        filterQuery = searchQuery + "%20";
    }
    else {
        filterQuery = searchQuery;
    }

    if (filter.size() > 0) {
        std::map<std::string, std::string>::iterator it = filter.begin();
        while (it != filter.end()) {
            filterQuery = filterQuery + it->first + ":" + it->second;

            if (std::next(it, 1) != filter.end()) {
                filterQuery = filterQuery + "%20";
            }
            it++;
        }
    }

    targetURL = "https://api.spotify.com/v1/search/?q=" + filterQuery + "&type=" + type + "&offset=" + to_string(offset) + "&limit=" + to_string(limit);
    
    /* Logging  */
    std::cout << targetURL << std::endl;

    CURL *curl;
    std::string res;
    
    curl = curl_easy_init();
    if(curl) {
        try {
            curl_easy_setopt(curl, CURLOPT_TCP_NODELAY, 0);
            curl_easy_setopt(curl, CURLOPT_URL, targetURL.c_str());
            curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, this->WriteCallback);
            curl_easy_setopt(curl, CURLOPT_WRITEDATA, &res);

            std::string bearer = "Content-Type: application/json"; 
            struct curl_slist *bearerChunk = nullptr;
            bearerChunk = curl_slist_append(bearerChunk, bearer.c_str());
            bearerChunk = curl_slist_append(bearerChunk, ("Authorization: Bearer " + regex_replace(this->TOKEN, regex("\""), "")).c_str());
            curl_easy_setopt(curl, CURLOPT_HTTPHEADER, bearerChunk);

            curl_easy_perform(curl);
            curl_easy_cleanup(curl);
        }
        catch (const char* Exception) {
            cerr << Exception << std::endl;
        }
    }

    return std::vector<std::string> {targetURL, res};
}

std::vector<std::string> CPPotify::browse(std::string browseCategory, std::string timestamp, std::string categoryID, std::string categoryObj, int limit, int offset) {
    std::string targetURL;
    
    if (browseCategory != "categories") {
        targetURL = "https://api.spotify.com/v1/browse/" + browseCategory + "?timestamp=" + timestamp + "&limit=" + to_string(limit) + "&offset=" + to_string(offset);
    }
    else { 
        std::string categoryString = (categoryObj == "") ? "/" + categoryID : "/" + categoryID + "/" + categoryObj;
        targetURL = "https://api.spotify.com/v1/browse/" + browseCategory + categoryString + "?timestamp=" + timestamp + "&limit=" + to_string(limit) + "&offset=" + to_string(offset);
    }
    
    /* Logging  */
    std::cout << targetURL << std::endl;

    CURL *curl;
    std::string res;
    
    curl = curl_easy_init();
    if(curl) {
        try {
            curl_easy_setopt(curl, CURLOPT_TCP_NODELAY, 0);
            curl_easy_setopt(curl, CURLOPT_URL, targetURL.c_str());
            curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, this->WriteCallback);
            curl_easy_setopt(curl, CURLOPT_WRITEDATA, &res);

            std::string bearer = "Content-Type: application/json"; 
            struct curl_slist *bearerChunk = nullptr;
            bearerChunk = curl_slist_append(bearerChunk, bearer.c_str());
            bearerChunk = curl_slist_append(bearerChunk, ("Authorization: Bearer " + regex_replace(this->TOKEN, regex("\""), "")).c_str());
            curl_easy_setopt(curl, CURLOPT_HTTPHEADER, bearerChunk);

            curl_easy_perform(curl);
            curl_easy_cleanup(curl);
        }
        catch (const char* Exception) {
            cerr << Exception << std::endl;
        }
    }

    return std::vector<std::string> {targetURL, res};
}

std::string CPPotify::getRequestToken() {
    return this->oAuthToken;
}

PYBIND11_MODULE(pybind11module, cpp) {
    cpp.doc() = "CPPotify Module - Python Spotify API using C++";
    py::class_<CPPotify>(cpp, "CPPotify")
            .def(py::init<std::string, std::string>())
            .def(py::init<std::string, std::string, std::string, std::string, std::string, std::string, bool>())
            .def("curlGET", &CPPotify::curlGET)
            .def("curlPOST", &CPPotify::curlPOST)
            .def("search", &CPPotify::search)
            .def("browse", &CPPotify::browse);
};
