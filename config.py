"""This file stores all the global constants"""

#All valid URL request arguments. These should be handled by the html form
VALID_URL_ARGS = [
    "track_name", "artist", "genre", "key", "mode", 
    "min_popularity", "max_popularity", "min_year", "max_year", 
    "min_danceability", "max_danceability", "min_energy", "max_energy",
    "min_loudness", "max_loudness", "min_valence", "max_valence",
    "min_tempo", "max_tempo", "min_duration", "max_duration",
    "search_by", "substr","sort_results_by"
]

#All valid genres in out dataset
GENRES = [
    "alt-rock", "dance", "dancehall", "detroit-techno", "edm",
    "electro", "electronic", "hard-rock", "indie-pop", "k-pop",
    "minimal-techno", "pop", "power-pop", "psych-rock",
    "punk-rock", "rock", "rock-n-roll", "techno"
]

#All valid URL request arguments that specify a min/max bound
MIN_MAX_FIELDS = [
    "min_popularity", "max_popularity", "min_year", "max_year", 
    "min_danceability", "max_danceability", "min_energy", "max_energy",
    "min_loudness", "max_loudness", "min_valence", "max_valence",
    "min_tempo", "max_tempo", "min_duration", "max_duration"
]

#Max number of songs the html page should render
MAX_SONGS_TO_DISPLAY = 1000

#How many songs to display without clicking the "load more" button
MIN_SONGS_TO_DISPLAY = 10