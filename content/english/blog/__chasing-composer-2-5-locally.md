---
title: "Chasing a Local Cursor-Like IDE on a 24 GB MacBook"
meta_title: "Local Cursor-Like Coding on an M4 MacBook - What Fits"
description: "I want Cursor's IDE features with a local model on my M4. Composer won't fit, the 2 GB trick needs macOS 26, and oMLX runs on the Sequoia I already have."
social_media_intro: "I want Cursor's repo loop on a local model, not a cloud bill per sidebar question. Chasing that on a 24 GB M4 MacBook. Link in the comments."
slug: "chasing-composer-2-5-locally"
date: "2026-08-02T12:40:00Z"
image: "/images/image-template.jpg"
image_prompt: "MacBook Pro on desk, split screen with blurred code editor and local model terminal, external SSD, evening room light, no product logos, no readable text, photorealistic, focused solo dev mood"
categories: ["Technology", "AI"]
author: "JoRap"
tags: ["Local AI", "Cursor", "Composer", "MacBook", "Apple Silicon", "MLX", "oMLX", "Ollama", "LLM", "TurboFieldfare", "Gemma", "Qwen", "Cline", "Kilo Code", "OpenCode", "Flash-MoE"]
related_notes:
  - local-first-software
  - building-a-personal-api
level_depth: 4
featured: false
draft: true
---

I don't need Cursor the product. I need what Cursor *does* - chat that knows the repo, inline edits, an agent that reads files and shows a diff before it applies anything. Glad I can chase that loop on my MacBook Pro M4 instead of paying a cloud bill for every sidebar question.

Composer 2.5 is the first model that made that feel worth chasing offline. Then I watched [a video about running a 26B model in about 2 GB of RAM on Apple Silicon](https://www.youtube.com/watch?v=vHhephsP6vU) - TurboFieldfare streaming MoE experts from SSD - and the target shifted. Not "clone Composer." Get Cursor-like features in an IDE, with a local brain big enough to be useful.

I haven't installed anything yet. I ran the numbers and the OS requirements first, same habit as when I mapped [local AI across my three machines](/blog/local-ai-my-machines/). Good thing, because the thing that blocked the shiny option wasn't memory. It was the operating system I'm sitting on. The thing that unblocked a better option was reading one more requirements line.

---

## What I actually want from the IDE

Strip the brand. The features:

1. **Chat with the workspace** - `@file`, `@folder`, ask about the repo without pasting half of it.
2. **Inline edit** - select a block, describe the change, accept or reject the patch.
3. **Agent loop** - read, plan, edit multiple files, run a command, show diffs before apply.
4. **Autocomplete** - Tab-style next-line guesses, if I can get them without a cloud dependency.

Cursor bundles those tightly. VS Code plus Continue, Cline, Zed, OpenCursor, NativeCode - same shape, different polish. The point of this post is the *shape*, not the sticker on the window.

---

## Composer 2.5 is not the local target

Cursor's launch post: Composer 2.5 is continued pretraining plus reinforcement learning on Moonshot's **Kimi K2.5**. Third-party writeups put most of the remaining compute on Cursor's own post-training - the part that makes it feel like Composer inside the IDE, and the part you can't download.

Kimi K2.5 is open-weight - **1T total parameters, about 32B active per token**. At native INT4 the weights are still roughly **600 GB**. The friendliest community quants I found still want on the order of **240 GB** of combined memory. My M4 has **24 GB**, with about **16 GB** I'd trust for a model while Slack and a browser stay open.

So "run Composer locally" is a no. Open weights ≠ fits on a laptop. What Cursor added in RL is also the part you can't clone. I stopped treating Composer as the download target.

Cursor itself also fights a pure-local setup. Staff said BYOK requests route through Cursor's servers for prompt building, so `localhost` fails and you need a public HTTPS tunnel. Tab stays cloud-only either way. That alone is enough reason to look for an IDE that speaks to `localhost` natively.

---

## The idea I like: TurboFieldfare's 2 GB trick

[TurboFieldfare](https://github.com/drumih/turbo-fieldfare) is the thing in that video. Custom Swift + Metal runtime for one model: **Gemma 4 26B-A4B** (about **3.88B active** per token).

The trick is not magic compression. MoE means only a few experts run per token. TurboFieldfare keeps a shared core and the KV cache in RAM - about **2 GB** with a 4K cache - and **streams the experts from SSD** as the router picks them. The model is still ~**14.3 GB on disk**. Memory stops tracking "how big is the whole file."

Published numbers:

| Machine | Decode speed (rough) |
|---------|----------------------|
| 8 GB M2 MacBook Air | ~5-6 tok/s |
| 24 GB M5 Pro | ~31-35 tok/s |

My unit is an **M4 with 24 GB**. The 8 GB floor is fine - I have headroom to spare. Two gigabytes of resident model is exactly the kind of budget that leaves room for the IDE, the browser, and a client Slack workspace. That part of the pitch lands.

---

## The blocker isn't memory. It's my OS.

TurboFieldfare wants **macOS 26, Metal 4, Swift 6.2**. I'm on **Sequoia**, which is macOS 15. Apple skipped from 15 to 26 when it switched to year-based numbering, so Tahoe is the version I'd need and Sequoia is one whole generation short. Metal 4 shipped with Tahoe. There's no back-port.

That's a funny place to land. I spent the first hour of this assuming 24 GB was the wall, then a laptop that clears the RAM requirement three times over got stopped by a version string.

The upgrade is available to me - the M4 runs Tahoe fine. But this is the machine I bill client hours on, and I don't move a working machine to a new major OS in the middle of paid work to test a one-model inference runtime. My usual Apple rule is skip the first revision, and Tahoe is well past that at **26.6**, so the caution is scheduling, not stability. It's a "between projects" job, not a tonight job.

Other limits from the project itself, which matter before I plan that upgrade:

- **One model only** - Gemma 4 26B-A4B instruction-tuned. Not Qwen Coder, not a Composer clone.
- **Text only** - no vision, no audio.
- **No tool execution in the server** - tool calls come back to the client for you to authorize. Fine for a careful agent UI. Not a drop-in "do everything" daemon.
- **One model-owning process** - not a multi-tenant stack.

So the exciting number (2 GB) is real, and the question for me is whether an OS upgrade plus a single-model runtime is worth it for a general Gemma build in an agent loop. Not whether 24 GB can hold it.

---

## Path A: after I upgrade to Tahoe

Parked until the OS moves, then:

1. Install TurboFieldfare, pull the Gemma pack (~15 GB download, ~14.3 GB on disk).
2. Run its OpenAI-compatible server on `127.0.0.1`.
3. Point a local-first agent UI at that endpoint - Continue, Cline, Zed agent, OpenCursor, NativeCode - whatever speaks OpenAI chat completions on localhost without a tunnel.
4. Measure real tok/s on *this* M4 with Cursor-sized context, not the marketing table.

Expected ceiling: useful chat and careful multi-file edits when I'm offline or on a private repo. Not Composer 2.5's sustained agent behavior. Gemma 4 26B-A4B is a general instruction MoE, not a Cursor-trained coding specialist.

[NEEDS SCENE: after the Tahoe upgrade - what broke on install, what tok/s you actually saw]

---

## Path B: oMLX, which actually runs on Sequoia

This is the one I'd install tonight. [oMLX](https://github.com/jundot/omlx) is a macOS-native MLX inference server, Apache 2.0, managed from a menu bar app with a web dashboard and a CLI. Requirements: **macOS 15.0+ (Sequoia)**, Apple Silicon, arm64. I clear that. No upgrade, no waiting.

The reason it belongs in this post is not that it's another model runner. It's that it goes after the exact failure I was about to accept.

**Two-tier KV cache.** Hot context stays in RAM, older blocks spill to **SSD** - and they survive across requests and across restarts. Ollama and LM Studio hold KV state in memory, so when a coding agent shifts context mid-session, which happens constantly, the cache is invalidated and recomputed from scratch. oMLX restores it from disk. The project claims time-to-first-token drops from 30-90 seconds to under 5 on long contexts.

Same architectural instinct as TurboFieldfare, aimed at a different pool. TurboFieldfare streams *weights* from SSD. oMLX streams *context* from SSD. On a 24 GB machine, the KV cache is what actually eats me alive during a long agent loop, so the second trick may matter more than the first.

It also speaks both **OpenAI** (`/v1/chat/completions`) and **Anthropic** (`/v1/messages`) endpoints on localhost, with one-click config for Claude Code, OpenCode, Codex, and OpenClaw. That's the Cursor-like agent loop, pointed at my own machine, no tunnel.

Models to try on it, all standard MLX pulls. Two scores on every row:

- **Composer closeness** - my rough **/10** for how near the model gets to Composer 2.5's job (coding + multi-file agent loop + sustained tool use). Composer itself is 10. Nothing on this laptop is close to 10. Shape and training both count - a coding MoE scores higher than a general chat model of the same size.
- **~Memory** - **4-bit MLX weight size on Hugging Face** (sum of model files), before a long agent context grows. On my M4 I'd still plan around **~16 GB usable** with apps open. oMLX can spill KV cache to SSD; the weights still have to fit.

Sorted by **memory, low first**. Re-checked on Hugging Face: there is no **Qwen3-Coder 14B**. The real under-10 GB coder is **Qwen2.5-Coder-14B**. New finds that earned a row: **Gemma 4 12B Composer-aimed**, **DeepSeek-Coder-V2-Lite**, **Qwen2.5-Coder 32B**, **Nemotron 30B-A3B**, **Gemma 4 E4B**.

| Rank | Model | ~Memory | Composer /10 | Fit on 24 GB | MLX repo / notes |
|:----:|-------|---------|:------------:|--------------|------------------|
| 1 | **Qwen3.5-4B** | **~2.8 GB** | **1** | Easy | [`Qwen3.5-4B-4bit`](https://huggingface.co/mlx-community/Qwen3.5-4B-4bit). Always-on helper. Not an agent. |
| 2 | **Qwen2.5-Coder 7B** | **~4.0 GB** | **2** | Easy | [`Qwen2.5-Coder-7B-Instruct-4bit`](https://huggingface.co/mlx-community/Qwen2.5-Coder-7B-Instruct-4bit). Tab-style only. |
| 3 | **Gemma 4 E4B** | **~4.8 GB** | **2** | Easy | [`gemma-4-e4b-it-4bit`](https://huggingface.co/mlx-community/gemma-4-e4b-it-4bit). Tiny MoE. Snippets, not agents. |
| 4 | **Qwen3.5-9B** | **~5.5 GB** | **3** | Easy | [`Qwen3.5-9B-4bit`](https://huggingface.co/mlx-community/Qwen3.5-9B-4bit). Best general chat under 10 GB. |
| 5 | **Gemma 4 12B Composer-aimed** | **~6.2 GB** | **5** | Easy | [`gemma-4-12b-coder-fable5-composer2.5-4bit`](https://huggingface.co/mlx-community/gemma-4-12b-coder-fable5-composer2.5-4bit). Community fine-tune aimed at Composer 2.5. Worth a try under 10 GB - not Cursor's weights. |
| 6 | **Qwen2.5-Coder 14B** | **~7.7 GB** | **5** | Comfortable | [`Qwen2.5-Coder-14B-Instruct-4bit`](https://huggingface.co/mlx-community/Qwen2.5-Coder-14B-Instruct-4bit). Start line for agent work. |
| 7 | **DeepSeek-R1-Distill 14B** | **~7.7 GB** | **4** | Comfortable | [`DeepSeek-R1-Distill-Qwen-14B-4bit`](https://huggingface.co/mlx-community/DeepSeek-R1-Distill-Qwen-14B-4bit). Hard bugs, adjacent job. |
| 8 | **DeepSeek-Coder-V2-Lite** | **~8.2 GB** | **4** | Comfortable | [`DeepSeek-Coder-V2-Lite-Instruct-4bit-mlx`](https://huggingface.co/mlx-community/DeepSeek-Coder-V2-Lite-Instruct-4bit-mlx). Older coder MoE. Still under 10 GB. |
| 9 | **gpt-oss 20B** | **~11.3 GB** | **3** | Good | [`gpt-oss-20b-MXFP4-Q8`](https://huggingface.co/mlx-community/gpt-oss-20b-MXFP4-Q8). General MoE. Low Composer priority. |
| 10 | **Codestral 22B** | **~11.7 GB** | **2** | Good | [`Codestral-22B-v0.1-4bit`](https://huggingface.co/mlx-community/Codestral-22B-v0.1-4bit). Autocomplete, not an agent brain. |
| 11 | **Devstral Small 2 24B** | **~14.1 GB** | **6** | Good | [`Devstral-Small-2-24B-Instruct-2512-4bit`](https://huggingface.co/mlx-community/Devstral-Small-2-24B-Instruct-2512-4bit). Agent-tuned edit → test → fix. |
| 12 | **Gemma 4 26B-A4B** | **~14.3 GB** | **4** | OK / tight | [`gemma-4-26b-a4b-it-4bit`](https://huggingface.co/mlx-community/gemma-4-26b-a4b-it-4bit). Full MLX load - not TurboFieldfare's 2 GB trick. |
| 13 | **Qwen3.6-27B** | **~15.0 GB** | **5** | OK / tight | [`Qwen3.6-27B-4bit`](https://huggingface.co/mlx-community/Qwen3.6-27B-4bit). Strong dense coder. |
| 14 | **Qwen3-Coder 30B-A3B** | **~16.0 GB** | **7** | Tight | [`Qwen3-Coder-30B-A3B-Instruct-4bit`](https://huggingface.co/mlx-community/Qwen3-Coder-30B-A3B-Instruct-4bit). Best Composer-shaped stretch that might fit. |
| 15 | **Nemotron 30B-A3B** | **~16.6 GB** | **5** | Tight | [`NVIDIA-Nemotron-3-Nano-30B-A3B-4bit`](https://huggingface.co/mlx-community/NVIDIA-Nemotron-3-Nano-30B-A3B-4bit). Agentic MoE alternative to Qwen. |
| 16 | **Qwen2.5-Coder 32B** | **~17.2 GB** | **6** | Tight | [`Qwen2.5-Coder-32B-Instruct-4bit`](https://huggingface.co/mlx-community/Qwen2.5-Coder-32B-Instruct-4bit). Dense coder. Hungrier than the 14B for a modest jump. |
| 17 | **DeepSeek-R1-Distill 32B** | **~17.2 GB** | **4** | Tight | [`DeepSeek-R1-Distill-Qwen-32B-4bit`](https://huggingface.co/mlx-community/DeepSeek-R1-Distill-Qwen-32B-4bit). Bigger reasoner. Close everything else first. |
| 18 | **Qwen3.6-35B-A3B** | **~19.0 GB** | **7** | Very tight | [`Qwen3.6-35B-A3B-4bit`](https://huggingface.co/mlx-community/Qwen3.6-35B-A3B-4bit). Same idea as 30B MoE, newer and hungrier. |
| 19 | **Qwen3-Coder-Next** | **~41.8 GB** | **8** | No | [`Qwen3-Coder-Next-4bit`](https://huggingface.co/mlx-community/Qwen3-Coder-Next-4bit). Calibration only. Studio / Ultra. |

**Qwen3.5-122B** and the big **GLM / MiniMax** builds sit with Next in the "oMLX demos them; my 24 GB does not" bucket.

### What I'd actually try under 10 GB

The full table is the map. The useful cut for *tonight* is stricter: keep the model under **~10 GB** of weight so Slack, a browser, and the IDE still have air, and so a long agent context has somewhere to grow. oMLX can spill KV to SSD. It cannot shrink the weights.

**1. Qwen2.5-Coder 14B (~7.7 GB) via oMLX - or Rapid-MLX - plus Kilo Code or Cline.**

This is the start line. Coding-tuned, still under 10 GB, Composer **5**/10. Pull [`mlx-community/Qwen2.5-Coder-14B-Instruct-4bit`](https://huggingface.co/mlx-community/Qwen2.5-Coder-14B-Instruct-4bit). Wire it to a localhost-native agent UI that still feels like Cursor's panel - **Kilo Code or Cline** in VS Code (`http://localhost:8000/v1`). OpenCode is fine if I want a terminal TUI instead. Do not shove it into Cursor. Cursor still wants a public HTTPS tunnel for BYOK.

I'd grab oMLX's **Sequoia DMG** (`macos15-sequoia`, not the Tahoe one) so the Metal kernels arrive precompiled. Rapid-MLX is the peer runner if I want a second opinion on speed and prompt cache; same models, same OpenAI-shaped endpoint, different emphasis. The model choice matters more than which of those two serves it.

First test is boring on purpose: a Hugo layout tweak or a small PHP function in a real repo, with the agent allowed to read files and show a diff. If the 14B fails that, jumping to a 30B won't save me with benchmark points alone.

Interesting alt under 10 GB from the re-search: **Gemma 4 12B Composer-aimed** (~6.2 GB, also **5**/10). Community fine-tune, not Cursor. I'd try it second if the Qwen 14B baseline feels flat.

**2. Qwen3.5-9B (~5.5 GB) if I want more room for context and apps.**

Same night, different trade. Lower Composer score (**3**/10) - strong general model, not a dedicated coder - but it leaves more gigabytes for KV cache, Slack, and the dozen Chrome tabs I pretend I'm about to close. If the 14B feels fine in quality but the machine starts paging during a long agent loop, drop to the 9B before I start closing client apps.

**3. Keep a 4B or 7B loaded only if I want a second, always-on autocomplete model.**

Qwen3.5-4B (~2.8 GB) or Qwen2.5-Coder 7B (~4.0 GB) are Tab-style helpers, not the agent. Composer **1-2**/10. Useful if the agent UI can point chat/agent at the 14B and autocomplete at the small one. Useless if I try to make the 4B run a multi-file edit loop. One brain for the agent. One small model for next-line guesses, if I bother.

**4. Flash-MoE only if I'm willing to experiment for a bigger Qwen MoE without blowing the 10 GB RAM cap.**

This is the wild card, not the default. Projects like [Flash-MoE](https://github.com/tayoun/flash-moe) stream MoE *experts* from SSD the way TurboFieldfare does - so a Qwen 35B-class MoE can sit around **~6 GB resident** while most of the weights stay on disk. That is the Composer-*shape* chase under 10 GB without waiting for Tahoe. It is also early, model-specific, and the kind of thing that burns a weekend. I'd try it after the 14B baseline works, not instead of it.

### Stretch order above 10 GB

Only after the under-10 GB path proves the agent UI and the workflow: **Devstral (~14.1 GB, 6/10) → Qwen3-Coder 30B-A3B (~16.0 GB, 7/10) → Qwen2.5-Coder 32B or Nemotron 30B-A3B if curious → only then 35B-A3B (~19.0 GB, 7/10) with everything closed.** Those are "close Slack first" loads. They are not tonight.

One thing to keep straight: on a normal MLX or Ollama load, MoE does **not** give you TurboFieldfare's memory trick. All experts sit in unified memory. Sparse activation buys speed, not a smaller resident footprint. "MoE" on a download page is not the same promise as "streams experts from SSD."

Two honest caveats before I get excited. oMLX's own guidance says 16 GB minimum but **64 GB+ recommended**, with the sweet spot an M-series Pro or Max - I'm at 24 GB on a base M4, under their comfortable line. And the benchmark writeups are specific about where the win lives: oMLX does not beat plain `mlx-lm` on a warm in-memory repeat. It wins when the cache would otherwise be **lost**, across a restart or an eviction. That's still my situation - I close the laptop constantly - but it's a narrower claim than the marketing.

There's also a gotcha worth writing down: a plain `pip install -e .` does **not** build the native Metal kernels, and affected models silently fall back to a much slower path. Building them needs full Xcode, not just Command Line Tools. The official DMG ships them precompiled. That's exactly the kind of thing I'd have spent an evening blaming on my hardware.

### Which agent UI, ranked for Cursor shape

Scores are rough **/10 for how close the UI feels to Cursor** when the brain is on localhost - not model quality. Cursor itself is 10, but it fails pure `localhost`.

| Rank | Tool | Cursor /10 | Notes |
|:----:|------|:----------:|-------|
| 1 | **Kilo Code** | **8** | VS Code agent panel, diffs, tools, MCP. Closest "Cursor sidebar" feel. |
| 2 | **Cline** | **8** | Same band as Kilo - Plan/Act, approve each step, inline diffs. |
| 3 | **Zed Agent** | **7** | Native agent in a fast editor. Close shape, different IDE. |
| 4 | **OpenCursor** | **6** | Local-first Cursor-like extension. Younger / thinner. |
| 5 | **Claude Code → oMLX** | **6** | Strong agent via Anthropic `/v1/messages`. Terminal, not an IDE. |
| 6 | **OpenCode** | **5** | Excellent TUI agent. Capability yes, Cursor UI no. |
| 7 | **Continue** | **4** | Better as Tab/chat helper beside Cline than as the main agent. |
| 8 | **Aider** | **4** | Git-native terminal pair programmer. Not an IDE. |

I'd install **Kilo or Cline** first. OpenCode or Claude Code if I'm living in the terminal that night.

### Next steps after oMLX is up

Once the Sequoia DMG is installed and the menu bar server is running:

1. **Pull the model** - [`mlx-community/Qwen2.5-Coder-14B-Instruct-4bit`](https://huggingface.co/mlx-community/Qwen2.5-Coder-14B-Instruct-4bit) (~7.7 GB).
2. **Smoke-test in oMLX's own chat** - one coding question. If that fails, fix the server before touching an agent.
3. **Point Kilo Code at localhost** - not Cursor. In VS Code:

   1. Install the **Kilo Code** extension and open its **Settings** (gear).
   2. Go to **Providers** → scroll to the bottom → **Custom provider**.
   3. Fill in:
      - **Provider ID:** `omlx` (any unique id)
      - **Display name:** `oMLX`
      - **Provider API:** **OpenAI Compatible** (Chat Completions - not Responses, not Anthropic)
      - **Base URL:** `http://localhost:8000/v1`  
        (or `http://127.0.0.1:8000/v1` - same machine, no trailing path beyond `/v1`)
      - **API key:** any non-empty placeholder if the field requires one, e.g. `ollama` or `not-needed` (oMLX does not validate it)
   4. Confirm the model id oMLX is advertising:

      ```bash
      curl -s http://localhost:8000/v1/models
      ```

      Use that exact `id` string in Kilo (often the folder name, HF-style id, or an **alias** you set in oMLX). If auto-fetch works after Base URL + key, pick it from the list. If not, add the model id manually.
   5. Select that model in Kilo's model picker, open a repo, and run a small agent task with diffs/approvals on.

   Optional: in oMLX's admin panel, set a short **model alias** (e.g. `qwen-coder-14b`) so `/v1/models` and Kilo both show a clean name. Requests accept the alias or the directory name.

   **If connection fails:** oMLX menu bar server must be running; Base URL must be `/v1` not `/v1/chat/completions` unless Kilo asks for a full endpoint; model id must match `curl` output exactly. Docs: [OpenAI-compatible providers](https://kilo.ai/docs/ai-providers/openai-compatible).

   Cline is the same idea (OpenAI-compatible base URL + model id). Prefer Kilo or Cline for Cursor-shaped UX; OpenCode if you want a TUI instead.
4. **First real edit** - Hugo layout or small PHP change in a real repo, diffs before apply. That is the pass/fail, not a HumanEval screenshot.
5. **Only then tune** - machine pages → drop to Qwen3.5-9B or try the Gemma 12B Composer-aimed build. Chat works but tools are messy → check oMLX tool settings, or try Rapid-MLX later. Quality is fine and I want more → stretch table above 10 GB with apps closed.

Tonight's bar: **oMLX serving → Kilo/Cline connected → one real file edit with a visible diff.**

[NEEDS SCENE: after install - which agent UI, what tok/s, did the Hugo/PHP test land]

---

## What I'd give up either way

**Speed.** Cloud Composer is fast enough that I stop watching the stream. Local on an M4 is a fraction of that - more if the weights are resident and small, less if you're streaming experts from SSD. Community notes put TurboFieldfare on an M4 nearer the **~5 tok/s** M2 band than the M5 Pro table, so Path A is a measurement job, not a promised 30+.

**Long agent memory.** Composer markets 200K context and long tool loops. On 24 GB, KV cache fights the weights, and agentic coding is "read a lot of files" - exactly when local setups get ugly. oMLX's SSD cache tier is the best answer I found to this, and it's a real one, but spilling to disk raises the ceiling rather than removing it.

**The trained behavior.** Cursor spent most of Composer 2.5's compute on post-training for sustained tasks and instruction following. An open 14B or 26B without that RL is a different animal in a twenty-step loop. It can write the function. It may forget why it opened the third file.

---

## What I'd actually do

Stop trying to shove a local model into Cursor. Wrong product for a localhost brain.

Split the job:

- **Paid / hard client work** - stay on Cursor + Composer while it earns its keep.
- **Tonight, on Sequoia, under 10 GB** - oMLX Sequoia DMG → pull **Qwen2.5-Coder 14B** ([MLX 4-bit](https://huggingface.co/mlx-community/Qwen2.5-Coder-14B-Instruct-4bit)) → wire **Kilo Code or Cline** to `http://localhost:8000/v1` → one real Hugo/PHP edit with a diff. Optional second pull: the **Gemma 4 12B Composer-aimed** build. Fall back to **Qwen3.5-9B** if I need more headroom. Optional 4B/7B only for autocomplete. Flash-MoE later, if I want a bigger MoE without raising the RAM floor.
- **After the next Tahoe window** - try TurboFieldfare and see whether a 26B streaming its weights from SSD beats a 14B sitting in RAM with its context on SSD.

Both videos point at the same move from different ends: stop treating unified memory as the only place model data can live. TurboFieldfare pages **weights** off the SSD. oMLX pages **context** off the SSD. On a 24 GB laptop, that reframe does more for me than any benchmark table, and only one of the two needs an OS I don't have.

I went into this sure that 24 GB was the constraint. It wasn't. The first blocker was a version string in About This Mac, and the thing that got me unstuck was reading one more requirements line instead of assuming the newest tool was the only one. Glad that boring line was there. Check the OS and framework requirements before you budget RAM. They're faster to read and they fail harder.

Sources: [Introducing Composer 2.5](https://cursor.com/blog/composer-2-5) - Cursor. [Kimi-K2.5 model card](https://huggingface.co/moonshotai/Kimi-K2.5) - Moonshot AI. [TurboFieldfare](https://github.com/drumih/turbo-fieldfare) and [Local AI On Apple Silicon uses 7X Less RAM](https://www.youtube.com/watch?v=vHhephsP6vU). [oMLX](https://github.com/jundot/omlx) and [Finally, The CORRECT Way to Run Local AI on a Mac](https://www.youtube.com/watch?v=JpJaEPGzPF4). [Rapid-MLX](https://rapidmlx.com/). [Flash-MoE](https://github.com/tayoun/flash-moe). [Run a local LLM with Cursor?](https://forum.cursor.com/t/run-a-local-llm-model-with-cursor/156489/3) - Cursor forum.
