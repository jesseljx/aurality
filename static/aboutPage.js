$(document).ready(function() {
    artistsPerClick = 20;
    allHiddenArtists = $(".hidden_artists");

    numHiddenArtists = allHiddenArtists.length
    numAllArtists = numHiddenArtists + artistsPerClick;
    
    currentIndex = 0;
    numDisplayedArtists = 20;

    $("#load_more_artists").click(function(e) { // click event for load more
        e.preventDefault();
        allHiddenArtists.slice(currentIndex, currentIndex + artistsPerClick).show(); // select next 10 hidden rows and show them
        currentIndex = currentIndex + artistsPerClick;
        numDisplayedArtists = numAllArtists;

        if (currentIndex >= numHiddenArtists - 1) {
            $(this).fadeOut(); // remove load more button if are no more rows left to display
            numDisplayedArtists = numHiddenArtists + artistsPerClick;
        }

        $(".results span").text(numDisplayedRows.toString());
        
    });

  
});