document.getElementById("year").textContent = new Date().getFullYear();

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
