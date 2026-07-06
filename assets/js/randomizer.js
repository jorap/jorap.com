/**
 * Game prompt randomizer: ranked prompts, personal icebreakers, concept spectrums,
 * either-or dilemmas, and conversation starters.
 */
(function () {
  var root = document.querySelector("[data-randomizer]");
  var dataEl = document.getElementById("randomizer-data");
  if (!root || !dataEl) return;

  var data;
  try {
    data = JSON.parse(dataEl.textContent);
    if (typeof data === "string") data = JSON.parse(data);
  } catch (e) {
    return;
  }

  var collections = (data && data.collections) || [];
  var byCollection = Object.create(null);
  collections.forEach(function (col) {
    byCollection[col.id] = col;
  });

  var views = {
    home: root.querySelector('[data-randomizer-view="home"]'),
    categories: root.querySelector('[data-randomizer-view="categories"]'),
    play: root.querySelector('[data-randomizer-view="play"]'),
  };

  var els = {
    lede: root.querySelector("[data-randomizer-lede]"),
    collections: root.querySelector("[data-randomizer-collections]"),
    collectionTitle: root.querySelector("[data-randomizer-collection-title]"),
    collectionTagline: root.querySelector("[data-randomizer-collection-tagline]"),
    categories: root.querySelector("[data-randomizer-categories]"),
    playMeta: root.querySelector("[data-randomizer-play-meta]"),
    hint: root.querySelector("[data-randomizer-hint]"),
    poles: root.querySelector("[data-randomizer-poles]"),
    scale: root.querySelector("[data-randomizer-scale]"),
    poleLeft: root.querySelector("[data-randomizer-pole-left]"),
    poleRight: root.querySelector("[data-randomizer-pole-right]"),
    prompt: root.querySelector("[data-randomizer-prompt]"),
    counter: root.querySelector("[data-randomizer-counter]"),
    shuffle: root.querySelector("[data-randomizer-shuffle]"),
    saveOffline: root.querySelector("[data-randomizer-save-offline]"),
    back: root.querySelector("[data-randomizer-back]"),
  };

  var state = {
    collectionId: "",
    categoryId: "",
    mode: "",
    items: [],
    index: -1,
  };

  function escapeHtml(str) {
    return String(str)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;");
  }

  function collectionMode(col) {
    return col.mode || "ranked-prompts";
  }

  function isDirectPlay(col) {
    if (col.categories && col.categories.length) return false;
    var mode = collectionMode(col);
    return mode === "spectrum" || mode === "personal" || mode === "ranked-prompts";
  }

  function isSpectrumMode(mode) {
    return mode === "spectrum";
  }

  function isPersonalMode(mode) {
    return mode === "personal";
  }

  function showView(name) {
    Object.keys(views).forEach(function (key) {
      if (views[key]) views[key].hidden = key !== name;
    });
    document.body.classList.toggle("randomizer-focus", name === "play");
  }

  function playUrl(collectionId, categoryId) {
    var url = new URL(window.location.href);
    url.search = "";
    if (collectionId) url.searchParams.set("set", collectionId);
    if (categoryId) url.searchParams.set("cat", categoryId);
    return url;
  }

  function pushRoute(collectionId, categoryId) {
    var url = playUrl(collectionId, categoryId);
    window.history.pushState(null, "", url.pathname + url.search);
  }

  function findCategory(collectionId, categoryId) {
    var col = byCollection[collectionId];
    if (!col || !col.categories) return null;
    for (var i = 0; i < col.categories.length; i += 1) {
      if (col.categories[i].id === categoryId) return col.categories[i];
    }
    return null;
  }

  function spectrumItems(col) {
    return (col.spectrums || []).map(function (pair) {
      return { left: pair.left || "", right: pair.right || "" };
    });
  }

  function flatItems(col) {
    var mode = collectionMode(col);
    if (mode === "spectrum") return spectrumItems(col);
    if (mode === "personal" || mode === "ranked-prompts") return (col.items || []).slice();
    return [];
  }

  function collectionCardHtml(col) {
    var mode = collectionMode(col);
    var count;
    var countLabel;
    if (mode === "spectrum") {
      count = (col.spectrums || []).length;
      countLabel = count + " spectrum" + (count === 1 ? "" : "s");
    } else if (mode === "personal" || mode === "ranked-prompts") {
      count = (col.items || []).length;
      countLabel = count + " prompt" + (count === 1 ? "" : "s");
    } else {
      count = (col.categories || []).length;
      countLabel = count + " categor" + (count === 1 ? "y" : "ies");
    }
    return (
      '<button type="button" class="randomizer-tile" data-randomizer-pick-collection="' +
      escapeHtml(col.id) +
      '">' +
      '<span class="randomizer-tile__title">' +
      escapeHtml(col.title) +
      "</span>" +
      '<span class="randomizer-tile__meta">' +
      escapeHtml(col.tagline) +
      "</span>" +
      '<span class="randomizer-tile__count">' +
      countLabel +
      "</span>" +
      "</button>"
    );
  }

  function categoryCardHtml(cat) {
    var count = (cat.items || []).length;
    return (
      '<a class="randomizer-tile randomizer-tile--link" href="' +
      escapeHtml(
        playUrl(state.collectionId, cat.id).pathname +
          playUrl(state.collectionId, cat.id).search
      ) +
      '" data-randomizer-pick-category="' +
      escapeHtml(cat.id) +
      '">' +
      '<span class="randomizer-tile__title">' +
      escapeHtml(cat.title) +
      "</span>" +
      '<span class="randomizer-tile__meta">' +
      count +
      " prompt" +
      (count === 1 ? "" : "s") +
      "</span>" +
      "</a>"
    );
  }

  function renderHome() {
    if (els.lede) {
      els.lede.textContent =
        "Five decks for table time. Pick one, shuffle, pass the phone.";
    }
    if (els.collections) {
      els.collections.innerHTML = collections.map(collectionCardHtml).join("");
    }
    showView("home");
  }

  function renderCategories(collectionId) {
    var col = byCollection[collectionId];
    if (!col || isDirectPlay(col)) {
      renderHome();
      return;
    }
    state.collectionId = collectionId;
    if (els.collectionTitle) els.collectionTitle.textContent = col.title;
    if (els.collectionTagline) els.collectionTagline.textContent = col.tagline || "";
    if (els.categories) {
      els.categories.innerHTML = (col.categories || []).map(categoryCardHtml).join("");
    }
    showView("categories");
  }

  function setPlayChrome(col, meta) {
    if (els.playMeta) els.playMeta.textContent = meta || col.title;
    if (els.hint) els.hint.textContent = col.play_hint || "";
    if (els.back) {
      els.back.setAttribute(
        "aria-label",
        isDirectPlay(col) ? "Back to all collections" : "Back to categories"
      );
    }
  }

  function renderPrompt() {
    var col = byCollection[state.collectionId];
    if (!col) return;

    var spectrumMode = isSpectrumMode(state.mode);
    var personalMode = isPersonalMode(state.mode);
    if (els.poles) els.poles.hidden = !spectrumMode;
    if (els.prompt) els.prompt.hidden = spectrumMode;
    if (els.scale) {
      if (personalMode) {
        els.scale.hidden = false;
        els.scale.textContent = col.scale_label || "On a scale of 1 to 100";
      } else {
        els.scale.hidden = true;
        els.scale.textContent = "";
      }
    }

    if (spectrumMode) {
      var pair = state.items[state.index] || { left: "", right: "" };
      if (els.poleLeft) els.poleLeft.textContent = pair.left;
      if (els.poleRight) els.poleRight.textContent = pair.right;
    } else {
      var text = "";
      if (state.index >= 0 && state.items[state.index]) {
        text = state.items[state.index];
      }
      if (els.prompt) els.prompt.textContent = text || "No prompts in this set yet.";
    }

    if (els.counter) {
      if (!state.items.length) {
        els.counter.textContent = "";
      } else {
        var label = spectrumMode ? "Spectrum" : "Prompt";
        els.counter.textContent =
          label + " " + (state.index + 1) + " of " + state.items.length;
      }
    }
  }

  function startPlay(collectionId, categoryId) {
    var col = byCollection[collectionId];
    var cat = findCategory(collectionId, categoryId);
    if (!col || !cat) {
      renderHome();
      return;
    }

    state.collectionId = collectionId;
    state.categoryId = categoryId;
    state.mode = collectionMode(col);
    state.items = (cat.items || []).slice();
    state.index = -1;

    setPlayChrome(col, col.title + " · " + cat.title);
    showView("play");
    if (state.items.length) shuffleNext();
    else renderPrompt();
  }

  function startFlatPlay(collectionId) {
    var col = byCollection[collectionId];
    if (!col || !isDirectPlay(col)) {
      renderHome();
      return;
    }

    state.collectionId = collectionId;
    state.categoryId = "";
    state.mode = collectionMode(col);
    state.items = flatItems(col);
    state.index = -1;

    setPlayChrome(col, col.title);
    showView("play");
    if (state.items.length) shuffleNext();
    else renderPrompt();
  }

  function shuffleNext() {
    if (!state.items.length) return;

    if (state.items.length === 1) {
      state.index = 0;
      renderPrompt();
      return;
    }

    var nextIndex = state.index;
    var guard = 0;
    while (nextIndex === state.index && guard < 20) {
      nextIndex = Math.floor(Math.random() * state.items.length);
      guard += 1;
    }
    state.index = nextIndex;
    renderPrompt();
  }

  function offlineCss() {
    return [
    "*,*::before,*::after{box-sizing:border-box}",
    "html{height:100%}",
    "body{margin:0;min-height:100dvh;display:flex;flex-direction:column;font-family:Inter,system-ui,-apple-system,Segoe UI,Roboto,sans-serif;",
    "background:#f5f3f0;color:#161412;line-height:1.5;-webkit-font-smoothing:antialiased}",
    ".randomizer-play{display:flex;flex:1;flex-direction:column;min-height:0;width:100%}",
    ".randomizer-play__stage{align-items:center;display:flex;flex:1;justify-content:center;min-height:0;",
    "padding:max(.75rem,env(safe-area-inset-top)) max(1rem,env(safe-area-inset-left)) .75rem max(1rem,env(safe-area-inset-right))}",
    ".randomizer-card{align-items:center;background:#eeebe6;border-radius:.75rem;display:flex;flex:1;flex-direction:column;justify-content:center;margin-inline:auto;",
    "max-width:48rem;min-height:min(52vh,28rem);padding:clamp(1.5rem,4vw,3rem);text-align:center;width:min(100%,48rem)}",
    ".randomizer-card__scale{color:#3d3a37;font-size:clamp(.875rem,2vw,1rem);font-weight:600;letter-spacing:.02em;margin:0 0 .75rem}",
    ".randomizer-card__poles{align-items:center;display:flex;flex-wrap:wrap;gap:.75rem 1rem;justify-content:center;width:100%}",
    ".randomizer-card__pole{flex:1 1 8rem;font-size:clamp(1.375rem,3.5vw,2rem);font-weight:600;line-height:1.35;min-width:0}",
    ".randomizer-card__bridge{color:#3d3a37;flex:0 0 auto;font-size:1.25rem}",
    ".randomizer-card__prompt{font-size:clamp(1.375rem,3.5vw,2rem);font-weight:600;line-height:1.35;margin:0;text-wrap:balance}",
    ".randomizer-play-actions{align-items:center;display:flex;flex:0 0 auto;flex-direction:column;gap:.75rem;justify-content:center;",
    "padding:0 max(1rem,env(safe-area-inset-left)) max(1.25rem,env(safe-area-inset-bottom)) max(1rem,env(safe-area-inset-right))}",
    ".btn{display:inline-flex;align-items:center;justify-content:center;font:inherit;font-weight:600;cursor:pointer;",
    "border:1px solid transparent;touch-action:manipulation}",
    ".btn-primary{background:#181614;border-color:#181614;color:#fff;border-radius:.25rem;",
    "font-size:1.0625rem;min-height:3.25rem;min-width:12rem;padding:.625rem 2rem}",
    ".btn-primary:hover,.btn-primary:focus-visible{opacity:.92;outline:none}",
    ".randomizer-play__counter{color:#3d3a37;font-size:.875rem;margin:0}",
    "@media (min-width:768px){.randomizer-play-actions{padding-inline:max(1.5rem,env(safe-area-inset-left)) max(1.5rem,env(safe-area-inset-right))}}",
    "@media (prefers-color-scheme:dark){",
    "body{background:#121110;color:#f5f2ed}",
    ".randomizer-card{background:#2a2824}",
    ".randomizer-card__scale,.randomizer-card__bridge,.randomizer-play__counter{color:#d9d4cd}",
    ".btn-primary{background:#f2efe9;border-color:#f2efe9;color:#121110}",
    "}",
    ].join("");
  }

  function offlineHtml() {
    var col = byCollection[state.collectionId];
    if (!col) return "";

    var directPlay = isDirectPlay(col);
    var cat = directPlay ? null : findCategory(state.collectionId, state.categoryId);
    if (!directPlay && !cat) return "";

    var payload = {
      title: directPlay ? col.title : cat.title,
      mode: state.mode,
      scale_label: col.scale_label || "",
      items: directPlay ? state.items : cat.items || [],
    };

    return (
      "<!DOCTYPE html>\n<html lang=\"en\">\n<head>\n<meta charset=\"utf-8\">\n" +
      "<meta name=\"viewport\" content=\"width=device-width,initial-scale=1,viewport-fit=cover\">\n" +
      "<title>" +
      escapeHtml(payload.title) +
      " - randomizer</title>\n<style>" +
      offlineCss() +
      "</style>\n</head>\n<body>\n" +
      '<div class="randomizer-play">\n' +
      '<div class="randomizer-play__stage"><div class="randomizer-card" id="card"></div></div>\n' +
      '<div class="randomizer-play-actions">\n' +
      '<button type="button" class="btn btn-primary randomizer-play__shuffle" id="shuffle">Shuffle</button>\n' +
      '<p class="randomizer-play__counter" id="counter"></p>\n' +
      "</div>\n</div>\n<script>\n" +
      "(function(){\n" +
      "var data=" +
      JSON.stringify(payload) +
      ";\n" +
      "var items=data.items||[];\n" +
      "var spectrum=data.mode==='spectrum';\n" +
      "var personal=data.mode==='personal';\n" +
      "var index=-1;\n" +
      "var card=document.getElementById('card');\n" +
      "var counter=document.getElementById('counter');\n" +
      "function el(tag,cls,text){\n" +
      "var node=document.createElement(tag);\n" +
      "if(cls)node.className=cls;\n" +
      "if(text!=null)node.textContent=text;\n" +
      "return node;\n" +
      "}\n" +
      "function render(){\n" +
      "card.textContent='';\n" +
      "if(!items.length){card.appendChild(el('p','randomizer-card__prompt','No prompts.'));counter.textContent='';return;}\n" +
      "if(spectrum){\n" +
      "var p=items[index];\n" +
      "var poles=el('div','randomizer-card__poles');\n" +
      "poles.appendChild(el('span','randomizer-card__pole',p.left));\n" +
      "poles.appendChild(el('span','randomizer-card__bridge','\\u2194'));\n" +
      "poles.appendChild(el('span','randomizer-card__pole',p.right));\n" +
      "card.appendChild(poles);\n" +
      "counter.textContent='Spectrum '+(index+1)+' of '+items.length;\n" +
      "}else{\n" +
      "if(personal&&data.scale_label){card.appendChild(el('p','randomizer-card__scale',data.scale_label));}\n" +
      "card.appendChild(el('p','randomizer-card__prompt',items[index]));\n" +
      "counter.textContent='Prompt '+(index+1)+' of '+items.length;\n" +
      "}\n" +
      "}\n" +
      "function shuffle(){\n" +
      "if(!items.length)return;\n" +
      "if(items.length===1){index=0;render();return;}\n" +
      "var next=index,g=0;\n" +
      "while(next===index&&g<20){next=Math.floor(Math.random()*items.length);g++;}\n" +
      "index=next;render();\n" +
      "}\n" +
      "document.getElementById('shuffle').addEventListener('click',shuffle);\n" +
      "shuffle();\n" +
      "})();\n" +
      "</scr" +
      "ipt>\n</body>\n</html>"
    );
  }

  function downloadOffline() {
    var col = byCollection[state.collectionId];
    if (!col) return;
    if (!isDirectPlay(col) && !findCategory(state.collectionId, state.categoryId)) return;

    var html = offlineHtml();
    var blob = new Blob([html], { type: "text/html;charset=utf-8" });
    var link = document.createElement("a");
    var slug = (state.categoryId || state.collectionId || "randomizer").replace(
      /[^a-z0-9-]+/gi,
      "-"
    );
    link.download = "randomizer-" + slug + ".html";
    link.href = URL.createObjectURL(blob);
    link.click();
    setTimeout(function () {
      URL.revokeObjectURL(link.href);
    }, 1000);
  }

  function routeFromLocation() {
    var params = new URLSearchParams(window.location.search);
    var setId = params.get("set") || "";
    var catId = params.get("cat") || "";
    var col = byCollection[setId];

    if (!setId || !col) {
      renderHome();
      return;
    }

    if (isDirectPlay(col)) {
      startFlatPlay(setId);
      return;
    }

    if (catId && findCategory(setId, catId)) {
      startPlay(setId, catId);
      return;
    }

    renderCategories(setId);
  }

  root.addEventListener("click", function (event) {
    var target = event.target.closest("[data-randomizer-pick-collection]");
    if (target) {
      event.preventDefault();
      var colId = target.getAttribute("data-randomizer-pick-collection");
      var col = byCollection[colId];
      if (col && isDirectPlay(col)) {
        pushRoute(colId, "");
        startFlatPlay(colId);
        return;
      }
      pushRoute(colId, "");
      renderCategories(colId);
      return;
    }

    target = event.target.closest("[data-randomizer-pick-category]");
    if (target) {
      event.preventDefault();
      var catId = target.getAttribute("data-randomizer-pick-category");
      pushRoute(state.collectionId, catId);
      startPlay(state.collectionId, catId);
    }
  });

  if (els.back) {
    els.back.addEventListener("click", function () {
      var col = byCollection[state.collectionId];
      if (col && isDirectPlay(col)) {
        pushRoute("", "");
        renderHome();
        return;
      }
      pushRoute(state.collectionId, "");
      renderCategories(state.collectionId);
    });
  }

  if (els.shuffle) {
    els.shuffle.addEventListener("click", shuffleNext);
  }

  if (els.saveOffline) {
    els.saveOffline.addEventListener("click", downloadOffline);
  }

  window.addEventListener("popstate", routeFromLocation);
  routeFromLocation();
})();
