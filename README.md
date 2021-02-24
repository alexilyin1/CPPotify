# CPPotify
A Python wrapper for the Spotify API built with C++ doing the heavy lifting. Takes advantage of the libcurl C++ library to make HTTP requests

## Installation

To use this library:

1. Clone the git repo

```
$ git clone https://github.com/alexilyin1/CPPotify.git && cd CPPotify/
```

2. Build the C++ package using CMake (make sure you are in the CPPotify directory after Step 1)

```
$ cmake ./
$ cmake --build ./
```

3. Install the requirements included in ```requirements.txt```

```
$ pip install -r requirements.txt
```

4. Make sure so include the location of the 'shared library' file in ```sys.path``` whenever importing CPPotify

```
# test.py

import sys
sys.path.insert(0, './CPPotify/source/py')
from CPPotify import CPPotify

cpp = CPPotify(CLIENT_ID, CLIENT_SECRET)
cpp.get_albums('abcd')
```

## Issues

Raise issues here, on [my website](alexilyin.me), or through [email](mailto:alexi20@mailfence.com?subject=CPPotify%20Issues)
