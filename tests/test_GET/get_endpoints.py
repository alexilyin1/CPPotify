import sys
sys.path.insert(0, '../../source/py')
from CPPotify import CPPotify

import unittest 
from keys import *


class GetAlbums(unittest.TestCase):

    def test_objects(self):
        self.CLIENT_ID = CLIENT_ID
        self.CLIENT_SECRET = CLIENT_SECRET

        self.album_ids = ['7rhO7zOEFdz8v5tdSC6JZA',
                         '2hiPqMWbwko9fxKd1JWUI1',
                         '4SEnNV8uDJVi1244tnjeEc']

        self.cppotify_obj = CPPotify(self.CLIENT_ID, self.CLIENT_SECRET)
        
        self.album_keys = [
                        'album_type',
                        'artists',
                        'available_markets',
                        'copyrights',
                        'external_ids',
                        'external_urls',
                        'genres',
                        'href',
                        'id',
                        'images',
                        'label',
                        'name',
                        'popularity',
                        'release_date',
                        'release_date_precision',
                        'restrictions',
                        'tracks',
                        'type',
                        'uri'
                    ]

    def get_album(self):
        for id in self.album_ids:
            album = self.cppotify_obj.get_albums(id)

            for key in self.album_keys:
                self.assertIn(key, album.keys())

            self.assertNotIn('error', album.keys())

    def get_album_tracks(self):
        for id in self.album_ids:
            tracks = self.cppotify_obj.get_albums(id, 'tracks')

            self.assertIn('items', tracks.keys())
            self.assertNotIn('error', tracks.keys())
            
