#!/usr/bin/env python3
"""Build grade-1-math-quiz in data/randomizer.yaml (200 items, answers 3–5 letters)."""
from __future__ import annotations

import re
from pathlib import Path
from typing import Literal

import yaml

ROOT = Path(__file__).resolve().parents[1]
YAML = ROOT / "data" / "randomizer.yaml"
COLLECTION_ID = "grade-1-math-quiz"

Difficulty = Literal["easy", "medium", "hard"]

WORDS: dict[int, str] = {
    0: "zero",
    1: "one",
    2: "two",
    3: "three",
    4: "four",
    5: "five",
    6: "six",
    7: "seven",
    8: "eight",
    9: "nine",
    10: "ten",
}

META = {
    "id": COLLECTION_ID,
    "title": "Grade 1 math quiz",
    "mode": "quiz",
    "tagline": "Addition, subtraction, and number bonds. Answers are 3 to 5 letters.",
    "play_hint": (
        "Read the question aloud. Let them guess before you reveal. "
        "Start with easy cards; hide one in a general quiz round when they are warmed up."
    ),
}


def w(n: int) -> str:
    return WORDS[n]


def valid_answer(answer: str) -> bool:
    a = answer.strip()
    return 3 <= len(a) <= 5 and a.isalpha()


def answer_leaks_in_question(question: str, answer: str) -> bool:
    a = answer.strip().lower()
    q_lower = question.lower()
    words = re.findall(r"[a-z]+", q_lower)
    if a in words:
        return True
    if a not in q_lower:
        return False
    return a != "hat" or q_lower.replace("what", "").find("hat") >= 0


def generate_pool() -> list[tuple[str, str, Difficulty]]:
    out: list[tuple[str, str, Difficulty]] = []
    seen: set[str] = set()

    def add(q: str, a: str, d: Difficulty) -> None:
        a = a.strip()
        if q in seen or not valid_answer(a) or answer_leaks_in_question(q, a):
            return
        seen.add(q)
        out.append((q, a, d))

    for a in range(0, 11):
        for b in range(0, 11):
            s = a + b
            if s <= 6:
                add(f"What is {w(a)} plus {w(b)}?", w(s), "easy")

    for a in range(1, 7):
        for b in range(0, a):
            add(f"What is {w(a)} minus {w(b)}?", w(a - b), "easy")

    for a in range(0, 11):
        for b in range(0, 11):
            s = a + b
            if 6 <= s <= 10:
                add(f"What is {w(a)} plus {w(b)}?", w(s), "medium")

    for a in range(1, 11):
        for b in range(0, a):
            d = a - b
            if d <= 10:
                add(f"What is {w(a)} minus {w(b)}?", w(d), "medium")

    for a in range(1, 10):
        for b in range(1, 10):
            s = a + b
            if s <= 10:
                add(f"{w(a).capitalize()} and {w(b)} together make what?", w(s), "medium")

    for total in range(3, 11):
        for part in range(1, total):
            add(f"What plus {w(part)} makes {w(total)}?", w(total - part), "hard")

    for n in range(2, 11):
        add(f"What is one less than {w(n)}?", w(n - 1), "hard")

    for a in range(7, 11):
        for b in range(2, 5):
            if a - b >= 3:
                add(f"Bonus round: {w(a)} minus {w(b)}?", w(a - b), "hard")

    for total in range(6, 11):
        for part in range(1, total):
            add(f"{w(part)} plus what makes {w(total)}?", w(total - part), "hard")

    for n in range(1, 6):
        if 2 * n <= 10:
            add(f"What is double {w(n)}?", w(2 * n), "hard")

    for n in range(2, 10):
        add(f"What is ten minus {w(n)}?", w(10 - n), "hard")

    for n in range(0, 9):
        add(f"What number comes after {w(n)}?", w(n + 1), "easy")

    for n in range(1, 10):
        add(f"What number comes before {w(n)}?", w(n - 1), "easy")

    for n in range(0, 10):
        add(f"What is one more than {w(n)}?", w(min(n + 1, 10)), "easy")

    return out


def pick_split(pool: list[tuple[str, str, Difficulty]]) -> list[tuple[str, str, Difficulty]]:
    by_d: dict[Difficulty, list[tuple[str, str, Difficulty]]] = {
        "easy": [],
        "medium": [],
        "hard": [],
    }
    for item in pool:
        by_d[item[2]].append(item)

    need = {"easy": 50, "medium": 100, "hard": 50}
    picked: list[tuple[str, str, Difficulty]] = []
    for d in ("easy", "medium", "hard"):
        bucket = by_d[d]
        if len(bucket) < need[d]:
            raise SystemExit(f"not enough {d} math questions: have {len(bucket)}, need {need[d]}")
        picked.extend(bucket[: need[d]])
    return picked


QUESTIONS = pick_split(generate_pool())


def validate(questions: list[tuple[str, str, Difficulty]]) -> None:
    if len(questions) != 200:
        raise SystemExit(f"expected 200 questions, got {len(questions)}")
    counts = {"easy": 0, "medium": 0, "hard": 0}
    seen_q: set[str] = set()
    for i, (q, a, d) in enumerate(questions, 1):
        counts[d] += 1
        if not valid_answer(a):
            raise SystemExit(f"#{i} bad answer: {q!r} → {a!r}")
        if answer_leaks_in_question(q, a):
            raise SystemExit(f"#{i} answer leaks: {q!r} → {a!r}")
        if q in seen_q:
            raise SystemExit(f"duplicate: {q!r}")
        seen_q.add(q)
    if counts != {"easy": 50, "medium": 100, "hard": 50}:
        raise SystemExit(f"bad split: {counts}")


def yaml_block() -> str:
    lines = [
        f"- id: {META['id']}",
        f"  title: {META['title']}",
        f"  mode: {META['mode']}",
        f"  tagline: {META['tagline']}",
        f"  play_hint: {META['play_hint']}",
        "  items:",
    ]
    for q, a, d in QUESTIONS:
        q_esc = q.replace('"', '\\"')
        lines.append(f'  - q: "{q_esc}"')
        lines.append(f"    a: {a.strip()}")
        lines.append(f"    d: {d}")
    return "\n".join(lines) + "\n"


def replace_collection() -> None:
    validate(QUESTIONS)
    text = YAML.read_text(encoding="utf-8")
    marker = f"- id: {COLLECTION_ID}"
    if marker in text:
        start = text.index(marker)
        rest = text[start + 1 :]
        nxt = rest.find("\n- id: ")
        text = text[:start] + (text[start + 1 + nxt :] if nxt >= 0 else text[:start])
    if not text.endswith("\n"):
        text += "\n"
    YAML.write_text(text + yaml_block(), encoding="utf-8")
    data = yaml.safe_load(YAML.read_text(encoding="utf-8"))
    col = next(c for c in data["collections"] if c["id"] == COLLECTION_ID)
    assert len(col["items"]) == 200
    print(f"Wrote {COLLECTION_ID} ({len(col['items'])} items) to {YAML}")


if __name__ == "__main__":
    replace_collection()
