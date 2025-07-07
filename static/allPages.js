$(document).ready(function() {

    let backToTopButton = document.getElementById("back_to_top");
  
    // When the user scrolls down 20px from the top of the document, show the button
    window.onscroll = function() {scrollFunction()};
  
    function scrollFunction() {
        if (document.body.scrollTop > 20 || document.documentElement.scrollTop > 20) {
            backToTopButton.style.display = "block";
        } else {
            backToTopButton.style.display = "none";
        }
    }
  
    $("#back_to_top").click(function(e) { // click event for load more
        e.preventDefault();
        $('html, body').animate({scrollTop: 0}, 500); // Smooth scroll to top
    });

});