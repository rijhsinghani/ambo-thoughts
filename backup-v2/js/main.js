/* Ambo Thoughts — JS */

(function () {
  "use strict";

  // ── Mobile menu toggle ──────────────────────────────────
  var toggle = document.querySelector(".menu-toggle");
  var nav = document.querySelector(".nav-links");

  if (toggle && nav) {
    toggle.addEventListener("click", function () {
      var isOpen = nav.classList.toggle("open");
      toggle.setAttribute("aria-expanded", isOpen);
      toggle.textContent = isOpen ? "\u2715" : "\u2630";
    });

    nav.querySelectorAll("a").forEach(function (link) {
      link.addEventListener("click", function () {
        nav.classList.remove("open");
        toggle.setAttribute("aria-expanded", "false");
        toggle.textContent = "\u2630";
      });
    });
  }

  // ── Set active nav link based on current page ───────────
  var currentPage = window.location.pathname.split("/").pop() || "index.html";
  document.querySelectorAll(".nav-links a").forEach(function (link) {
    var href = link.getAttribute("href");
    if (href === currentPage || (currentPage === "" && href === "index.html")) {
      link.classList.add("active");
    }
  });

  // ── Hero Slider — auto-rotate + arrow navigation ───────
  var slider = document.querySelector(".hero-slider");
  if (slider) {
    var slides = slider.querySelectorAll(".slide");
    var prevBtn = slider.querySelector(".slider-prev");
    var nextBtn = slider.querySelector(".slider-next");
    var currentSlide = 0;
    var slideCount = slides.length;
    var autoInterval = 5000; // 5 seconds per slide
    var timer;

    function goToSlide(index) {
      slides[currentSlide].classList.remove("active");
      currentSlide = (index + slideCount) % slideCount;
      slides[currentSlide].classList.add("active");
    }

    function nextSlide() {
      goToSlide(currentSlide + 1);
    }

    function prevSlide() {
      goToSlide(currentSlide - 1);
    }

    function startAutoRotate() {
      timer = setInterval(nextSlide, autoInterval);
    }

    function resetAutoRotate() {
      clearInterval(timer);
      startAutoRotate();
    }

    if (nextBtn) {
      nextBtn.addEventListener("click", function () {
        nextSlide();
        resetAutoRotate();
      });
    }

    if (prevBtn) {
      prevBtn.addEventListener("click", function () {
        prevSlide();
        resetAutoRotate();
      });
    }

    // Pause auto-rotate on hover
    slider.addEventListener("mouseenter", function () {
      clearInterval(timer);
    });

    slider.addEventListener("mouseleave", function () {
      startAutoRotate();
    });

    // Start auto-rotation
    if (slideCount > 1) {
      startAutoRotate();
    }
  }
})();
