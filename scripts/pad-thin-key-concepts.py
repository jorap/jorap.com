#!/usr/bin/env python3
"""Add principle sentences to key_concept when shareable_lines cannot reach four."""

from __future__ import annotations

import sys
from pathlib import Path

import yaml

from notes_content import dump_frontmatter, split_frontmatter

ROOT = Path(__file__).resolve().parents[1]
NOTES = ROOT / "content/english/notes"

KEY_PAD: dict[str, str] = {
    "anti-fragile-systems.md": "Test backups while the app still works - not after the export dies.",
    "attention-to-detail.md": "Small misses compound into incidents when nobody catches them early.",
    "building-a-personal-api.md": "Frontmatter and folder shape are the contract between past me and future me.",
    "context-aware-capture.md": "Six weeks later, only the why saves a bookmark from becoming junk.",
    "create.md": (
        "One topic in, one atomic note out - same shape as the rest of the garden.\n\n"
        "The prompt picks an improvement principle, one standup-sized claim, then actionable examples."
    ),
    "decision-quality.md": "A choice that only looks good in the meeting room is not a quality decision.",
    "deliberate-practice.md": "Train the slice that breaks - not the part you already nail clean.",
    "discipline.md": "The feeling that started the habit will leave - the commitment stays.",
    "drafting-in-public.md": "Rough drafts in public beat polished drafts hoarded in private.",
    "eliminate-before-managing.md": "Remove the hazard before you buy another harness for it.",
    "ethical-leadership.md": "The team copies what you tolerate, not what you preach.",
    "finish-strong.md": "The last commitment closed is what makes the launch real.",
    "follow-their-lead.md": "Enter their frame before you try to redirect the conversation.",
    "getting-things-done.md": "Capture everything, clarify next actions, trust the weekly review.",
    "graph-view-analytics.md": "Orphan notes and over-linked hubs both signal a graph that needs pruning.",
    "habit-formation.md": "Autopilot beats re-deciding the same small move every morning.",
    "heed-every-near-miss.md": "Luck covering a near-miss is not proof the system works.",
    "intellectual-sourcing.md": "Without a source, six months later I won't trust my own synthesis.",
    "lean-startup.md": "Validate before you scale - polish comes after proof someone wants it.",
    "normalization-of-deviance.md": "The third shortcut without pushback is the warning, not the disaster.",
    "note-relationships.md": (
        "Extends builds on another note. Contradicts names the tradeoff. "
        "Implements makes it real. Alternative names another path."
    ),
    "okf-export.md": "Authoring stays in Hugo; OKF is the agent-readable pass-off copy.",
    "own-the-error.md": "Name the miss clearly so the team learns from it - not from blame theater.",
    "preparedness.md": "Practice the move slowly so you can run it when the clock is loud.",
    "reliability.md": "People stop chasing updates when you close loops without reminders.",
    "resilience.md": "Stay useful to the people counting on you after the hit lands.",
    "risk-management.md": "Likelihood times severity sets how strong the control needs to be.",
    "safety-by-design.md": "Make the dangerous move hard by default - not just forbidden on paper.",
    "situational-control.md": "Steer pace, agenda, and boundaries when you cannot own every outcome.",
    "slow-the-moment.md": "One deliberate breath buys room for a better second move.",
    "standard-operating-procedures.md": "Written steps beat improvisation when stress shrinks working memory.",
    "systems-for-growth.md": "Install the loops on ordinary Tuesdays - not only when results are due.",
    "the-second-brain-workflow.md": "Capture daily, organize by project, distill on reuse, express weekly.",
    "versatility.md": "Stay useful across roles, tools, and contexts when the team shifts.",
    "weekly-review-checklists.md": "The checklist should be boring on purpose - same steps every week.",
}

KEY_PAD_EXTRA: dict[str, str] = {
    "attention-to-detail.md": "Catch loose ends before they become customer-facing incidents.",
    "decision-quality.md": "Sleep on it, then check whether the choice still holds.",
    "getting-things-done.md": "The task inbox and the note garden are separate lanes - Allen owns tasks.",
    "graph-view-analytics.md": "Read the graph for orphans and over-linked hubs before they skew the garden.",
    "intellectual-sourcing.md": "A cited note is one I can defend in conversation months later.",
    "own-the-error.md": "Repair what broke, then fix the process that let it through.",
    "the-second-brain-workflow.md": "Express weekly closes the loop - capture and organize are not enough.",
    "weekly-review-checklists.md": "Skip the fancy template - repeat the same short list even on travel weeks.",
    "adaptability.md": "Same aim, different plan when the ground moves.",
    "analog-capture-tools.md": "Paper still goes in the same inbox when screens are off limits.",
    "blameless-after-action-review.md": "Fix the runbook after rollback - not the person who pushed deploy.",
    "great-commission.md": "Go, baptize, teach obedience - under Christ's authority, not recruitment zeal.",
    "process-over-outcomes.md": "Protect the routine you can rerun when motivation dips.",
    "ship-it.md": "Good enough shipped beats perfect still sitting in drafts.",
}

DESCRIPTION_FIX: dict[str, str] = {
    "weekly-review-checklists.md": "Weekly review works when the same short checklist runs every Sunday on purpose.",
}

KEY_REPLACE: dict[str, str] = {
    "weekly-review-checklists.md": (
        "The checklist should be boring on purpose.\n\n"
        "Same steps every week: empty inbox, scan calendar, check projects, pick one express action."
    ),
}


def main() -> int:
    changed = 0
    targets = set(KEY_PAD) | set(KEY_PAD_EXTRA) | set(KEY_REPLACE) | set(DESCRIPTION_FIX)
    for name in sorted(targets):
        path = NOTES / name
        if not path.exists():
            continue
        pad = KEY_PAD.get(name, "")
        text = path.read_text(encoding="utf-8")
        raw_fm, body = split_frontmatter(text)
        fm = yaml.safe_load(raw_fm) or {}
        if name in KEY_REPLACE:
            fm["key_concept"] = KEY_REPLACE[name]
        elif name == "create.md":
            fm["key_concept"] = pad
        else:
            existing = (fm.get("key_concept") or "").rstrip()
            if pad not in existing:
                fm["key_concept"] = f"{existing}\n\n{pad}" if existing else pad
        extra = KEY_PAD_EXTRA.get(name)
        if extra:
            existing = (fm.get("key_concept") or "").rstrip()
            if extra not in existing:
                fm["key_concept"] = f"{existing}\n\n{extra}" if existing else extra
        if name in DESCRIPTION_FIX:
            fm["description"] = DESCRIPTION_FIX[name]
        new_text = f"---\n{dump_frontmatter(fm)}\n---{body}"
        if new_text != text:
            path.write_text(new_text, encoding="utf-8")
            changed += 1
    print(f"Padded key_concept on {changed} note(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
