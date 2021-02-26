#include "../module/CPPotify.h"
#include "../module/authControl.h"
#include <iostream>
#include <chrono>

using namespace std;


int main(){
    
    std::string CLIENT_ID = "ff898288f3a747bba87c39d33c29a3c0";
    std::string CLIENT_SECRET = "fb6ec63e1a6043baa59ea863b8e1235b";
    std::string REDIRECT_URI = "https://example.com/callback";
    std::string STATE = "34fFs29kd09";
    std::string SCOPE = "user-read-private user-read-email user-modify-playback-state";
    bool SHOW_DIALOG = false;
    //CPPotify cpp = {CLIENT_ID, CLIENT_SECRET, "AQCY6AZElVppDDFLoge3p7MR2E9VGDf8AmRMbB5N_9N3IMWmGNskmPiObM483sRhmQS9sEvve8erA-lNJhSMYN2WDgIpVdIaNpFaVTjY3ysCUYwkOJWube3WMqggl8fL3lB3D6ztGSDWRiLqWhGN0hui9ABdVeRjAdvu1DUH6dv5QpgvnUqGl_0yzzUoE2d3DAvzUnHPbAYPBm3iMYTH34neHMGIYW7hwGd7yqwnpASz781Mgabz0iYg2DdmiSzI", REDIRECT_URI, STATE, SCOPE, SHOW_DIALOG};
    CPPotify cpp = {CLIENT_ID, CLIENT_SECRET};
    cout << cpp.getTracks("0psS4i5YooJrXfDnGvWRLi")[1] << endl;
    
    //cout << ac.auth() << endl;
    //cout << cpp.search("weezer", "track", std::map<std::string, std::string>{}, 2, 0)[1] << endl;

    return 0;
}