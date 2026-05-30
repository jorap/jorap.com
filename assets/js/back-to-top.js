/*
 * Back-to-top button + scroll-progress ring.
 * Used by themes/jorap/layouts/partials/components/back-to-top.html.
 * Safe no-op if either element is absent.
 */
(function () {
  "use strict";

  const button = document.getElementById("back-to-top");
  const ring = document.querySelector(".progress-ring__progress");
  if (!button || !ring) return;

  // CSP-safe replacement for the previous inline `onclick=…` handler.
  const trigger = button.querySelector("[data-back-to-top]");
  trigger?.addEventListener("click", () => {
    window.scrollTo({ top: 0, behavior: "smooth" });
  });

  const RADIUS = 20;
  const CIRCUMFERENCE = 2 * Math.PI * RADIUS;
  ring.style.strokeDasharray = `${CIRCUMFERENCE} ${CIRCUMFERENCE}`;
  ring.style.strokeDashoffset = String(CIRCUMFERENCE);

  let ticking = false;
  const update = () => {
    if (ticking) return;
    ticking = true;
    requestAnimationFrame(() => {
      const scrollable =
        document.documentElement.scrollHeight - window.innerHeight;
      const pct = scrollable > 0 ? window.scrollY / scrollable : 0;
      ring.style.strokeDashoffset = String(CIRCUMFERENCE - pct * CIRCUMFERENCE);
      button.classList.toggle("hidden", window.scrollY <= 300);
      ticking = false;
    });
  };

  window.addEventListener("scroll", update, { passive: true });
  update();
})();
