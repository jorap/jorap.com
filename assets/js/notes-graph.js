/**
 * Obsidian Publish-style force-directed note graph (no dependencies).
 */
(function () {
  var panels = document.querySelectorAll("[data-notes-graph]");
  if (!panels.length) return;

  panels.forEach(function (panel) {
    initGraph(panel);
  });

  function initGraph(panel) {
    var dataEl = panel.querySelector(".notes-graph-data");
    var container = panel.querySelector(".notes-graph");
    var emptyEl = panel.closest(".container, .row, section, article")?.querySelector(".notes-graph-empty") ||
      document.querySelector(".notes-graph-empty");
    var searchEl = panel.querySelector(".notes-graph-search");
    var resetEl = panel.querySelector(".notes-graph-reset");
    var expandEl = panel.querySelector(".notes-graph-expand");
    var zoomInEl = panel.querySelector(".notes-graph-zoom-in");
    var zoomOutEl = panel.querySelector(".notes-graph-zoom-out");
    var filterEls = panel.querySelectorAll("[data-graph-filter]");
    if (!dataEl || !container) return;

    var data;
    try {
      data = JSON.parse(dataEl.textContent);
    } catch (e) {
      return;
    }

    if (!data.nodes || !data.nodes.length) {
      if (emptyEl) emptyEl.classList.remove("hidden");
      return;
    }

    var prefersReducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    var focusId = data.focus || null;

    var canvas = document.createElement("canvas");
    canvas.className = "notes-graph__canvas";
    canvas.setAttribute("aria-hidden", "true");
    container.appendChild(canvas);
    var ctx = canvas.getContext("2d");
    if (!ctx) return;

    var nodes = data.nodes.map(function (n) {
      return {
        id: n.id,
        title: n.title,
        url: n.url,
        x: 0,
        y: 0,
        vx: 0,
        vy: 0,
        degree: n.totalDegree || 0,
        inDegree: n.inDegree || 0,
        outDegree: n.outDegree || 0,
        orphan: Boolean(n.orphan),
        hub: Boolean(n.hub),
        deadEnd: Boolean(n.deadEnd),
      };
    });

    var nodeById = {};
    nodes.forEach(function (n) {
      nodeById[n.id] = n;
    });

    var focusNode = focusId ? nodeById[focusId] : null;

    var edgeKeys = {};
    var edges = (data.edges || [])
      .map(function (e) {
        var source = nodeById[e.source];
        var target = nodeById[e.target];
        if (!source || !target || source === target) return null;
        var key = source.id < target.id ? source.id + "\0" + target.id : target.id + "\0" + source.id;
        if (edgeKeys[key]) return null;
        edgeKeys[key] = true;
        return { source: source, target: target };
      })
      .filter(Boolean);

    edges.forEach(function (e) {
      e.source.degree += 1;
      e.target.degree += 1;
    });

    var width = 0;
    var height = 0;
    var transform = { x: 0, y: 0, k: 1 };
    var defaultTransform = { x: 0, y: 0, k: 1 };
    var hovered = focusNode || null;
    var searchQuery = "";
    var graphFilter = "all";
    var draggingNode = null;
    var dragMoved = false;
    var dragStart = null;
    var panning = false;
    var panStart = null;
    var simAlpha = prefersReducedMotion ? 0 : 1;
    var frame = 0;
    var needsFrame = true;
    var rafId = 0;
    var lastWidth = 0;
    var lastHeight = 0;

    function resolveToken(token, fallback) {
      var probe = document.createElement("span");
      probe.style.display = "none";
      probe.style.color = fallback;
      document.body.appendChild(probe);
      probe.style.color = "var(" + token + ")";
      var resolved = window.getComputedStyle(probe).color;
      document.body.removeChild(probe);
      ctx.fillStyle = fallback;
      try {
        ctx.fillStyle = resolved;
      } catch (e) {
        return fallback;
      }
      return ctx.fillStyle || fallback;
    }

    function readColors() {
      return {
        edge: resolveToken("--color-ink-faint", "#6b6762"),
        edgeActive: resolveToken("--color-ink-muted", "#6b6762"),
        node: resolveToken("--color-ink-faint", "#6b6762"),
        nodeActive: resolveToken("--color-accent", "#181614"),
        nodeHover: resolveToken("--color-ink", "#161412"),
        nodeFocus: resolveToken("--color-accent", "#181614"),
        nodeOrphan: resolveToken("--color-warning", "#b45309"),
        nodeHub: resolveToken("--color-accent", "#181614"),
        nodeDeadEnd: resolveToken("--color-ink-muted", "#6b6762"),
        surface: resolveToken("--color-surface", "#f5f3f0"),
        label: resolveToken("--color-ink", "#161412"),
      };
    }

    var colors = readColors();

    function labelFontSize() {
      return Math.max(9, 11 / transform.k);
    }

    function labelOffset(node) {
      return nodeRadius(node) + 4;
    }

    function nodeRadius(node) {
      var base = Math.min(7, 2.5 + Math.sqrt(node.degree || 0) * 0.9);
      return focusNode && node === focusNode ? Math.max(base, 5.5) : base;
    }

    function containerSize() {
      var rect = container.getBoundingClientRect();
      var w = rect.width || container.clientWidth;
      var h = rect.height || container.clientHeight;
      if (h < 8) {
        h = container.classList.contains("is-expanded") ? Math.min(window.innerHeight * 0.78, 768) : 280;
      }
      if (w < 8) {
        w = rect.width || 320;
      }
      return { width: Math.max(w, 1), height: Math.max(h, 1) };
    }

    function resize() {
      var size = containerSize();
      var dpr = window.devicePixelRatio || 1;
      var sizeChanged = size.width !== lastWidth || size.height !== lastHeight;
      width = size.width;
      height = size.height;
      lastWidth = width;
      lastHeight = height;
      canvas.width = Math.max(1, Math.floor(width * dpr));
      canvas.height = Math.max(1, Math.floor(height * dpr));
      canvas.style.width = width + "px";
      canvas.style.height = height + "px";
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
      if (!frame || sizeChanged) {
        initPositions();
      }
      needsFrame = true;
    }

    function prelayout() {
      if (prefersReducedMotion) return;
      simAlpha = 1;
      for (var i = 0; i < 200; i++) {
        simulate();
      }
      simAlpha = focusNode ? 0.15 : 0.2;
    }

    function initPositions() {
      var cx = width / 2;
      var cy = height / 2;
      var radius = Math.min(width, height) * (focusNode ? 0.32 : 0.34);

      if (focusNode) {
        focusNode.x = cx;
        focusNode.y = cy;
        focusNode.vx = 0;
        focusNode.vy = 0;
        var others = nodes.filter(function (n) {
          return n !== focusNode;
        });
        others.forEach(function (n, i) {
          var angle = (i / Math.max(others.length, 1)) * Math.PI * 2 - Math.PI / 2;
          n.x = cx + Math.cos(angle) * radius;
          n.y = cy + Math.sin(angle) * radius;
          n.vx = 0;
          n.vy = 0;
        });
        return;
      }

      nodes.forEach(function (n, i) {
        var angle = (i / nodes.length) * Math.PI * 2;
        n.x = cx + Math.cos(angle) * radius;
        n.y = cy + Math.sin(angle) * radius;
        n.vx = 0;
        n.vy = 0;
      });
    }

    function screenToWorld(x, y) {
      return {
        x: (x - transform.x) / transform.k,
        y: (y - transform.y) / transform.k,
      };
    }

    function worldToScreen(x, y) {
      return {
        x: x * transform.k + transform.x,
        y: y * transform.k + transform.y,
      };
    }

    function viewNodes() {
      var visible;
      if (typeFilterActive() || !focusNode) {
        visible = nodes;
      } else {
        var set = neighborsOf(focusNode);
        visible = nodes.filter(function (n) {
          return set[n.id];
        });
      }
      if (graphFilter === "all") return visible;
      return visible.filter(passesFilter);
    }

    function fitToView() {
      var visible = viewNodes();
      if (!visible.length || !width || !height) return;

      var minX = Infinity;
      var minY = Infinity;
      var maxX = -Infinity;
      var maxY = -Infinity;
      visible.forEach(function (n) {
        var r = nodeRadius(n) + 10;
        var labelH = labelFontSize() + 6;
        minX = Math.min(minX, n.x - r);
        minY = Math.min(minY, n.y - r);
        maxX = Math.max(maxX, n.x + r);
        maxY = Math.max(maxY, n.y + r + labelH);
      });

      var useFocusCenter = focusNode && !typeFilterActive();
      var pad = useFocusCenter ? 44 : 56;
      var graphW = Math.max(maxX - minX, 1);
      var graphH = Math.max(maxY - minY, 1);
      var k = Math.min((width - pad * 2) / graphW, (height - pad * 2) / graphH, useFocusCenter ? 2 : 1.8);
      k = Math.max(k, 0.25) * 2;

      var cx = useFocusCenter ? focusNode.x : (minX + maxX) / 2;
      var cy = useFocusCenter ? focusNode.y : (minY + maxY) / 2;

      defaultTransform = {
        k: k,
        x: width / 2 - cx * k,
        y: height / 2 - cy * k,
      };

      transform = {
        x: defaultTransform.x,
        y: defaultTransform.y,
        k: defaultTransform.k,
      };
      needsFrame = true;
    }

    function neighborsOf(node) {
      var set = Object.create(null);
      set[node.id] = true;
      edges.forEach(function (e) {
        if (e.source === node) set[e.target.id] = true;
        if (e.target === node) set[e.source.id] = true;
      });
      return set;
    }

    function matchesSearch(node) {
      if (!searchQuery) return true;
      return node.title.toLowerCase().indexOf(searchQuery) !== -1;
    }

    function passesFilter(node) {
      if (graphFilter === "all") return true;
      if (graphFilter === "orphan") return node.orphan;
      if (graphFilter === "hub") return node.hub;
      if (graphFilter === "deadEnd") return node.deadEnd;
      return true;
    }

    function typeFilterActive() {
      return graphFilter !== "all";
    }

    function nodeFill(node, isFocus, isHover, inHighlight, highlight) {
      if (isFocus) return colors.nodeFocus;
      if (isHover) return colors.nodeHover;
      if (node.orphan && (graphFilter === "all" || graphFilter === "orphan")) return colors.nodeOrphan;
      if (node.hub && (graphFilter === "all" || graphFilter === "hub")) return colors.nodeHub;
      if (node.deadEnd && (graphFilter === "all" || graphFilter === "deadEnd")) return colors.nodeDeadEnd;
      if (inHighlight && highlight) return colors.nodeActive;
      return colors.node;
    }

    function hitTest(worldPos) {
      for (var i = nodes.length - 1; i >= 0; i--) {
        var n = nodes[i];
        if (typeFilterActive() && !passesFilter(n)) continue;
        var r = nodeRadius(n) + 5;
        var dx = worldPos.x - n.x;
        var dy = worldPos.y - n.y;
        if (dx * dx + dy * dy <= r * r) return n;
      }
      return null;
    }

    function simulate() {
      if (simAlpha <= 0.002) return false;

      var linkDistance = focusNode ? 115 : 140;
      var linkStrength = 0.14 * simAlpha;
      var repulsion = 3800 * simAlpha;
      var centerStrength = (focusNode ? 0.006 : 0.012) * simAlpha;
      var cx = width / 2;
      var cy = height / 2;

      edges.forEach(function (e) {
        var dx = e.target.x - e.source.x;
        var dy = e.target.y - e.source.y;
        var dist = Math.sqrt(dx * dx + dy * dy) || 1;
        var force = ((dist - linkDistance) / dist) * linkStrength;
        var fx = dx * force;
        var fy = dy * force;
        if (e.source !== draggingNode && e.source !== focusNode) {
          e.source.vx += fx;
          e.source.vy += fy;
        }
        if (e.target !== draggingNode && e.target !== focusNode) {
          e.target.vx -= fx;
          e.target.vy -= fy;
        }
      });

      for (var i = 0; i < nodes.length; i++) {
        for (var j = i + 1; j < nodes.length; j++) {
          var a = nodes[i];
          var b = nodes[j];
          var dx = a.x - b.x;
          var dy = a.y - b.y;
          var dist = Math.sqrt(dx * dx + dy * dy) || 1;
          var minDist = nodeRadius(a) + nodeRadius(b) + 36;
          var repel = repulsion / (dist * dist);
          if (dist < minDist) {
            repel += ((minDist - dist) / dist) * 0.65 * simAlpha;
          }
          var fx = (dx / dist) * repel;
          var fy = (dy / dist) * repel;
          if (a !== draggingNode && a !== focusNode) {
            a.vx += fx;
            a.vy += fy;
          }
          if (b !== draggingNode && b !== focusNode) {
            b.vx -= fx;
            b.vy -= fy;
          }
        }
      }

      nodes.forEach(function (n) {
        if (n === draggingNode) return;
        if (focusNode && n === focusNode) {
          n.x = cx;
          n.y = cy;
          n.vx = 0;
          n.vy = 0;
          return;
        }
        n.vx += (cx - n.x) * centerStrength;
        n.vy += (cy - n.y) * centerStrength;
        n.vx *= 0.84;
        n.vy *= 0.84;
        n.x += n.vx;
        n.y += n.vy;
      });

      simAlpha *= prefersReducedMotion ? 0 : 0.988;
      return true;
    }

    function draw() {
      ctx.clearRect(0, 0, width, height);
      ctx.save();
      ctx.translate(transform.x, transform.y);
      ctx.scale(transform.k, transform.k);

      var highlight = hovered
        ? neighborsOf(hovered)
        : typeFilterActive() || !focusNode
          ? null
          : neighborsOf(focusNode);
      var hasFilter = Boolean(searchQuery);

      edges.forEach(function (e) {
        if (typeFilterActive() && (!passesFilter(e.source) || !passesFilter(e.target))) return;
        var active = highlight && highlight[e.source.id] && highlight[e.target.id];
        var visible =
          !hasFilter ||
          (matchesSearch(e.source) && matchesSearch(e.target)) ||
          active;
        var dimmed = (highlight && !active) || (hasFilter && !visible);

        ctx.beginPath();
        ctx.moveTo(e.source.x, e.source.y);
        ctx.lineTo(e.target.x, e.target.y);
        ctx.strokeStyle = active ? colors.edgeActive : colors.edge;
        ctx.globalAlpha = dimmed ? 0.05 : active ? 0.55 : 0.2;
        ctx.lineWidth = (active ? 1.2 : 0.85) / transform.k;
        ctx.stroke();
      });

      ctx.globalAlpha = 1;
      nodes.forEach(function (n) {
        if (typeFilterActive() && !passesFilter(n)) return;
        var r = nodeRadius(n);
        var isFocus = !typeFilterActive() && focusNode && n === focusNode;
        var isHover = hovered === n;
        var inHighlight = !highlight || highlight[n.id];
        var matches = matchesSearch(n);
        var dimmed = (highlight && !inHighlight) || (hasFilter && !matches && !isHover);

        if (isFocus) {
          ctx.beginPath();
          ctx.fillStyle = colors.nodeFocus;
          ctx.globalAlpha = 0.12;
          ctx.arc(n.x, n.y, r + 8, 0, Math.PI * 2);
          ctx.fill();
        }

        ctx.beginPath();
        ctx.fillStyle = nodeFill(n, isFocus, isHover, inHighlight, highlight);
        ctx.globalAlpha = dimmed ? 0.08 : isFocus ? 1 : isHover ? 1 : inHighlight && highlight ? 0.95 : 0.65;
        ctx.arc(n.x, n.y, r, 0, Math.PI * 2);
        ctx.fill();

        if (isFocus || isHover) {
          ctx.strokeStyle = colors.nodeActive;
          ctx.lineWidth = (isFocus ? 1.6 : 1.25) / transform.k;
          ctx.globalAlpha = 0.95;
          ctx.stroke();
        }

        var fontSize = labelFontSize();
        var labelY = n.y + labelOffset(n);
        ctx.font = (isFocus ? "600 " : "") + fontSize + "px Inter, system-ui, sans-serif";
        ctx.textAlign = "center";
        ctx.textBaseline = "top";
        var labelAlpha = dimmed ? 0.15 : isFocus ? 1 : isHover ? 1 : inHighlight && highlight ? 0.95 : 0.82;
        ctx.lineWidth = Math.max(2.5, 3.5 / transform.k);
        ctx.lineJoin = "round";
        ctx.strokeStyle = colors.surface;
        ctx.fillStyle = nodeFill(n, isFocus, isHover, inHighlight, highlight);
        ctx.globalAlpha = labelAlpha;
        ctx.strokeText(n.title, n.x, labelY);
        ctx.fillText(n.title, n.x, labelY);
      });

      ctx.restore();
    }

    function setHovered(node) {
      hovered = node;
      container.classList.toggle("notes-graph--hover", Boolean(node));
      wake();
    }

    function zoomAt(factor, clientX, clientY) {
      var rect = canvas.getBoundingClientRect();
      var cx = typeof clientX === "number" ? clientX - rect.left : width / 2;
      var cy = typeof clientY === "number" ? clientY - rect.top : height / 2;
      var worldBefore = screenToWorld(cx, cy);
      var nextK = Math.min(7, Math.max(0.18, transform.k * factor));
      transform.k = nextK;
      transform.x = cx - worldBefore.x * nextK;
      transform.y = cy - worldBefore.y * nextK;
      wake();
    }

    canvas.addEventListener("pointermove", function (evt) {
      var pos = pointerPos(evt);
      if (panning && panStart) {
        transform.x = panStart.transformX + (pos.x - panStart.x);
        transform.y = panStart.transformY + (pos.y - panStart.y);
        wake();
        return;
      }
      if (draggingNode) {
        var world = screenToWorld(pos.x, pos.y);
        if (
          dragStart &&
          (Math.abs(world.x - dragStart.x) > 4 || Math.abs(world.y - dragStart.y) > 4)
        ) {
          dragMoved = true;
        }
        draggingNode.x = world.x;
        draggingNode.y = world.y;
        draggingNode.vx = 0;
        draggingNode.vy = 0;
        simAlpha = Math.max(simAlpha, 0.3);
        wake();
        return;
      }
      var world = screenToWorld(pos.x, pos.y);
      setHovered(hitTest(world));
    });

    canvas.addEventListener("pointerdown", function (evt) {
      var pos = pointerPos(evt);
      var world = screenToWorld(pos.x, pos.y);
      var node = hitTest(world);
      if (node && node !== focusNode) {
        draggingNode = node;
        dragMoved = false;
        dragStart = { x: world.x, y: world.y };
        simAlpha = Math.max(simAlpha, 0.35);
        canvas.setPointerCapture(evt.pointerId);
        setHovered(node);
        return;
      }
      panning = true;
      panStart = { x: pos.x, y: pos.y, transformX: transform.x, transformY: transform.y };
      canvas.setPointerCapture(evt.pointerId);
      setHovered(focusNode || null);
      wake();
    });

    function endPointer(evt) {
      if (draggingNode && !panning && !dragMoved) {
        var pos = pointerPos(evt);
        var world = screenToWorld(pos.x, pos.y);
        var node = hitTest(world);
        if (node && node.url && node !== focusNode) {
          if (evt.metaKey || evt.ctrlKey) {
            window.open(node.url, "_blank", "noopener");
          } else {
            window.location.href = node.url;
          }
        }
      }
      draggingNode = null;
      dragMoved = false;
      dragStart = null;
      panning = false;
      panStart = null;
      wake();
    }

    canvas.addEventListener("pointerup", endPointer);
    canvas.addEventListener("pointercancel", function () {
      draggingNode = null;
      dragMoved = false;
      dragStart = null;
      panning = false;
      panStart = null;
      wake();
    });

    canvas.addEventListener(
      "wheel",
      function (evt) {
        evt.preventDefault();
        zoomAt(evt.deltaY < 0 ? 1.1 : 1 / 1.1, evt.clientX, evt.clientY);
      },
      { passive: false }
    );

    canvas.addEventListener("pointerleave", function () {
      if (!draggingNode && !panning) setHovered(focusNode || null);
    });

    if (searchEl) {
      searchEl.addEventListener("input", function () {
        searchQuery = searchEl.value.trim().toLowerCase();
        if (searchQuery) {
          var match = null;
          for (var i = 0; i < nodes.length; i++) {
            if (matchesSearch(nodes[i])) {
              match = nodes[i];
              break;
            }
          }
          if (match) {
            hovered = match;
            var screen = worldToScreen(match.x, match.y);
            transform.x += width / 2 - screen.x;
            transform.y += height / 2 - screen.y;
          }
        } else {
          hovered = focusNode || null;
        }
        wake();
      });
    }

    if (resetEl) {
      resetEl.addEventListener("click", function () {
        if (searchEl) searchEl.value = "";
        searchQuery = "";
        hovered = focusNode || null;
        initPositions();
        fitToView();
        simAlpha = prefersReducedMotion ? 0 : focusNode ? 0.6 : 0.85;
        wake();
      });
    }

    if (zoomInEl) {
      zoomInEl.addEventListener("click", function () {
        zoomAt(1.15);
      });
    }

    if (zoomOutEl) {
      zoomOutEl.addEventListener("click", function () {
        zoomAt(1 / 1.15);
      });
    }

    if (expandEl) {
      expandEl.addEventListener("click", function () {
        var expanded = container.classList.toggle("is-expanded");
        expandEl.setAttribute("aria-pressed", expanded ? "true" : "false");
        expandEl.title = expanded ? "Collapse graph" : "Expand graph";
        expandEl.setAttribute("aria-label", expandEl.title);
        resize();
        fitToView();
        draw();
        wake();
      });
    }

    if (filterEls.length) {
      filterEls.forEach(function (btn) {
        btn.addEventListener("click", function () {
          graphFilter = btn.getAttribute("data-graph-filter") || "all";
          filterEls.forEach(function (el) {
            var active = el === btn;
            el.classList.toggle("is-active", active);
            el.setAttribute("aria-pressed", active ? "true" : "false");
          });
          hovered = graphFilter === "all" ? focusNode || null : null;
          fitToView();
          draw();
          wake();
        });
      });
    }

    function wake() {
      needsFrame = true;
      if (!rafId) {
        rafId = window.requestAnimationFrame(loop);
      }
    }

    function loop() {
      rafId = 0;
      var simulating = !prefersReducedMotion && simulate();
      if (needsFrame || simulating || draggingNode || panning || (hovered && hovered !== focusNode)) {
        draw();
        needsFrame = false;
        frame += 1;
        rafId = window.requestAnimationFrame(loop);
      }
    }

    function pointerPos(evt) {
      var rect = canvas.getBoundingClientRect();
      return { x: evt.clientX - rect.left, y: evt.clientY - rect.top };
    }

    function boot() {
      colors = readColors();
      resize();
      prelayout();
      fitToView();
      draw();
      frame = 1;
      wake();
    }

    boot();
    requestAnimationFrame(function () {
      requestAnimationFrame(boot);
    });

    if (typeof ResizeObserver !== "undefined") {
      var resizeObserver = new ResizeObserver(function () {
        resize();
        fitToView();
        draw();
        wake();
      });
      resizeObserver.observe(container);
    } else {
      window.addEventListener("resize", function () {
        resize();
        fitToView();
        draw();
        wake();
      });
    }
  }
})();
