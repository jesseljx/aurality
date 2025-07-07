# Team Aurality ReadMe

**Project Created By:**
- Jesse Lindholm
- Prompt Eua-anant
- Klaus Beasley
- River Schmidt-Eder

### How to run flask app

    brew services start postgresql@14
    source ~/cs257VENV/bin/activate
    python3 flask_app.py
    deactivate #quit venv

### Command line command for song retrieval:
    python3 command_line.py [-h] [-k [0|1|2|3|4|5|6|7|8|9|10|11]] [-m [0|1]] [-T MAX_TEMPO] [-t MIN_TEMPO] [-D MAX_DURATION] [-d MIN_DURATION] [-g GENRE] [-s SONG] [-i ID] [-r ARTIST]
                   [-y YEAR] [-p MIN_POPULARITY] [-P MAX_POPULARITY] [-b MIN_DANCEABILITY] [-B MAX_DANCEABILITY] [-e MIN_ENERGY] [-E MAX_ENERGY]
                   [-l MIN_LOUDNESS] [-L MAX_LOUDNESS] [-v MIN_VALENCE] [-V MAX_VALENCE] [-S SEARCH_SUBSTR]

    -k --key            #int: the key of the song, from 0 to 11. 0 = C, 11 = B.
    -m --mode           #int: 1 for major, 0 for minor
    -T --max_tempo      #int: in BPM. Songs returned shouldn't be faster than this tempo.
    -t --min_tempo      #int: in BPM. Songs returned shouldn't be slower than this tempo.
    -D --max_duration   #int: in milliseconds. Songs returned shouldn't be longer than this value.
    -d --min_duration   #int: in milliseconds. Songs returned shouldn't be shorter than this value.
    -g --genre          #str: genre. Valid genres include rap, pop, edm, latin, r&b, rock. To input multiple genres, separate each with a comma.
    -s --song           #str: exact song name
    -i --id             #str: unique song ID
    -r --artist         #str: exact artist name
    -y --year           #int: year the song was released
    -p --min_popularity #int: minimum popularity score
    -P --max_popularity #int: maximum popularity score
    -b --min_danceability #float: minimum danceability score (0.0 to 1.0)
    -B --max_danceability #float: maximum danceability score (0.0 to 1.0)
    -e --min_energy     #float: minimum energy score (0.0 to 1.0)
    -E --max_energy     #float: maximum energy score (0.0 to 1.0)
    -l --min_loudness   #float: minimum loudness (in dB)
    -L --max_loudness   #float: maximum loudness (in dB)
    -v --min_valence    #float: minimum valence (happiness) score (0.0 to 1.0)
    -V --max_valence    #float: maximum valence (happiness) score (0.0 to 1.0)
    -S --search_substr  #str: substring search for song title, artist, or album. Syntax: 'song:substring' or 'artist:substring'.

## Feature 1: retrieve songs from attributes:

Prints all songs that satisfy the set of attribute values provided in the command line options (see above).


Examples:

`python3 command_line.py -k 0 -m 1` #prints all songs in C major

`python3 command_line.py -t 80 -T 200 -k 0 -m 1` #prints all songs in C major with BPM >= 80 and <= 200

`python3 command_line.py -g "rap,pop"` #prints all songs that are either rap or pop

`python3 command_line.py -s "I Love You"` #prints all songs where the song name is **exactly** as specified. Case sensitive.

`python3 command_line.py -y 2020` #prints all songs released in the year 2020.

`python3 command_line.py -p 50 -P 100` #prints all songs with popularity between 50 and 100.

`python3 command_line.py -b 0.6 -B 1.0` #prints all songs with a danceability score between 0.6 and 1.0.

`python3 command_line.py -e 0.7 -E 1.0` #prints all songs with an energy score between 0.7 and 1.0.

`python3 command_line.py -l -10 -L 0` #prints all songs with loudness between -10 dB and 0 dB.

`python3 command_line.py -v 0.5 -V 1.0` #prints all songs with valence (happiness) between 0.5 and 1.0.

## Feature 2: retrieve songs from title, album, or artist using substring matching:

Prints all songs where the name, artist, or album contains the substring provided by the user. Users can separate substrings with a '|', and MUST specify whether the substring is for song, artist or album. Search will include songs that have either of the substrings. Ignores case. Examples below.

`python3 command_line.py -S "song:Never Really Ov"` prints all songs that has "Never Really Ov" as a substring in its song title. Case is always ignored.

`python3 command_line.py -S 'artist:bieber|PeRRy'` prints all songs that has "bieber" OR "PeRRy" as a substring in its artist name. Case is always ignored.

`python3 command_line.py -S 'album:Non-existent-substring-in-dataset'` prints all the songs with "Non-existent-substring-in-dataset" as a substring in its album. Case is always ignored. This should print out an empty DataFrame.

`python3 command_line.py -S 'never really over'` this is invalid as the user does not specify whether the substring is for song, artist, or album.

## Feature 2: retrieve songs from title, album, or artist using substring matching:

Prints all songs where the name, artist, or album contains the substring provided by the user. Users can separate substrings with a '|', and MUST specify whether the substring is for song, artist or album. Search will include songs that have either of the substrings. Ignores case. Examples below.

`python3 command_line.py -S "song:Never Really Ov"` prints all songs that has "Never Really Ov" as a substring in its song title. Case is always ignored.

`python3 command_line.py -S 'artist:bieber|PeRRy'` prints all songs that has "bieber" OR "PeRRy" as a substring in its artist name. Case is always ignored.

`python3 command_line.py -S 'album:Non-existent-substring-in-dataset'` prints all the songs with "Non-existent-substring-in-dataset" as a substring in its album. Case is always ignored. This should print out an empty DataFrame.

`python3 command_line.py -S 'never really over'` this is invalid as the user does not specify whether the substring is for song, artist, or album.

# Front-End ReadMe
## Scanability
The website utilizes headings, drop-down filters, and plain song information to ensure effortless scanning of material.\
Consumers can detect crucial song traits such as artist, genre, tempo, and popularity without an excess of scrolling or reading.
## Satisficing
Consumers can find pertinent songs without the necessity to sift through all available songs. Consumers can make use of filtering functions in order to simplify their search as opposed to deeply inspecting all songs.\
The filters and search feature allow the users to have an acceptable result without too much hassle.
## Muddling Through
The interface does not require that the users fully understand its structure to search and find useful results.\
Users can start with a broad search and proceed to limit their choices as they navigate the filters, and the search\ suggestions and filter controls guide the users in making their searches progressively more accurate.
# Accessibility Features
Contrast & Readability: The site uses a high-contrast purple header and black text on a light background for readability.\
Keyboard Navigation: Dropdowns and the search box offer tab-based navigation for users with keyboards.\
Alt Text for Images: All the images on the site have descriptive alt text to assist visually impaired users.
## Headings for Structure
The page is structured with headings such as:\
Main Title ("Aurality Playlist Maker") for identification and branding purposes.\
Navigation Links ("Search", "Your Playlist", "About") for quick links to different areas.\
Song Listings with Subheadings (for example, artist name, song attributes) for structured information.
## Alt Text for Images
Alt text for all the icons and images in the interface is available to screen readers to make it visually accessible to people with disabilities.

## FRONTEND IMPROVEMENT 1:
Usability issue: searchbar clickable area didn't cover whole visible width\
Page used: datastyle.css (changes modified index.html)\
To address: increased clickable area width

## FRONTEND IMPROVEMENT 2:
Usability issue: results only sortable by popularity\
Pages used: index.html, datasource.py, flask_app.py\
To address: added feature to allow searching on different parameters

## FRONTEND IMPROVEMENT 3:
Usability issue: Users don't understand how to use the site and the filter parameters\
Pages used: about.html, datastyle.css\
To address: added site use instructions and descriptions about each filter parameter in the About page

## FRONTEND IMPROVEMENT 4:
Usability issue: Users don't have a way to easily go back to top of the page\
Pages used: index.html, about.html, datastyle.css, allPages.js\
To address: added a back to top button whose behaviour is programmed in allPages.js

## FRONTEND IMPROVEMENT 5:
Usability issue: If there are too many songs returned from the query, there are too many visible elements in the website and it slows down.\
Pages used: index.html, about.html, datastyle.css, js files\
To address: only display a fixed number of results and added a "load more" button for the user to see more results

## Code Smell #1 Long Methods (Filter Functions):
Code smell: The original implementation of the filter songs() and filter_song_old() functions were a bit longer than they should have been and many responsibilities, violating the Single Responsibility Principle (SRP).\
Pages used: flask_app.py\
To address: turned filter_songs() into specialized helper functions. convert_args_to_dict() extracts query parameters, ErrCheck.get_attr_errors() validates attributes, ErrCheck.get_single_value_err() checks for invalid query values, format_attrs() ensures attribute name consistency, and format_result() converts raw results into a readable format. This refactor improves readability, resuseability, and debugging.

## Code Smell #2 Hardcoded Constants Instead of Centralized Config:
Code smell: The original implementation hardcoded various constants (e.g., valid URL arguments, genre lists, min/max filters) across multiple files instead of using a centralized, easily accessible and editable configuration in a single file, making maintenance difficult and prone to inconsistencies.\
Pages used: flask_app.py, config.py\
To address: Introduced config.py to store constants such as VALID_URL_ARGS, MIN_MAX_FIELDS, MAX_SONGS_TO_DISPLAY, and MIN_SONGS_TO_DISPLAY that is used in various files like flask_app and err_check.py. Refactored flask_app.py to import these values, ensuring easier updates and improving code aesthetic.

## Code Smell #3 Naming & Commenting Issues
Code Smell: Inconsistent naming and unclear comments reduced code readability. Variables like search_param and search_string lacked clarity, and inputs were used inconsistently, so we changed it to search_by and substr to indicate that the search_by is the field name to perform the search on, and substr means each result should contain substr as a substring. Some docstrings were misleading, such as is_valid_bound, which incorrectly described its function.\
Pages used: config.py, flask_app.py, app_database.py, command_line.py, input_validate.py, helper_func.py\
To address: Renamed search_param to search_by, search_string to search_substr, and standardized inputs as attrs. Updated misleading docstrings and removed redundant comments for clarity.
