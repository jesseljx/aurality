# Project Proposal

**Title**: Aurality

**Dataset summary**: dataset of 30000 songs/tracks published in the year range 1957 to 2020, each with attributes like key, tempo, genre, subgenre, track name, track artist, track album, year published, etc. 

**Dataset Metadata:**
- URL: https://www.kaggle.com/datasets/joebeachcapital/30000-spotify-songs
- Date downloaded: 01/19/2025
- Authorship: Joakim Arvidsson
- Exact name and version: 30000 Spotify Songs, Updated a year ago
- Terms of use: according to Database Contents License (DbCL) v1.0
- Suggested citation: none

## 3 interesting or meaningful ways that a user could interact with the data.

1. DJ’s that want to build a cohesive set list from a single song they know, without manually sorting and reorganizing the tracks by key, tempo, etc.
    - **Interaction mechanism:**
        - search bar where the user can input one song and if it exists in the dataset, then there will be a button + for the user to add it to their playlist. Additionally, there will be an option to reorder the songs in the playlist to make it more cohesive eg. the tempo of the second song is within +-5 of the first song, and the key of the second song is similar to the first, according to the circle of fifths.

        For example:
        - User: [Track A (125 BPM, G Major), Track B (124 BPM, e-flat minor), Track C (123 BPM, C Major)]
        - Website: [Track C → Track A → Track B]
    
    - **Benefits:**
        - The DJ can use our website to come up with a tracklist draft where each song transitions nicely into the next song, without having to manually reorder the songs.
    
    - **Harms:**
        - Most songs in the dataset are in English language, and some genres are not even in the dataset. 
        - Also, since we’re probably using only one algorithm for reordering the songs, the DJs might not get the reordering that they want. For example, if the algorithm generates a playlist where the tempo starts slow, then gradually increases from one song to the next, but the DJ wanted a different tempo change, then there’s nothing to be done.
        - Could exclude users that want to incorporate tracks that are not in the dataset.

2. Event organizers and hosts that also want a cohesive set list for events that creates a good atmosphere for the event
    - **Interaction mechanism:**
        -   in addition to a search bar that accepts a song, the website also provides an additional dropdown that filters the songs by genre, so the music playlist would be appropriate to the occasion. 
    - **Benefits:** 
        - the user can select what genre, or perhaps even subgenres, they want in their playlist.
    - **Harms:** 
        - same as above. Also, just because two songs are in the same genre does not mean that they are both appropriate for the same event. For example, if one song has lots of swear words, then it’s certainly inappropriate for formal gatherings.

3. Casual music listeners that also want a cohesive set list for personal enjoyment and social gatherings
    - Same as above
