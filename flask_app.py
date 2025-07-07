from ProductionCode.datasource import DataSource
from config import VALID_URL_ARGS, MIN_MAX_FIELDS, MAX_SONGS_TO_DISPLAY, MIN_SONGS_TO_DISPLAY
from flask import Flask, request, render_template
import pandas as pd
import err_check as ErrCheck

#source ~/.venvs/cs257_venv/bin/activate

"""
This file uses the Flask library to implement a barebone database-driven server that 
allows user to query a music dataset through URLs via two features:
    -- find songs where the song name, artist, or album contains the input string
    -- find songs where the musical parameters (eg. key, mode) are as specified
"""

#Global variables
app = Flask(__name__)

@app.errorhandler(404)
def display_404(e):
   """Notifies the user if they typed in the wrong URL"""

   return render_template("404_page.html", title = "404 Error")

@app.errorhandler(500)
def display_500(e):
   """Notifies the user if there is a bug on our end."""

   return render_template("500_page.html", title = "500 Error")

@app.route('/trigger-error-500')
def trigger_error_500():
    ''' A function that intentionally raises an Error.'''
    raise Exception("Intentional 500 error for testing.")

@app.route("/", strict_slashes = False)
def display_homepage():
    """A homepage that provides instruction for how to query the dataset"""

    attrs = convert_args_to_dict()
    sort_results_by = "popularity"
    attrs = format_attrs(attrs)
    data_source = DataSource()
    requested_data = data_source.get_songs_by_attributes(attrs, sort_results_by)

    rows=requested_data.values.tolist()
    rows=format_result(rows)
    num_all_rows = len(rows)
    
    first_few_rows = rows[:MIN_SONGS_TO_DISPLAY]
    hidden_rows = rows[MIN_SONGS_TO_DISPLAY:MAX_SONGS_TO_DISPLAY]
    
    num_first_few_rows = len(first_few_rows)
   
    return render_template("index.html",num_first_few_rows=num_first_few_rows, num_all_rows=num_all_rows, first_few_rows=first_few_rows, hidden_rows = hidden_rows)

@app.route("/about/", strict_slashes = False)
def display_about():
    """An about page that provides info about unique artists
    and the creators of the website.
    """
    data_source = DataSource()
    unique_artists = data_source.get_unique_artists()
    return render_template("about.html", title="About page", artists=unique_artists)

@app.route("/search", strict_slashes = False)
def filter_songs():
    """Top-level function that returns a table of songs where
    the attribute values satisfy the user's request arguments.
      
    Similar functionality to the route ("/search/<search_by>/attributes") below, 
    except that this route is activated when the user submits through html form
    """

    #Convert query string url to attr dict
    attrs = convert_args_to_dict()
    sort_results_by = attrs.pop("sort_results_by")

    #Check for invalid query field names
    attr_err_msg = ErrCheck.get_attr_errors(attrs)
    if attr_err_msg is not None: 
        return attr_err_msg
    
    #Check for invalid query values
    single_value_err_msg = ErrCheck.get_single_value_err(attrs) 
    if single_value_err_msg is not None:
        return single_value_err_msg

    #Convert the attrs dict values to correct format
    attrs = format_attrs(attrs)

    #Filters the data according to the attrs dict
    data_source = DataSource()
    requested_data = data_source.get_songs_by_attributes(attrs, sort_results_by)
    
    if requested_data is None or len(requested_data) == 0:
        num_first_few_rows = num_all_rows = 0
        first_few_rows = hidden_rows = []
    else:
        rows=requested_data.values.tolist()
        rows=format_result(rows)
        num_all_rows = len(rows)
        if num_all_rows > MIN_SONGS_TO_DISPLAY:
            first_few_rows = rows[:MIN_SONGS_TO_DISPLAY]
            hidden_rows = rows[MIN_SONGS_TO_DISPLAY:MAX_SONGS_TO_DISPLAY]
        else:
            first_few_rows = rows[:num_all_rows]
            hidden_rows = []
        
        num_first_few_rows = len(first_few_rows)

    return render_template("index.html",num_first_few_rows=num_first_few_rows, num_all_rows=num_all_rows, first_few_rows=first_few_rows, hidden_rows = hidden_rows)

@app.route("/uniqueartists", strict_slashes = False)
def display_unique_artists():
    data_source = DataSource()
    return data_source.get_unique_artists()

def convert_args_to_dict():
    """Converts the HTTP query string into a dict.
    Also, for any attribute in our dataset that's not in the query string, 
    add that attribute to the dict with value = None.

    Returns:
        dict: A dictionary with request arguments.
    """
    attrs = request.args.to_dict()

    for attr in VALID_URL_ARGS: 
        attrs[attr] = request.args.get(attr, None)

    return attrs

def format_attrs(attrs: dict) -> dict:
    """Formats the input dictionary by grouping min/max attributes into lists 
       and renaming certain attributes to match the database schema."""

    mins_maxes_actual_name = [
        "popularity", "year_released", "danceability", "energy",
        "loudness", "valence", "tempo", "duration_ms"
    ]

    for i in range(len(mins_maxes_actual_name)):
        idx = i * 2
        attrs[mins_maxes_actual_name[i]] = [
            attrs.pop(MIN_MAX_FIELDS[idx]), 
            attrs.pop(MIN_MAX_FIELDS[idx + 1])
        ]

    attrs["search"] = [attrs.pop("search_by"), attrs.pop("substr")]

    return attrs

def format_result(rows : list):
    """For converting any values with unconventionaly represenation into something more understandable.
    eg. Key = 1 and Mode = 1 is converted to C major"""

    keys_from_number = {"0": "C",
                        "1": "C#/Db",
                        "2": "D",
                        "3": "D#/Eb",
                        "4": "E",
                        "5": "F",
                        "6": "F#/Gb",
                        "7": "G",
                        "8": "G#/Ab",
                        "9": "A",
                        "10": "A#/Bb",
                        "11": "B"
                        }
    modes_from_number = {"0" : "minor",
                         "1" : "major"
                        }
    
    for row in rows:
        row[8] = keys_from_number[str(row[8])] #key is stored at index 8
        row[10] = modes_from_number[str(row[10])] #mode is stored at index 10

    return rows

if __name__== '__main__':
   app.run(port=5140)