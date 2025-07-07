import unittest
from flask_app import *
from err_check import *

#In the VScode terminal, run this command: 
# source ~/.venvs/cs257_venv/bin/activate
# python3 -m unittest discover Tests/

class Test_Flask(unittest.TestCase):

    def setUp(self): #runs before each test method
        '''Sets up the test client for the Flask app.'''
        self.client = app.test_client()

    def test_500_error(self): #this returns 400 error :(
        '''Tests the 500 error handler of the Flask application created in the ind_flask_app.py file.
        A bug must exist in the search_for_song() function in the ind_flask_app.py for this test to pass.'''
        error_message_500 = """<html>

<head>
    <title>500 Error</title>
    <link rel="stylesheet" href="../static/datastyle.css">
</head>

<body>
    
    <nav>
        <ul>
            <li><a href="/">Search</a></li>
            <li><a href="/playlist">Your Playlist</a></li>
            <li><a href="/about/">About</a></li>
        </ul>
    </nav>
    <p>We are experiencing some bugs! We'll try to fix them as soon as possible.</p>
    <p>Please stay tuned, or try a different query.</p>
</body>
</html>"""
        response = self.client.get('/trigger-error-500', follow_redirects=True)
        self.assertEqual(response.status_code, 200) #check for a successful request
        self.assertIn(error_message_500.encode("utf-8"), response.data)

    def test_route_standard(self):
        """Tests standard cases for the /search route and /uniqueartists route"""
        #Each item is a tuple consisting of (1) url, and (2) Expected song names returned by the server, in order .
        reference = []
        reference.append(("/search?key=8","Kill Bill", "1")) #single attribute for filter_data
        reference.append(("/search?min_tempo=124&max_tempo=126&max_duration=200000&min_duration=170000","The Nights", "2")) #Multiple attributes for filter_data
        reference.append(("/search?search_by=artist&substr=Lewis","Before You Go", "3")) #Test for search_by_substr
        reference.append(("/search?search_by=track_name&substr=call|you&min_tempo=124", "Made You Look", "5")) #Test for search_by_substr and filter_data
        reference.append(("/search?max_duration=170000", "Kill Bill","6"))        
        reference.append(("/search?genre=pop&search_by=artist&substr=Ed Sheeran","Perfect","8"))
        reference.append(("/search?key=5","Snooze", "10"))
        reference.append(("/search?key=1&mode=0","Die For You - Remix","11"))
        reference.append(("/search?min_tempo=122&max_tempo=123","Lay Low", "14"))
        reference.append(("/search?genre=pop&min_tempo=121&max_tempo=125&min_duration=175000&max_duration=195000","Sacrifice","17"))

        #Loop through reference: send url to server -> get response -> format response into list -> compare to expected list
        for i in range(len(reference)):
            response = self.client.get(reference[i][0], follow_redirects=True) #requests.get(reference[i][0]).text #Send a GET Request to the server and retrieve the response
            response = response.data.decode("utf-8")
           
            expected_first_song_title = reference[i][1]
            unit_test_msg = reference[i][2]

            self.assertIn(expected_first_song_title, response, unit_test_msg)

    def test_route_standard_empty(self):
        """Test for valid URLS where no songs satisfies the conditions specified by the URL query string"""

        #Each item in reference is a tuple consisting of (1) url that should return no songs, and (2) unittest assert msg
        reference = []
        no_songs_msg = "No songs match the input conditions"

        #Tempo
        reference.append(("/search?min_tempo=200&max_tempo=100", "min_tempo=200&max_tempo=100"))
        reference.append(("/search?min_tempo=120.000000001&max_tempo=120.000000002", "min_tempo=120.000000001&max_tempo=120.000000002"))
        reference.append(("/search?min_tempo=998&max_tempo=999", "min_tempo=998&max_tempo=999"))

        #Duration
        reference.append(("/search?min_duration=80000&max_duration=70000", "min_duration=80000&max_duration=70000"))
        reference.append(("/search?min_duration=80000.000000001&max_duration=80000.000000002", "min_duration=120.000000001&max_duration=120.000000002"))
        reference.append(("/search?min_duration=999999999999&max_duration=999999999998", "min_duration=999999999998&max_duration=999999999999"))

        #Popularity
        reference.append(("/search?min_popularity=50&max_popularity=49", "min_popularity=50&max_popularity=49"))
        reference.append(("/search?min_popularity=50.000000001&max_popularity=50.000000002", "min_popularity=50.000000001&max_popularity=50.000000002"))

        #Danceability
        reference.append(("/search?min_danceability=0.50&max_danceability=0.49", "min_danceability=0.50&max_danceability=0.49"))
        reference.append(("/search?min_danceability=0.50000000001&max_danceability=0.50000000002", "min_danceability=0.50000000001&max_danceability=0.50000000002"))

        #Energy
        reference.append(("/search?min_energy=0.50&max_energy=0.49", "min_energy=0.50&max_energy=0.49"))
        reference.append(("/search?min_energy=0.50000000001&max_energy=0.50000000002", "min_energy=0.50000000001&max_energy=0.50000000002"))

        #Valence
        reference.append(("/search?min_valence=0.50&max_valence=0.49", "min_valence=0.50&max_valence=0.49"))
        reference.append(("/search?min_valence=0.50000000001&max_valence=0.50000000002", "min_valence=0.50000000001&max_valence=0.50000000002"))

        #Year
        reference.append(("/search?min_year=2005&max_year=2004", "min_year=2005&max_year=2004"))
        reference.append(("/search?min_year=2005.8&max_year=2004.2", "min_year=2005.8&max_year=2004.2"))
        reference.append(("/search?min_year=1990&max_year=1999", "min_year=1990&max_year=1999"))
        reference.append(("/search?min_year=2024&max_year=2029", "min_year=2024&max_year=2029"))

        #Multiple
        reference.append(("/search?search_by=artist&substr=Taylor+Swift&genre=dancehall", "search_by=artist&substr=Taylor+Swift&genre=dancehall"))
        reference.append(("/search?search_by=artist&substr=Taylor+Swift&min_tempo=209", "search_by=artist&substr=Taylor+Swift&min_tempo=209"))
        reference.append(("/search?genre=dancehall&max_tempo=35", "genre=dancehall&max_tempo=35"))
        
        #Loop through reference: send request to flask app -> get response -> compare to expected
        for i in range(len(reference)):
            response = self.client.get(reference[i][0], follow_redirects=True) 
            response = response.data.decode("utf-8")
            self.assertEqual(response, no_songs_msg, reference[i][1])

    def test_route_edge(self):
        """Tests if the website displays expected err msg when URL or query string is invalid.
        Relevant routes tested: ('/search/')"""
        
        #Each item is a tuple consisting of (1) url, (2) expected error msg for user, and (3) unittest assert msg.
        reference = []

        #Invalid attributes
        reference.append(("/search?donkey=1", ErrMsgBuilder().add_invalid_argument_error("donkey").finalize_error_message().msg, "/search?donkey=1"))
        reference.append(("/search?donkey=1&banana=3&key=1", ErrMsgBuilder().add_invalid_argument_error("donkey").add_invalid_argument_error("banana").finalize_error_message().msg, "/search?donkey=1&banana=3&key=1"))

        # Invalid key
        key_err_msg = ErrMsgBuilder().add_invalid_key_error().finalize_error_message().msg
        reference.append(("/search?key=-1", key_err_msg, "key=-1"))
        reference.append(("/search?key=12", key_err_msg, "key=12"))
        reference.append(("/search?key=-11", key_err_msg, "key=-11"))

        #Invalid mode
        mode_err_msg = ErrMsgBuilder().add_invalid_mode_error().finalize_error_message().msg
        reference.append(("/search?mode=2", mode_err_msg, "mode=2"))
        reference.append(("/search?mode=-1", mode_err_msg, "mode=-1"))

        #Invalid min_tempo, max_tempo, min_duration, or max_duration
        bound_limits_err_msg = ErrMsgBuilder().add_invalid_numeric_bounds_error().finalize_error_message().msg
        reference.append(("/search?min_tempo=andante", bound_limits_err_msg, "min_tempo=andante"))

        #Invalid genre
        reference.append(("/search?genre=popp", ErrMsgBuilder().add_invalid_genre_error("popp").finalize_error_message().msg, "genre=popp"))
        reference.append(("/search?genre=1", ErrMsgBuilder().add_invalid_genre_error("1").finalize_error_message().msg, "genre=1"))

        #Invalid search_by
        search_by_err = ErrMsgBuilder().add_invalid_search_by_error().finalize_error_message().msg
        reference.append(("/search?search_by=dog", search_by_err, "search_by=dog"))

        #Multiple invalids
        reference.append(("/search?search_by=dog&mode=-1&genre=banana&max_tempo=speedy",ErrMsgBuilder().add_invalid_mode_error().add_invalid_numeric_bounds_error().add_invalid_genre_error("banana").add_invalid_search_by_error().finalize_error_message().msg, "/search_by=artist&mode=-1&genre=banana&max_tempo=speedy"))

        for i in range(len(reference)):
            response = self.client.get(reference[i][0], follow_redirects=True) #requests.get(reference[i][0]).text #Send a GET Request to the server and retrieve the response
            response = response.data.decode("utf-8")
            self.assertEqual(response, reference[i][1],reference[i][2])

    #----------------------------TEST FOR FLASK-SPECIFIC FUNCTIONS-----------------------------------

    def test_get_attr_errors(self):
        """Test if the get_attr_errors function works as expected"""

        reference = []

        #Standard cases
        reference.append(({"mode" : 30}, None, "wrong mode value"))
        reference.append(({"mode" : 1}, None, "correct mode value"))
        reference.append(({"mode" : 1, "key" : 7, "genre" : "pop"}, None, "multiple"))

        #Edge cases
        reference.append(({"asdeafwewegweg" : 3}, ErrMsgBuilder().add_invalid_argument_error("asdeafwewegweg").finalize_error_message().msg, "invalid attr: asdeafwewegweg"))
        reference.append(({"mode" : 1,"donkey" : 3, "key" : 7}, ErrMsgBuilder().add_invalid_argument_error("donkey").finalize_error_message().msg, "invalid attr: donkey"))

        for i in range(len(reference)):
            self.assertEqual(get_attr_errors(reference[i][0]), reference[i][1], reference[i][2])


    def test_get_single_value_err(self):
        """Test if the get_single_value_err function works as expected"""

        reference = []
        # mins_maxes_actual_name = ["popularity", "year_released", "danceability", "energy", "loudness", "valence", "tempo", "duration_ms"]


        #Standard cases
        
        reference.append(({"mode" : 1, "key" : 7, "search_by": "track_name", "substr" : "call", "artist": "Swift", "min_year": 2014, "max_year": 2020, 
                        "min_popularity": 1, "max_popularity": 40, "min_danceability": .3, "max_danceability": .7, 
                        "min_energy": .3, "max_energy": .7, "min_loudness": None, "max_loudness": .7, "min_valence": .2, "max_valence": .7,
                        "min_tempo" : 100, "max_tempo" : None, "min_duration" : 300000, "max_duration" : 500000, "genre" : "pop"},
                        None, "Multiple non-None values + search_by_substr"))
        reference.append(({"mode" : 1, "key" : None, "search_by": None, "substr" : None, "artist": None, "min_year": None, "max_year": None, 
                        "min_popularity": None, "max_popularity": None, "min_danceability": None, "max_danceability": None, 
                        "min_energy": None, "max_energy": None, "min_loudness": None, "max_loudness": None, "min_valence": None, "max_valence": None,
                        "min_tempo" : None, "max_tempo" : None, "min_duration" : None, "max_duration" : None, "genre" : None}, None, "One non-None value"))

        #Edge case
        reference.append(({"mode" : -2, "key" : 20, "search_by": "apple", "substr" : "call", "artist": "Swift", "min_year": 2014, "max_year": 2020, 
                        "min_popularity": 1, "max_popularity": 40, "min_danceability": .3, "max_danceability": .7, 
                        "min_energy": "no", "max_energy": "yes", "min_loudness": None, "max_loudness": .7, "min_valence": .2, "max_valence": .7,
                        "min_tempo" : 100, "max_tempo" : None, "min_duration" : 300000, "max_duration" : 500000, "genre" : "rapp"},
                            ErrMsgBuilder().add_invalid_key_error().add_invalid_mode_error().add_invalid_numeric_bounds_error().add_invalid_genre_error("rapp").add_invalid_search_by_error().finalize_error_message().msg,
                            "Multiple invalid values"))
        
        for i in range(len(reference)):
            self.assertEqual(get_single_value_err(reference[i][0]), reference[i][1], reference[i][2])

    
    def test_is_valid_search_by(self):
        """Test if the is_valid_search_by function correctly identifies valid or invalid search_by"""

        reference = []

        #Standard cases
        reference.append(({"mode" : "1", "key" : "7", "search_by": "track_name", "substr" : "call", "artist": "Swift", "min_year": 2014, "max_year": 2020, 
                        "min_popularity": 1, "max_popularity": 40, "min_danceability": .3, "max_danceability": .7, 
                        "min_energy": .3, "max_energy": .7, "min_loudness": .3, "max_loudness": .7, "min_valence": .2, "max_valence": .7,
                        "min_tempo" : "100", "max_tempo" : "300", "min_duration" : "300000", "max_duration" : "500000", "genre" : "pop"},
                        True, "artist"))
        reference.append(({"mode" : "1", "key" : "7", "search_by": None, "substr" : "", "artist": "Swift", "min_year": 2014, "max_year": 2020, 
                        "min_popularity": 1, "max_popularity": 40, "min_danceability": .3, "max_danceability": .7, 
                        "min_energy": .3, "max_energy": .7, "min_loudness": .3, "max_loudness": .7, "min_valence": .2, "max_valence": .7,
                        "min_tempo" : "100", "max_tempo" : "300", "min_duration" : "300000", "max_duration" : "500000", "genre" : "pop"},
                        True, "none"))

        #Edge cases
        reference.append(({"mode" : "1", "key" : "7", "search_by": "track_name", "substr" : None, "artist": "Swift", "min_year": 2014, "max_year": 2020, 
                        "min_popularity": 1, "max_popularity": 40, "min_danceability": .3, "max_danceability": .7, 
                        "min_energy": .3, "max_energy": .7, "min_loudness": .3, "max_loudness": .7, "min_valence": .2, "max_valence": .7,
                        "min_tempo" : "100", "max_tempo" : "300", "min_duration" : "300000", "max_duration" : "500000", "genre" : "pop"},
                        True, "song is None"))
        reference.append(({"mode" : "1", "key" : "7", "search_by": "track_name", "substr" : "", "album" : None, "artist": "Swift", "min_year": 2014, "max_year": 2020, 
                        "min_popularity": 1, "max_popularity": 40, "min_danceability": .3, "max_danceability": .7, 
                        "min_energy": .3, "max_energy": .7, "min_loudness": .3, "max_loudness": .7, "min_valence": .2, "max_valence": .7,
                        "min_tempo" : "100", "max_tempo" : "300", "min_duration" : "300000", "max_duration" : "500000", "genre" : "pop"},
                        True, "song is empty"))
        reference.append(({"mode" : "1", "key" : "7", "search_by": "artist", "substr" : "", "album" : None, "artist": "Swift", "min_year": 2014, "max_year": 2020, 
                        "min_popularity": 1, "max_popularity": 40, "min_danceability": .3, "max_danceability": .7, 
                        "min_energy": .3, "max_energy": .7, "min_loudness": .3, "max_loudness": .7, "min_valence": .2, "max_valence": .7,
                        "min_tempo" : "100", "max_tempo" : "300", "min_duration" : "300000", "max_duration" : "500000", "genre" : "pop"},
                        True, "artist is None"))
        reference.append(({"mode" : "1", "key" : "7", "search_by": "artist", "substr" : "", "album" : None, "artist": "Swift", "min_year": 2014, "max_year": 2020, 
                        "min_popularity": 1, "max_popularity": 40, "min_danceability": .3, "max_danceability": .7, 
                        "min_energy": .3, "max_energy": .7, "min_loudness": .3, "max_loudness": .7, "min_valence": .2, "max_valence": .7,
                        "min_tempo" : "100", "max_tempo" : "300", "min_duration" : "300000", "max_duration" : "500000", "genre" : "pop"},
                        True, "artist is empty"))
        reference.append(({"mode" : "1", "key" : "7", "search_by": "basoef", "substr" : "", "album" : None, "artist": "Swift", "min_year": 2014, "max_year": 2020, 
                        "min_popularity": 1, "max_popularity": 40, "min_danceability": .3, "max_danceability": .7, 
                        "min_energy": .3, "max_energy": .7, "min_loudness": .3, "max_loudness": .7, "min_valence": .2, "max_valence": .7,
                        "min_tempo" : "100", "max_tempo" : "300", "min_duration" : "300000", "max_duration" : "500000", "genre" : "pop"},
                        False, "bad search_by"))

        for i in range(len(reference)):
            self.assertEqual(is_valid_search_by(reference[i][0]), reference[i][1], reference[i][2])

    def test_is_valid_genre(self):
        """Test if the is_valid_genre function correctly identifies valid or invalid genre strings"""

        reference = []

        #Standard cases
        reference.append(("alt-rock,pop,dancehall,psych-rock,edm,rock",True,"6 genres"))
        genres = ["alt-rock", "dance", "dancehall" , "detroit-techno", "edm" , "electro" , "electronic" ,"hard-rock", "indie-pop", 
          "k-pop" , "minimal-techno" , "pop",  "power-pop", "psych-rock", "punk-rock", "rock", "rock-n-roll", "techno"]
        reference.append(("edm,edm,edm,edm",True,"4 edms"))
        reference.append(("edm",True,"1 genre"))
        reference.append((None,True,"none"))
        reference.append(("",True,"empty string"))

        #Edge cases
        reference.append(("popp",False,"wrong genre"))

        for i in range(len(reference)):
            self.assertEqual(is_valid_genre(reference[i][0]), reference[i][1], reference[i][2])
        
    def test_is_valid_bound(self):
        """Test if the is_valid_bound function correctly identifies whether 
        all item in list is suitable for tempo, duration, etc values"""

        reference = []
        
        #Standard case
        reference.append((["1","2","3","4","5","6","7","8","100000", None, None, "9"],True,"standards"))

        #Edge case
        reference.append((["a","1"],False,"string"))
        reference.append((["","1"],True,"Empty string"))

        for i in range(len(reference)):
            self.assertEqual(is_valid_bound(reference[i][0]), reference[i][1], reference[i][2])

    def test_is_valid_mode(self):
        """Test if the is_valid_mode function correctly identifies whether 
        input is a suitable mode (0 = minor, 1 = major)"""

        reference = []
        
        #standard case
        reference.append(("1",True,"Major"))
        reference.append(("0",True,"Minor"))
        reference.append((0+1,True,"int"))
        reference.append((None,True,"None"))
        reference.append(("",True,"empty string"))

        #edge case
        reference.append(("-1",False,"-1"))
        reference.append(("2",False,"2"))
        reference.append(("2-1",False,"2-1"))
        reference.append(("a",False,"a"))

        for i in range(len(reference)):
            self.assertEqual(is_valid_mode(reference[i][0]), reference[i][1], reference[i][2])

    def test_is_valid_key(self):
        """Test if the is_valid_key function returns true if input is one of the valid keys (0 up to 11)
        and return false if otherwise."""

        reference = []

        #standard cases
        reference.append((None,True,"None"))

        for i in range(0,12):
            self.assertEqual(is_valid_key(str(i)), True, f"standard: {i}")
        
        #edge case
        reference.append(("-1",False,"-1"))
        reference.append(("12",False,"12"))
        reference.append(("2-1",False,"2-1"))
        reference.append(("a",False,"a"))
        reference.append(("",True,"empty string"))

        for i in range(len(reference)):
            self.assertEqual(is_valid_mode(reference[i][0]), reference[i][1], reference[i][2])

    def test_is_int(self):
        """Test for a function that should returns true if int-convertible."""

        reference = []

        #Standard cases
        reference.append(("1",True,"1"))
        reference.append(("-1",True,"-1"))
        reference.append(("1241",True,"1241"))
        reference.append(("-6372",True,"-6372"))

        #Edge cases
        reference.append(("-6372.1",False,"-6372.1"))
        reference.append(("0.0000000000000001", False, "Fraction"))
        reference.append(("", False, "Empty string"))
        reference.append((None, False, "None"))

        for i in range(len(reference)):
            self.assertEqual(is_int(reference[i][0]), reference[i][1], reference[i][2])
            
    def test_format_attrs(self):
        """Test for a function that should formats the input_dict by converting to proper types"""

        reference = []
            # mins_maxes_actual_name = ["popularity", "year_released", "danceability", "energy", "loudness", "valence", "tempo", "duration_ms"]


        #Standard case. No edge case since function should only be used on certain input, which is exhaustively captured by these examples.
        attr_dict_1 = {"mode" : 1, "key" : 7, "search_by": "track_name", "substr" : "call", "artist": "Swift", "min_year": 2014, "max_year": 2020, 
                        "min_popularity": 1, "max_popularity": 40, "min_danceability": .3, "max_danceability": .7, 
                        "min_energy": .3, "max_energy": .7, "min_loudness": .3, "max_loudness": .7, "min_valence": .2, "max_valence": .7,
                        "min_tempo" : 100, "max_tempo" : 300, "min_duration" : 300000, "max_duration" : 500000, "genre" : "pop"}
        expected_dict_1 = {"mode" : 1, "key" : 7, "search": ["track_name", "call"], "artist": "Swift", "year_released": [2014, 2020], 
                           "popularity": [1,40], "danceability": [.3, .7], "energy": [.3, .7], "loudness": [.3, .7], "valence": [.2, .7], 
                           "tempo": [100,300], "duration_ms" : [300000,500000], "genre" : "pop"}
        reference.append((attr_dict_1,expected_dict_1, "No None values"))

        attr_dict_2 = {"mode" : None, "key" : None, "search_by": "track_name", "substr" : "call", "artist": "Swift", "min_year": None, "max_year": 2020, 
                        "min_popularity": None, "max_popularity": 40, "min_danceability": .3, "max_danceability": None, 
                        "min_energy": .3, "max_energy": None, "min_loudness": None, "max_loudness": .7, "min_valence": .2, "max_valence": None,
                        "min_tempo" : 100, "max_tempo" : None, "min_duration" : None, "max_duration" : "500000", "genre" : "pop"}
        expected_dict_2 = {"mode" : None, "key" : None, "search": ["track_name", "call"], "artist": "Swift", "year_released": [None, 2020], 
                           "popularity": [None,40], "danceability": [.3, None], "energy": [.3, None], "loudness": [None, .7], "valence": [.2, None], 
                           "tempo": [100,None], "duration_ms" : [None,"500000"], "genre" : "pop"} 
        reference.append((attr_dict_2,expected_dict_2, "Lists are half-None"))


        attr_dict_3 = {"mode" : None, "key" : None, "search_by": None, "substr" : None, "artist": "Swift", "min_year": None, "max_year": None, 
                        "min_popularity": None, "max_popularity": None, "min_danceability": None, "max_danceability": None, 
                        "min_energy": None, "max_energy": None, "min_loudness": None, "max_loudness": None, "min_valence": None, "max_valence": None,
                        "min_tempo" : None, "max_tempo" : None, "min_duration" : None, "max_duration" : None, "genre" : "pop"}
        expected_dict_3 = {"mode" : None, "key" : None, "search": [None, None], "artist": "Swift", "year_released": [None, None], 
                           "popularity": [None,None], "danceability": [None, None], "energy": [None, None], "loudness": [None, None], "valence": [None, None], 
                           "tempo": [None,None], "duration_ms" : [None,None], "genre" : "pop"} 
        reference.append((attr_dict_3,expected_dict_3, "Lists are all None"))

        for i in range(len(reference)):
            self.assertEqual(format_attrs(reference[i][0]), reference[i][1], reference[i][2])

if __name__ == '__main__':
    unittest.main()