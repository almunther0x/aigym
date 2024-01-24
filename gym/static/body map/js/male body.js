// Get references to the SVG muscle groups and video elements
const abdominalsGroup = document.getElementById("abdominals");
const obliquesGroup = document.getElementById("obliques");
const abdominalsVideo = document.getElementById("abdominals-video");
const obliquesVideo = document.getElementById("obliques-video");

// Add click event listeners to the muscle group elements
abdominalsGroup.addEventListener("click", function () {
    // Hide all videos initially
    abdominalsVideo.style.display = "block";
    obliquesVideo.style.display = "none";

    // Play the abdominals video
    abdominalsVideo.play();
});

obliquesGroup.addEventListener("click", function () {
    // Hide all videos initially
    abdominalsVideo.style.display = "none";
    obliquesVideo.style.display = "block";

    // Play the obliques video
    obliquesVideo.play();
});