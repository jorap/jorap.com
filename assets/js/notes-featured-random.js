/**
 * Notes home: featured block shows one random garden note per visit.
 */
(function () {
  var root = document.querySelector("[data-notes-featured-random]");
  var dataEl = document.querySelector(".notes-featured-random-data");
  var slot = document.querySelector("[data-notes-featured-random-slot]");
  if (!root || !dataEl || !slot) return;

  var pool;
  try {
    pool = JSON.parse(dataEl.textContent);
  } catch (e) {
    pool = [];
  }

  var skipArticleSelector =
    ".notes-graph-panel, .notes-toolbar, .article-title, .toc-wrapper, .notes-outgoing, .notes-see-also, .notes-backlinks, .notes-note-flashcards";

  function escapeHtml(str) {
    return String(str)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;");
  }

  function pickOne() {
    if (!pool.length) return null;
    return pool[Math.floor(Math.random() * pool.length)];
  }

  function cloneArticleBody(article) {
    var body = document.createElement("div");
    body.className = "notes-random-body";
    var children = article.children;

    for (var i = 0; i < children.length; i += 1) {
      var child = children[i];
      if (child.matches(skipArticleSelector)) continue;
      body.appendChild(child.cloneNode(true));
    }

    return body;
  }

  function setEmpty() {
    slot.innerHTML =
      '<p class="notes-featured-random-empty text-ink-muted text-sm">No notes in the garden yet.</p>';
  }

  function render(pick) {
    if (!pick) {
      setEmpty();
      return;
    }

    slot.innerHTML = '<p class="notes-random-loading text-ink-muted text-sm">Loading…</p>';

    fetch(pick.url)
      .then(function (res) {
        if (!res.ok) throw new Error("fetch failed");
        return res.text();
      })
      .then(function (html) {
        var doc = new DOMParser().parseFromString(html, "text/html");
        var article = doc.querySelector("article");
        var titleEl = doc.querySelector(".article-title");
        if (!article || !titleEl) throw new Error("parse failed");

        var panel = document.createElement("article");
        panel.className =
          "notes-featured-random-panel notes-random-panel border-divider rounded border p-5";

        var heading = document.createElement("h2");
        heading.className = "h4 mb-3";
        var link = document.createElement("a");
        link.className = "text-accent no-underline hover:underline";
        link.href = pick.url;
        link.textContent = titleEl.textContent.trim();
        heading.appendChild(link);
        panel.appendChild(heading);
        panel.appendChild(cloneArticleBody(article));

        slot.innerHTML = "";
        slot.appendChild(panel);
      })
      .catch(function () {
        slot.innerHTML =
          '<article class="notes-featured-random-panel notes-random-panel border-divider rounded border p-5">' +
          '<h2 class="h4 mb-3"><a class="text-accent no-underline hover:underline" href="' +
          escapeHtml(pick.url) +
          '">' +
          escapeHtml(pick.title) +
          "</a></h2>" +
          '<p class="text-ink-muted text-sm">Could not load this note. Open the link to read it.</p>' +
          "</article>";
      });
  }

  render(pickOne());
})();
