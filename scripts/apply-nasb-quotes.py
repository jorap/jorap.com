#!/usr/bin/env python3
"""Apply NASB 1995 wording to direct scripture quotes in faith notes."""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NOTES = ROOT / "content" / "english" / "notes"
DATA = ROOT / "data" / "scripture-nasb1995.json"

# ponytail: one-shot migration map — old paraphrase → NASB 1995 (unique strings only)
REPLACEMENTS: list[tuple[str, str]] = [
    (
        "Where your treasure is, there your heart will be. (Matthew 6:19-21).",
        "for where your treasure is, there your heart will be also. (Matthew 6:19-21).",
    ),
    (
        "You're the light of the world, like a city on a hill. (Matthew 5:14-16).",
        "You are the light of the world. A city set on a hill cannot be hidden. (Matthew 5:14-16).",
    ),
    (
        "The greatest commandment Jesus named: love the Lord with all your heart, soul, mind, and strength (Matthew 22:37-38).",
        "Jesus named the great and foremost commandment: YOU SHALL LOVE THE LORD YOUR GOD WITH ALL YOUR HEART, AND WITH ALL YOUR SOUL, AND WITH ALL YOUR MIND (Matthew 22:37-38).",
    ),
    (
        "When a scribe asked which commandment was first, Jesus quoted Deuteronomy 6:5 - whole-person devotion",
        "When a scribe asked which commandment was first, Jesus quoted Deuteronomy 6:5: You shall love the LORD your God with all your heart and with all your soul and with all your might - whole-person devotion",
    ),
    (
        "Enter by the narrow gate - the road to life is hard and few find it; the broad road to destruction is easy and crowded (Matthew 7:13-14).",
        "Enter through the narrow gate; for the gate is wide and the way is broad that leads to destruction, and there are many who enter through it. For the gate is small and the way is narrow that leads to life, and there are few who find it. (Matthew 7:13-14).",
    ),
    (
        "The road to life is hard and few find it; the broad road to destruction is easy and crowded (Matthew 7:13-14).",
        "For the gate is small and the way is narrow that leads to life, and there are few who find it. (Matthew 7:13-14).",
    ),
    (
        "Worry can't add a single hour to life. (Matthew 6:25-34).",
        "And who of you by being worried can add a single hour to his life? (Matthew 6:27).",
    ),
    (
        "Don't conform to the world's pattern. Be transformed by renewing your mind. Then you can test and approve what God's will is - good, pleasing, perfect.",
        "And do not be conformed to this world, but be transformed by the renewing of your mind, so that you may prove what the will of God is, that which is good and acceptable and perfect.",
    ),
    (
        "Romans 12:2's outcome: then you can test and approve what God's will is - good, pleasing, perfect.",
        "Romans 12:2's outcome: so that you may prove what the will of God is, that which is good and acceptable and perfect.",
    ),
    (
        "The coin bore Caesar's image; give it back to him. (Matthew 22:21).",
        "Render to Caesar the things that are Caesar's. (Matthew 22:21).",
    ),
    (
        "Give, pray, and fast for the Father's eyes - not to be seen by people (Matthew 6:1-18).",
        "Beware of practicing your righteousness before men to be noticed by them. (Matthew 6:1). Give, pray, and fast for the Father who sees in secret (Matthew 6:1-18).",
    ),
    (
        "Jesus rejected the limit of \"eye for eye\" as a personal ethic for disciples. (Matthew 5:38-39).",
        "An eye for an eye, and a tooth for a tooth - but I say to you, do not resist an evil person; but whoever slaps you on your right cheek, turn the other to him also. (Matthew 5:38-39).",
    ),
    (
        "Jesus deepened the law against false vows: disciples should be so truthful that extra oaths aren't needed. (Matthew 5:33-37).",
        "let your statement be, 'Yes, yes' or 'No, no'; anything beyond these is of evil. (Matthew 5:33-37).",
    ),
    (
        "Anything beyond simple yes/no comes from evil",
        "anything beyond these is of evil",
    ),
    (
        "Both builders hear the sermon; only one obeys. (Matthew 7:24-27).",
        "everyone who hears these words of Mine and acts on them, may be compared to a wise man who built his house on the rock. (Matthew 7:24-27).",
    ),
    (
        "Empty \"Lord, Lord\" without doing the Father's will is the fool's house (Matthew 7:21-23).",
        "Not everyone who says to Me, 'Lord, Lord,' will enter the kingdom of heaven, but he who does the will of My Father who is in heaven will enter. (Matthew 7:21-23).",
    ),
    (
        "Paul says the builder \"will be saved, yet so as through fire\"",
        "If any man's work is burned up, he will suffer loss; but he himself will be saved, yet so as through fire",
    ),
    (
        "Love, joy, peace, patience, and the rest in Galatians 5. (Galatians 5:22-23).",
        "the fruit of the Spirit is love, joy, peace, patience, kindness, goodness, faithfulness, gentleness, self-control (Galatians 5:22-23).",
    ),
    (
        "One cluster the Spirit grows - love, joy, peace, patience, and the rest in Galatians 5. (Galatians 5:22-23).",
        "the fruit of the Spirit is love, joy, peace, patience, kindness, goodness, faithfulness, gentleness, self-control (Galatians 5:22-23).",
    ),
    (
        "**works of the flesh** (sexual immorality, jealousy, fits of anger, envy, and the rest in Galatians 5:19-21)",
        "**works of the flesh** (immorality, impurity, sensuality, idolatry, sorcery, enmities, strife, jealousy, outbursts of anger, disputes, dissensions, factions, envying, drunkenness, carousing - Galatians 5:19-21)",
    ),
    (
        "[[Grace]] is a gift I never earned - unmerited favor (Ephesians 2:8-9; John 3:16; Romans 4:5).",
        "For by grace you have been saved through faith; and that not of yourselves, it is the gift of God; not as a result of works, so that no one may boast. (Ephesians 2:8-9). Faith credited as righteousness for the one who believes (Romans 4:5).",
    ),
    (
        "Ephesians 2:10 keeps the order straight: saved by grace through faith first, then created in Christ Jesus for good works.",
        "For we are His workmanship, created in Christ Jesus for good works, which God prepared beforehand so that we would walk in them. (Ephesians 2:10).",
    ),
    (
        "Same rescue, two angles - rich in mercy, saved by grace (Ephesians 2:4-5).",
        "But God, being rich in mercy, because of His great love with which He loved us, even when we were dead in our transgressions, made us alive together with Christ (by grace you have been saved). (Ephesians 2:4-5).",
    ),
    (
        "God declares me righteous through faith in Christ alone - once, at faith, before my obedience catches up (Romans 3:24, 4:5, 5:1).",
        "being justified as a gift by His grace through the redemption which is in Christ Jesus (Romans 3:24). Faith credited as righteousness (Romans 4:5). Therefore, having been justified by faith, we have peace with God through our Lord Jesus Christ (Romans 5:1).",
    ),
    (
        "Once, at faith, before my obedience catches up (Romans 3:24, 4:5, 5:1).",
        "Therefore, having been justified by faith, we have peace with God through our Lord Jesus Christ (Romans 5:1).",
    ),
    (
        "Romans 8:29 names the aim - conformed to the image of His Son.",
        "Romans 8:29 names the aim - to become conformed to the image of His Son.",
    ),
    (
        "Romans 12:2 opens with don't conform to this world's pattern.",
        "And do not be conformed to this world (Romans 12:2).",
    ),
    (
        "be transformed by renewing your mind",
        "be transformed by the renewing of your mind",
    ),
    (
        "Don't conform to this world's pattern - refuse before renewal reshapes the mind.",
        "And do not be conformed to this world - refuse before renewal reshapes the mind.",
    ),
    (
        "Seventy times seven ends the ledger-keeping.",
        "up to seventy times seven (Matthew 18:22) ends the ledger-keeping.",
    ),
    (
        "Jesus overturned the tribal reading of \"neighbor.\" Loving only people who love you back is ordinary; loving enemies is divine-shaped. (Matthew 5:44-45).",
        "love your enemies and pray for those who persecute you. (Matthew 5:44-45). Loving only people who love you back is ordinary; loving enemies is divine-shaped.",
    ),
    (
        "Bless, pray, reflect the Father who sends rain on just and unjust alike.",
        "love your enemies and pray for those who persecute you - He causes His sun to rise on the evil and the good, and sends rain on the righteous and the unrighteous (Matthew 5:44-45).",
    ),
    (
        "It's positive and active: *do* unto others, not merely avoid doing harm. (Matthew 7:12).",
        "In everything, therefore, treat people the same way you want them to treat you, for this is the Law and the Prophets. (Matthew 7:12).",
    ),
    (
        "It's positive and active: do unto others, not merely avoid doing harm. (Matthew 7:12).",
        "In everything, therefore, treat people the same way you want them to treat you, for this is the Law and the Prophets. (Matthew 7:12).",
    ),
    (
        "Jesus pairs this with Judge Not: don't condemn souls, but do evaluate fruit. (Matthew 7:16-20).",
        "You will know them by their fruits. (Matthew 7:16-20). Jesus pairs this with Judge Not: don't condemn souls, but do evaluate fruit.",
    ),
    (
        "Jesus forbids harsh, hypocritical condemnation… (Matthew 7:1-5).",
        "Do not judge so that you will not be judged. (Matthew 7:1-5).",
    ),
    (
        "Peacemaking is work: reconciliation, truth spoken in love, de-escalation… (Matthew 5:9).",
        "Blessed are the peacemakers, for they shall be called sons of God. (Matthew 5:9). Peacemaking is work: reconciliation, truth spoken in love, de-escalation.",
    ),
    (
        "The Beatitudes bless the meek - strength without grasping for status.",
        "Blessed are the gentle, for they shall inherit the earth (Matthew 5:5) - strength without grasping for status.",
    ),
    (
        "Meek inherit the earth - strength without grasping for status.",
        "Blessed are the gentle, for they shall inherit the earth (Matthew 5:5) - strength without grasping for status.",
    ),
    (
        "Merciful obtain mercy - kindness Jesus blessed.",
        "Blessed are the merciful, for they shall receive mercy (Matthew 5:7) - kindness Jesus blessed.",
    ),
    (
        "Mission flows from resurrection authority, not human recruitment zeal. (Matthew 28:19-20).",
        "Go therefore and make disciples of all the nations, baptizing them in the name of the Father and the Son and the Holy Spirit, teaching them to observe all that I commanded you; and lo, I am with you always, even to the end of the age. (Matthew 28:19-20).",
    ),
    (
        "He washed feet the night before the cross. (Matthew 23:12, Mark 10:43-45).",
        "For even the Son of Man did not come to be served, but to serve, and to give His life a ransom for many. (Mark 10:45).",
    ),
    (
        "The Son of Man came to serve, not be served.",
        "For even the Son of Man did not come to be served, but to serve, and to give His life a ransom for many (Mark 10:45).",
    ),
    (
        "Jesus elevates restored relationship over religious performance. (Matthew 5:23-24).",
        "leave your offering there before the altar and go; first be reconciled to your brother, and then come and present your offering. (Matthew 5:23-24).",
    ),
    (
        "If your brother has something against you, go reconcile first - then come offer your gift.",
        "first be reconciled to your brother, and then come and present your offering (Matthew 5:23-24).",
    ),
    (
        "The test isn't whether I believe God should be first - it's what actually gets my first ten minutes of the day (Matthew 6:33).",
        "seek first His kingdom and His righteousness, and all these things will be added to you (Matthew 6:33) - the test is what actually gets my first ten minutes of the day.",
    ),
    (
        "Anger is murder, lust is adultery, in the heart.",
        "everyone who is angry with his brother shall be guilty before the court; everyone who looks at a woman with lust for her has already committed adultery with her in his heart (Matthew 5:22, 28).",
    ),
    (
        "\"Poor in spirit\" is bankruptcy before God, receiving the kingdom as gift rather than wage.",
        "Blessed are the poor in spirit, for theirs is the kingdom of heaven (Matthew 5:3) - bankruptcy before God, receiving the kingdom as gift rather than wage.",
    ),
    (
        "good, pleasing, perfect",
        "good and acceptable and perfect",
    ),
    (
        "Test His will - good, pleasing, perfect.",
        "Prove His will - good and acceptable and perfect.",
    ),
    (
        "Mind renewal lets me discern God's will - good, pleasing, perfect.",
        "Mind renewal lets me prove what the will of God is - good and acceptable and perfect.",
    ),
]


def apply() -> int:
    changed = 0
    for path in sorted(NOTES.glob("*.md")):
        text = path.read_text(encoding="utf-8")
        orig = text
        for old, new in REPLACEMENTS:
            text = text.replace(old, new)
        if text != orig:
            path.write_text(text, encoding="utf-8")
            changed += 1
            print(f"updated {path.name}")
    return changed


def self_check() -> None:
    import json

    data = json.loads(DATA.read_text(encoding="utf-8"))
    assert len(data["verses"]) >= 40
    # spot-check a migrated note
    treasure = (NOTES / "treasure-in-heaven.md").read_text(encoding="utf-8")
    assert "there your heart will be also" in treasure
    renewed = (NOTES / "renewed-mind.md").read_text(encoding="utf-8")
    assert "do not be conformed to this world" in renewed.lower()


if __name__ == "__main__":
    n = apply()
    self_check()
    print(f"Done — {n} note(s) updated")
