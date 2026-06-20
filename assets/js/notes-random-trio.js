/**
 * Random Trio page: pick a trio and load note bodies into columns.
 */
(function () {
  var root = document.querySelector("[data-notes-random-trio]");
  var dataEl = document.querySelector(".notes-random-trio-data");
  var shuffleAllBtn = document.querySelector("[data-random-trio-shuffle-all]");
  var shuffleLeftBtn = document.querySelector("[data-random-trio-shuffle-left]");
  var shuffleCenterBtn = document.querySelector("[data-random-trio-shuffle-center]");
  var shuffleRightBtn = document.querySelector("[data-random-trio-shuffle-right]");
  var copyPromptBtn = document.querySelector("[data-random-trio-copy-prompt]");
  var sendPromptBtn = document.querySelector("[data-random-trio-send-prompt]");
  var promptEl = document.querySelector("[data-random-trio-prompt]");
  var emptyPageEl = document.querySelector("[data-random-trio-empty-page]");
  if (!root || !dataEl) return;

  var slotCount = 3;
  var slots = root.querySelectorAll("[data-random-trio-slot]");
  var currentNotes = [null, null, null];
  var pool;
  var aiChatUrl = "https://chatgpt.com/?q=";
  var aiChatOpenedLabel = "Opened";
  var aiChatCopiedLabel = "Copied — paste in chat";
  var PROMPT_PREFILL_MAX_URL = 1800;

  try {
    pool = JSON.parse(dataEl.textContent);
  } catch (e) {
    pool = [];
  }

  function pickOne(excludeUrls) {
    if (!pool.length) return null;

    var exclude = excludeUrls || [];
    var candidates = pool.filter(function (entry) {
      return exclude.indexOf(entry.url) === -1;
    });

    if (!candidates.length) {
      candidates = pool.slice();
    }

    return candidates[Math.floor(Math.random() * candidates.length)];
  }

  function pickMany(count) {
    var picks = [];
    var exclude = [];

    for (var i = 0; i < count; i += 1) {
      var pick = pickOne(exclude);
      if (!pick) break;
      picks.push(pick);
      exclude.push(pick.url);
    }

    while (picks.length < count) {
      picks.push(null);
    }

    return picks;
  }

  function escapeHtml(str) {
    return String(str)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;");
  }

  function setSlotLoading(slot) {
    slot.innerHTML = '<p class="notes-random-loading text-ink-muted text-sm">Loading…</p>';
    slot.classList.remove("notes-random-panel--empty");
  }

  function setSlotEmpty(slot) {
    slot.innerHTML =
      '<p class="notes-random-empty text-ink-muted text-sm">Not enough notes to fill this column.</p>';
    slot.classList.add("notes-random-panel--empty");
  }

  function normalizeText(str) {
    return String(str || "")
      .replace(/\s+/g, " ")
      .trim();
  }

  function buildPrompt(notes) {
    var usable = notes.filter(function (note) {
      return note && note.title;
    });

    if (!usable.length) {
      return "Shuffle to load three notes, then paste this prompt into your AI chat.";
    }

    var lines = [
      "I'm exploring connections between three notes from my digital garden. Help me discover new ideas by analyzing how they relate.",
      "",
    ];

    usable.forEach(function (note, index) {
      lines.push("Note " + (index + 1) + ': "' + note.title + '"');
      if (note.url) lines.push("URL: " + window.location.origin + note.url);
      if (note.bodyText) lines.push(note.bodyText);
      lines.push("");
    });

    lines.push("Please analyze:");
    lines.push("- All three notes together");
    lines.push("- Note 1 + Note 2");
    lines.push("- Note 1 + Note 3");
    lines.push("- Note 2 + Note 3");
    lines.push("");
    lines.push("For each combination, provide:");
    lines.push("- 3 unexpected links (surprising connections or new ideas)");
    lines.push("- 3 atomic note titles (clear, one-idea titles I can turn into [[wikilinks]])");
    lines.push("- 3 questions the pairing raises");
    lines.push("- 3 gaps, tensions, or contradictions worth exploring");
    lines.push("");
    lines.push("Constraints:");
    lines.push("- Keep all suggestions practical for a personal knowledge garden");
    lines.push("- One idea per note, clear atomic titles");
    lines.push("- Focus on actionable insights, not abstract theory");

    return lines.join("\n");
  }

  function updatePrompt(notes) {
    if (!promptEl) return;
    promptEl.value = buildPrompt(notes);
  }

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
    if (prompt === "Loading notes…") return false;
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
      flashButton(sendPromptBtn, aiChatOpenedLabel);
      return;
    }

    if (!navigator.clipboard) {
      openChat(aiChatFallbackUrl(aiChatUrl));
      return;
    }

    navigator.clipboard.writeText(prompt).then(function () {
      openChat(aiChatFallbackUrl(aiChatUrl));
      flashButton(sendPromptBtn, aiChatCopiedLabel);
    });
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

  function equalizePanelHeights() {
    var panels = root.querySelectorAll(".notes-random-panel");
    if (panels.length < 2) return;

    panels.forEach(function (panel) {
      panel.style.minHeight = "";
    });

    var maxHeight = 0;
    panels.forEach(function (panel) {
      maxHeight = Math.max(maxHeight, panel.offsetHeight);
    });

    if (maxHeight > 0) {
      panels.forEach(function (panel) {
        panel.style.minHeight = maxHeight + "px";
      });
    }
  }

  function renderNote(slot, pick) {
    if (!pick) {
      setSlotEmpty(slot);
      return Promise.resolve(null);
    }

    setSlotLoading(slot);

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
        panel.className = "notes-random-panel border-divider rounded border p-5";

        var heading = document.createElement("h2");
        heading.className = "h5 mb-3";
        var link = document.createElement("a");
        link.className = "text-accent no-underline hover:underline";
        link.href = pick.url;
        link.textContent = titleEl.textContent.trim();
        heading.appendChild(link);
        panel.appendChild(heading);
        panel.appendChild(cloneNoteContent(article));

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
          '<article class="notes-random-panel border-divider rounded border p-5">' +
          '<h2 class="h5 mb-3"><a class="text-accent no-underline hover:underline" href="' +
          escapeHtml(pick.url) +
          '">' +
          escapeHtml(pick.title) +
          "</a></h2>" +
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

  function shuffleAll() {
    if (!pool.length) {
      if (emptyPageEl) emptyPageEl.classList.remove("hidden");
      slots.forEach(setSlotEmpty);
      currentNotes = [null, null, null];
      updatePrompt([]);
      return;
    }

    if (emptyPageEl) emptyPageEl.classList.add("hidden");
    if (promptEl) promptEl.value = "Loading notes…";

    var picks = pickMany(slotCount);
    Promise.all(
      Array.prototype.map.call(slots, function (slot, index) {
        return renderNote(slot, picks[index]);
      })
    ).then(function (notes) {
      currentNotes = notes;
      updatePrompt(currentNotes);
      window.requestAnimationFrame(equalizePanelHeights);
    });
  }

  function shuffleSide(index) {
    if (!pool.length) return;

    var exclude = [];
    currentNotes.forEach(function (note, i) {
      if (i !== index && note && note.url) {
        exclude.push(note.url);
      }
    });

    var pick = pickOne(exclude);
    if (!pick) return;

    if (promptEl) promptEl.value = "Loading notes…";

    renderNote(slots[index], pick).then(function (note) {
      currentNotes[index] = note;
      updatePrompt(currentNotes);
      window.requestAnimationFrame(equalizePanelHeights);
    });
  }

  var bindTap = window.jorapBindTouchClick || function (el, fn) {
    el.addEventListener("click", fn);
  };
  var bindTapIf = window.jorapBindTouchClickIf || function (el, fn) {
    if (el) bindTap(el, fn);
  };

  bindTapIf(shuffleAllBtn, shuffleAll);
  bindTapIf(shuffleLeftBtn, function () {
    shuffleSide(0);
  });
  bindTapIf(shuffleCenterBtn, function () {
    shuffleSide(1);
  });
  bindTapIf(shuffleRightBtn, function () {
    shuffleSide(2);
  });
  bindTapIf(copyPromptBtn, function (event) {
    event.preventDefault();
    event.stopPropagation();
    copyPrompt();
  });
  bindTapIf(sendPromptBtn, function (event) {
    event.preventDefault();
    event.stopPropagation();
    sendPromptToAI();
  });

  window.addEventListener(
    "resize",
    function () {
      equalizePanelHeights();
    },
    { passive: true }
  );

  shuffleAll();
})();
