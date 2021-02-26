#include "authControl.h"
#include <regex>
#include <iostream>
#include <curl/curl.h>
#include <nlohmann/json.hpp>

authControl::authControl() {}

authControl::authControl(std::string ID) : CLIENT_ID(ID) {}

authControl::authControl(std::string ID, std::string SECRET) : CLIENT_ID(ID), CLIENT_SECRET(SECRET) {
    this->TOKEN = this->auth()[0];
}

authControl::~authControl() {}

static const char* base64_chars[2] = {
             "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
             "abcdefghijklmnopqrstuvwxyz"
             "0123456789"
             "+/",

             "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
             "abcdefghijklmnopqrstuvwxyz"
             "0123456789"
             "-_"
};

std::string authControl::base64_encode(unsigned char const* bytes_to_encode, size_t in_len, bool url) {

    size_t len_encoded = (in_len +2) / 3 * 4;

    unsigned char trailing_char = url ? '.' : '=';\
    const char* base64_chars_ = base64_chars[url];

    std::string ret;
    ret.reserve(len_encoded);

    unsigned int pos = 0;

    while (pos < in_len) {
        ret.push_back(base64_chars_[(bytes_to_encode[pos + 0] & 0xfc) >> 2]);

        if (pos+1 < in_len) {
           ret.push_back(base64_chars_[((bytes_to_encode[pos + 0] & 0x03) << 4) + ((bytes_to_encode[pos + 1] & 0xf0) >> 4)]);

           if (pos+2 < in_len) {
              ret.push_back(base64_chars_[((bytes_to_encode[pos + 1] & 0x0f) << 2) + ((bytes_to_encode[pos + 2] & 0xc0) >> 6)]);
              ret.push_back(base64_chars_[  bytes_to_encode[pos + 2] & 0x3f]);
           }
           else {
              ret.push_back(base64_chars_[(bytes_to_encode[pos + 1] & 0x0f) << 2]);
              ret.push_back(trailing_char);
           }
        }
        else {

            ret.push_back(base64_chars_[(bytes_to_encode[pos + 0] & 0x03) << 4]);
            ret.push_back(trailing_char);
            ret.push_back(trailing_char);
        }

        pos += 3;
    }

    return ret;
}

size_t authControl::WriteCallback(void *contents, size_t size, size_t nmemb, void *userp) {
    ((std::string*)userp)->append((char*)contents, size * nmemb);
    return size * nmemb;
}

std::vector<std::string> authControl::auth() {
    CURL *curl;
    std::string res;

    curl = curl_easy_init();
    
    if(curl) {
        try {
            curl_easy_setopt(curl, CURLOPT_TCP_NODELAY, 0);
            curl_easy_setopt(curl, CURLOPT_URL, "https://accounts.spotify.com/api/token");
            curl_easy_setopt(curl, CURLOPT_POSTFIELDS, "grant_type=client_credentials");
            curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, this->WriteCallback);
            curl_easy_setopt(curl, CURLOPT_WRITEDATA, &res);

            std::string enc = this->base64_encode(reinterpret_cast<const unsigned char*>((this->CLIENT_ID + ":" + this->CLIENT_SECRET).data()), (this->CLIENT_ID + ":" + this->CLIENT_SECRET).length(), false);
            
            std::string httpAuth = "Authorization: Basic " + enc;
            struct curl_slist *authChunk = nullptr;
            authChunk = curl_slist_append(authChunk, httpAuth.c_str());

            curl_easy_setopt(curl, CURLOPT_HTTPHEADER, authChunk);

            curl_easy_perform(curl);
            curl_easy_cleanup(curl);
        }
        catch (const char* Exception) {
            std::cerr << Exception << std::endl;
        }
    }

    auto j = nlohmann::json::parse(res);
    return std::vector<std::string> {to_string(j["access_token"])};
}

std::string authControl::reAuth() {
    return "";
}

std::string authControl::setToken() {
    return this->auth()[0];
}

std::string authControl::getClientID() {
    return this->CLIENT_ID;
}

std::string authControl::getClientSecret() {
    return this->CLIENT_SECRET;
}

std::string authControl::getToken() {
    if (this->TOKEN == "") {
        return "Authorization not completed, use the auth() method before continuing";
    }
    else {
        return this->TOKEN;
    }
}

bool authControl::checkAuth() {
    return this->getToken() == "";
}

clientCredentials::clientCredentials(std::string ID, std::string SECRET) : authControl(ID, SECRET) {}

oAuth::oAuth(std::string ID, std::string SECRET, std::string oAuthToken, std::string REDIRECT_URI, std::string STATE, std::string SCOPE, bool SHOW_DIALOG) : authControl(ID, SECRET) {
    this->oAuthToken = oAuthToken; 
    this->REDIRECT_URI = REDIRECT_URI;
    this->STATE = STATE;
    this->SCOPE = SCOPE;
    this->SHOW_DIALOG = SHOW_DIALOG;

    std::vector<std::string> tokens = this->auth();
    this->TOKEN = tokens[0];
    this->REFRESH_TOKEN = tokens[1];
}

std::string urlEncEasy(std::string url) {
    std::string res;

    for (auto c : url) {
        if (c == ':') {
            res += "%3A";
        }
        else if (c == '/') {
            res += "%2F";
        }
        else {
            res += c;
        }
    }
    
    return res;
}

std::vector<std::string> oAuth::auth() {
    CURL *curl;
    std::string res;

    curl = curl_easy_init();
    
    if(curl) {
        try {
            curl_easy_setopt(curl, CURLOPT_TCP_NODELAY, 0);
            curl_easy_setopt(curl, CURLOPT_URL, "https://accounts.spotify.com/api/token");

            std::string body = "grant_type=authorization_code&code=" + this->getAuthToken() + "&redirect_uri=" + urlEncEasy(this->getRedirectURI());

            curl_easy_setopt(curl, CURLOPT_POSTFIELDS, body.c_str());     
            curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, this->WriteCallback);
            curl_easy_setopt(curl, CURLOPT_WRITEDATA, &res);

            std::string enc = this->base64_encode(reinterpret_cast<const unsigned char*>((this->getClientID() + ":" + this->getClientSecret()).data()), (this->getClientID() + ":" + this->getClientSecret()).length(), false);
            
            std::string encType = "Content-Type: application/x-www-form-urlencoded";
            std::string httpAuth = "Authorization: Basic " + enc;
            struct curl_slist *authChunk = nullptr;
            authChunk = curl_slist_append(authChunk, encType.c_str());
            authChunk = curl_slist_append(authChunk, httpAuth.c_str());

            curl_easy_setopt(curl, CURLOPT_HTTPHEADER, authChunk);

            curl_easy_perform(curl);
            curl_easy_cleanup(curl);
        }
        catch (const char* Exception) {
            std::cerr << Exception << std::endl;
        }
    }

    std::cout << res << std::endl;

    auto j = nlohmann::json::parse(res);
    return std::vector<std::string> {to_string(j["access_token"]), to_string(j["refresh_token"])};
}

std::string oAuth::reAuth() {
    CURL *curl;
    std::string res;

    curl = curl_easy_init();
    
    if(curl) {
        try {
            curl_easy_setopt(curl, CURLOPT_TCP_NODELAY, 0);
            curl_easy_setopt(curl, CURLOPT_URL, "https://accounts.spotify.com/api/token");

            std::string body = "grant_type=refresh_token&refresh_token=" + this->getRefreshToken();

            curl_easy_setopt(curl, CURLOPT_POSTFIELDS, body.c_str());     
            curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, this->WriteCallback);
            curl_easy_setopt(curl, CURLOPT_WRITEDATA, &res);

            std::string enc = this->base64_encode(reinterpret_cast<const unsigned char*>((this->getClientID() + ":" + this->getClientSecret()).data()), (this->getClientID() + ":" + this->getClientSecret()).length(), false);
            
            std::string encType = "Content-Type: application/x-www-form-urlencoded";
            std::string httpAuth = "Authorization: Basic " + enc;
            struct curl_slist *authChunk = nullptr;
            authChunk = curl_slist_append(authChunk, encType.c_str());
            authChunk = curl_slist_append(authChunk, httpAuth.c_str());

            curl_easy_setopt(curl, CURLOPT_HTTPHEADER, authChunk);

            curl_easy_perform(curl);
            curl_easy_cleanup(curl);
        }
        catch (const char* Exception) {
            std::cerr << Exception << std::endl;
        }
    }

    std::cout << res << std::endl;

    auto j = nlohmann::json::parse(res);
    return to_string(j["access_token"]);
}

std::string oAuth::getRedirectURI() {
    return this->REDIRECT_URI;
}

std::string oAuth::getAuthToken() {
    return this->oAuthToken;
}

std::string oAuth::getRefreshToken() {
    return this->REFRESH_TOKEN;
}

std::string oAuth::getScope() {
    return this->SCOPE;
}

std::string oAuth::getState() {
    return this->STATE;
}

bool oAuth::getDialog() {
    return this->SHOW_DIALOG;
}