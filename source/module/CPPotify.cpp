#include "CPPotify.h"
#include <regex>
#include <array>
#include <typeinfo>
#include <algorithm>
#include <curl/curl.h>
#include <nlohmann/json.hpp>
#include <pybind11/stl.h>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace std;

CPPotify::CPPotify(std::string ID, std::string SECRET) : CLIENT_ID(ID), CLIENT_SECRET(SECRET) {
    clientCredentials ac(this->CLIENT_ID, this->CLIENT_SECRET);
    this->ac = ac;
    this->TOKEN = ac.getToken();
}

CPPotify::CPPotify(std::string ID, std::string SECRET, std::string oAuthToken, std::string REDIRECT_URI, std::string STATE, std::string SCOPE, bool SHOW_DIALOG) : CLIENT_ID(ID), CLIENT_SECRET(SECRET), oAuthToken(oAuthToken), REDIRECT_URI(REDIRECT_URI), STATE(STATE), SCOPE(SCOPE), SHOW_DIALOG(SHOW_DIALOG) {
    oAuth ac(this->CLIENT_ID, this->CLIENT_SECRET, this->oAuthToken, this->REDIRECT_URI, this->STATE, this->SCOPE, this->SHOW_DIALOG);
    this->ac = ac;
    this->TOKEN = ac.getToken();
}

CPPotify::~CPPotify() {}

size_t CPPotify::WriteCallback(void *contents, size_t size, size_t nmemb, void *userp) {
    ((std::string*)userp)->append((char*)contents, size * nmemb);
    return size * nmemb;
}

std::vector<std::string> CPPotify::curlGET(std::string spotifyObj, std::map<std::string, std::string> payload) {
    std::string selfStr = (payload["self"] == "1" && payload["obj"] != "") ? "me/" + spotifyObj : "me";

    std::string spotifyObjStr = (payload["self"] == "1") ? "me/" + spotifyObj : spotifyObj;
    
    std::string idStr = "";
    if (payload["id"] != "") {
        idStr = (payload["id"].size() <= 22) ? "/" + payload["id"] : "/ids=" + payload["id"];
    }

    std::string payloadStr = (payload["self"] == "1" && payload["obj"] == "") ? selfStr : spotifyObjStr + idStr;
    
    if (payload["obj"] != "") {
        payloadStr = payloadStr + "/" + payload["obj"] + "?";
    }
    else {
        payloadStr = payloadStr + "?";
    }

    auto it1 = payload.find("self");
    auto it2 = payload.find("obj");
    auto it3 = payload.find("id");

    payload.erase(it1);
    payload.erase(it2);
    payload.erase(it3);
    
    auto it = payload.begin();
    while (it != payload.end()) {
        if (it->second != "") {
            payloadStr = payloadStr + it->first + "=" + it->second;

            if (it->first != "offset" || std::next(it, 1) != payload.end()) {
                payloadStr = payloadStr + "&";
            }
        }

        it++;
    }

    std::string targetURL = "https://api.spotify.com/v1/" + payloadStr;
    
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

std::vector<std::string> CPPotify::curlPOST(std::string spotifyObj, std::map<std::string, std::string> payload) { 
    std::string spotifyObjStr = "me/" + spotifyObj;
    
    std::string payloadStr = spotifyObjStr;

    if (payload["obj"] != "") {
        payloadStr = payloadStr + "/" + payload["obj"] + "?";
    }
    else {
        payloadStr = payloadStr;
    }

    auto it2 = payload.find("obj");

    payload.erase(it2);
    
    std::string POSTFIELDS = "";
    if (payload.size() > 0) {
        auto it = payload.begin();
        while (it != payload.end()) {
            if (it->second != "") {
                POSTFIELDS = POSTFIELDS + it->first + "=" + it->second;

                if (std::next(it, 1) != payload.end()) {
                    POSTFIELDS = POSTFIELDS + "&";
                }
            }

            it++;
        }
    }

    std::string targetURL = "https://api.spotify.com/v1/" + payloadStr + POSTFIELDS;

    /* Logging  */
    std::cout << targetURL << std::endl;
    std::cout << POSTFIELDS << std::endl;

    CURL *curl;
    std::string res;
    
    curl = curl_easy_init();
    if(curl) {
        try {
            curl_easy_setopt(curl, CURLOPT_TCP_NODELAY, 0);
            curl_easy_setopt(curl, CURLOPT_URL, targetURL.c_str());
            curl_easy_setopt(curl, CURLOPT_POST, 1);
            curl_easy_setopt(curl, CURLOPT_POSTFIELDS, "");
            curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, this->WriteCallback);
            curl_easy_setopt(curl, CURLOPT_WRITEDATA, &res);
            
            struct curl_slist *authChunk = nullptr;            
            authChunk = curl_slist_append(authChunk, "Accept: application/json");
            authChunk = curl_slist_append(authChunk, "Content-Type: application/json");
            authChunk = curl_slist_append(authChunk, ("Authorization: Bearer " + this->TOKEN).c_str());

            curl_easy_setopt(curl, CURLOPT_HTTPHEADER, authChunk);

            curl_easy_perform(curl);
            curl_easy_cleanup(curl);
        }
        catch (const char* Exception) {
            std::cerr << Exception << std::endl;
        }
    }
    
    return std::vector<std::string> {targetURL, res};
}

std::vector<std::string> CPPotify::getAlbums(std::string albumID, std::string albumObj, int limit, int offset) { 
    if (albumObj != "" && albumObj != "tracks") {
        throw std::invalid_argument("Received invalid argument for album_obj argument, value " + albumObj + " must match 'tracks'");
    }

    if (albumID.size() > 1150) {
        throw std::length_error("Exceeded limit of 50 Spotify IDs");
    }

    std::map<std::string, std::string> payload{
        {"self", "0"},
        {"id", albumID},
        {"obj", albumObj},
        {"limit", to_string(limit)},
        {"offset", to_string(offset)}};

    return this->curlGET("albums", payload);
}

std::vector<std::string> CPPotify::getArtists(std::string artistID, std::string artistObj, std::string include_groups, int limit, int offset) {
    if (artistObj != "" && (artistObj != "albums" && artistObj != "top-tracks" && artistObj != "related-artists")) {
        throw std::invalid_argument("Received invalid argument for artist_obj argument, value " + artistObj + " must match 'albums', 'top-tracks' or 'related-tracks'");
    }

    if (artistID.size() > 1150) { 
        throw std::length_error("Exceeded limit of 50 Spotify IDs");
    }

    std::map<std::string, std::string> payload{
        {"self", "0"},
        {"id", artistID},
        {"obj", artistObj},
        {"include_groups", include_groups},
        {"limit", to_string(limit)},
        {"offset", to_string(offset)}};

    return this->curlGET("artists", payload);
}

std::vector<std::string> CPPotify::getEpisodes(std::string episodeID) {
    if (episodeID.size() > 1150) {
        throw std::length_error("Exceeded limit of 50 Spotify IDs");
    }

    std::map<std::string, std::string> payload{
        {"self", "0"},
        {"id", episodeID}};

    return this->curlGET("episodes", payload);
}

std::vector<std::string> CPPotify::getPlayer(std::string playerObj, std::string deviceID) {
    if (playerObj != "" && (playerObj != "devices" && playerObj != "currently-playing" && playerObj != "recently-played")) {
        throw std::invalid_argument("Received invalid player_obj argument, value " + playerObj + " must be equal to 'devices', 'currently-playing' or 'recently-player");
    }

    std::map<std::string, std::string> payload{
        {"self", "0"},
        {"obj", playerObj},
        {"device_id", deviceID}};

    return this->curlGET("player", payload);
}

std::vector<std::string> CPPotify::getPlaylists(bool getOwnPlaylists, std::string userID, std::string playlistID, std::string playlistObj, std::string fields, int limit, int offset) {
    if (playlistObj != "" && (playlistObj != "tracks" && playlistObj != "images")) {
        throw std::invalid_argument("Received invalid playlist_obj argument, value " + playlistObj + " must match 'tracks' or 'images'");
    }

    if (getOwnPlaylists && (userID != "" || playlistID != "" || playlistObj != "")) {
        throw std::invalid_argument("Can not use user_id, playlist_id or playlist_obj arguments when returning a user's own playlists");
    }

    std::map<std::string, std::string> payload{
        {"self", to_string(getOwnPlaylists)},
        {"id", (playlistID == "") ? userID : playlistID},
        {"obj", playlistObj},
        {"fields", fields},
        {"limit", to_string(limit)},
        {"offset", to_string(offset)}};

    return this->curlGET("playlists", payload);
}

std::vector<std::string> CPPotify::getProfiles(bool getOwnProfile, std::string userID) {
    if (getOwnProfile && userID != "") {
        throw std::invalid_argument("get_own_profile and user_id arguments cannot be used concurrently");
    }
    
    std::map<std::string, std::string> payload{
        {"self", to_string(getOwnProfile)},
        {"id", userID}};

    return this->curlGET("", payload);
}

std::vector<std::string> CPPotify::getShows(std::string showID, std::string showObj) {
    if (showObj != "episodes") {
        throw std::invalid_argument("Received invalid show_obj argument, value " + showObj + " must be equal to 'episodes'");
    }
    
    if (showID.size() > 1150) {
        throw std::length_error("Exceeded limit of 50 Spotify IDs");
    }

    std::map<std::string, std::string> payload{
        {"self", "0"},
        {"id", showID},
        {"obj", showObj}};

    return this->curlGET("shows", payload);
}

std::vector<std::string> CPPotify::getTracks(std::string trackID, std::string trackObj){
    if (trackObj != "" && trackObj != "audio-analysis" && trackObj != "audio-features") {
        throw std::invalid_argument("Received invalid track_obj argument, value " + trackObj + " must match 'audio-analysis' or 'audio-features'. If left blank will default to 'tracks'");
    }

    if (trackID.size() > 1150) {
        throw std::length_error("Exceeded limit of 50 Spotify IDs");
    }

    if (trackID.size() > 22 && trackObj == "audio-analysis") {
        throw std::invalid_argument("Spotify API does not return audio-analysis results for multiple tracks");
    }

    std::map<std::string, std::string> payload{
        {"self", "0"},
        {"id", trackID},
        {"obj", ""}};

    return this->curlGET((trackObj == "" || trackObj == "tracks") ? "tracks" : trackObj, payload);
}

std::vector<std::string> CPPotify::browse(std::string browseCategory, std::string categoryID, std::string categoryObj, std::string timestamp, int limit, int offset) {
    if (browseCategory != "categories" && browseCategory != "featured-playlists" && browseCategory != "new-releases") {
        throw std::invalid_argument("Received invalid argument for browse_category argument, value " + browseCategory + " must be equal to 'categories', 'featured-playlists' or 'new-releases'");
    }

    if (categoryObj != "" && categoryObj != "playlists") {
        throw std::invalid_argument("Recevied invalid argument for category_obj argument, value " + categoryObj + " must be equal to 'playlists'");
    }

    if (browseCategory == "categories" && categoryObj != "") {
        browseCategory = browseCategory + "/" + categoryID + "/" + categoryObj;
    }
    else if (browseCategory == "categories") {
        browseCategory = browseCategory + "/" + categoryID;
    }

    std::map<std::string, std::string> payload{
        {"self", "0"},
        {"id", ""},
        {"obj", browseCategory},
        {"timestamp", (browseCategory == "featured-playlists") ? timestamp : ""},
        {"limit", to_string(limit)},
        {"offset", to_string(offset)}};

    return this->curlGET("browse", payload);
}

std::vector<std::string> CPPotify::search(std::string query, std::string objType, std::map<std::string, std::string> filt, int limit, int offset) {
    std::string filtKeys[] {"album", "artist", "track", "year"};
    std::string filtStr;

    if (query != "" && filt.size() > 0) {
        filtStr = query + "%20";
    }
    else {
        filtStr = query;
    }

    auto it = filt.begin();
    if (filt.size() > 0) {
        while (it != filt.end()) {
            if (std::find(std::begin(filtKeys), std::end(filtKeys), it->first) != std::end(filtKeys)) {
                filtStr = filtStr + it->first + ":" + it->second;

                if (std::next(it, 1) != filt.end()) {
                    filtStr = filtStr + "%20";
                }
            }
            else {
                throw std::invalid_argument("Received invalid argument in the filt dictionary, " + it->first + " must be equal to 'album', 'artist', 'track' or 'year'");
            }

            it++;
        }
    }

    if (query == "" && filt == std::map<std::string, std::string>()) {
        throw std::invalid_argument("Both query and filt arguments are not used. If not using a query search, must search using filt argument");
    }

    std::map<std::string, std::string> payload{
        {"self", "0"},
        {"q", filtStr},
        {"type", objType},
        {"limit", to_string(limit)},
        {"offset", to_string(offset)}};

    return this->curlGET("search", payload);
}

std::vector<std::string> CPPotify::postPlayer(std::string playerAction, std::string songURI, std::string deviceID) {
    if (playerAction != "next" && playerAction != "previous" && playerAction != "queue") {
        throw std::invalid_argument("Received invalid argument for player_action argument, value " + playerAction + " must be equal to 'next', 'previous' or 'queue'");
    }

    std::map<std::string, std::string> payload{
        {"obj", playerAction},
        {"uri", songURI},
        {"device_id", deviceID}};

    return this->curlPOST("player", payload);
}

std::string CPPotify::reAuth() {
    this->TOKEN = ac.auth()[0];
    return this->TOKEN;
}

std::string CPPotify::getClientID() {
    return this->CLIENT_ID;
}
std::string CPPotify::getClientSecret() {
    return this->CLIENT_SECRET;
}

std::string CPPotify::getAuthToken() {
    return this->oAuthToken;
}

std::string CPPotify::getRedirectURI() {
    return this->REDIRECT_URI;
}

std::string CPPotify::getState() {
    return this->STATE;
}

std::string CPPotify::getScope() {
    return this->SCOPE;
}

bool CPPotify::getShowDialog() {
    return this->SHOW_DIALOG;
}

std::string CPPotify::getToken() {
    return this->TOKEN;
}

PYBIND11_MODULE(pybind11module, cpp) {
    cpp.doc() = "CPPotify Module - Python Spotify API using C++";
    py::class_<CPPotify>(cpp, "CPPotify")
            .def(py::init<std::string, std::string>())
            .def(py::init<std::string, std::string, std::string, std::string, std::string, std::string, bool>())
            .def("curlGET", &CPPotify::curlGET)
            .def("getAlbums", &CPPotify::getAlbums)
            .def("getArtists", &CPPotify::getArtists)
            .def("getEpisodes", &CPPotify::getEpisodes)
            .def("getPlayer", &CPPotify::getPlayer)
            .def("getPlaylists", &CPPotify::getPlaylists)
            .def("getProfiles", &CPPotify::getProfiles)
            .def("getShows", &CPPotify::getShows)
            .def("getTracks", &CPPotify::getTracks)
            .def("browse", &CPPotify::browse)
            .def("search", &CPPotify::search)
            .def("postPlayer", &CPPotify::postPlayer)
            .def("getToken", &CPPotify::getToken)
            .def("reAuth", &CPPotify::reAuth);
};