/**
 * Notes index: status filters, facets, and search.
 */
(function () {
  var grid = document.querySelector("[data-notes-grid]");
  if (!grid) return;

  var items = grid.querySelectorAll(".notes-grid-item");
  var statusFilters = document.querySelectorAll("[data-notes-filter]");
  var toggleFilters = document.querySelectorAll("[data-notes-toggle]");
  var searchEl = document.querySelector("[data-notes-search]");
  var tagEl = document.querySelector("[data-notes-tag]");
  var categoryEl = document.querySelector("[data-notes-category]");
  var emptyEl = document.querySelector("[data-notes-filter-empty]");

  var state = {
    status: "all",
    search: "",
    tag: "",
    category: "",
    featured: false,
    cards: false,
    issues: false,
  };

  function readUrlState() {
    var params = new URLSearchParams(window.location.search);
    var status = params.get("status");
    if (status) state.status = status;
    var tag = params.get("tag");
    if (tag) state.tag = tag;
    var category = params.get("category");
    if (category) state.category = category;
    if (params.get("featured") === "1") state.featured = true;
    if (params.get("cards") === "1") state.cards = true;
    if (params.get("issues") === "1") state.issues = true;
    var q = params.get("q");
    if (q) state.search = q;
  }

  function syncControls() {
    statusFilters.forEach(function (btn) {
      var name = btn.getAttribute("data-notes-filter");
      var on = name === state.status;
      btn.classList.toggle("is-active", on);
      btn.setAttribute("aria-pressed", on ? "true" : "false");
    });
    toggleFilters.forEach(function (btn) {
      var name = btn.getAttribute("data-notes-toggle");
      var on = Boolean(state[name]);
      btn.classList.toggle("is-active", on);
      btn.setAttribute("aria-pressed", on ? "true" : "false");
    });
    if (searchEl) searchEl.value = state.search;
    if (tagEl) tagEl.value = state.tag;
    if (categoryEl) categoryEl.value = state.category;
  }

  function itemMatches(item) {
    var status = item.getAttribute("data-note-status") || "";
    var stale = item.getAttribute("data-note-stale") === "true";
    var statusOk =
      state.status === "all" ||
      (state.status === "stale" && stale) ||
      (state.status !== "stale" && status === state.status);
    if (!statusOk) return false;

    if (state.featured && item.getAttribute("data-note-featured") !== "true") return false;
    if (state.cards && item.getAttribute("data-note-cards") !== "true") return false;
    if (state.issues && item.getAttribute("data-note-issues") !== "true") return false;

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
    if (state.status !== "all") params.set("status", state.status);
    if (state.tag) params.set("tag", state.tag);
    if (state.category) params.set("category", state.category);
    if (state.featured) params.set("featured", "1");
    if (state.cards) params.set("cards", "1");
    if (state.issues) params.set("issues", "1");
    if (state.search) params.set("q", state.search);
    var qs = params.toString();
    var next = window.location.pathname + (qs ? "?" + qs : "");
    if (next !== window.location.pathname + window.location.search) {
      window.history.replaceState(null, "", next);
    }
  }

  var bindTap = window.jorapBindTouchClick || function (el, fn) {
    el.addEventListener("click", fn);
  };

  statusFilters.forEach(function (btn) {
    bindTap(btn, function () {
      state.status = btn.getAttribute("data-notes-filter") || "all";
      syncControls();
      applyFilters();
      updateUrl();
    });
  });

  toggleFilters.forEach(function (btn) {
    bindTap(btn, function () {
      var name = btn.getAttribute("data-notes-toggle");
      if (!name) return;
      state[name] = !state[name];
      syncControls();
      applyFilters();
      updateUrl();
    });
  });

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
