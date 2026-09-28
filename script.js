const yearEl = document.getElementById("year");
if (yearEl) yearEl.textContent = new Date().getFullYear();

/* Timeline: the recent three carry the argument, the earlier years are there
   for anyone who wants them. Collapsed by default rather than cut, so the
   depth stays without the page reading as a CV. */
(function () {
  const toggle = document.getElementById("timeline-toggle");
  if (!toggle) return;

  const extra = document.querySelectorAll(".timeline-extra");
  if (!extra.length) {
    toggle.hidden = true;
    return;
  }

  toggle.addEventListener("click", function () {
    const opening = toggle.getAttribute("aria-expanded") !== "true";
    extra.forEach(function (el) {
      el.hidden = !opening;
    });
    toggle.setAttribute("aria-expanded", String(opening));
    toggle.textContent = opening ? "Hide the earlier years" : "Show the earlier years";
  });
})();

/* Reusable Photo Carousel Controller
   Handles touch scroll snap sync, prev/next buttons, keyboard navigation,
   and accessible slide counters. */
(function () {
  const carousels = document.querySelectorAll(".carousel-container");
  if (!carousels.length) return;

  carousels.forEach(function (carousel) {
    const track = carousel.querySelector(".carousel-track");
    const slides = carousel.querySelectorAll(".carousel-slide");
    const prevBtn = carousel.querySelector(".carousel-btn.prev");
    const nextBtn = carousel.querySelector(".carousel-btn.next");
    const counter = carousel.querySelector(".carousel-counter");

    if (!track || !slides.length) return;

    let currentIndex = 0;
    const totalSlides = slides.length;

    function updateState() {
      if (counter) {
        counter.textContent = (currentIndex + 1) + " / " + totalSlides;
      }
      if (prevBtn) {
        prevBtn.disabled = currentIndex === 0;
      }
      if (nextBtn) {
        nextBtn.disabled = currentIndex === totalSlides - 1;
      }
    }

    function scrollToSlide(index) {
      if (index < 0 || index >= totalSlides) return;
      currentIndex = index;
      const targetSlide = slides[currentIndex];
      if (targetSlide) {
        track.scrollTo({
          left: targetSlide.offsetLeft - track.offsetLeft,
          behavior: "smooth"
        });
      }
      updateState();
    }

    if (prevBtn) {
      prevBtn.addEventListener("click", function () {
        scrollToSlide(currentIndex - 1);
      });
    }

    if (nextBtn) {
      nextBtn.addEventListener("click", function () {
        scrollToSlide(currentIndex + 1);
      });
    }

    // Sync on touch swipe / scroll
    let scrollTimeout;
    track.addEventListener("scroll", function () {
      clearTimeout(scrollTimeout);
      scrollTimeout = setTimeout(function () {
        const scrollLeft = track.scrollLeft;
        let closestIndex = 0;
        let minDiff = Infinity;
        slides.forEach(function (slide, idx) {
          const diff = Math.abs((slide.offsetLeft - track.offsetLeft) - scrollLeft);
          if (diff < minDiff) {
            minDiff = diff;
            closestIndex = idx;
          }
        });
        if (currentIndex !== closestIndex) {
          currentIndex = closestIndex;
          updateState();
        }
      }, 50);
    }, { passive: true });

    // Keyboard arrow navigation
    carousel.addEventListener("keydown", function (e) {
      if (e.key === "ArrowLeft") {
        e.preventDefault();
        scrollToSlide(currentIndex - 1);
      } else if (e.key === "ArrowRight") {
        e.preventDefault();
        scrollToSlide(currentIndex + 1);
      }
    });

    updateState();
  });
})();
