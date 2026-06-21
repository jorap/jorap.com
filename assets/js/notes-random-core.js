/**
 * Shared helpers for random note / duo UIs.
 */
(function () {
  var SKIP_ARTICLE =
    ".notes-graph-panel, .notes-toolbar, .article-title, .toc-wrapper, .notes-outgoing, .notes-see-also, .notes-backlinks, .notes-note-flashcards";
  var PROMPT_PREFILL_MAX_URL = 1800;

  function escapeHtml(str) {
    return String(str)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;");
  }

  function normalizeText(str) {
    return String(str || "")
      .replace(/\s+/g, " ")
      .trim();
  }

  function cloneArticleBody(article) {
    var body = document.createElement("div");
    body.className = "notes-random-body";
    var children = article.children;

    for (var i = 0; i < children.length; i += 1) {
      var child = children[i];
      if (child.matches(SKIP_ARTICLE)) continue;
      body.appendChild(child.cloneNode(true));
    }

    return body;
  }

  function cloneNoteContent(article) {
    var body = document.createElement("div");
    body.className = "notes-random-body";
    var contentEl = article.querySelector(".notes-content");
    if (!contentEl) return body;

    var clone = contentEl.cloneNode(true);
    clone.querySelectorAll(".notes-flashcard, .notes-note-flashcards").forEach(function (node) {
      node.remove();
    });
    body.appendChild(clone);
    return body;
  }

  function setSlotLoading(slot) {
    slot.innerHTML = '<p class="notes-random-loading text-ink-muted text-sm">Loading…</p>';
    slot.classList.remove("notes-random-panel--empty");
  }

  function setSlotEmpty(slot, message) {
    slot.innerHTML = '<p class="notes-random-empty text-ink-muted text-sm">' + message + "</p>";
    slot.classList.add("notes-random-panel--empty");
  }

  function renderNoteIntoSlot(slot, pick, opts) {
    opts = opts || {};

    if (!pick) {
      setSlotEmpty(slot, opts.emptyMessage || "No notes in the garden yet.");
      return Promise.resolve(null);
    }

    setSlotLoading(slot);

    var headingTag = opts.headingTag || "h3";
    var panelClass =
      "notes-random-panel border-divider rounded border p-5" + (opts.panelExtraClass ? " " + opts.panelExtraClass : "");
    var bodyFn = opts.bodyMode === "content" ? cloneNoteContent : cloneArticleBody;

    return fetch(pick.url)
      .then(function (res) {
        if (!res.ok) throw new Error("fetch failed");
        return res.text();
      })
      .then(function (html) {
        var doc = new DOMParser().parseFromString(html, "text/html");
        var article = doc.querySelector("article");
        var titleEl = doc.querySelector(".article-title");
        var contentEl = doc.querySelector(".notes-content");
        if (!article || !titleEl || !contentEl) throw new Error("parse failed");

        var panel = document.createElement("article");
        panel.className = panelClass;

        var heading = document.createElement(headingTag);
        heading.className = opts.headingClass || "h5 mb-3";
        var link = document.createElement("a");
        link.className = "text-accent no-underline hover:underline";
        link.href = pick.url;
        link.textContent = titleEl.textContent.trim();
        heading.appendChild(link);
        panel.appendChild(heading);
        panel.appendChild(bodyFn(article));

        slot.innerHTML = "";
        slot.appendChild(panel);
        slot.classList.remove("notes-random-panel--empty");

        return {
          title: titleEl.textContent.trim(),
          url: pick.url,
          bodyText: normalizeText(contentEl.textContent),
        };
      })
      .catch(function () {
        slot.innerHTML =
          "<article class=\"" +
          panelClass +
          '">' +
          "<" +
          headingTag +
          ' class="' +
          (opts.headingClass || "h5 mb-3") +
          '"><a class="text-accent no-underline hover:underline" href="' +
          escapeHtml(pick.url) +
          '">' +
          escapeHtml(pick.title) +
          "</a></" +
          headingTag +
          ">" +
          '<p class="text-ink-muted text-sm">Could not load this note. <a href="' +
          escapeHtml(pick.url) +
          '">Open it directly</a>.</p></article>';

        return {
          title: pick.title,
          url: pick.url,
          bodyText: "",
        };
      });
  }

  function pickOne(pool, excludeUrls) {
    if (!pool.length) return null;

    var exclude = excludeUrls || [];
    var candidates = pool.filter(function (entry) {
      return exclude.indexOf(entry.url) === -1;
    });

    if (!candidates.length) candidates = pool.slice();
    return candidates[Math.floor(Math.random() * candidates.length)];
  }

  function connectionPromptTail(heading) {
    return [
      heading,
      "- 3 unexpected links (surprising connections or new ideas)",
      "- 3 atomic note titles (clear, one-idea titles I can turn into [[wikilinks]])",
      "- 3 questions the pairing raises",
      "- 3 gaps, tensions, or contradictions worth exploring",
      "",
      "Constraints:",
      "- Keep suggestions practical for a personal knowledge garden",
      "- One idea per note, clear atomic titles",
      "- Focus on actionable insights, not abstract theory",
    ];
  }

  function createAiHelpers(opts) {
    var promptEl = opts.promptEl;
    var aiChatUrl = opts.aiChatUrl;
    var copyPromptBtn = opts.copyPromptBtn;
    var sendPromptBtn = opts.sendPromptBtn;
    var openedLabel = opts.openedLabel;
    var copiedLabel = opts.copiedLabel;

    function flashButton(btn, message) {
      if (!btn) return;
      var original = btn.textContent;
      btn.textContent = message;
      window.setTimeout(function () {
        btn.textContent = original;
      }, 1600);
    }

    function promptIsReady() {
      if (!promptEl) return false;
      var prompt = promptEl.value;
      if (!prompt) return false;
      if (prompt === "Loading note…" || prompt === "Loading notes…") return false;
      if (prompt.indexOf("Shuffle to load") === 0) return false;
      return true;
    }

    function aiChatFallbackUrl(template) {
      var qIndex = template.indexOf("?q=");
      if (qIndex !== -1) return template.slice(0, qIndex);
      var queryIndex = template.indexOf("?");
      if (queryIndex !== -1) return template.slice(0, queryIndex);
      return template;
    }

    function copyPrompt() {
      if (!promptEl || !navigator.clipboard || !promptIsReady()) return;

      navigator.clipboard.writeText(promptEl.value).then(function () {
        flashButton(copyPromptBtn, "Copied");
      });
    }

    function sendPromptToAI() {
      if (!promptEl || !promptIsReady()) return;

      var prompt = promptEl.value;
      var prefillUrl = aiChatUrl + encodeURIComponent(prompt);

      function openChat(url) {
        window.open(url, "_blank", "noopener,noreferrer");
      }

      if (prefillUrl.length <= PROMPT_PREFILL_MAX_URL) {
        openChat(prefillUrl);
        flashButton(sendPromptBtn, openedLabel);
        return;
      }

      if (!navigator.clipboard) {
        openChat(aiChatFallbackUrl(aiChatUrl));
        return;
      }

      navigator.clipboard.writeText(prompt).then(function () {
        openChat(aiChatFallbackUrl(aiChatUrl));
        flashButton(sendPromptBtn, copiedLabel);
      });
    }

    return {
      flashButton: flashButton,
      promptIsReady: promptIsReady,
      copyPrompt: copyPrompt,
      sendPromptToAI: sendPromptToAI,
    };
  }

  function bindTapIf(el, fn) {
    var bind = window.jorapBindTouchClickIf;
    if (bind) {
      bind(el, fn);
      return;
    }
    if (el) el.addEventListener("click", fn);
  }

  window.jorapNotesRandomCore = {
    cloneArticleBody: cloneArticleBody,
    connectionPromptTail: connectionPromptTail,
    createAiHelpers: createAiHelpers,
    bindTapIf: bindTapIf,
    normalizeText: normalizeText,
    pickOne: pickOne,
    renderNoteIntoSlot: renderNoteIntoSlot,
    setSlotEmpty: setSlotEmpty,
    setSlotLoading: setSlotLoading,
  };
})();
