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

function setRating(starIndex) {
    rating = starIndex;
    showRating();
}
