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

  // ── Hero slider — auto-rotate + arrow navigation + dots + swipe ──────
  var slides = document.querySelectorAll(".hero-slider .slide");
  var prevBtn = document.querySelector(".slider-prev");
  var nextBtn = document.querySelector(".slider-next");
  var dots = document.querySelectorAll(".slider-dots .dot");

  if (slides.length > 1) {
    var current = 0;
    var total = slides.length;
    var interval;

    function goToSlide(index) {
      slides[current].classList.remove("active");
      if (dots.length) {
        dots[current].classList.remove("active");
        dots[current].setAttribute("aria-selected", "false");
      }
      current = (index + total) % total;
      slides[current].classList.add("active");
      if (dots.length) {
        dots[current].classList.add("active");
        dots[current].setAttribute("aria-selected", "true");
      }
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

    // Dot click handlers
    dots.forEach(function (dot, i) {
      dot.addEventListener("click", function () {
        goToSlide(i);
        resetAutoRotate();
      });
    });

    // Touch swipe support
    var slider = document.querySelector(".hero-slider");
    if (slider) {
      var touchStartX = 0;
      var touchEndX = 0;
      var minSwipeDistance = 50;

      slider.addEventListener(
        "touchstart",
        function (e) {
          touchStartX = e.changedTouches[0].screenX;
        },
        { passive: true },
      );

      slider.addEventListener(
        "touchend",
        function (e) {
          touchEndX = e.changedTouches[0].screenX;
          var diff = touchStartX - touchEndX;
          if (Math.abs(diff) > minSwipeDistance) {
            if (diff > 0) {
              goToSlide(current + 1);
            } else {
              goToSlide(current - 1);
            }
            resetAutoRotate();
          }
        },
        { passive: true },
      );
    }

    startAutoRotate();
  }
})();
