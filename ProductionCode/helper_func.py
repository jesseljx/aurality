import pandas as pd
import re

"""Old file before moving to psql. This includes helper functions for basic functionality. Deprecated."""

def load_data(): 
    """Arguments: None
    Returns: data in pandas DataFrame
    Purpose: Loads the data from a file"""
    
    data = pd.read_csv("Data/dummy_spotify_songs.csv")
    return data

def get_unique_artists(data : pd.DataFrame) -> pd.DataFrame:
    """Return all unique artists in the data input"""
    nparray =  data["artist"].unique()
    return pd.DataFrame(nparray, columns = ['Artists'])

def filter_data(data : pd.DataFrame, filters : dict) -> pd.DataFrame:
    """THIS FUNCTION IS NOT SAFE! Make sure to call an error checking function first! 
            - (check_conditions in command_line.py, or get_attr_error and get_single_value_error in flask_app.py)

    Filters a pandas DataFrame based on specified conditions.
    Arguments:
    df : pd.DataFrame
        The DataFrame to filter.
    filters : dict
        A dictionary with column names as keys and filtering conditions as values.
        Conditions can be:
        - A tuple (<lower_bound>, <upper_bound>) for range filtering.
        - A single value for exact matching.
        - None to skip filtering for that column.
    Returns:
    -------
    pd.DataFrame
        A filtered DataFrame containing rows that match the specified conditions.
    """
    for column, value in filters.items():        
        if value is None:
            continue
        if column == "tempo" or column == "duration": #For any numeric attribute with lower/upper bound
            lower_bound = value[0] 
            upper_bound = value[1] 
            if lower_bound is not None: 
                data = data[data[column] >= lower_bound]
            if upper_bound is not None:
                data = data[data[column] <= upper_bound]
        elif column == "genre": #Genre is a special case we have to deal with

            #Convert input string to list of genres
            all_selected_genres = value.split(",")
            
            #Check which genres are NOT in input genres
            available_genres = ["rap", "r&b", "edm", "pop", "rock", "latin"]
            for genre in available_genres:
                if genre not in all_selected_genres:
                    data = data[data[column] != genre] #Weed out songs not in specified genres
        else:
            data = data[data[column] == value]
    return data

def normalize_column(column: pd.Series) -> pd.Series:
    """Arguments:
        A Series (pandas)
    Returns:
        A Series
    Purpose:
        Convert column data to lowercase strings to compare case-insensitively."""
    return column.astype(str).str.lower()

def contains_keywords(column: pd.Series, keywords: list) -> pd.Series:
    """Arguments:
        A Series (pandas)
        A list of strings
    Returns:
        A Series
    Purpose:
        Check if any keywords appear in the column."""
    return column.str.contains('|'.join(keywords), na=False)

def search_by_substr(data: pd.DataFrame, search_substr: str, search_by: str) -> pd.DataFrame:
    """THIS FUNCTION IS NOT SAFE! Make sure to call an error checking function first! 
            - (check_conditions in command_line.py, or get_attr_error and get_single_value_error in flask_app.py)
            
    Arguments: A DataFrame and a string containing search keywords (user inputted on CL)
    Returns: A filtered DataFrame containing matching songs.
    Purpose: Search for songs based on artist name, track name, or album name.
        Returns a dataframe consisting of all songs where the search_substr is 
        a substring in the songs' track name, artist name, or album name."""
    
    keywords = [word.lower() for word in search_substr.split("|")] #convert search string to all lowercase
    for i in range(len(keywords)): #Don't combine this with the statement above. We want to escape the parens and NOT the vertical bar
        keywords[i] = re.escape(keywords[i])

    data_lower = data[[search_by]].apply(normalize_column) #make relevant columns lowercase
    filter = data_lower.apply(lambda col: contains_keywords(col, keywords)) #filter lowercase data by the search keywords
    return data[filter.any(axis=1)]

