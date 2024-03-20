// script.js

const slides = document.querySelectorAll('.slide');
let currentSlide = 0;

function showSlide(n) {
    slides[currentSlide].style.display = 'none';
    currentSlide = n;
    slides[currentSlide].style.display = 'block';
}

function nextSlide() {
    const currentForm = document.querySelector(`#slide${currentSlide + 1}-form`);
    if (currentForm.checkValidity()) {
        showSlide(currentSlide + 1);
    } else {
        currentForm.reportValidity();
    }
}

showSlide(currentSlide);
