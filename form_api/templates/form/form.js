document.addEventListener("DOMContentLoaded", function () {
    const steps = document.querySelectorAll(".step");
    const nextButtons = document.querySelectorAll(".next");
    const prevButtons = document.querySelectorAll(".prev");
    let currentStep = 0;

    steps[currentStep].classList.add("active");

    nextButtons.forEach(button => {
        button.addEventListener("click", () => {
            steps[currentStep].classList.remove("active");
            currentStep++;
            steps[currentStep].classList.add("active");
        });
    });

    prevButtons.forEach(button => {
        button.addEventListener("click", () => {
            steps[currentStep].classList.remove("active");
            currentStep--;
            steps[currentStep].classList.add("active");
        });
    });

    document.getElementById("multiStepForm").addEventListener("submit", function (e) {
        e.preventDefault();
        alert("Form submitted!");
    });
});

