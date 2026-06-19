/**
 * Notes index: status filters and random note picker.
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

  filters.forEach(function (btn) {
    btn.addEventListener("click", function () {
      var name = btn.getAttribute("data-notes-filter");
      filters.forEach(function (b) {
        var on = b === btn;
        b.classList.toggle("is-active", on);
        b.setAttribute("aria-pressed", on ? "true" : "false");
      });
      applyFilter(name);
    });
  });

  var randomBtn = document.querySelector("[data-notes-random]");
  var randomData = document.querySelector(".notes-random-data");
  if (randomBtn && randomData) {
    var pool;
    try {
      pool = JSON.parse(randomData.textContent);
    } catch (e) {
      pool = [];
    }

    randomBtn.addEventListener("click", function () {
      if (!pool.length) return;
      var pick = pool[Math.floor(Math.random() * pool.length)];
      if (pick && pick.url) {
        window.location.href = pick.url;
      }
    });
  }
})();
