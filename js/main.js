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

  // ── Hero slider — auto-rotate + arrow navigation ──────
  var slides = document.querySelectorAll(".hero-slider .slide");
  var prevBtn = document.querySelector(".slider-prev");
  var nextBtn = document.querySelector(".slider-next");

  if (slides.length > 1) {
    var current = 0;
    var total = slides.length;
    var interval;

    function goToSlide(index) {
      slides[current].classList.remove("active");
      current = (index + total) % total;
      slides[current].classList.add("active");
    }

    function startAutoRotate() {
      interval = setInterval(function () {
        goToSlide(current + 1);
      }, 5000);
    }

    function resetAutoRotate() {
      clearInterval(interval);
      startAutoRotate();
    }

    if (prevBtn) {
      prevBtn.addEventListener("click", function () {
        goToSlide(current - 1);
        resetAutoRotate();
      });
    }

    if (nextBtn) {
      nextBtn.addEventListener("click", function () {
        goToSlide(current + 1);
        resetAutoRotate();
      });
    }

    startAutoRotate();
  }
})();
