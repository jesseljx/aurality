# User Analysis for Command Line Features

## Current features

Usage: 

python3 command_line.py [-k [0\|1|2|3|4|5|6|7|8|9|10|11]] 
                               [-m [0\|1]] [-T MAX_TEMPO] [-t MIN_TEMPO] [-D MAX_DURATION]
                               [-d MIN_DURATION] [-g GENRE] [-s SONG] [-r ARTIST] 
                               [-l ALBUM] [-S SEARCH_SUBSTR]

## Analysis

### Case 1: Prints to stdout all the songs in the speciied key, tempo range, and genre.

Potential Users: party hosts that want to get tracks that will fit well (based on key/mode/tempo/genre) into their sets
Potential Benefits: the user find tracks that will fit into their sets and allow for good transitions, based on desired tempo, key, genre, duration, and mode

Critique (some assumptions about users embedded in the design):
- Assumption 1: Familiar with the parameters of music like key, tempo, and genre.
- Assumption 2: The keys are in numbers from 0 to 11, representing C to B. This assumes that the user can convert between letter representation of a key like C# to a numeric representation like 1.

Imagine (pick an assumption and imagine how it excludes user):
- Assumption 1: if the user is not familiar with the BPM tempo, then they won't have any idea how fast their sets would be, unless they hear a few tracks in a particular tempo. Also, genre is a cultural thing that's not universally recognzied.
- Assumption 2: makes it harder to find songs in the desired key, if the user is only familiar with the letter representation of keys

Design
- Assumption 1: add a basic infographic that maps English terms like fast, danceable, slow, etc to numeric BPMs, as well as providing popular songs that fit the tempo description
- Assumption 2: add an if statement where if the user input key is not an int, convert it to an int using the lookup table, then pass it to the filter_data function. Alternatively, change the dataset so that the keys are in letters, since that's the representation that most people use.

### Case 2: prints out song info based on the artist and song name the user inputted

Potential Users: Casual music listeners who want to quickly find details about a song, but only remembers part of a song name, artist name, or album name.

Potential Benefits: Allows users to retrieve song data based on easily remembered details like artist, song name or album name. Simplifies the process of finding specific song-related information for casual and technical users alike, as the user don't have to type the full name.

Critique (some assumptions about users embedded in the design): 
- Assumption 1: Users type in part of the song/artist/album name correctly, and know if what they type in is incorrect.
- Assumption 2: Users want the song where either the name, artist name, or album name includes the search string as a substring.
- Assumption 3: Users only care about searching for songs based on textual metadata like artist name, track name, or album name. 
- Assumption 4: Users are comfortable typing in English and using a command-line interface.

Imagine (pick an assumption and imagine how it excludes users):
- Assumption 1: If users misspell an artist or album name (e.g., "Rihana" instead of "Rihanna"), they won’t get relevant results.
- Assumption 2: If there is a song called "Billie Eilish" and the user wants to search for that song, our website would return unnecessary results: any song where "Billie Eilish" is a substring of either the song name, artist, or album name, would be returned.
- Assumption 3: Users might want to search for songs based on other attributes, like energy, mood, popularity, or release year, not just textual metadata like artist names.
- Assumption 4: excludes users with accessibility needs (e.g., vision impairments) might want to use voice input or audio-based search methods instead of typing.

Design: 
- Assumption 1: add support for fuzzy matching to handle misspelled artist, album, or track names.
- Assumption 2: add a dropdown that lets the user to specify whether they want to get songs based on song name, artist, or album name.
- Assumption 3: extend filter capabilities to include additional attributes like danceability, mood, energy, or tempo.
- Assumption 4: include audio search methods (e.g., voice to text).
- Also, redesign to incorporate more natural language queries (e.g., “songs to relax to”) or  Revisit how the design could accommodate users unfamiliar with technical musical terms or those looking for more intuitive search options.

# User Analysis for Flask Features

## Current features

Usage: 

    Welcome to the homepage!<br><br>
    To view all songs in our dataset, use the following URL:<br>
    IP:PORT/search/none/attributes<br><br>

    To filter the dataset, use the following syntax for URL:<br>
    IP:PORT/search/&ltsearch_by&gt/attributes?&ltarg&gt=&ltvalue&gt&&ltarg&gt=&ltvalue&gt&...<br><br>

    Multiple &ltarg&gt and &ltvalue&gt can be supplied. Valid &ltarg&gt variable include:<br>
        &emsp;song<br>
            &emsp;&emsp;&ltvalue&gt can be any string<br>
        &emsp;artist<br>
            &emsp;&emsp;&ltvalue&gt can be any string<br>
        &emsp;album<br>
            &emsp;&emsp;&ltvalue&gt can be any string<br>
        &emsp;genre<br>
            &emsp;&emsp;&ltvalue&gt must be a string of genres, where each is separated by a comma. Valid genres include rap, r&b, edm, pop, rock, latin.<br>
            &emsp;&emsp;Example: genre=rap,r&b,pop<br>
        &emsp;key<br>
            &emsp;&emsp;&ltvalue&gt must be an integer between 0 to 11, inclusive. 0 represents C, 11 represents B<br>
        &emsp;mode<br>
            &emsp;&emsp;&ltvalue&gt must either 1 or 0.<br>
            &emsp;&emsp;1 is major, 0 is minor<br>
        &emsp;tlb<br>
            &emsp;&emsp;&ltvalue&gt must be an int greater than 0<br>
            &emsp;&emsp;all songs returned have tempo >= &ltvalue&gt<br>
        &emsp;tub<br>
            &emsp;&emsp;&ltvalue&gt must be an int greater than 0<br>
            &emsp;&emsp;all songs returned have tempo <= &ltvalue&gt<br>
        &emsp;dlb<br>
            &emsp;&emsp;&ltvalue&gt must be an int greater than 0<br>
            &emsp;&emsp;all songs returned have tempo >= &ltvalue&gt<br>
        &emsp;dub<br>
            &emsp;&emsp;&ltvalue&gt must be an int greater than 0<br>
            &emsp;&emsp;all songs returned have tempo <= &ltvalue&gt<br><br><br>


    &ltsearch_by&gt specifies what &ltarg&gt should the program perform substring searching. Can be either "artist", "album", "song" or "none"<br>
    For example, if search_by is "song", the program returns all songs that include the &ltvalue&gt of the &ltarg&gt "song" as a substring. Case is ignored.<br>
    To search using multiple keywords, use the delimiter | to separate each keyword. Examples below.<br><br>

    Examples:<br>
        &emsp;/search/artist/attributes?artist=Katy&tlb=100&tub=130       #returns all songs where "Katy" is a substring of the artist name and song is between 100 and 130 bpm<br>
        &emsp;/search/none/attributes?key=7&mode=1                          #returns all songs in G major<br>
        &emsp;/search/song/attributes?song=call|you&key=1                   #returns all songs in C# where the song name contains either "call" or "you"<br>


## Analysis

### Case 1: Querying Tables

Potential Users: DJs attempting to query a list of attribute specific data from our database. They may be looking for songs from a specific artist, or songs with particular keys.

Potential Benefits: This may work as a very quick way for users to be able to quickly see a swath of data related to their queries at one time. Allowing them to query data relevant to any row header will also allow them to return many different song attributes in these lists.

Potential Harms: The amount of data provided by these tables may be overwhelming if too many datapoints match the query. The compactness of the data in the tables may also be uncomforatable to the eye.

Critique (some assumptions about users embedded in the design):
- Assumption 1: Users will be able to easily read and navigate the text displayed by the Flask app.
- Assumption 2: Users will be able to remember the arguments to specify what is to be returned by the table correctly.

Imagine (pick an assumption and imagine how it excludes user):
- Assumption 1: This assumption excludes users who may have difficulty seeing things. Without bolded text for labelling or categorization, it may make it more difficult for these users.
- Assumption 2: We're assuming that users will know to say query "artist" in the URL box as opposed to something like "creator" when passing arguments to query a specific thing. We're assuming they may not mess up and request a synonym instead which would cause issues.

Design
- Assumption 1: Add a bit of markdown to what is returned by the flask app if at all possible. Likely bolding row headers to increase readability.
- Assumption 2: We can potentially create multiple synonyms for arguments that can all work to return the same thing. This will make our Flask app less intensive on the memories of our users.

### Case 2: Returning Unique Artist

Potential Users: Users curious about the artists included in our database may return a list of all unique artists to better understand the songs covered in our database.

Potential Benefits: Knowing artist names associated with a database is a great way to know songs associated with a database as you can associate an artist with many songs. It can also help users to understand what genres are covered most in our database as artists tend to be consistently associated with certain genres. 

Critique (some assumptions about users embedded in the design): 
- Assumption 1: Users just want unique artists as opposed to say unique tempos or keys.
- Assumption 2: Users will want to see all unique artists in our database as opposed to artist narrowed down by a particular keyword, i.e. all artists with the work "d" in them.


Imagine (pick an assumption and imagine how it excludes users):
- Assumption 1: This excludes those who are interested in unique data other than artists.
- Assumption 2: We assume that users will want a filterless request of all artists which excludes those who may want to filter their unique artists.

Design: 
- Assumption 1: We may add other functionalities like unique genre or unique key to make it possible for users to better understand our datasets in different ways.
- Assumption 2: We may include a way to filter the unique artists in order to make the request less overwhelming and more relevant.

# User Analysis for Database Features

## Analysis

### Assumption #1: The Many Data Points That We Have Are Actually Practical

Critique (some assumptions about users embedded in the design):
The platform assumes listeners find value in exact audio features like danceability, energy, and acousticness, expecting they will want control over subtle qualities of their songs. It also assumes listeners listen purposefully–picking songs based on some mood or activity–and are willing to engage with tech metrics to find the best playlist.

Imagine (pick an assumption and imagine how it excludes user):
An average user opens the software in pursuit of upbeat tunes and is met by technical filters like "valence" and "loudness." With no simplistic explanations, they are intimidated and end up applying default playlists and are deprived of more sophisticated individualization features.


Design:
Offer affect-based filters (e.g., "Happy," "Chill") instead of raw data points. Use simple vs. expert modes for different levels of users. Employ tooltips to explain technical parlance in simpler terms.


### Assumption #2 We Cover Diverse Enough Areas of Music Genre-wise: 

Critique (some assumptions about users embedded in the design): 
The structure assumes that the genre and subgenre classifications currently in use provide access to a wide variety of music, accepting multicultural tastes and cultures. It assumes that the user will have access to the genres that they enjoy or learn about others using the system of genre tagging being used, and that this classification is wide enough and inclusive enough to accept global musical tastes.

Imagine (pick an assumption and imagine how it excludes users):
A user who is interested in niche genres, like traditional Japanese Enka or Brazilian Forró, searches the site but is only able to find broad categories like "World Music" or "Latin." The lack of specific genre representation makes the user feel excluded and leads them to believe the site is primarily focused on Western mainstream music.

Design:
Broaden genre tags to include specific regional and niche genres. Develop playlists that feature underrepresented types of music. Leverage a "Browse by Region" feature to help customers browse diverse musical cultures.

# User Analysis for Front-End

### Assumption #1: Filter Selection is Scannable

Critique (some assumptions about users embedded in the design): 
The front-end currently has a great, wide array of potential filters that users can use. They are all very uniform in their appearance and are organized compactly into their own search area close to the search bar. They all have example inputs in labeled in gray font to help with muddling through. It can be argued that the filters also reduce satisficing due to the wide-array of options they present. It would be hard to say that users are settling for a lack of ability to information. Unfortunately, these filters may be more useful if spread out horizontally.

Imagine (pick an assumption and imagine how it excludes users):
This feature may exclude users in that it assumes that users will have a comforatable experience reading the filters in the current compact format in which they exist. The current format may challenge people with vision issues. It may also just be a bit of an inconvenience as it could exist in a more left to right reading format with less breaks.

Design:
To fix this we can design a filters section that is still organized but slightly more spread out. We should make it such that the filters are spread out but with some padding on the sides to make them into more readable lines. We could also increase the size of the text for the filters to make them easier to read.

# User Analysis for Front-End Features

### Assumption #1 Our Search Tools (Specifically Filters) Are Scannable: 

Critique (some assumptions about users embedded in the design): 
The structure assumes that the genre and subgenre classifications currently in use provide access to a wide variety of music, accepting multicultural tastes and cultures. It assumes that the user will have access to the genres that they enjoy or learn about others using the system of genre tagging being used, and that this classification is wide enough and inclusive enough to accept global musical tastes.

Imagine (pick an assumption and imagine how it excludes users):
A user who is interested in niche genres, like traditional Japanese Enka or Brazilian Forró, searches the site but is only able to find broad categories like "World Music" or "Latin." The lack of specific genre representation makes the user feel excluded and leads them to believe the site is primarily focused on Western mainstream music.

Design:
Broaden genre tags to include specific regional and niche genres. Develop playlists that feature underrepresented types of music. Leverage a "Browse by Region" feature to help customers browse diverse musical cultures.

### Assumption #2 We Have a Graphically Satisfying Front-Page: 

Critique (some assumptions about users embedded in the design):
We currently have a front-page that is geared to be very functional in nature. It has a wide-array of filters, and a good navigation bar for searching, playlists, and to read more about the project. Some of our filters even include things like drop down menus further adding variety to our array of tools. Graphically speaking though, it can be agrued that our front page could be enhanced. Text sizes could be different. Some fonts could be styled differently. Colors and dividers could better show and categorize how some of these tools could be used.

Imagine (pick an assumption and imagine how it excludes users):
Our current design may exclude users that are looking for a more graphically pleasing experience during the use of our tool. DJs, for example, can care about the graphical appearance of their overall setup. Without that aesthetic, it may be seen as a bit of an inconvenience to them. Even some music enthusiasts or regular users may benefit from some tweaks to the graphical style of the site.

Design: Our graphical issues can be fixed by slightly altering fonts. The banner font, for example, could be stylized to better differentiate itself from the rest of the body. The navigation bar could feature centered text or a different style of text. The style of font for the filters could also be improved to better differentiate it from the rest of the page. Graphical changes such as this may improve usability and overall user experience.

# User Analysis for Front-End Features

### Assumption #1 Our Search Tools (Specifically Filters) Are Scannable: 

Critique (some assumptions about users embedded in the design): 
The structure assumes that the genre and subgenre classifications currently in use provide access to a wide variety of music, accepting multicultural tastes and cultures. It assumes that the user will have access to the genres that they enjoy or learn about others using the system of genre tagging being used, and that this classification is wide enough and inclusive enough to accept global musical tastes.

Imagine (pick an assumption and imagine how it excludes users):
A user who is interested in niche genres, like traditional Japanese Enka or Brazilian Forró, searches the site but is only able to find broad categories like "World Music" or "Latin." The lack of specific genre representation makes the user feel excluded and leads them to believe the site is primarily focused on Western mainstream music.

Design:
Broaden genre tags to include specific regional and niche genres. Develop playlists that feature underrepresented types of music. Leverage a "Browse by Region" feature to help customers browse diverse musical cultures.

### Assumption #2 We Have a Graphically Satisfying Front-Page: 

Critique (some assumptions about users embedded in the design):
We currently have a front-page that is geared to be very functional in nature. It has a wide-array of filters, and a good navigation bar for searching, playlists, and to read more about the project. Some of our filters even include things like drop down menus further adding variety to our array of tools. Graphically speaking though, it can be agrued that our front page could be enhanced. Text sizes could be different. Some fonts could be styled differently. Colors and dividers could better show and categorize how some of these tools could be used.

Imagine (pick an assumption and imagine how it excludes users):
Our current design may exclude users that are looking for a more graphically pleasing experience during the use of our tool. DJs, for example, can care about the graphical appearance of their overall setup. Without that aesthetic, it may be seen as a bit of an inconvenience to them. Even some music enthusiasts or regular users may benefit from some tweaks to the graphical style of the site.


Design: Our graphical issues can be fixed by slightly altering fonts. The banner font, for example, could be stylized to better differentiate itself from the rest of the body. The navigation bar could feature centered text or a different style of text. The style of font for the filters could also be improved to better differentiate it from the rest of the page. Graphical changes such as this may improve usability and overall user experience.

### Assumption #3 Our Layout is Understandable to Very Casual Users: 

Critique (some assumptions about users embedded in the design):
Our search user experience is helpful and simple, possessing a rich variety of filters upon which users are able to iterate in a clear manner. It stimulates exploration without requiring knowledge about the way search logic works. Drop-downs, checkboxes, and search input allow users an avenue to refine their search iteratively, contributing to the feeling of "muddling through" by permiting them to refine parameters as they please. But the layout does not provide strong visual signals to those that may not instantly know what the filters mean. While users can naturally work with the filters there is no strong indication of which filters to use and how to combine them. The project could benefit from some potential tooltips. 

Imagine (pick an assumption and imagine how it excludes users):
The current design assumes that users have prior knowledge of music attributes (e.g. BPM, loudness, valence). But general music listeners or inexperienced playlist creators may not have a clear idea what these terms refer to or how these aspects affect their search results. A music producer or DJ will inherently realize the meaning of filters by BPM for choosing songs, but an average listener may not.

Design: To assist muddling through better, we might consider tooltips for tempo, valence, and energy filters that briefly explain how they are used. The project could possibly also apply pre-filled sample searches to better show how different filters can be used. More spacing or color separation may benefit muddling through as well.