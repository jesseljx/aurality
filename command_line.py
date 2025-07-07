import argparse
# import pandas as pds
import err_check as ErrCheck
from ProductionCode.datasource import DataSource
import pandas as pd

data_source = DataSource()

def main():
    
    """python3 command_line.py [-h] [-k [0|1|2|3|4|5|6|7|8|9|10|11]] [-m [0|1]] [-T MAX_TEMPO] [-t MIN_TEMPO] [-D MAX_DURATION] [-d MIN_DURATION] [-g GENRE] [-s SONG] [-i ID] [-r ARTIST]
                       [-y MIN_YEAR] [-Y MAX_YEAR] [-p MIN_POPULARITY] [-P MAX_POPULARITY] [-b MIN_DANCEABILITY] [-B MAX_DANCEABILITY] [-e MIN_ENERGY] [-E MAX_ENERGY]
                       [-l MIN_LOUDNESS] [-L MAX_LOUDNESS] [-v MIN_VALENCE] [-V MAX_VALENCE] [-S SEARCH_SUBSTR]\nHelp: python3 command_line.py -h\n\n"""

    parser = argparse.ArgumentParser(usage=usage_msg())
    add_args(parser) # creates parser, adds all cmdline arguments to the parser
    args = parser.parse_args()


    if check_conditions(args) == False:
        print(usage_msg())
        return
    

    search_substr, search_by = parse_search_substr(args.search_substr)


    filtered_data = data_source.get_songs_by_attributes(get_filter(args,search_by,search_substr), "popularity")

    #Makes the print function print all columns, so the tests work.
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', 200)

    print(filtered_data)
    print("["+ str(len(filtered_data)) + " rows]")

def parse_search_substr(search_substr):
    """Purpose: This function extracts the search parameter and search string from a given input 
    by locating the first occurrence of a colon (":") and splitting the string accordingly.
    Arguments: search_substr (str): A string containing a search parameter and search string separated by a colon.
    Returns: tuple (str, str): A tuple containing the extracted search string and search parameter."""

    if search_substr is None:
        return None,"none"
    idx = search_substr.find(":")
    search_by = search_substr[:idx]
    search_substr = search_substr[idx + 1:]

    if search_by == "song":
        search_by = "track_name"

    return search_substr, search_by

    
def get_filter(args, search_by, search_substr):
    '''
    Arguments: args (Namespace): Parsed command-line arguments.
    Returns: a dictionary: A dictionary containing the given command line filter arguments
    Purpose: Extracts filtering options from the command-line arguments (does NOT include -S (song-search)
    and structures them into a dictionary for data filtering.
    '''
    attrs = {"key": args.key,
                "mode": args.mode,
                "genre": args.genre,
                "track_name": args.song, #track name
                "track_id": args.id,
                "artist": args.artist,
                "tempo": (args.min_tempo, args.max_tempo),
                "duration_ms": (args.min_duration, args.max_duration),
                "popularity": (args.min_popularity,args.max_popularity),
                "year_released": (args.min_year,args.max_year),
                "danceability": (args.min_danceability,args.max_danceability),
                "energy": (args.min_energy,args.max_energy),
                "loudness": (args.min_loudness,args.max_loudness),
                "valence": (args.min_valence,args.max_valence),
                "search":(search_by, search_substr)
                }
    return attrs



def add_args(parser):
    """Arguments: An ArgumentParser
    Returns: None
    Purpose: Defines and adds all command-line arguments to the parser."""
    parser.add_argument("-k", "--key", #type=int, #choices=[0,1,2,3,4,5,6,7,8,9,10,11], 
                        help="""Restricts output to songs of given key. 
                        Given number represents how many half steps the key is above C. Input range: 0-11""")
    parser.add_argument("-m", "--mode", #type=int, #choices=[0,1], 
                        help="""Restricts output to songs of given mode. 
                        minor = 0, Major = 1""")
    parser.add_argument("-T", "--max_tempo", #type=int, 
                        help="""Restricts output to songs with at most given tempo.""")
    parser.add_argument("-t", "--min_tempo", #type=int, 
                        help="""Restricts output to songs with at least given tempo.""")
    parser.add_argument("-D", "--max_duration", #type=int, 
                        help="""Restricts output to songs with at most given duration.""")
    parser.add_argument("-d", "--min_duration", #type=int, 
                        help="""Restricts output to songs with at least given duration.""")
    parser.add_argument("-g", "--genre", #type=str,
                        help="""Restricts output to songs of given genres.""")
    parser.add_argument("-s", "--song", #type=str,
                        help="""Restricts output to songs of given name.""")
    parser.add_argument("-i", "--id", #type=str,
                        help="""Restricts output to songs of given id.""")
    parser.add_argument("-r", "--artist", #type=str,
                        help="""Restricts output to songs from given artist.""")
    # parser.add_argument("-l", "--album", #type=str,
    #                     help="""Restricts output to songs from given album.""")
    parser.add_argument("-y", "--min_year", #type=str,
                        help="""Restricts output to songs released in given year.""")
    parser.add_argument("-Y", "--max_year", #type=str,
                        help="""Restricts output to songs released in given year.""")
    parser.add_argument("-p", "--min_popularity", #type=str,
                        help="""Restricts output to songs of at least given popularity.""")
    parser.add_argument("-P", "--max_popularity", #type=str,
                        help="""Restricts output to songs of at most given popularity.""")
    parser.add_argument("-b", "--min_danceability", #type=str,
                        help="""Restricts output to songs of at least given given danceability.""")
    parser.add_argument("-B", "--max_danceability", #type=str,
                        help="""Restricts output to songs of at most given given danceability.""")
    parser.add_argument("-e", "--min_energy", #type=str,
                        help="""Restricts output to songs of at least given given energy.""")
    parser.add_argument("-E", "--max_energy", #type=str,
                        help="""Restricts output to songs of at most given given energy.""")
    parser.add_argument("-l", "--min_loudness", #type=str,
                        help="""Restricts output to songs of at least given given loudness.""")
    parser.add_argument("-L", "--max_loudness", #type=str,
                        help="""Restricts output to songs of at most given given loudness.""")
    parser.add_argument("-v", "--min_valence", #type=str,
                        help="""Restricts output to songs of at least given given happiness (1 = happy, 0 = sad).""")
    parser.add_argument("-V", "--max_valence", #type=str,
                        help="""Restricts output to songs of at most given given happiness (1 = happy, 0 = sad).""")
    parser.add_argument("-S", "--search_substr", #type=str,
                        help="""Restricts output to songs whose title, artist, and album name are similar to the user input. Delimit by '|'.""")

def check_conditions(args):
    """Purpose: check the type and bounds conditions for the user-inputted arguments
    Arguments: args (Namespace): the user-inputted arguments
    Returns: true if both checks are true, otherwise false"""
    return check_type_conditions(args) and check_bounds_conditions(args)

def check_type_conditions(args):
    """Purpose: check the type conditions for the strs and ints inputted in the user's arguments
    Arguments: args (Namespace): the user-inputted arguments
    Returns: true if both checks are true, otherwise false"""
    return check_type_cond_int(args) and check_type_cond_str(args) and check_type_cond_float(args)

def check_type_cond_int(args):
    """Purpose: checks if the type of all user-inputted arguments for numerical conditions are int or None
    Arguments: args (Namespace): the user-inputted arguments
    Returns: true if all user arguments are of None or int type, otherwise false"""
    int_args = [args.key, args.mode, args.max_duration, args.min_duration]
    all_correct_type = True
    for arg in int_args:
        all_correct_type = all_correct_type and (arg == None or ErrCheck.is_int(arg))
    
    return all_correct_type

def check_type_cond_str(args):
    """Purpose: checks if the type of all user-inputted arguments for string conditions are str or None
    Arguments: args (Namespace): the user-inputted arguments
    Returns: true if all user arguments are of None or int type, otherwise false"""
    str_args = [args.genre, args.song, args.artist]    
    all_correct_type = True
    for arg in str_args:
        all_correct_type = all_correct_type and (arg == None or type(arg) == str)

    is_correct_substr = check_search_substr(args.search_substr)
    return all_correct_type and is_correct_substr

def check_type_cond_float(args):
    """Purpose: checks if the type of all user-inputted arguments for float conditions are floats or None
    Arguments: args (Namespace): the user-inputted arguments
    Returns: true if all user arguments are of None or float type, otherwise false"""
    str_args = [args.min_danceability, args.max_danceability, args.min_energy, args.max_energy, args.min_valence,args.max_valence, args.min_loudness, args.max_loudness, args.min_popularity, args.max_popularity, args.min_tempo,  args.max_tempo]    
    all_correct_type = True
    for arg in str_args:
        all_correct_type = all_correct_type and (arg == None or ErrCheck.is_float(arg))

    return all_correct_type

def check_search_substr(search_substr):
    """Purpose: Determines whether the argument value for search_substr is valid.
    Arguments: search_subtr (str) 
    Return: true if the argument value for search_substr is valid. Else, false."""
    if search_substr is None:
        return True
    
    idx = search_substr.find(":")
    if idx == -1:
        return False
    
    search_by = search_substr[:idx]

    if search_by in ["song","artist"]:
        return True

    return False

def check_bounds_conditions(args):
    """Purpose: checks if the bounds of the user-inputted arguments for numerical conditions are in range and thus, valid
    Arguments: args (Namespace): the user-inputted arguments
    Returns: true if all user arguments are valid, otherwise false"""
    return (args.key == None or (int(args.key) >= 0 and int(args.key) <= 11)) and \
            (args.mode == None or int(args.mode) in [0,1])

def usage_msg(name=None):
    '''
    Arguments: A string (option, default = None)
    Returns: A string (the usage message)
    Purpose: Generates and returns a usage message explaining the command-line options.
    '''
    usage = """python3 command_line.py [-h] [-k [0|1|2|3|4|5|6|7|8|9|10|11]] [-m [0|1]] [-T MAX_TEMPO] [-t MIN_TEMPO] [-D MAX_DURATION] [-d MIN_DURATION] [-g GENRE] [-s SONG] [-i ID] [-r ARTIST]
                       [-y MIN_YEAR] [-Y MAX_YEAR] [-p MIN_POPULARITY] [-P MAX_POPULARITY] [-b MIN_DANCEABILITY] [-B MAX_DANCEABILITY] [-e MIN_ENERGY] [-E MAX_ENERGY]
                       [-l MIN_LOUDNESS] [-L MAX_LOUDNESS] [-v MIN_VALENCE] [-V MAX_VALENCE] [-S SEARCH_SUBSTR]\nHelp: python3 command_line.py -h\n\n"""
    return usage

if __name__=='__main__':
    main()


# code = subprocess.Popen(['python3','-u', 'ProductionCode/basic_cl.py', "1", "2"],stdin=subprocess.PIPE, stdout=subprocess.PIPE, encoding='utf8')
# output, err = code.communicate()