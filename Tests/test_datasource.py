import unittest
import ProductionCode.datasource as ds

#IF WE HAVE TIME: do test for get_songs_by_attribute

class Test_ProductionCode(unittest.TestCase):
    
    def test_get_filter_data_query_str(self):
        reference = [({"key": None,
                "mode": "",
                "genre": "alt-rock",
                "track_name": "", 
                "track_id": "",
                "artist": "",
                "tempo": (None, ""),
                "duration_ms": (None, None),
                "popularity": ("",""),
                "year_released": ("2014","2016"),
                "danceability": ("0.5",None),
                "energy": ("0.6",""),
                "loudness": ("","-3"),
                "valence": (None,"0.9"),
                "search":("track_name", "Love")
                },
                "SELECT * FROM songs WHERE genre ~ 'alt-rock' AND year_released >= 2014 AND year_released <= 2016 AND danceability >= 0.5 AND energy >= 0.6 AND loudness <= -3 AND valence <= 0.9 AND track_name ~* '.*(Love).*' ORDER BY popularity DESC;",
                "Multiple"),

                #EDGE CASE
                ({"key": None,
                "mode": None,
                "genre": None,
                "track_name": None, #track name
                "track_id": None,
                "artist": None,
                "tempo": (None, None),
                "duration_ms": (None, None),
                "popularity": (None,None),
                "year_released": (None,None),
                "danceability": (None,None),
                "energy": (None,None),
                "loudness": (None,None),
                "valence": (None,None),
                "search":(None,None)
                },
                "SELECT * FROM songs ORDER BY popularity DESC;",
                "All none"),

                #EDGE CASE
                ({"key": "",
                "mode": "",
                "genre": "",
                "track_name": "", #track name
                "track_id": "",
                "artist": "",
                "tempo": ("", ""),
                "duration_ms": ("", ""),
                "popularity": ("",""),
                "year_released": ("",""),
                "danceability": ("",""),
                "energy": ("",""),
                "loudness": ("",""),
                "valence": ("",""),
                "search":("","")
                },
                None,
                "All empty")
        ]

        for i in range(len(reference)):
            print(ds.DataSource.get_filter_data_query_str(reference[i][0],"popularity"))
            self.assertEqual(ds.DataSource.get_filter_data_query_str(reference[i][0], "popularity"), reference[i][1], reference[i][2])
    
    def test_get_attribute_type(self):
        reference = [
            ("track_name", "str"),
            ("artist", "str"),
            ("track_id", "str"),
            ("genre", "multiple"),
            ("key", "single"),
            ("mode", "single"),
            ("search", "search"),
            ("popularity", "bound"),
            ("year_released", "bound"),
            ("danceability", "bound"),
            ("energy", "bound"),
            ("loudness", "bound"),
            ("valence", "bound"),
            ("tempo", "bound"),
            ("duration_ms", "bound"),
            ("nionoiewng", None) #Edge case
        ]

        for item in reference:
            attr = item[0]
            expected_type = item[1]
            self.assertEqual(ds.DataSource.get_attribute_type(attr), expected_type, f"Failed for attribute: {attr}")

if __name__ == '__main__':
    unittest.main()