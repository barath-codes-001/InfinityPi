document.addEventListener("DOMContentLoaded", function () {

    const form = document.getElementById("piForm");
    const loading = document.getElementById("loading");
    const buttons = document.querySelectorAll("button");

    form.addEventListener("submit", function () {

        // Show loading animation
        loading.style.display = "block";

        // Disable buttons
        buttons.forEach(button => {
            button.disabled = true;
            button.innerText = "Processing...";
        });

    });

});