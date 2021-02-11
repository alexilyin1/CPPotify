#include "../module/CPPotify.h"
#include "../module/authControl.h"
#include <iostream>
#include <chrono>

using namespace std;


int main(){
    std::string id = "7EgBkZlqWRwvjmyc115LLR";
    cout << to_string(id.size()) << endl;
    
    string CLIENT_ID = "ff898288f3a747bba87c39d33c29a3c0";
    string CLIENT_SECRET = "fb6ec63e1a6043baa59ea863b8e1235b";
    string REDIRECT_URL = "https://example.com/callback";
    oAuth ac = {CLIENT_ID, CLIENT_SECRET, REDIRECT_URL};
    //cout << cpp.search("weezer", "track", std::map<std::string, std::string>{}, 2, 0)[1] << endl;

    return 0;
}