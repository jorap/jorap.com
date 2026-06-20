/**
 * Notes index: status filters.
 */
(function () {
  var grid = document.querySelector("[data-notes-grid]");
  if (!grid) return;

  var items = grid.querySelectorAll(".notes-grid-item");
  var filters = document.querySelectorAll("[data-notes-filter]");
  var emptyEl = document.querySelector("[data-notes-filter-empty]");
  var active = "all";

  function applyFilter(name) {
    active = name;
    var visible = 0;

    items.forEach(function (item) {
      var status = item.getAttribute("data-note-status") || "";
      var stale = item.getAttribute("data-note-stale") === "true";
      var show =
        name === "all" ||
        (name === "stale" && stale) ||
        (name !== "stale" && status === name);

      item.classList.toggle("hidden", !show);
      if (show) visible += 1;
    });

    if (emptyEl) {
      emptyEl.classList.toggle("hidden", visible > 0);
    }
  }

  var bindTap = window.jorapBindTouchClick || function (el, fn) {
    el.addEventListener("click", fn);
  };

  filters.forEach(function (btn) {
    bindTap(btn, function () {
      var name = btn.getAttribute("data-notes-filter");
      filters.forEach(function (b) {
        var on = b === btn;
        b.classList.toggle("is-active", on);
        b.setAttribute("aria-pressed", on ? "true" : "false");
      });
      applyFilter(name);
    });
  });
})();
