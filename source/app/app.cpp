#include "../module/CPPotify.h"
#include "../module/authControl.h"
#include <iostream>
#include <chrono>

using namespace std;


int main(){
    
    string CLIENT_ID = "ff898288f3a747bba87c39d33c29a3c0";
    string CLIENT_SECRET = "fb6ec63e1a6043baa59ea863b8e1235b";
    string REDIRECT_URL = "https://example.com/callback";
    oAuth ac = {CLIENT_ID, CLIENT_SECRET, REDIRECT_URL, "AQAOR2HsawRHrhvrdN_u2vD0xtFgDqLm9gHRwx5OcvCEXtBlNxOr7b5RfJBNUgWxclfGUnCaqm0JVysEAmLddXBaazoyTzw5D5s9F4lQX5UhCy-BNp0JkJ19sj0TleMAqfU3EtkxyrgjwiFkG4NfeT9vSRSh_9OMNIQ-CzSr9dD-VFWLXYZAgzOf09B6kPSTwsLgIywrwvbNVrR0gEorQv4MLsg"};
    cout << ac.auth() << endl;
    //cout << cpp.search("weezer", "track", std::map<std::string, std::string>{}, 2, 0)[1] << endl;

    return 0;
}