from config import GENRES, MIN_MAX_FIELDS, VALID_URL_ARGS

class ErrMsgBuilder:
    """
    A utility class for building an error msg.
    Each function adds specific info to the msg.
    """
    def __init__(self):
        self.msg = ""
        
    def add_invalid_argument_error(self, arg):
        """For invalid argument/attribute in the HTTP query string"""

        self.msg = f"&emsp;Invalid request argument: {arg}<br>"
        return self

    def add_missing_argument_error(self):
        """For no argument in the HTTP query string"""

        self.msg = "Please provide at least one input argument.<br>"
        return self
    
    def add_invalid_key_error(self):
        """For invalid input key"""

        self.msg += "&emsp;Key must be an int between 0 to 11, inclusive. 0 represents C. 11 represents B.<br>"
        return self
        
    def add_invalid_genre_error(self, genre):
        """For invalid genre string"""

        self.msg += f"&emsp;{genre} is not a genre in our dataset. Available genres include rap, r&b, edm, pop, rock, latin<br>"
        return self

    def add_invalid_mode_error(self):
        """For invalid mode"""

        self.msg += "&emsp;Mode must an int with value of either 0 or 1.<br>"
        return self

    def add_invalid_numeric_bounds_error(self):
        """For invalid tempo or duration"""

        if "Tempo (BPM)" not in self.msg:
            self.msg += "&emsp;Tempo (BPM) and duration (milliseconds) must be integers more than zero<br>"
        return self
        
    def add_invalid_search_by_error(self):
        """For invalid search_by route parameter"""

        self.msg += "&emsp;search_by must be either \"song\", \"artist\", or \"none\".<br>"
        return self

    def finalize_error_message(self):
        """For closing the err msg before returning it to the user"""

        self.msg = "Invalid input:<br>" + self.msg + "Check homepage for more instructions"
        return self

def get_attr_errors(attrs : dict):
    """
    Returns an error message if there is an invalid attribute in the URL.
    Else, return None.
    """

    err = ErrMsgBuilder()

    attr_names = attrs.keys()
    
    for attr in attr_names: # If the url has invalid parameters
        if attr not in VALID_URL_ARGS:
            err.add_invalid_argument_error(attr)
    if err.msg != "": # If there is an invalid parameter
        err.finalize_error_message()
        return err.msg

    return None

def get_single_value_err(attrs) -> str:
    """
    Check if the values provided in the query string is valid
    
    Returns None if valid.
    Returns an err msg if invalid.
    """

    err = ErrMsgBuilder()

    if not is_valid_key(attrs["key"]):
        err.add_invalid_key_error()
    if not is_valid_mode(attrs["mode"]):
        err.add_invalid_mode_error()
    if not is_valid_bound([attrs[val] for val in MIN_MAX_FIELDS]):
        err.add_invalid_numeric_bounds_error()
    if not is_valid_genre(attrs["genre"]):
        err.add_invalid_genre_error(attrs["genre"])
    if not is_valid_search_by(attrs):
        err.add_invalid_search_by_error()

    if err.msg != "":
        err.finalize_error_message()
        return err.msg
    return None

def is_valid_search_by(attrs):
    """Check if the route parameter search_by is valid.
    
    Returns true if attrs is one of the following:
        -- "none"
        -- "track_name"
        -- "artist"
        AND the attrs dictionary value for search_by is not None
    """
    search_by = attrs["search_by"]

    if search_by is None or search_by.lower() == "none":
        return True
    if search_by in [None, "track_name","artist"]:
        return True
    return False

def is_valid_genre(genre_str) -> bool:
    """Check if input is a valid genre
    
    Returns true if one of the following:
        -- input is None
        -- input is a string that contains genres separated by a comma, where each genre is a genre in our dataset
    
    Example: "pop,rap,latin" should return true
    """

    if genre_str is None or genre_str == "":
        return True
    
    all_selected_genres = genre_str.split(",")
    for genre in all_selected_genres:
        if genre not in GENRES:
            return False
    return True

def is_valid_bound(values : list) -> bool:
    """Check if list of values is a valid bound (or quantitative) variable
    
    Returns true if one of the following:
        -- all non-None elements are int-convertible
    """

    for v in values:
        if v is not None and v != "":
            if not is_float(v):
                return False    
    
    return True

def is_valid_mode(mode) -> bool:
    """Check if input is a valid mode
    
    Returns true if one of the following:
        -- input is None
        -- input is 0
        -- input is 1
    """

    if mode is None or mode == "":
        return True
    if not is_int(mode):
        return False
    
    mode = int(mode)
    if mode != 1 and mode != 0:
        return False
    return True
    
def is_valid_key(key) -> bool:
    """Check if input is a valid key.
    
    Returns true if one of the following:
        -- value is int-convertible and >=0 and <= 11
        -- value is None
    """

    if key is None or key == "":
        return True
    if not is_int(key):
        return False
    key = int(key)
    if key > 11 or key < 0:
        return False
    return True

def is_int(item) -> bool:
    """Returns true if convertible to int. False otherwise."""
    
    try:
        int(item)
    except:
        return False
    return True

def is_float(item) -> bool:
    """Returns true if convertible to float. False otherwise."""
    
    try:
        float(item)
    except:
        return False
    return True

