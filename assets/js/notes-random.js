/**
 * Shared helpers for random note / duo UIs.
 */
(function () {
  var SKIP_ARTICLE =
    ".notes-graph-panel, .notes-toolbar, .notes-article-header, .article-title, .notes-copy-md, .toc-wrapper, .notes-outgoing, .notes-see-also, .notes-backlinks, .notes-note-flashcards";
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

  function connectionPromptIntro() {
    return "I'm exploring connections between two ideas in my notes garden (PKM, faith, ethics, systems). Note text is assembled from frontmatter: description, key_concept, examples, relationships.";
  }

  function formatPromptNote(index, note, origin) {
    var lines = ["Note " + index + ":"];
    if (!note || !note.title) return lines;
    lines.push('"' + note.title + '"');
    if (note.url) lines.push("URL: " + origin + note.url);
    if (note.bodyText) lines.push(note.bodyText);
    return lines;
  }

  function connectionPromptTail() {
    return [
      "---",
      "",
      "## TASK",
      "",
      "Analyze how these notes relate. Generate outputs that are:",
      "- Concrete and actionable (what to do next time the situation shows up)",
      "- Atomic (one claim per note title or relationship row)",
      "- Multi-scale (immediate move → short experiment → longer habit)",
      "",
      "Topics span PKM, gospel, ethics, and systems — not workflow-only.",
      "Avoid abstract theory unless tied to a move I'd make this week.",
      "",
      "Voice: plain words, first person where natural, specific scenes. No AI filler (\"crucial\", \"delve\", \"leverage\", \"Furthermore\"). Read like JoRap typed it mid-life.",
      "",
      "---",
      "",
      "## OUTPUT FORMAT",
      "",
      "### 1. Core Relationship",
      "1–2 sentences explaining the deepest connection between the notes.",
      "",
      "---",
      "",
      "### 2. 3 Unexpected Links (Insight → Mechanism → Action)",
      "Each must include:",
      "- Insight (what is connected)",
      "- Mechanism (why/how it connects)",
      "- Action (what I can do immediately)",
      "",
      "---",
      "",
      "### 3. 3 Sibling Atomic Note Stubs",
      "Notes missing from the garden that would strengthen this connection. Each:",
      "- title (3–7 words, reusable [[wikilink]] target)",
      "- one-line claim (description-ready)",
      "- suggested relationships rows (type + [[wikilink]] + reason) tying it to notes above",
      "",
      "---",
      "",
      "### 4. 3 Relationship Rows to Add",
      "YAML-ready rows I could paste into frontmatter on an existing note:",
      "- type: extends | contradicts | implements | alternative",
      "- wikilink: \"[[Note Title]]\"",
      "- reason: one short clause",
      "",
      "---",
      "",
      "### 5. 3 Quick Wins (2–15 minutes)",
      "- Action",
      "- Why it matters",
      "- Immediate effect",
      "",
      "---",
      "",
      "### 6. 3 Experiments (Validation Layer)",
      "Each includes:",
      "- Name",
      "- Steps (simple, executable)",
      "- Time required (5–15 min / daily / weekly)",
      "- Expected outcome",
      "- Success indicator",
      "",
      "---",
      "",
      "### 7. 3 Quotable One-Liners",
      "Self-contained truths I'd say aloud — paradox, tension, or practical shift. No hashtags, no thread setup.",
      "",
      "---",
      "",
      "## RULES",
      "",
      "- Prefer usefulness over creativity",
      "- If uncertain, default to a simpler action or experiment",
      "- Every insight must connect to at least one action or relationship row",
      "- New note stubs use frontmatter shape (empty body) — not body ## sections",
      "- Do not [[wikilink]] utility/meta pages (Graph, Issues, Flashcards, Review) — use URLs",
      "- Keep outputs minimal but high-signal",
    ];
  }

  function createAiHelpers(opts) {
    var promptEl = opts.promptEl;
    var copyPromptBtn = opts.copyPromptBtn;
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

    function sendPromptToChat(chatUrl, sendBtn, prefill) {
      if (!promptEl || !promptIsReady()) return;

      var prompt = promptEl.value;

      function openChat(url) {
        window.open(url, "_blank", "noopener,noreferrer");
      }

      if (prefill && chatUrl.indexOf("?q=") !== -1) {
        var prefillUrl = chatUrl + encodeURIComponent(prompt);
        if (prefillUrl.length <= PROMPT_PREFILL_MAX_URL) {
          openChat(prefillUrl);
          flashButton(sendBtn, openedLabel);
          return;
        }
      }

      if (!navigator.clipboard) {
        openChat(aiChatFallbackUrl(chatUrl));
        return;
      }

      navigator.clipboard.writeText(prompt).then(function () {
        openChat(aiChatFallbackUrl(chatUrl));
        flashButton(sendBtn, copiedLabel);
      });
    }

    return {
      flashButton: flashButton,
      promptIsReady: promptIsReady,
      copyPrompt: copyPrompt,
      sendPromptToChat: sendPromptToChat,
    };
  }

  function wireSendPromptButtons(prefix, ai) {
    var btns = document.querySelectorAll("[data-" + prefix + "-send-prompt]");
    Array.prototype.forEach.call(btns, function (btn) {
      bindTapIf(btn, function (event) {
        event.preventDefault();
        event.stopPropagation();
        var chatUrl = btn.getAttribute("data-ai-chat-url") || "https://chatgpt.com/?q=";
        var prefill = btn.getAttribute("data-ai-prefill") === "true";
        ai.sendPromptToChat(chatUrl, btn, prefill);
      });
    });
  }

  function bindTapIf(el, fn) {
    var bind = window.jorapBindTouchClickIf;
    if (bind) {
      bind(el, fn);
      return;
    }
    if (el) el.addEventListener("click", fn);
  }

  function buildAdjacency(edges) {
    var adj = Object.create(null);
    (edges || []).forEach(function (edge) {
      var s = edge.source;
      var t = edge.target;
      if (!adj[s]) adj[s] = [];
      if (!adj[t]) adj[t] = [];
      adj[s].push(t);
      adj[t].push(s);
    });
    return adj;
  }

  function shortestPath(adj, start, end) {
    if (!start || !end || start === end) return [start];
    if (!adj[start] || !adj[end]) return null;

    var queue = [start];
    var prev = Object.create(null);
    prev[start] = null;

    while (queue.length) {
      var node = queue.shift();
      if (node === end) break;
      (adj[node] || []).forEach(function (next) {
        if (prev[next] !== undefined) return;
        prev[next] = node;
        queue.push(next);
      });
    }

    if (prev[end] === undefined) return null;

    var path = [];
    var cur = end;
    while (cur) {
      path.unshift(cur);
      cur = prev[cur];
    }
    return path;
  }

  function pathHopLabel(path) {
    if (!path || path.length < 2) return "";
    var hops = path.length - 1;
    return hops + " hop" + (hops === 1 ? "" : "s");
  }

  function renderPathChain(chainEl, path, titleByUrl) {
    if (!chainEl) return;
    var horizontal = chainEl.classList.contains("notes-path-chain--row");
    var items = (path || []).map(function (url) {
      var title = (titleByUrl && titleByUrl[url]) || url;
      return (
        '<a class="text-accent no-underline hover:underline" href="' +
        escapeHtml(url) +
        '">' +
        escapeHtml(title) +
        "</a>"
      );
    });

    if (horizontal) {
      chainEl.innerHTML = items.join(
        '<span class="text-ink-muted px-1" aria-hidden="true">→</span>'
      );
      return;
    }

    chainEl.innerHTML = items
      .map(function (link) {
        return "<li>" + link + "</li>";
      })
      .join("");
  }

  function renderPathBetween(opts) {
    opts = opts || {};
    var resultEl = opts.resultEl;
    var chainEl = opts.chainEl;
    var emptyEl = opts.emptyEl;
    var start = opts.start;
    var end = opts.end;
    var sameNoteMsg = opts.sameNoteMsg || "Pick two different notes.";
    var noPathMsg = opts.noPathMsg || "No path found through wikilinks.";

    if (!resultEl) return null;

    if (!start || !end) {
      resultEl.classList.add("hidden");
      if (emptyEl) emptyEl.classList.add("hidden");
      return null;
    }

    if (start === end) {
      resultEl.classList.add("hidden");
      if (emptyEl) {
        emptyEl.classList.remove("hidden");
        emptyEl.textContent = sameNoteMsg;
      }
      return [start];
    }

    var path = shortestPath(opts.adj, start, end);
    if (!path || path.length < 2) {
      resultEl.classList.add("hidden");
      if (emptyEl) {
        emptyEl.classList.remove("hidden");
        emptyEl.textContent = noPathMsg;
      }
      return null;
    }

    if (emptyEl) emptyEl.classList.add("hidden");
    resultEl.classList.remove("hidden");
    renderPathChain(chainEl, path, opts.titleByUrl);
    return path;
  }

  function pathPromptLine(path, titleByUrl) {
    if (!path || path.length < 2) return "";
    return (
      "A shortest wikilink path between these notes (others may exist):\n" +
      path
        .map(function (url) {
          return titleByUrl[url] || url;
        })
        .join(" → ")
    );
  }

  window.jorapNotesRandomCore = {
    buildAdjacency: buildAdjacency,
    cloneArticleBody: cloneArticleBody,
    connectionPromptIntro: connectionPromptIntro,
    connectionPromptTail: connectionPromptTail,
    formatPromptNote: formatPromptNote,
    createAiHelpers: createAiHelpers,
    wireSendPromptButtons: wireSendPromptButtons,
    bindTapIf: bindTapIf,
    normalizeText: normalizeText,
    pathHopLabel: pathHopLabel,
    pathPromptLine: pathPromptLine,
    pickOne: pickOne,
    renderNoteIntoSlot: renderNoteIntoSlot,
    renderPathBetween: renderPathBetween,
    renderPathChain: renderPathChain,
    setSlotEmpty: setSlotEmpty,
    setSlotLoading: setSlotLoading,
    shortestPath: shortestPath,
  };
})();

/**
 * Shared note picker: wire <select> elements to random note / duo slots.
 */
(function () {
  function findInPool(pool, url) {
    if (!url) return null;
    for (var i = 0; i < pool.length; i += 1) {
      if (pool[i].url === url) return pool[i];
    }
    return null;
  }

  window.jorapNotesRandomSelect = {
    findInPool: findInPool,

    setValue: function (select, url) {
      if (!select) return;
      select.value = url || "";
    },

    wire: function (select, pool, callbacks) {
      if (!select) return;

      select.addEventListener("change", function () {
        var url = select.value;
        if (!url) {
          select.value = callbacks.getCurrentUrl ? callbacks.getCurrentUrl() || "" : "";
          return;
        }

        var blocked = callbacks.getBlockedUrls ? callbacks.getBlockedUrls() : [];
        if (blocked.indexOf(url) !== -1) {
          select.value = callbacks.getCurrentUrl ? callbacks.getCurrentUrl() || "" : "";
          return;
        }

        var pick = findInPool(pool, url);
        if (pick && callbacks.onPick) {
          callbacks.onPick(pick);
        }
      });
    },
  };
})();

/**
 * Notes home: featured block shows three random garden notes per visit.
 */
(function () {
  var core = window.jorapNotesRandomCore;
  if (!core) return;

  var root = document.querySelector("[data-notes-featured-random]");
  var dataEl = document.querySelector(".notes-featured-random-data");
  var slot = document.querySelector("[data-notes-featured-random-slot]");
  if (!root || !dataEl || !slot) return;

  var PICK_COUNT = 3;

  var pool = [];
  try {
    pool = JSON.parse(dataEl.textContent);
  } catch (e) {
    pool = [];
  }

  function escapeHtml(str) {
    return String(str)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;");
  }

  function pickMany(count) {
    var picks = [];
    var exclude = [];
    var n = Math.min(count, pool.length);

    for (var i = 0; i < n; i += 1) {
      var pick = core.pickOne(pool, exclude);
      if (!pick) break;
      picks.push(pick);
      exclude.push(pick.url);
    }

    return picks;
  }

  function cardHtml(pick) {
    var desc = pick.description
      ? '<p class="notes-card__body text-ink-muted relative z-[1] mb-0 flex-1 text-sm leading-snug pointer-events-none">' +
        escapeHtml(pick.description) +
        "</p>"
      : '<div class="notes-card__spacer relative z-[1] flex-1 pointer-events-none" aria-hidden="true"></div>';

    return (
      '<article class="notes-card notes-card--interactive border-divider relative flex h-full w-full flex-col overflow-hidden rounded-xl border bg-elevated p-5 shadow-sm transition-[box-shadow,border-color] duration-200 ease-out motion-reduce:transition-none">' +
      '<a class="notes-card__overlay" href="' +
      escapeHtml(pick.url) +
      '" data-wikilink-preview="' +
      escapeHtml(pick.url) +
      '" aria-label="' +
      escapeHtml(pick.title) +
      '"></a>' +
      '<h3 class="h6 notes-card__title relative z-[1] mb-2 font-medium pointer-events-none">' +
      escapeHtml(pick.title) +
      "</h3>" +
      desc +
      "</article>"
    );
  }

  function render() {
    if (!pool.length) {
      slot.innerHTML =
        '<p class="notes-featured-random-empty text-ink-muted col-span-full text-sm">No notes in the garden yet.</p>';
      return;
    }

    slot.innerHTML = pickMany(PICK_COUNT)
      .map(cardHtml)
      .join("");
  }

  render();
})();

/**
 * Blog post or note page: one random garden note + connection AI prompt.
 */
(function () {
  var core = window.jorapNotesRandomCore;
  if (!core) return;

  var isBlog = !!document.querySelector("[data-blog-random-notes]");
  var prefix = isBlog ? "blog-random" : "notes-single-random";
  var root = document.querySelector("[data-" + prefix + "-notes]");
  var dataEl = document.querySelector("." + prefix + "-notes-data") || document.querySelector(".notes-single-random-data");
  if (!root || !dataEl) return;

  var shuffleBtn = document.querySelector("[data-" + prefix + "-shuffle]");
  var selectEl = document.querySelector("[data-" + prefix + "-select]");
  var copyPromptBtn = document.querySelector("[data-" + prefix + "-copy-prompt]");
  var promptEl = document.querySelector("[data-" + prefix + "-prompt]");
  var emptyPageEl = document.querySelector("[data-" + prefix + "-empty]");
  var slot = root.querySelector("[data-" + prefix + "-slot]");
  var pathResultEl = document.querySelector("[data-notes-single-random-path]");
  var pathChainEl = document.querySelector("[data-notes-single-random-path-chain]");
  var pathEmptyEl = document.querySelector("[data-notes-single-random-path-empty]");

  var currentNote = null;
  var currentPath = null;
  var pool = [];
  var currentUrl = "";
  var currentTitle = "";
  var adj = Object.create(null);
  var titleByUrl = Object.create(null);
  var aiChatOpenedLabel = "Opened";
  var aiChatCopiedLabel = "Copied — paste in chat";

  try {
    var config = JSON.parse(dataEl.textContent);
    if (Array.isArray(config)) {
      pool = config;
    } else {
      pool = config.notes || [];
      if (config.currentUrl) currentUrl = config.currentUrl;
      if (config.currentTitle) currentTitle = config.currentTitle;
      if (config.aiChatOpenedLabel) aiChatOpenedLabel = config.aiChatOpenedLabel;
      if (config.aiChatCopiedLabel) aiChatCopiedLabel = config.aiChatCopiedLabel;
      if (!isBlog && config.graphEdges) adj = core.buildAdjacency(config.graphEdges);
    }
  } catch (e) {
    pool = [];
  }

  pool.forEach(function (item) {
    titleByUrl[item.url] = item.title;
  });
  if (!isBlog && currentUrl && currentTitle) {
    titleByUrl[currentUrl] = currentTitle;
  }

  var ai = core.createAiHelpers({
    promptEl: promptEl,
    copyPromptBtn: copyPromptBtn,
    openedLabel: aiChatOpenedLabel,
    copiedLabel: aiChatCopiedLabel,
  });

  function getPageContext() {
    var titleEl = document.querySelector("article .article-title");
    if (!titleEl) return null;

    var bodyText = "";
    if (isBlog) {
      var contentEl = document.querySelector("article .content");
      if (contentEl) {
        var clone = contentEl.cloneNode(true);
        clone.querySelectorAll(".tags_section, .share_section").forEach(function (node) {
          node.remove();
        });
        bodyText = core.normalizeText(clone.textContent);
      }
      return {
        title: titleEl.textContent.trim(),
        url: window.location.pathname,
        bodyText: bodyText,
        label: "Blog post",
      };
    }

    var notesContent = document.querySelector("article .notes-content");
    if (notesContent) bodyText = core.normalizeText(notesContent.textContent);

    return {
      title: titleEl.textContent.trim(),
      url: currentUrl || window.location.pathname,
      bodyText: bodyText,
      label: "Current note",
    };
  }

  function buildPrompt(note) {
    if (!note || !note.title) {
      return "Shuffle to load a note, then paste this prompt into your AI chat.";
    }

    var page = getPageContext();
    var origin = window.location.origin;
    var lines = [core.connectionPromptIntro(), ""];

    if (page && page.title) {
      lines.push.apply(lines, core.formatPromptNote(1, page, origin));
      lines.push("");
    }

    lines.push.apply(lines, core.formatPromptNote(2, note, origin));
    lines.push("");

    if (!isBlog && currentPath && currentPath.length > 1) {
      lines.push(core.pathPromptLine(currentPath, titleByUrl));
      lines.push("");
    }

    lines.push.apply(lines, core.connectionPromptTail());

    return lines.join("\n");
  }

  function updatePath() {
    if (isBlog) return;
    currentPath = core.renderPathBetween({
      resultEl: pathResultEl,
      chainEl: pathChainEl,
      emptyEl: pathEmptyEl,
      adj: adj,
      titleByUrl: titleByUrl,
      start: currentUrl,
      end: currentNote && currentNote.url,
    });
  }

  function syncSelect(url) {
    if (window.jorapNotesRandomSelect) {
      window.jorapNotesRandomSelect.setValue(selectEl, url);
    }
  }

  function loadNote(pick) {
    if (!pool.length) {
      if (emptyPageEl) emptyPageEl.classList.remove("hidden");
      core.setSlotEmpty(
        slot,
        isBlog ? "No notes in the garden yet." : "No other notes in the garden yet."
      );
      currentNote = null;
      syncSelect("");
      updatePath();
      if (promptEl) promptEl.value = buildPrompt(null);
      return;
    }

    if (emptyPageEl) emptyPageEl.classList.add("hidden");
    if (promptEl) promptEl.value = "Loading note…";

    core.renderNoteIntoSlot(slot, pick).then(function (note) {
      currentNote = note;
      syncSelect(note && note.url ? note.url : "");
      updatePath();
      if (promptEl) promptEl.value = buildPrompt(currentNote);
    });
  }

  function shuffle() {
    loadNote(pool.length ? core.pickOne(pool) : null);
  }

  core.bindTapIf(shuffleBtn, shuffle);
  if (window.jorapNotesRandomSelect && selectEl) {
    window.jorapNotesRandomSelect.wire(selectEl, pool, {
      getCurrentUrl: function () {
        return currentNote && currentNote.url ? currentNote.url : "";
      },
      getBlockedUrls: function () {
        return currentUrl ? [currentUrl] : [];
      },
      onPick: function (pick) {
        loadNote(pick);
      },
    });
  }
  core.bindTapIf(copyPromptBtn, function (event) {
    event.preventDefault();
    event.stopPropagation();
    ai.copyPrompt();
  });
  core.wireSendPromptButtons(prefix, ai);

  shuffle();
})();

/**
 * Random Duo page: two garden notes side by side + AI prompt.
 */
(function () {
  var core = window.jorapNotesRandomCore;
  if (!core) return;

  var root = document.querySelector("[data-notes-random-duo]");
  var dataEl = document.querySelector(".notes-random-duo-data");
  var graphEl = document.querySelector(".notes-random-duo-graph-data");
  var shuffleBtn = document.querySelector("[data-random-duo-shuffle]");
  var shuffleLeftBtn = document.querySelector("[data-random-duo-shuffle-left]");
  var shuffleRightBtn = document.querySelector("[data-random-duo-shuffle-right]");
  var selectEls = document.querySelectorAll("[data-random-duo-select]");
  var copyPromptBtn = document.querySelector("[data-random-duo-copy-prompt]");
  var promptEl = document.querySelector("[data-random-duo-prompt]");
  var emptyPageEl = document.querySelector(".notes-random-empty-page");
  var pathResultEl = document.querySelector("[data-random-duo-path]");
  var pathChainEl = document.querySelector("[data-random-duo-path-chain]");
  if (!root || !dataEl) return;

  var slots = root.querySelectorAll("[data-random-duo-slot]");
  var currentNotes = [null, null];
  var currentPath = null;
  var pool = [];
  var adj = Object.create(null);
  var titleByUrl = Object.create(null);
  try {
    pool = JSON.parse(dataEl.textContent);
  } catch (e) {
    pool = [];
  }

  pool.forEach(function (item) {
    titleByUrl[item.url] = item.title;
  });

  if (graphEl) {
    try {
      adj = core.buildAdjacency(JSON.parse(graphEl.textContent) || []);
    } catch (e) {
      adj = Object.create(null);
    }
  }

  var ai = core.createAiHelpers({
    promptEl: promptEl,
    copyPromptBtn: copyPromptBtn,
    openedLabel: "Opened",
    copiedLabel: "Copied — paste in chat",
  });

  function pickTwo() {
    if (!pool.length) return [];
    if (pool.length === 1) return [pool[0], null];
    var first = core.pickOne(pool, []);
    var second = core.pickOne(pool, first ? [first.url] : []);
    return [first, second];
  }

  function buildPrompt(notes) {
    var usable = notes.filter(function (note) {
      return note && note.title;
    });

    if (!usable.length) {
      return "Shuffle to load two notes, then paste this prompt into your AI chat.";
    }

    var origin = window.location.origin;
    var lines = [core.connectionPromptIntro(), ""];

    usable.forEach(function (note, index) {
      lines.push.apply(lines, core.formatPromptNote(index + 1, note, origin));
      lines.push("");
    });

    if (currentPath && currentPath.length > 1) {
      lines.push(core.pathPromptLine(currentPath, titleByUrl));
      lines.push("");
    }

    lines.push.apply(lines, core.connectionPromptTail());

    return lines.join("\n");
  }

  function updatePath() {
    var left = currentNotes[0];
    var right = currentNotes[1];
    currentPath = core.renderPathBetween({
      resultEl: pathResultEl,
      chainEl: pathChainEl,
      adj: adj,
      titleByUrl: titleByUrl,
      start: left && left.url,
      end: right && right.url,
    });
  }

  function refreshPrompt() {
    if (promptEl) promptEl.value = buildPrompt(currentNotes);
  }

  function equalizePanelHeights() {
    var panels = root.querySelectorAll(".notes-random-panel");
    if (panels.length < 2) return;

    panels.forEach(function (panel) {
      panel.style.minHeight = "";
    });

    // Side-by-side only (md+); stacked columns should use natural height.
    if (!window.matchMedia("(min-width: 768px)").matches) return;

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

  function syncSelect(index, url) {
    if (!window.jorapNotesRandomSelect || !selectEls[index]) return;
    window.jorapNotesRandomSelect.setValue(selectEls[index], url);
  }

  function syncAllSelects() {
    currentNotes.forEach(function (note, index) {
      syncSelect(index, note && note.url ? note.url : "");
    });
  }

  function loadSlot(index, pick) {
    if (promptEl) promptEl.value = "Loading notes…";

    return core
      .renderNoteIntoSlot(slots[index], pick, {
        headingTag: "h2",
        bodyMode: "content",
        emptyMessage: "Not enough notes to fill this column.",
      })
      .then(function (note) {
        currentNotes[index] = note;
        syncSelect(index, note && note.url ? note.url : "");
        updatePath();
        refreshPrompt();
        window.requestAnimationFrame(equalizePanelHeights);
        return note;
      });
  }

  function shuffleBoth() {
    if (!pool.length) {
      if (emptyPageEl) emptyPageEl.classList.remove("hidden");
      slots.forEach(function (slot) {
        core.setSlotEmpty(slot, "Not enough notes to fill this column.");
      });
      currentNotes = [null, null];
      syncAllSelects();
      updatePath();
      refreshPrompt();
      return;
    }

    if (emptyPageEl) emptyPageEl.classList.add("hidden");
    if (promptEl) promptEl.value = "Loading notes…";

    var picks = pickTwo();
    Promise.all(
      Array.prototype.map.call(slots, function (slot, index) {
        return core.renderNoteIntoSlot(slot, picks[index], {
          headingTag: "h2",
          bodyMode: "content",
          emptyMessage: "Not enough notes to fill this column.",
        });
      })
    ).then(function (notes) {
      currentNotes = notes;
      syncAllSelects();
      updatePath();
      refreshPrompt();
      window.requestAnimationFrame(equalizePanelHeights);
    });
  }

  function shuffleSide(index) {
    if (!pool.length) return;

    var otherIndex = index === 0 ? 1 : 0;
    var exclude = [];
    var otherNote = currentNotes[otherIndex];
    if (otherNote && otherNote.url) exclude.push(otherNote.url);

    var pick = core.pickOne(pool, exclude);
    if (!pick) return;

    loadSlot(index, pick);
  }

  function wireSelects() {
    if (!window.jorapNotesRandomSelect) return;

    Array.prototype.forEach.call(selectEls, function (selectEl) {
      var index = parseInt(selectEl.getAttribute("data-random-duo-select"), 10);
      if (isNaN(index)) return;

      window.jorapNotesRandomSelect.wire(selectEl, pool, {
        getCurrentUrl: function () {
          var note = currentNotes[index];
          return note && note.url ? note.url : "";
        },
        getBlockedUrls: function () {
          var blocked = [];
          currentNotes.forEach(function (note, i) {
            if (i !== index && note && note.url) blocked.push(note.url);
          });
          return blocked;
        },
        onPick: function (pick) {
          loadSlot(index, pick);
        },
      });
    });
  }

  core.bindTapIf(shuffleBtn, shuffleBoth);
  core.bindTapIf(shuffleLeftBtn, function () {
    shuffleSide(0);
  });
  core.bindTapIf(shuffleRightBtn, function () {
    shuffleSide(1);
  });
  core.bindTapIf(copyPromptBtn, function (event) {
    event.preventDefault();
    event.stopPropagation();
    ai.copyPrompt();
  });
  core.wireSendPromptButtons("random-duo", ai);

  window.addEventListener("resize", equalizePanelHeights, { passive: true });

  wireSelects();
  shuffleBoth();
})();
