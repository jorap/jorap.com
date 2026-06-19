/**
 * Notes single: two random garden notes + AI prompt with the current note.
 */
(function () {
  var root = document.querySelector("[data-notes-single-random-notes]");
  var dataEl = document.querySelector(".notes-single-random-data");
  var shuffleAllBtn = document.querySelector("[data-notes-single-random-shuffle-all]");
  var shuffleLeftBtn = document.querySelector("[data-notes-single-random-shuffle-left]");
  var shuffleRightBtn = document.querySelector("[data-notes-single-random-shuffle-right]");
  var copyPromptBtn = document.querySelector("[data-notes-single-random-copy-prompt]");
  var sendPromptBtn = document.querySelector("[data-notes-single-random-send-prompt]");
  var promptEl = document.querySelector("[data-notes-single-random-prompt]");
  var emptyPageEl = document.querySelector("[data-notes-single-random-empty]");
  if (!root || !dataEl) return;

  var slotCount = 2;
  var slots = root.querySelectorAll("[data-notes-single-random-slot]");
  var currentNotes = [null, null];
  var pool;
  var currentUrl = "";
  var aiChatUrl = "https://chatgpt.com/?q=";
  var aiChatOpenedLabel = "Opened";
  var aiChatCopiedLabel = "Copied — paste in chat";
  var PROMPT_PREFILL_MAX_URL = 1800;

  try {
    var config = JSON.parse(dataEl.textContent);
    pool = config.notes || [];
    if (config.currentUrl) currentUrl = config.currentUrl;
    if (config.aiChatUrl) aiChatUrl = config.aiChatUrl;
    if (config.aiChatOpenedLabel) aiChatOpenedLabel = config.aiChatOpenedLabel;
    if (config.aiChatCopiedLabel) aiChatCopiedLabel = config.aiChatCopiedLabel;
  } catch (e) {
    pool = [];
  }

  function pickOne(excludeUrls) {
    if (!pool.length) return null;

    var exclude = (excludeUrls || []).slice();
    if (currentUrl && exclude.indexOf(currentUrl) === -1) {
      exclude.push(currentUrl);
    }

    var candidates = pool.filter(function (entry) {
      return exclude.indexOf(entry.url) === -1;
    });

    if (!candidates.length) {
      candidates = pool.filter(function (entry) {
        return entry.url !== currentUrl;
      });
    }

    if (!candidates.length) return null;

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
    slot.innerHTML = '<p class="notes-random-two-loading text-ink-muted text-sm">Loading…</p>';
    slot.classList.remove("notes-random-two-panel--empty");
  }

  function setSlotEmpty(slot) {
    slot.innerHTML =
      '<p class="notes-random-two-empty text-ink-muted text-sm">Not enough notes to fill this column.</p>';
    slot.classList.add("notes-random-two-panel--empty");
  }

  function normalizeText(str) {
    return String(str || "")
      .replace(/\s+/g, " ")
      .trim();
  }

  function promptInstructions(noteCount) {
    var lines = ["Please analyze:"];

    if (noteCount >= 2) {
      lines.push("- All three together (current note + Note 1 + Note 2)");
      lines.push("- Current note + Note 1");
      lines.push("- Current note + Note 2");
    } else if (noteCount === 1) {
      lines.push("- Current note + Note 1");
    } else {
      lines.push("- Current note alone — suggest note topics that would pair well with it");
    }

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

  function getCurrentNoteContext() {
    var titleEl = document.querySelector("article .article-title");
    var contentEl = document.querySelector("article .notes-content");
    if (!titleEl) return null;

    var bodyText = "";
    if (contentEl) {
      bodyText = normalizeText(contentEl.textContent);
    }

    return {
      title: titleEl.textContent.trim(),
      url: currentUrl || window.location.pathname,
      bodyText: bodyText,
    };
  }

  function buildPrompt(notes) {
    var currentNote = getCurrentNoteContext();
    var usable = notes.filter(function (note) {
      return note && note.title;
    });

    if (!currentNote && !usable.length) {
      return "Shuffle to load two notes, then paste this prompt into your AI chat.";
    }

    var lines = [
      "I'm exploring connections between a note I'm reading and two other notes from my digital garden. Help me discover new ideas by analyzing how they relate.",
      "",
    ];
    var origin = window.location.origin;

    if (currentNote && currentNote.title) {
      lines.push('Current note: "' + currentNote.title + '"');
      if (currentNote.url) lines.push("URL: " + origin + currentNote.url);
      if (currentNote.bodyText) lines.push(currentNote.bodyText);
      lines.push("");
    }

    usable.forEach(function (note, index) {
      lines.push("Note " + (index + 1) + ': "' + note.title + '"');
      if (note.url) lines.push("URL: " + origin + note.url);
      if (note.bodyText) lines.push(note.bodyText);
      lines.push("");
    });

    lines.push(promptInstructions(usable.length));

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

  var skipArticleSelector =
    ".notes-graph-panel, .notes-toolbar, .article-title, .toc-wrapper, .notes-outgoing, .notes-see-also, .notes-backlinks";

  function cloneArticleBody(article) {
    var body = document.createElement("div");
    body.className = "notes-random-two-body";
    var children = article.children;

    for (var i = 0; i < children.length; i += 1) {
      var child = children[i];
      if (child.matches(skipArticleSelector)) continue;
      body.appendChild(child.cloneNode(true));
    }

    return body;
  }

  function equalizePanelHeights() {
    var panels = root.querySelectorAll(".notes-random-two-panel");
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
        panel.className = "notes-random-two-panel border-divider rounded border p-5";

        var heading = document.createElement("h3");
        heading.className = "h5 mb-3";
        var link = document.createElement("a");
        link.className = "text-accent no-underline hover:underline";
        link.href = pick.url;
        link.textContent = titleEl.textContent.trim();
        heading.appendChild(link);
        panel.appendChild(heading);
        panel.appendChild(cloneArticleBody(article));

        slot.innerHTML = "";
        slot.appendChild(panel);
        slot.classList.remove("notes-random-two-panel--empty");

        return {
          title: titleEl.textContent.trim(),
          url: pick.url,
          bodyText: normalizeText(contentEl.textContent),
        };
      })
      .catch(function () {
        slot.innerHTML =
          '<article class="notes-random-two-panel border-divider rounded border p-5">' +
          '<h3 class="h5 mb-3"><a class="text-accent no-underline hover:underline" href="' +
          escapeHtml(pick.url) +
          '">' +
          escapeHtml(pick.title) +
          "</a></h3>" +
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
      currentNotes = [null, null];
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

  if (shuffleAllBtn) {
    shuffleAllBtn.addEventListener("click", shuffleAll);
  }

  if (shuffleLeftBtn) {
    shuffleLeftBtn.addEventListener("click", function () {
      shuffleSide(0);
    });
  }

  if (shuffleRightBtn) {
    shuffleRightBtn.addEventListener("click", function () {
      shuffleSide(1);
    });
  }

  if (copyPromptBtn) {
    copyPromptBtn.addEventListener("click", function (event) {
      event.preventDefault();
      event.stopPropagation();
      copyPrompt();
    });
  }

  if (sendPromptBtn) {
    sendPromptBtn.addEventListener("click", function (event) {
      event.preventDefault();
      event.stopPropagation();
      sendPromptToAI();
    });
  }

  window.addEventListener(
    "resize",
    function () {
      equalizePanelHeights();
    },
    { passive: true }
  );

  shuffleAll();
})();
