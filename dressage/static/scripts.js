var refreshSeconds;
var rating;

var paused = false;
var counterSeconds = 0;

var refreshCounter2 = setInterval(function() {
    if (!paused) {
        counterSeconds += 1;
    }

    var totalSecondsLeft = refreshSeconds - counterSeconds;

    var minutes = Math.floor(totalSecondsLeft / 60)
    var seconds = totalSecondsLeft % 60;

    document.getElementById("time-remaining").innerHTML = minutes + ":" + (seconds+'').padStart(2, '0');

    if (totalSecondsLeft < 0) {
        clearInterval(refreshCounter2);
        window.location.reload();
        document.getElementById("refresh-display").innerHTML = "Error: Refresh manually";
    }
}, 1000);

function pauseCountdown() {
    paused = !paused;
}

function highlightStars(starIndex) {
    for (var i=1; i <= 5; i++) {
        document.getElementById("rating-"+i).innerHTML = (i <= starIndex) ? "★" : "☆";
    }
}

function showRating() {
    highlightStars(rating);
}

function setRating(starIndex, file_reference) {
    rating = starIndex;
    showRating();
    $.ajax({
        url: '/_save_rating',
        data: {
            rating: rating,
            file_reference: file_reference
        },
        success: function(response) {
            console.log(response);
            elements = document.getElementsByClassName("starRatings")
            for (var i=0; i < elements.length; i++) {
                elements[i].style.color = 'rgba(243, 229, 171, 0.66)';
            }
        },
        error: function(error) {
            console.log(error);
            elements = document.getElementsByClassName("starRatings")
            for (var i=0; i < elements.length; i++) {
                elements[i].style.color = 'rgba(139, 0, 0, 0.66)';
            }
        }
    });
}

function flagPicture(file_reference) {
    $.ajax({
        url: '/_flag_picture',
        data: {
            file_reference: file_reference
        },
        success: function(response) {
            console.log(response);
            flag = document.getElementById("flag");
            flag.style.backgroundColor = 'rgba(243, 229, 171, 0.66)';
            flag.style.border = '1px solid rgba(243, 229, 171, 0.33)';
        },
        error: function(error) {
            console.log(error);
            flag = document.getElementById("flag");
            flag.style.backgroundColor = 'rgba(139, 0, 0, 0.66)';
            flag.style.border = '1px solid rgba(139, 0, 0, 0.33)';
        }
    });
}
