"use strict";

const form1 = document.getElementById("form1");
const form2 = document.getElementById("form2");
const form3 = document.getElementById("form3");
const progressEl = document.getElementById("progress");
const circles = document.querySelectorAll(".circle");
let currentActive = 1;

// Function to show the specified form and hide others
function showForm(formToShow) {
    const forms = [form1, form2, form3];
    forms.forEach(form => {
        if (form === formToShow) {
            form.style.left = "25px"; // Show the form
        } else {
            form.style.left = "450px"; // Hide the form
        }
    });
}

// Function to handle moving to the next form
function nextForm() {
    if (currentActive < circles.length) {
        currentActive++;
        updateProgress();
        showForm(document.getElementById(`form${currentActive}`));
    }
}

// Function to handle going back to the previous form
function prevForm() {
    if (currentActive > 1) {
        currentActive--;
        updateProgress();
        showForm(document.getElementById(`form${currentActive}`));
    }
}

// Function to update the progress bar
function updateProgress() {
    circles.forEach((circle, index) => {
        if (index < currentActive) {
            circle.classList.add("active");
        } else {
            circle.classList.remove("active");
        }
    });

    const progressWidth = ((currentActive - 1) / (circles.length - 1)) * 100 + "%";
    progressEl.style.width = progressWidth;
}

// Event listeners for navigation buttons
document.getElementById("next1").addEventListener("click", nextForm);
document.getElementById("next2").addEventListener("click", nextForm);
document.getElementById("back1").addEventListener("click", prevForm);
document.getElementById("back2").addEventListener("click", prevForm);

// Initial setup
updateProgress();
showForm(form1); // Show the first form initially
