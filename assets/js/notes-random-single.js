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
  var sendPromptBtn = document.querySelector("[data-" + prefix + "-send-prompt]");
  var promptEl = document.querySelector("[data-" + prefix + "-prompt]");
  var emptyPageEl = document.querySelector("[data-" + prefix + "-empty]");
  var slot = root.querySelector("[data-" + prefix + "-slot]");

  var currentNote = null;
  var pool = [];
  var currentUrl = "";
  var aiChatUrl = "https://chatgpt.com/?q=";
  var aiChatOpenedLabel = "Opened";
  var aiChatCopiedLabel = "Copied — paste in chat";

  try {
    var config = JSON.parse(dataEl.textContent);
    if (Array.isArray(config)) {
      pool = config;
    } else {
      pool = config.notes || [];
      if (config.currentUrl) currentUrl = config.currentUrl;
      if (config.aiChatUrl) aiChatUrl = config.aiChatUrl;
      if (config.aiChatOpenedLabel) aiChatOpenedLabel = config.aiChatOpenedLabel;
      if (config.aiChatCopiedLabel) aiChatCopiedLabel = config.aiChatCopiedLabel;
    }
  } catch (e) {
    pool = [];
  }

  var ai = core.createAiHelpers({
    promptEl: promptEl,
    aiChatUrl: aiChatUrl,
    copyPromptBtn: copyPromptBtn,
    sendPromptBtn: sendPromptBtn,
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
    var intro = isBlog
      ? "I'm reading a blog post and a note from my digital garden. Help me find connections between them."
      : "I'm reading a note from my digital garden and another note I'd like to pair with it. Help me find connections between them.";
    var analyze = isBlog
      ? "Analyze how this post and this note connect:"
      : "Analyze how these two notes connect:";

    var lines = [intro, ""];
    var origin = window.location.origin;

    if (page && page.title) {
      lines.push(page.label + ': "' + page.title + '"');
      if (page.url) lines.push("URL: " + origin + page.url);
      if (page.bodyText) lines.push(page.bodyText);
      lines.push("");
    }

    lines.push('Note: "' + note.title + '"');
    if (note.url) lines.push("URL: " + origin + note.url);
    if (note.bodyText) lines.push(note.bodyText);
    lines.push("");
    lines.push.apply(lines, core.connectionPromptTail(analyze));

    return lines.join("\n");
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
      if (promptEl) promptEl.value = buildPrompt(null);
      return;
    }

    if (emptyPageEl) emptyPageEl.classList.add("hidden");
    if (promptEl) promptEl.value = "Loading note…";

    core.renderNoteIntoSlot(slot, pick).then(function (note) {
      currentNote = note;
      syncSelect(note && note.url ? note.url : "");
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
  core.bindTapIf(sendPromptBtn, function (event) {
    event.preventDefault();
    event.stopPropagation();
    ai.sendPromptToAI();
  });

  shuffle();
})();
