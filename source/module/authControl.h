#ifndef AUTHCONTROL_H
#define AUTHCONTROL_H

#include <string>
#include <vector>

/* Base Class */ 
class authControl {
private:
    std::string CLIENT_ID;
    std::string CLIENT_SECRET;
    std::string TOKEN = "";

public:
    authControl();
    authControl(std::string ID);
    authControl(std::string ID, std::string SECRET);
    ~authControl();

    /*
    C++ Base 64 encoding method borrowed from 
    https://renenyffenegger.ch/notes/development/Base64/Encoding-and-decoding-base-64-with-cpp

    (C) 2004-2017, 2020 René Nyffenegger
    */
    std::string base64_encode(unsigned char const* bytes_to_encode, size_t in_len, bool url);

    static size_t WriteCallback(void *contents, size_t size, size_t nmemb, void *userp);

    virtual std::vector<std::string> auth();
    virtual std::string reAuth();

    std::string setToken();
    std::string getClientID();
    std::string getClientSecret();
    std::string getToken();
    bool checkAuth();
};

/* Client Credentials authorization */
class clientCredentials : public authControl {
public:
    clientCredentials(std::string ID, std::string SECRET);
};

/* oAuth authorization */
class oAuth : public authControl {
private:
    std::string oAuthToken;
    std::string TOKEN;
    std::string REDIRECT_URI; 
    std::string STATE;
    std::string SCOPE; 
    bool SHOW_DIALOG;
    std::string REFRESH_TOKEN;

public:
    oAuth(std::string CLIENT_ID, std::string CLIENT_SECRET, std::string oAuthToken, std::string REDIRECT_URI, std::string STATE = "34fFs29kd09", std::string SCOPE = "user-read-private user-read-email", bool SHOW_DIALOG = false);

    std::vector<std::string> auth();
    std::string reAuth();

    std::string getAuthToken();
    std::string getRefreshToken();
    std::string getRedirectURI();
    std::string getState();
    std::string getScope();
    bool getDialog();
};

#endif
