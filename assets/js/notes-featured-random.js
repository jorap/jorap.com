/**
 * Notes home: featured block shows one random garden note per visit.
 */
(function () {
  var core = window.jorapNotesRandomCore;
  if (!core) return;

  var root = document.querySelector("[data-notes-featured-random]");
  var dataEl = document.querySelector(".notes-featured-random-data");
  var slot = document.querySelector("[data-notes-featured-random-slot]");
  if (!root || !dataEl || !slot) return;

  var pool = [];
  try {
    pool = JSON.parse(dataEl.textContent);
  } catch (e) {
    pool = [];
  }

  function render(pick) {
    if (!pick) {
      slot.innerHTML =
        '<p class="notes-featured-random-empty text-ink-muted text-sm">No notes in the garden yet.</p>';
      return;
    }

    core.renderNoteIntoSlot(slot, pick, {
      headingTag: "h2",
      headingClass: "h5 mb-3",
      panelExtraClass: "notes-featured-random-panel",
    });
  }

  render(pool.length ? core.pickOne(pool) : null);
})();
