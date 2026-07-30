---
title: "Local AI on My Linux Desktop, Windows Laptop, and M4 MacBook"
meta_title: "Local AI on Linux, Windows, and Mac - What Actually Fits"
description: "I mapped local AI on my Ryzen Linux box, a 6 GB VRAM Windows laptop, and my M4 MacBook against Signal Coders' tiers - conservative GPU budgets and Tier 0-2 model picks."
slug: "local-ai-my-machines"
date: "2026-07-28T12:00:00Z"
image: "/images/feature-consistent-ai-output.jpg"
categories: ["Technology", "AI", "Productivity"]
author: "JoRap"
tags: ["Local AI", "Linux", "Windows", "MacBook", "Ollama", "MLX", "Hardware", "LLM", "Cursor", "AMD", "Apple Silicon", "NVIDIA"]
related_notes:
  - local-first-software
  - building-a-personal-api
  - the-knowledge-lifecycle
aliases: ["local-ai-two-systems"]
featured: false
draft: true
---

I wanted local AI on the machines I already own - not a cloud bill for every sidebar question, not another subscription. I have three boxes in rotation: a **Linux Mint desktop** with a Ryzen 5 8500G and Radeon 740M, a **Windows laptop** (WebFX-G15, i5-13450HX, **6 GB VRAM**, **16 GB RAM**), and a **MacBook Pro M4 with 24 GB RAM** for client work. Same question on all of them: how much memory can the GPU actually use?

Short answer: it depends which machine. The Windows laptop has **real dedicated VRAM** - just not much of it. The Mac shares one clean pool. The Linux box borrows from system RAM through GTT, with a rougher driver path. All three need a **conservative budget** before you pull a model, because the OS, the browser, and Cursor all want their cut first.

---

## Three different memory stories

Discrete GPUs have their own memory chip. Integrated and unified setups pretend they don't - or share everything.

On the **Linux desktop**, the Radeon 740M sits inside the CPU die. The BIOS carves out a tiny fixed slice - **512 MB** on my board - and the rest shows up as **GTT**, shared system memory the GPU can reach when a workload asks for it. My box reports about **15 GB** of GTT against **32 GB** total RAM.

On the **Windows laptop**, the GPU reports **6 GB VRAM** - a separate pool from the **16 GB** system RAM. That sounds like a clean split. It isn't, because Windows still lives in system RAM and **partial GPU offload** will spill layers back into the 16 GB pool when a model doesn't fit. Six gigabytes is below the **8 GB floor** most local-AI guides treat as serious.

On the **MacBook**, Apple Silicon uses **unified memory**. CPU, GPU, and Neural Engine draw from the same **24 GB** pool. There is no separate VRAM line in Activity Monitor. macOS just decides how much Metal can wire up at runtime.

---

## Conservative GPU budget: Linux desktop (Ryzen 8500G / Radeon 740M)

These are the numbers I'd **plan around**, not the theoretical maximum.

| Pool | What my box reports | Conservative usable for local AI |
|------|---------------------|--------------------------------|
| BIOS carve-out ("VRAM") | **512 MB** | Ignore it - too small for LLMs |
| GTT (GPU shared RAM) | **~15 GB** | **~12 GB** for model weights |
| Full system RAM (CPU path) | **32 GB** | **~25 GB** if I close the heavy tabs |

Why not use all 15 GB of GTT? Cinnamon, Brave, Cursor, and a few client tabs already sit on the machine while I work. I also run **no swap** on this install. Push past comfortable RAM and the OOM killer shows up - no graceful slowdown, just dead processes.

**GPU path (Vulkan / llama.cpp):** I'd treat **12 GB** as the hard planning number. A **7B model at Q4** needs roughly 4-5 GB and fits. **13B at Q4** is already tight on GPU memory alone, and the 740M only has **four graphics cores**. Tokens per second will be modest even when it loads.

**CPU path (Ollama or llama.cpp on CPU):** I can reach for **25 GB** of the 32 GB pool if I'm willing to go slow. That's where a **13B or 20B Q4** model becomes realistic - not fast, but it runs without begging a cloud API.

**ROCm:** not a practical option on the 740M. I don't plan around it.

The Linux box is a **RAM-size play**, not a **GPU-speed play**. Useful for offline experiments and models I'd run overnight. Not the machine I'd open for a snappy chat while a WordPress build is already chewing CPU.

---

## Conservative GPU budget: Windows laptop (WebFX-G15 / i5-13450HX)

This is the tightest box of the three. Gaming-laptop specs on paper, **16 GB RAM** in practice.

| Pool | What the machine reports | Conservative usable for local AI |
|------|--------------------------|--------------------------------|
| Dedicated VRAM | **6 GB** | **~5 GB** for model weights |
| System RAM (CPU / offload spill) | **16 GB** (~15.7 GB usable) | **~12 GB** if I close everything else |

Why only **5 GB** on a 6 GB card? Windows, the display driver, and a browser tab already reserve headroom. Push a **7B Q4** model (~5 GB weights) to the limit and there's almost nothing left for KV cache. Long context on this box is a fantasy.

**GPU path (Ollama / LM Studio / llama.cpp CUDA):** plan for **Tier 0** models - **3B-8B at Q4**. A **14B model does not fit** fully on 6 GB VRAM. You can offload layers to system RAM, but with only **16 GB** total, the machine starts **thrashing** fast.

**CPU path:** technically possible for slightly bigger quants, but **16 GB RAM** is the real ceiling. I'd treat this as a **GPU-first** laptop and stay small.

**Software path:** **Ollama** or **LM Studio** on Windows. CUDA support is the upside here - the 740M Linux box can't match NVIDIA's tooling even when Linux has more shared memory on paper.

The Windows laptop is my **travel / secondary** box for local AI. Fine for offline chat with a small model. Not where I'd run Tier 1 14B or anything Tier 2.

---

## Conservative GPU budget: MacBook Pro M4, 24 GB

Same rule: plan conservative, not peak.

| Pool | Total | Conservative usable for local AI |
|------|-------|--------------------------------|
| Unified memory | **24 GB** | **~16 GB** for model weights + KV cache |

macOS and my usual work stack (browser, Slack, sometimes a staging tab) eat the rest. Apple can expose more to Metal - people bump `iogpu.wired_limit_mb` toward **20 GB** - but I wouldn't start there on a machine I bill client hours on. Sixteen gigabytes is the number I trust with everything else still open.

**What fits at ~16 GB GPU budget:**

- **7B-8B at Q4 or Q8** - comfortable daily driver
- **14B at Q4** - fine if I'm not also hoarding forty Chrome tabs
- **27B-32B at Q4** - possible, but I'd close apps and accept that I'm living on the edge

**What I'd skip on 24 GB:** **70B** anything. Not enough room, and swap on a laptop feels like punishment.

**Software path:** **MLX** or **Ollama** (MLX backend on recent builds). Metal is the reason the Mac feels fast here - not raw gigabytes. The M4's memory bandwidth beats my desktop iGPU by a wide margin even when the model sizes look similar on paper.

---

## Side by side - the numbers I actually use

| | Linux desktop (8500G) | Windows laptop (G15) | MacBook Pro M4 24 GB |
|---|---|---|---|
| **Dedicated VRAM** | None (512 MB BIOS slice) | **6 GB** | None |
| **Conservative GPU budget** | **~12 GB** | **~5 GB** | **~16 GB** |
| **CPU / full-RAM ceiling** | **~25 GB** | **~12 GB** | N/A - same pool |
| **Sweet spot models** | Tier 1 on GPU; Tier 2 on CPU | Tier 0 on GPU | Tier 1 daily; Tier 2 when closed up |
| **Signal Coders tier** | Tier 1 memory / Tier 0 GPU speed | **Tier 0** | Tier 1.5 daily; Tier 2 stretched |
| **Framework I'd reach for** | llama.cpp (Vulkan or CPU), Ollama | Ollama, LM Studio | MLX, Ollama |
| **Honest limit** | Slow GPU, no swap safety net | 6 GB VRAM + 16 GB RAM wall | 24 GB total, not expandable |

The Windows laptop is the reality check in that table. It has **real VRAM** - and still lands at **Tier 0** because six gigabytes is not eight. The Mac's unified memory path just works. The 740M on Linux has more shared headroom on paper, but weaker silicon and thinner drivers.

---

## Where my machines land on Signal Coders' tier map

I found a useful frame in [Signal Coders' 2026 local AI hardware guide](https://www.youtube.com/watch?v=96iZUOu5fwc). They sort rigs into tiers by how much memory you can actually give the model - not by marketing names on the box.

| Tier | Label | Rough hardware | What they recommend |
|------|-------|----------------|---------------------|
| **0** | No GPU / 8 GB | CPU-only laptops | Llama 3.2 small, tiny Qwen builds |
| **1** | 16 GB comfort zone | Mid GPUs, 16 GB laptops | **Llama 3.2**, **Qwen 8B-14B**, **Gemma 12B** |
| **2** | 24 GB+ sweet spot | 3090/4090 class, full 24 GB Macs | **Bonsai 27B**, **Qwen 27B/32B** |
| **3+** | Workstation / ceiling | MoE monsters, homelab | Out of scope for these three |

They also give Mac users a **half-tier bump** - unified memory shares cleanly, so a 24 GB Mac isn't quite the same headache as a **16 GB Windows laptop** with a small VRAM pool. I felt that on the G15 before I ran the numbers.

**My mapping with conservative GPU budgets:**

| Machine | Conservative tier | Stretch tier | Honest caveat |
|---------|-------------------|--------------|---------------|
| **Linux desktop** (~12 GB GPU) | **Tier 1** for model size | **Tier 2 on CPU** (or Bonsai on GPU) | Tier 1 *memory*, Tier 0 *speed* on the 740M |
| **Windows laptop** (~5 GB VRAM) | **Tier 0** | **Bonsai 27B** on GPU only | 16 GB RAM kills Tier 1 offload |
| **MacBook M4 24 GB** (~16 GB daily) | **Tier 1** (+ half-tier bump) | **Tier 2** when I close Slack | Full 24 GB pool unlocks their enthusiast tier |

That video stopped me from treating "32 GB system RAM" on the Linux box as "I am Tier 2 now." Shared GTT is not the same as a 24 GB RTX card. The Windows laptop taught me the opposite mistake - **dedicated VRAM on the label** doesn't mean Tier 1 if the number is six.

---

## Models I'd pull - Signal Coders Tier 1 and Tier 2

These follow the families from that guide. All via **Ollama** unless noted; on the Mac I'd grab **MLX** builds of the same names when I want Metal speed.

### Linux desktop - Tier 1 (GPU, ~12 GB budget)

Signal Coders' Tier 1 picks, sized for my **~12 GB** GTT ceiling. I run these on **Vulkan** through llama.cpp or Ollama with GPU offload.

| # | Model | Ollama pull | Why |
|---|-------|-------------|-----|
| 1 | **Qwen3 14B** | `ollama pull qwen3:14b` | Their Tier 1 flagship. Fits at Q4 with context room on 12 GB. |
| 2 | **Gemma 3 12B** | `ollama pull gemma3:12b` | Tier 1 generalist. Dense, multimodal, Apache license. |
| 3 | **Qwen3 8B** | `ollama pull qwen3:8b` | "Qwen small" from the video - fast fallback when 14B feels sluggish on the 740M. |
| 4 | **Llama 3.2 3B** | `ollama pull llama3.2:3b` | Tier 0-1 bridge model. Near-instant on weak iGPU when I just need a sanity check. |
| 5 | **Llama 3.1 8B** | `ollama pull llama3.1:8b` | Still the safest Tier 1 general chat if Qwen3 builds act up on AMDGPU. |

Expect modest tokens per second. These are Tier 1 **by memory**, not by snappiness.

### Linux desktop - Tier 2 (CPU or special-case GPU)

Tier 2 on this box means **patience** or a compressed build. I don't pretend the 740M is a 4090.

| # | Model | How I'd run it | Why |
|---|-------|----------------|-----|
| 1 | **Bonsai 27B** | GPU (Vulkan) - ~4 GB at 1-bit | Signal Coders' Tier 2 wildcard. 27B-class reasoning in a footprint that actually fits my iGPU. |
| 2 | **Qwen3 27B** | CPU overnight | Their Tier 2 dense pick. ~16 GB at Q4 - fits my **~25 GB** CPU ceiling if I close Brave. |
| 3 | **Qwen2.5 32B** | CPU overnight | Same tier family. Smarter, slower. Background job, not interactive chat. |
| 4 | **Qwen3 32B** | CPU overnight | Newer Tier 2 option from the guide. I'd try this before buying hardware. |
| 5 | **DeepSeek-R1-Distill 32B** | CPU overnight | Tier 2 reasoning variant. For prompts where I want visible step-by-step logic. |

**Bonsai** is the one Tier 2 model that doesn't insult the 740M. The dense 27B/32B builds are **RAM-size plays** - fine at 2 AM, useless during a client call.

### Windows laptop - Tier 0 (GPU, ~5 GB VRAM)

Signal Coders' **Tier 0** picks - the only honest tier for **6 GB VRAM** and **16 GB RAM**. CUDA via **Ollama** or **LM Studio**.

| # | Model | Ollama pull | Why |
|---|-------|-------------|-----|
| 1 | **Qwen3 8B** | `ollama pull qwen3:8b` | Top of what fits at Q4 on **~5 GB**. Short context only. |
| 2 | **Llama 3.1 8B** | `ollama pull llama3.1:8b` | The safe 8 GB-tier model, squeezed onto a 6 GB card. |
| 3 | **Gemma 3 4B** | `ollama pull gemma3:4b` | Leaves real VRAM headroom. Good for travel and battery life. |
| 4 | **Llama 3.2 3B** | `ollama pull llama3.2:3b` | Fast sanity checks. What I run when the hotel Wi-Fi is lying about "high speed." |
| 5 | **Phi-4-mini** | `ollama pull phi4-mini` | Tiny footprint. CPU-friendly fallback when the GPU is already full. |

I'd skip **Gemma 12B** and **Qwen 14B** here unless I enjoy watching Task Manager eat the whole **16 GB** pool.

### Windows laptop - stretch (Bonsai only)

Tier 2 dense models are a non-starter on **16 GB RAM**. One exception:

| Model | How I'd run it | Why |
|-------|----------------|-----|
| **Bonsai 27B** | GPU (CUDA) - ~4 GB at 1-bit | Signal Coders' Tier 2 compressed build. **27B-class** reasoning in a footprint the 6 GB card can actually hold. |

That's the only Tier 2 family I'd try on this laptop. Everything else belongs on the Mac or the Linux box overnight.

### MacBook Pro M4, 24 GB - Tier 1 (daily, ~16 GB budget)

Tier 1 with Signal Coders' **half-tier Mac bump**. Slack and a staging tab can stay open.

| # | Model | Ollama pull | Why |
|---|-------|-------------|-----|
| 1 | **Qwen3 14B** | `ollama pull qwen3:14b` | Default Tier 1 workhorse. Best balance of smarts and speed on **~16 GB**. |
| 2 | **Gemma 3 12B** | `ollama pull gemma3:12b` | Their Tier 1 generalist. Great summaries and tool-shaped tasks. |
| 3 | **Qwen3 8B** | `ollama pull qwen3:8b` | Fast chat when 14B is overkill. Q8 is viable on Metal here. |
| 4 | **Llama 3.2 3B** | `ollama pull llama3.2:3b` | Quick drafts beside a WordPress tab. Barely touches the budget. |
| 5 | **Qwen2.5-Coder 14B** | `ollama pull qwen2.5-coder:14b` | Tier 1 coding pick for PHP and theme work - same memory class as Qwen3 14B. |

### MacBook Pro M4, 24 GB - Tier 2 (close apps, full 24 GB pool)

Signal Coders' enthusiast tier. I only open these when I'm not billing hours on something else memory-hungry.

| # | Model | Ollama pull | Why |
|---|-------|-------------|-----|
| 1 | **Bonsai 27B** | Custom GGUF / MLX | Tier 2 compressed 27B. Fits with room to breathe on 24 GB unified memory. |
| 2 | **Qwen3 27B** | `ollama pull qwen3:27b` | Their Tier 2 dense default. The reason I bought 24 GB instead of 16 GB. |
| 3 | **Qwen2.5 32B** | `ollama pull qwen2.5:32b` | Slightly older, still excellent. Tight at Q4 - I close Chrome first. |
| 4 | **Qwen3 32B** | `ollama pull qwen3:32b` | Newer Tier 2 ceiling on a single 24 GB Mac. |
| 5 | **DeepSeek-R1-Distill 32B** | `ollama pull deepseek-r1:32b` | Tier 2 reasoning. For hard prompts I'd otherwise send to a cloud model. |

On the Mac, Tier 2 is **real** - not an overnight CPU crawl. The Windows laptop and the Linux box trade speed for size in different ways. The G15 just has less of both.

---

## Models that work across machines

The **WebFX-G15** sets the floor. If a model fits **~5 GB VRAM** on Windows, it runs on all three. Anything bigger splits the fleet.

### Top 5 on all three machines

Sized to the **~5 GB** Windows ceiling. Same `ollama pull` on every box; swap **MLX** on the Mac if you want Metal speed.

| # | Model | Ollama pull | ~Q4 size | Best for | Why it's the universal pick |
|---|-------|-------------|----------|----------|----------------------------|
| 1 | **Gemma 3 4B** | `ollama pull gemma3:4b` | ~2.2 GB | General | Comfortable margin on the 6 GB card. Still useful on Linux and Mac - not just a toy model. |
| 2 | **Qwen3 8B** | `ollama pull qwen3:8b` | ~5 GB | General / light coding | Best **dense** quality that clears all three. Tight on the G15 - keep context short. |
| 3 | **Llama 3.2 3B** | `ollama pull llama3.2:3b` | ~2 GB | Speed checks | Fastest round-trip on every GPU. My "does this prompt even parse?" model. |
| 4 | **Qwen2.5-Coder 7B** | `ollama pull qwen2.5-coder:7b` | ~4.7 GB | **Coding** | Same footprint class as Qwen 8B. The cross-platform coding default for PHP and theme work. |
| 5 | **Bonsai 27B** | Custom GGUF / MLX | ~4 GB (1-bit) | **Thinking** | The cheat code. **27B-class** reasoning in a Tier 0 footprint. Different install per OS, but it actually fits every GPU here. |

**All-three coding pick:** **Qwen2.5-Coder 7B** - nothing else in this size class beats it for PHP, WordPress scaffolding, and regex. **Qwen3 8B** is fine for light code questions; use the Coder build when the output has to compile.

**All-three thinking pick:** **Bonsai 27B** - step-by-step logic and tool-shaped tasks at 27B scale. Runner-up: **DeepSeek-R1-Distill 8B** (`ollama pull deepseek-r1:8b`, ~5 GB) if you want visible chain-of-thought and an easy Ollama pull on every box.

**What failed the all-three test:** **Qwen3 14B**, **Gemma 3 12B**, and every dense **27B/32B** build. They fit Linux and Mac fine. The Windows laptop either offloads into **16 GB RAM** and chokes, or won't load at all.

### Top 5 on two of three (Linux + Mac)

This is the meaningful pair - both machines have headroom above the G15. I use these when I'm **not** on the Windows laptop.

| # | Model | Ollama pull | Best for | Works on | Skips |
|---|-------|-------------|----------|----------|-------|
| 1 | **Qwen3 14B** | `ollama pull qwen3:14b` | General | Linux GPU, Mac daily | Windows - needs ~8-10 GB at Q4 |
| 2 | **Gemma 3 12B** | `ollama pull gemma3:12b` | General / multimodal | Linux GPU, Mac daily | Windows - ~7.5 GB at Q4 |
| 3 | **Qwen2.5-Coder 14B** | `ollama pull qwen2.5-coder:14b` | **Coding** | Linux GPU, Mac daily | Windows - client-code tier |
| 4 | **DeepSeek-R1-Distill 14B** | `ollama pull deepseek-r1:14b` | **Thinking** | Linux GPU, Mac daily | Windows - ~8 GB at Q4 |
| 5 | **Qwen2.5 32B** | `ollama pull qwen2.5:32b` | General (heavy) | Linux CPU overnight, Mac Tier 2 | Windows - **16 GB RAM** ceiling |

**Linux + Mac coding pick:** **Qwen2.5-Coder 14B** - the one I'd open beside a WordPress staging tab. Multi-file theme work, `functions.php`, block patterns. **Qwen3 14B** handles code too, but the Coder build targets it.

**Linux + Mac thinking pick:** **DeepSeek-R1-Distill 14B** for step-by-step reasoning on both boxes with apps open. When I can close everything on the Mac (or run overnight on Linux), **DeepSeek-R1-Distill 32B** (`ollama pull deepseek-r1:32b`) is the hardest thinking I'd run locally before reaching for a cloud model.

**Dropped from this table:** **Qwen3 27B** - still a strong general Tier 2 pick, but for thinking I'd take **DeepSeek-R1-Distill 14B** at the same memory tier, and for coding **Qwen2.5-Coder 14B** beats it on client work.

**Linux + Windows** and **Mac + Windows** don't get their own lists. Every model that fits both laptops either already appears in the **all-three** table above, or it's **Bonsai** again. The G15 is always the gate.

**Practical rule:** one **all-three** model synced everywhere (I'd pick **Gemma 3 4B** for chat or **Qwen2.5-Coder 7B** for code), then specialist builds on Linux and Mac when I need more brain.

### Coding vs thinking - quick reference

| Job | All three machines | Linux + Mac only |
|-----|-------------------|------------------|
| **Coding** | **Qwen2.5-Coder 7B** | **Qwen2.5-Coder 14B** |
| **Thinking / reasoning** | **Bonsai 27B** (or **DeepSeek-R1-Distill 8B** for easy Ollama) | **DeepSeek-R1-Distill 14B** daily; **DeepSeek-R1-Distill 32B** when stretched |
| **General chat** | **Qwen3 8B** or **Gemma 3 4B** | **Qwen3 14B** |

**Coding** means generated code I'd paste into a repo - PHP, CSS, JS, shell, SQL. **Thinking** means multi-step logic, debugging a weird bug, or planning before I type. I don't confuse them: a general 14B model will write code, but the **Coder** distill wins on structure; a chat model will reason, but **R1-Distill** shows its work.

---

## Where each machine earns its keep

**MacBook** - interactive local AI while I'm working. Quick rewrites, summarizing a long doc, testing a prompt before it touches a client repo. If I need a response in seconds, this is the machine.

**Linux desktop** - bigger models I can run slowly in the background, local experiments that don't need to travel, and anything I'd rather not send upstream. It's also where **Brave Origin** and my always-on tabs already live, so I treat GPU inference as a bonus, not the main event.

**Windows laptop** - offline chat on the road, LM Studio when someone hands me a GGUF file, small-model tests before I pull the same build on the Mac. Tier 0 is the ceiling for daily use. **Bonsai** when I want a taste of Tier 2 without lugging the MacBook.

I still use cloud models for heavy client work. Local AI on these three boxes is a **privacy and offline cushion**, not a full replacement. Signal Coders' tier map plus conservative GPU numbers stopped me from downloading a Tier 2 32B file on the wrong machine and wondering why the fan spun for ten minutes before nothing happened.

**Check your own numbers before you trust a YouTube thumbnail:**

- **Linux** - sysfs GTT and VRAM carve-out:

```bash
cat /sys/class/drm/card*/device/mem_info_vram_total
cat /sys/class/drm/card*/device/mem_info_gtt_total
```

Divide by 1024 three times for gibibytes. Then shave off a few gigabytes for the OS and call that your real budget.

- **Windows** - Task Manager → Performance → GPU. Note **Dedicated GPU memory** (mine says **6 GB**) and **Memory** (mine says **16 GB**). If dedicated VRAM is under 8 GB, start at Tier 0 no matter what the CPU sticker says.

- **Mac** - Activity Monitor → Memory. You have one pool; plan **~16 GB** for the model with apps open, **~22 GB** if you close everything.
