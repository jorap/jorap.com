/**
 * Create Note page: topic → atomic-note AI prompt (principles + actionable output).
 */
(function () {
  var core = window.jorapNotesRandomCore;
  if (!core) return;

  var topicEl = document.querySelector("[data-note-creator-topic]");
  var hintEl = document.querySelector("[data-note-creator-hint]");
  var dataEl = document.querySelector(".notes-creator-garden-data");
  var promptEl = document.querySelector("[data-note-creator-prompt]");
  var copyPromptBtn = document.querySelector("[data-note-creator-copy-prompt]");
  if (!topicEl || !promptEl) return;

  var garden = [];
  try {
    garden = JSON.parse(dataEl ? dataEl.textContent : "[]");
  } catch (e) {
    garden = [];
  }

  var PLACEHOLDER = "Enter a topic above to generate the prompt.";
  var debounceTimer = null;
  var defaultHint = hintEl ? hintEl.textContent : "";

  function topicReady() {
    return String(topicEl.value || "").replace(/\s+/g, " ").trim().length > 0;
  }

  function topicWords(topic) {
    return String(topic || "")
      .toLowerCase()
      .split(/[^a-z0-9]+/)
      .filter(function (word) {
        return word.length > 2;
      });
  }

  function noteSearchText(note) {
    return (note.title + " " + (note.tags || []).join(" ")).toLowerCase();
  }

  function relevantGardenNotes(topic, limit) {
    var words = topicWords(topic);
    if (!words.length) return garden.slice(0, limit || 24);

    var scored = garden
      .map(function (note) {
        var hay = noteSearchText(note);
        var score = 0;
        words.forEach(function (word) {
          if (hay.indexOf(word) !== -1) score += 1;
        });
        return { note: note, score: score };
      })
      .filter(function (row) {
        return row.score > 0;
      })
      .sort(function (a, b) {
        return b.score - a.score || a.note.title.localeCompare(b.note.title);
      });

    if (!scored.length) return garden.slice(0, limit || 24);
    return scored.slice(0, limit || 24).map(function (row) {
      return row.note;
    });
  }

  function formatGardenSection(notes) {
    if (!notes.length) return "(No published garden notes yet.)";
    return notes
      .map(function (note) {
        var tags = (note.tags || []).slice(0, 4).join(", ");
        return tags ? "- [[" + note.title + "]] (" + tags + ")" : "- [[" + note.title + "]]";
      })
      .join("\n");
  }

  function buildPrompt(topic) {
    var trimmed = String(topic || "").replace(/\s+/g, " ").trim();
    if (!trimmed) return PLACEHOLDER;

    var today = new Date().toISOString().replace(/\.\d{3}Z$/, "Z");
    var related = relevantGardenNotes(trimmed, 30);

    return [
      "CONTEXT:",
      "I'm building a notes garden (Hugo, content/english/notes/). Each file is one atomic note: one claim I'd say out loud. Too many \"and\"s means split into separate notes with [[wikilinks]].",
      "",
      "Allowed body sections only:",
      "- Opening line (one-breath definition — no \"Term =\" prefix)",
      "- ## Key Concept (one sentence, then next paragraph for stakes, distinctions, wikilinks; not a second definition)",
      "- ## Examples (up to five plain bullets — best scenes first, no genre labels)",
      "- ## Note Relationships (markdown table; must include at least one extends row and one contradicts row)",
      "- ## See also (optional)",
      "",
      "No other ## headings. Principles and actionable solutions belong in Key Concept and Examples — not in extra sections.",
      "",
      "Voice: plain words, first person where natural, specific scenes, no AI filler (\"crucial\", \"delve\", \"leverage\", \"Furthermore\"). Read like JoRap typed it mid-life, not a textbook.",
      "",
      "TOPIC: " + trimmed,
      "",
      "EXISTING GARDEN NOTES (prefer these [[wikilink]] targets when they fit):",
      formatGardenSection(related),
      "",
      "ROLE:",
      "You are a PKM editor and principle researcher. Find the clearest improvement principles on the topic, then distill each into one atomic note with a concrete next move.",
      "",
      "ACTION:",
      "",
      "1) RESEARCH THE TOPIC",
      "   - List 3–7 principles that would actually improve how someone handles this topic day to day.",
      "   - For each principle, name: the core claim (one sentence), why it helps, and one actionable move someone could do in the next 24 hours.",
      "   - Drop vague or duplicate principles. Keep only claims I'd cite in conversation.",
      "",
      "2) ATOMIZE",
      "   - If more than one principle survives, output ONE note now (the strongest, most actionable claim) and list the others as suggested sibling notes to create separately.",
      "   - Do not pack multiple principles into one file.",
      "",
      "3) CHECK THE GARDEN",
      "   - Before writing wikilinks, note which existing notes this claim extends, contradicts, implements, or alternatives to.",
      "   - Use [[Note Title]] only (no pipe aliases). Link real concepts from the garden list when they fit.",
      "",
      "4) WRITE THE ATOMIC NOTE",
      "   Opening line:",
      "   - One-breath definition (what it is — quotable, no wikilink dump; don't prefix with \"Title =\").",
      "",
      "   ## Key Concept:",
      "   - First paragraph: one sentence — the angle, not a second definition.",
      "   - Next paragraph: stakes, distinctions from neighbors, [[wikilinks]] to the graph.",
      "   - If you need a second claim, that's another note.",
      "",
      "   ## Examples — up to five plain bullets (no genre labels), each showing principle → immediate move:",
      "   - Mid-action scenes: thumb on send, jeepney, clinic, group chat, bedtime, inbox",
      "   - First person where natural; one concrete move per bullet",
      "   - Rank strongest first; skip template-y setting swaps",
      "",
      "   ## Note Relationships — table:",
      "   | Relationship | Wikilink | Reason |",
      "   | extends | [[...]] | ... |",
      "   | contradicts | [[...]] | when the opposite frame fits better |",
      "   (Add implements / alternative rows when they fit.)",
      "",
      "   ## See also — optional, 2–4 related notes with short tag hints",
      "",
      "5) FRONTMATTER",
      "   Output valid Hugo YAML:",
      "   ---",
      "   title: \"Human Title\"",
      "   meta_title: \"Human Title - Short Subtitle\"",
      "   description: \"One sentence: the single claim this note makes.\"",
      "   date: " + today,
      "   image: \"/images/note.jpg\"",
      "   categories: [\"Ideas\", \"Tips\"]",
      "   author: \"JoRap\"",
      "   tags: [...]",
      "   slug: \"kebab-case-slug\"",
      "   featured: false",
      "   draft: false",
      "   aliases: []",
      "   ---",
      "",
      "6) QUALITY GATE (run before finishing)",
      "   - Atomic test: Can I say the whole note in one breath without \"and\" joining two ideas?",
      "   - Action test: Does every Example show a move, not just a definition?",
      "   - Lint test: Only allowed ## sections? extends + contradicts in the table?",
      "   - Voice test: Would JoRap say this aloud? Any word I'd pause to define?",
      "   - Link test: Every [[wikilink]] points to a plausible existing or proposed note title?",
      "",
      "FORMAT:",
      "1. Brief research summary (principles found, which one you're writing, siblings to create next)",
      "2. Full markdown file ready to save as content/english/notes/{slug}.md",
      "3. Bulleted list of suggested sibling atomic notes (title + one-line claim each)",
      "",
      "TARGET AUDIENCE:",
      "Practical, personal notes garden. Readers should finish knowing what the principle is and what to do next time the situation shows up.",
    ].join("\n");
  }

  function refreshPrompt() {
    var topic = topicEl.value;
    promptEl.value = buildPrompt(topic);
    if (hintEl) {
      var trimmed = String(topic || "").replace(/\s+/g, " ").trim();
      hintEl.textContent = trimmed
        ? relevantGardenNotes(trimmed, 30).length +
          " garden notes matched for wikilink hints. Copy the prompt or open it in your AI chat."
        : defaultHint;
    }
  }

  var ai = core.createAiHelpers({
    promptEl: promptEl,
    copyPromptBtn: copyPromptBtn,
    openedLabel: "Opened",
    copiedLabel: "Copied — paste in chat",
  });

  core.bindTapIf(copyPromptBtn, function (event) {
    event.preventDefault();
    if (!topicReady()) return;
    ai.copyPrompt();
  });

  var sendBtns = document.querySelectorAll("[data-note-creator-send-prompt]");
  Array.prototype.forEach.call(sendBtns, function (btn) {
    core.bindTapIf(btn, function (event) {
      event.preventDefault();
      event.stopPropagation();
      if (!topicReady()) return;
      var chatUrl = btn.getAttribute("data-ai-chat-url") || "https://chatgpt.com/?q=";
      var prefill = btn.getAttribute("data-ai-prefill") === "true";
      ai.sendPromptToChat(chatUrl, btn, prefill);
    });
  });

  topicEl.addEventListener("input", function () {
    window.clearTimeout(debounceTimer);
    debounceTimer = window.setTimeout(refreshPrompt, 200);
  });

  refreshPrompt();

  // ponytail: self-check — fails if prompt builder regresses
  if (typeof console !== "undefined" && console.assert) {
    console.assert(
      buildPrompt("inbox overwhelm").indexOf("TOPIC: inbox overwhelm") !== -1,
      "note creator prompt must embed topic"
    );
    console.assert(relevantGardenNotes("capture productivity", 5).length > 0, "relevantGardenNotes must match");
    console.assert(buildPrompt("").indexOf(PLACEHOLDER) === 0, "empty topic must show placeholder");
  }
})();
