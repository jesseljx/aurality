function displayFilter(dropdownID, specifierID) {
    /** 
     * Called via an onclick event. Displays the dropdown for a particular dropdownID and specifierID
     * Assumes that dropdownID and specifier ID are valid IDs in indedropdown.html
    */
  
    var specifier = document.getElementById(specifierID);
    var dropdown = document.getElementById(dropdownID);
    if (specifier.style.display === "none") {
        specifier.style.display = "block";
        dropdown.setAttribute("class","dropdown_flipped")
    } else {
        specifier.style.display = "none";
        dropdown.setAttribute("class","dropdown_regular")
    }
}
  
$(document).ready(function() {
    if ($(".row").length == 0 ) {
        let results = $(".results")
        results.html("<div class=\"row\"><p>No songs match your input conditions.</p></div>")
    }

    let rowsPerClick = 10; //How many rows to load when "load more" button is clicked
    let firstFewRows = $(".row")
    let allHiddenRows = $(".hidden_row")
    let numHiddenRows = allHiddenRows.length
  
    let numTotalRows = allHiddenRows.length + firstFewRows.length;
    let numDisplayedRows = firstFewRows.length
    let currentIndex = 0; 
  
    $("#load_more_results").click(function(e) { // click event for load more
        e.preventDefault();
        allHiddenRows.slice(currentIndex, currentIndex + rowsPerClick).show(); // select next 10 hidden rows and show them
        currentIndex = currentIndex + rowsPerClick
        numDisplayedRows = numDisplayedRows + rowsPerClick
  
        if (currentIndex >= numHiddenRows - 1) {
            $(this).fadeOut(); // remove load more button if are no more rows left to display
            numDisplayedRows = numTotalRows
        }
  
        $(".results span").text(numDisplayedRows.toString())
        
    });
  
    
});