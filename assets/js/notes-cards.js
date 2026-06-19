/**
 * Cards index: filter by tag chip.
 */
(function () {
  var root = document.querySelector("[data-notes-cards]");
  if (!root) return;

  var filters = root.querySelectorAll("[data-notes-cards-filter]");
  var items = root.querySelectorAll("[data-notes-cards-item]");
  var emptyEl = root.querySelector("[data-notes-cards-empty]");

  function applyFilter(tag) {
    var visible = 0;

    items.forEach(function (item) {
      var tags = (item.getAttribute("data-notes-cards-tags") || "").split(",").filter(Boolean);
      var show = tag === "all" || tags.indexOf(tag) !== -1;
      item.classList.toggle("hidden", !show);
      if (show) visible += 1;
    });

    filters.forEach(function (btn) {
      var active = btn.getAttribute("data-notes-cards-filter") === tag;
      btn.classList.toggle("is-active", active);
      btn.setAttribute("aria-pressed", active ? "true" : "false");
    });

    if (emptyEl) {
      emptyEl.classList.toggle("hidden", visible > 0);
    }
  }

  filters.forEach(function (btn) {
    btn.addEventListener("click", function () {
      applyFilter(btn.getAttribute("data-notes-cards-filter") || "all");
    });
  });
})();
