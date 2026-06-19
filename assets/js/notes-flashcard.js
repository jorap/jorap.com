/**
 * Flip cards: click or Enter/Space toggles front/back.
 */
(function () {
  function toggle(card, btn) {
    var flipped = card.classList.toggle("is-flipped");
    btn.setAttribute("aria-pressed", flipped ? "true" : "false");
  }

  document.addEventListener("click", function (event) {
    var btn = event.target.closest("[data-flashcard-flip]");
    if (!btn) return;
    var card = btn.closest("[data-flashcard]");
    if (!card) return;
    toggle(card, btn);
  });

  document.addEventListener("keydown", function (event) {
    if (event.key !== "Enter" && event.key !== " ") return;
    var btn = event.target.closest("[data-flashcard-flip]");
    if (!btn) return;
    event.preventDefault();
    var card = btn.closest("[data-flashcard]");
    if (!card) return;
    toggle(card, btn);
  });
})();
