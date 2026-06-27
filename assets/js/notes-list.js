/**
 * Notes index: search and tag/category facets.
 */
(function () {
  var grid = document.querySelector("[data-notes-grid]");
  if (!grid) return;

  var items = grid.querySelectorAll(".notes-grid-item");
  var searchEl = document.querySelector("[data-notes-search]");
  var tagEl = document.querySelector("[data-notes-tag]");
  var categoryEl = document.querySelector("[data-notes-category]");
  var emptyEl = document.querySelector("[data-notes-filter-empty]");

  var state = {
    search: "",
    tag: "",
    category: "",
  };

  function readUrlState() {
    var params = new URLSearchParams(window.location.search);
    var tag = params.get("tag");
    if (tag) state.tag = tag;
    var category = params.get("category");
    if (category) state.category = category;
    var q = params.get("q");
    if (q) state.search = q;
  }

  function syncControls() {
    if (searchEl) searchEl.value = state.search;
    if (tagEl) tagEl.value = state.tag;
    if (categoryEl) categoryEl.value = state.category;
  }

  function itemMatches(item) {
    if (state.tag) {
      var tags = (item.getAttribute("data-note-tags") || "").split(/\s+/).filter(Boolean);
      if (tags.indexOf(state.tag) === -1) return false;
    }

    if (state.category) {
      var cats = (item.getAttribute("data-note-categories") || "").split(/\s+/).filter(Boolean);
      if (cats.indexOf(state.category) === -1) return false;
    }

    if (state.search) {
      var hay = item.getAttribute("data-note-search") || "";
      if (hay.indexOf(state.search) === -1) return false;
    }

    return true;
  }

  function applyFilters() {
    var visible = 0;
    items.forEach(function (item) {
      var show = itemMatches(item);
      item.classList.toggle("hidden", !show);
      if (show) visible += 1;
    });
    if (emptyEl) emptyEl.classList.toggle("hidden", visible > 0);
  }

  function updateUrl() {
    var params = new URLSearchParams();
    if (state.tag) params.set("tag", state.tag);
    if (state.category) params.set("category", state.category);
    if (state.search) params.set("q", state.search);
    var qs = params.toString();
    var next = window.location.pathname + (qs ? "?" + qs : "");
    if (next !== window.location.pathname + window.location.search) {
      window.history.replaceState(null, "", next);
    }
  }

  if (searchEl) {
    searchEl.addEventListener("input", function () {
      state.search = searchEl.value.trim().toLowerCase();
      applyFilters();
      updateUrl();
    });
  }

  if (tagEl) {
    tagEl.addEventListener("change", function () {
      state.tag = tagEl.value || "";
      applyFilters();
      updateUrl();
    });
  }

  if (categoryEl) {
    categoryEl.addEventListener("change", function () {
      state.category = categoryEl.value || "";
      applyFilters();
      updateUrl();
    });
  }

  readUrlState();
  syncControls();
  applyFilters();

  if (state.tag || state.category) {
    var refineEl = document.querySelector(".notes-list-refine");
    if (refineEl) refineEl.open = true;
  }
})();
