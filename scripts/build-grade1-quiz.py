#!/usr/bin/env python3
"""Build or refresh grade-1 quiz in data/randomizer.yaml (200 items, answers 3–5 chars)."""
from __future__ import annotations

import re
from pathlib import Path
from typing import Literal

import yaml

ROOT = Path(__file__).resolve().parents[1]
YAML = ROOT / "data" / "randomizer.yaml"
COLLECTION_ID = "grade-1-quiz"

Difficulty = Literal["easy", "medium", "hard"]

# 25% easy · 50% medium · 25% hard — answers are full grade-1 words (3–5 letters).
EASY: list[tuple[str, str]] = [
    ("What animal says meow?", "cat"),
    ("What animal says woof?", "dog"),
    ("What animal says moo?", "cow"),
    ("What animal says oink?", "pig"),
    ("What animal says quack?", "duck"),
    ("What animal says baa?", "sheep"),
    ("What animal says neigh?", "horse"),
    ("What animal says ribbit?", "frog"),
    ("What animal says hoot?", "owl"),
    ("What animal says buzz?", "bee"),
    ("What animal says cluck?", "hen"),
    ("What color is grass?", "green"),
    ("What color is the sky on a clear day?", "blue"),
    ("What color is snow?", "white"),
    ("What color is a ripe strawberry?", "red"),
    ("What star gives us light and heat?", "sun"),
    ("What do you see in the sky at night?", "moon"),
    ("What do you drink when you are thirsty?", "water"),
    ("What sweet food do bees make?", "honey"),
    ("What do hens lay?", "eggs"),
    ("What is water when it is frozen?", "ice"),
    ("What body part do you see with?", "eyes"),
    ("What body part do you hear with?", "ears"),
    ("What body part do you smell with?", "nose"),
    ("What is at the end of your arm?", "hand"),
    ("What is at the end of your leg?", "foot"),
    ("What do you sleep on?", "bed"),
    ("What do you sit on?", "chair"),
    ("What do you wear on your feet?", "shoes"),
    ("What do you wear on your head?", "hat"),
    ("What is one plus one?", "two"),
    ("What is two plus two?", "four"),
    ("What is the opposite of hot?", "cold"),
    ("What is the opposite of big?", "small"),
    ("What is the opposite of up?", "down"),
    ("What is the opposite of day?", "night"),
    ("What is the opposite of happy?", "sad"),
    ("What do you call a very young child?", "baby"),
    ("What round toy do you throw?", "ball"),
    ("What do you kick a ball with?", "foot"),
    ("What wags on a happy dog?", "tail"),
    ("What do you read stories in?", "book"),
    ("What big yellow ride takes you to school?", "bus"),
    ("What sweet treat do kids lick?", "candy"),
    ("What white drink comes from cows?", "milk"),
    ("What red fruit is crunchy?", "apple"),
    ("What do you open to go inside?", "door"),
    ("What do you drink from?", "cup"),
    ("How many fingers are on one hand?", "five"),
    ("Where do fish live?", "water"),
]

MEDIUM: list[tuple[str, str]] = [
    ("What falls from gray clouds in the sky?", "rain"),
    ("What white flakes fall when it is cold?", "snow"),
    ("What body part do you taste with?", "mouth"),
    ("What hard white things chew food?", "teeth"),
    ("What covers your whole body?", "skin"),
    ("What beats inside your chest?", "heart"),
    ("What grows on top of your head?", "hair"),
    ("How many toes are on one foot?", "five"),
    ("What do you eat soup from?", "bowl"),
    ("What do you write with?", "pen"),
    ("What do you cook in on the stove?", "pan"),
    ("What bakes food in the kitchen?", "oven"),
    ("What do you wash your hands with?", "soap"),
    ("What do you dry off with?", "towel"),
    ("What white food comes from a hen?", "egg"),
    ("What sweet stuff do you put on bread?", "jam"),
    ("What do you eat for breakfast with butter?", "toast"),
    ("What veggie makes you cry when you cut it?", "onion"),
    ("What do you use to cut food?", "knife"),
    ("What do you use to make a sandwich?", "bread"),
    ("What do you stir soup with?", "spoon"),
    ("What is two plus one?", "three"),
    ("What is three plus two?", "five"),
    ("What is four plus two?", "six"),
    ("What is five plus five?", "ten"),
    ("What number comes right after one?", "two"),
    ("What number comes right after four?", "five"),
    ("What number comes right before three?", "two"),
    ("What do birds use to fly?", "wings"),
    ("What do you find at the beach?", "sand"),
    ("What toy do you fly when it is windy?", "kite"),
    ("What do plants grow from?", "seed"),
    ("What is hot and can burn wood?", "fire"),
    ("What has four wheels and drives on roads?", "car"),
    ("What floats on water?", "boat"),
    ("What rides on tracks and says choo-choo?", "train"),
    ("Where do you see animals in cages?", "zoo"),
    ("What is the opposite of fast?", "slow"),
    ("What is the opposite of open?", "shut"),
    ("What is the opposite of wet?", "dry"),
    ("What is the opposite of old?", "new"),
    ("What is the opposite of loud?", "soft"),
    ("What is the opposite of dark?", "light"),
    ("What do you call a friend you play with?", "buddy"),
    ("What are children your age called?", "kids"),
    ("What do you bang with sticks?", "drum"),
    ("What do you use to unlock a door?", "key"),
    ("What does a key open?", "lock"),
    ("What do you tie on your shoes?", "bow"),
    ("What do you use to call people?", "phone"),
    ("What big animal loves honey?", "bear"),
    ("What yellow fruit is very sour?", "lemon"),
    ("What yellow kernels do you eat?", "corn"),
    ("What sweet food has candles on birthdays?", "cake"),
    ("What round dessert is cut in slices?", "pie"),
    ("What soft round bread do you eat?", "bun"),
    ("What green veggie is long and skinny?", "bean"),
    ("What fuzzy yellow baby bird says peep?", "chick"),
    ("Where do you put garbage?", "trash"),
    ("What warm things go on your feet?", "socks"),
    ("What covers you in bed?", "sheet"),
    ("What do you use on messy hair?", "comb"),
    ("What gives light in your room?", "lamp"),
    ("What do you sweep the floor with?", "broom"),
    ("What do we breathe?", "air"),
    ("What toy spins fast on the ground?", "top"),
    ("What loud sound comes with thunder?", "boom"),
    ("What white puff is in the sky?", "cloud"),
    ("What tall plant has a trunk?", "tree"),
    ("What green plant covers the ground?", "grass"),
    ("What shines in the sky at night?", "star"),
    ("How many legs does a dog have?", "four"),
    ("How many eyes do most people have?", "two"),
    ("How many ears do most people have?", "two"),
    ("How many wheels does a bike have?", "two"),
    ("How many fingers are on two hands?", "ten"),
    ("What drink comes from oranges?", "juice"),
    ("What short sleep do you take in the day?", "nap"),
    ("What do bunnies do when they go?", "hop"),
    ("What pet swims and blows bubbles?", "fish"),
    ("What do birds make in trees?", "nest"),
    ("What is a baby dog called?", "puppy"),
    ("What is a baby sheep called?", "lamb"),
    ("What is a baby cow called?", "calf"),
    ("What animal has a bushy tail and red fur?", "fox"),
    ("What insect wiggles in garden soil?", "worm"),
    ("What black bird says caw?", "crow"),
    ("What color is chocolate?", "brown"),
    ("What tells you the time?", "clock"),
    ("What meal do you eat at noon?", "lunch"),
    ("What do you sit on and pump your legs?", "swing"),
    ("What sea animal has big claws?", "crab"),
    ("What long animal has no legs?", "snake"),
    ("What dry grass do farm animals eat?", "hay"),
    ("What moves sand at the beach?", "scoop"),
    ("What rubber shoes do you wear in puddles?", "boots"),
    ("What big white bird swims in water?", "swan"),
    ("How many legs does a table have?", "four"),
    ("What color is a stop sign?", "red"),
    ("What helps plants grow from the sky?", "sun"),
]

HARD: list[tuple[str, str]] = [
    ("What big cat has a mane?", "lion"),
    ("What animal has black and white stripes?", "zebra"),
    ("What desert animal has one hump?", "camel"),
    ("What big cat has orange and black stripes?", "tiger"),
    ("What animal carries its house on its back?", "snail"),
    ("What bear is black and white?", "panda"),
    ("What big sea fish has sharp teeth?", "shark"),
    ("What animal flies at night and hangs upside down?", "bat"),
    ("What tiny insect lifts heavy things?", "ant"),
    ("What color is a dark piece of coal?", "black"),
    ("What color is a flamingo?", "pink"),
    ("What color is a fire truck?", "red"),
    ("What green part is on a tree?", "leaf"),
    ("What long water flows to the sea?", "river"),
    ("What is a little lake?", "pond"),
    ("What is seven minus two?", "five"),
    ("What is eight minus five?", "three"),
    ("What is nine minus four?", "five"),
    ("What is eight minus three?", "five"),
    ("How many days are in one week?", "seven"),
    ("How many sides does a triangle have?", "three"),
    ("How many corners does a square have?", "four"),
    ("How many wheels does a tricycle have?", "three"),
    ("How many sides does a square have?", "four"),
    ("What paper in class shows the weather?", "chart"),
    ("What helps you measure how long things are?", "ruler"),
    ("What pin holds paper on a corkboard?", "tack"),
    ("What sticky stuff holds paper?", "glue"),
    ("What do teachers write with on a board?", "chalk"),
    ("What has black and white keys you press?", "piano"),
    ("What shows roads and places?", "map"),
    ("What home do bees live in?", "hive"),
    ("What does a horse pull on a farm?", "cart"),
    ("What big boat sails on the ocean?", "ship"),
    ("Where do you buy milk and eggs?", "shop"),
    ("Who is your mother's sister?", "aunt"),
    ("Who is your father's brother?", "uncle"),
    ("What bird flies in a V?", "goose"),
    ("What white grains do many people eat?", "rice"),
    ("What white and yellow flower grows in grass?", "daisy"),
    ("What do library books sit on?", "shelf"),
    ("How many arms does an octopus have?", "eight"),
    ("What planet do we live on?", "earth"),
    ("How many legs does an insect have?", "six"),
    ("How many legs does a spider have?", "eight"),
    ("How many sides does a star have?", "five"),
    ("How many seasons are in one year?", "four"),
    ("How many planets go around the sun?", "eight"),
    ("What in your head helps you think?", "brain"),
    ("How many corners does a circle have?", "none"),
]

META = {
    "id": COLLECTION_ID,
    "title": "Grade 1 quick quiz",
    "mode": "quiz",
    "tagline": "Short questions for first graders. Every answer is 3 to 5 letters.",
    "play_hint": (
        "Read the question aloud. Let them guess before you reveal the answer. "
        "Tap Shuffle for a random question — about half are medium, a quarter easy, a quarter hard."
    ),
}


def build_questions() -> list[tuple[str, str, Difficulty]]:
    out: list[tuple[str, str, Difficulty]] = []
    for q, a in EASY:
        out.append((q, a, "easy"))
    for q, a in MEDIUM:
        out.append((q, a, "medium"))
    for q, a in HARD:
        out.append((q, a, "hard"))
    return out


QUESTIONS = build_questions()


def valid_answer(answer: str) -> bool:
    a = answer.strip()
    return 3 <= len(a) <= 5 and a.isalpha()


def answer_leaks_in_question(question: str, answer: str) -> bool:
    """True when the answer word appears inside the question text."""
    a = answer.strip().lower()
    q_lower = question.lower()
    words = re.findall(r"[a-z]+", q_lower)
    if a in words:
        return True
    if a not in q_lower:
        return False
    # ponytail: ignore the only common false positive — "hat" inside "what"
    return a != "hat" or q_lower.replace("what", "").find("hat") >= 0


def validate(questions: list[tuple[str, str, Difficulty]]) -> None:
    if len(questions) != 200:
        raise SystemExit(f"expected 200 questions, got {len(questions)}")
    counts = {"easy": 0, "medium": 0, "hard": 0}
    seen_q: set[str] = set()
    for i, (q, a, d) in enumerate(questions, 1):
        a = a.strip()
        counts[d] += 1
        if not valid_answer(a):
            raise SystemExit(f"#{i} bad answer ({len(a)} chars): {q!r} → {a!r}")
        if answer_leaks_in_question(q, a):
            raise SystemExit(f"#{i} answer leaks in question: {q!r} → {a!r}")
        if q in seen_q:
            raise SystemExit(f"duplicate question: {q!r}")
        seen_q.add(q)
    if counts["easy"] != 50 or counts["medium"] != 100 or counts["hard"] != 50:
        raise SystemExit(f"bad difficulty split: {counts} (want 50 easy, 100 medium, 50 hard)")


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
        text = text[: text.index(marker)]
    if not text.endswith("\n"):
        text += "\n"
    YAML.write_text(text + yaml_block(), encoding="utf-8")
    data = yaml.safe_load(YAML.read_text(encoding="utf-8"))
    col = next(c for c in data["collections"] if c["id"] == COLLECTION_ID)
    assert len(col["items"]) == 200
    print(f"Wrote {COLLECTION_ID} ({len(col['items'])} items) to {YAML}")


if __name__ == "__main__":
    replace_collection()
