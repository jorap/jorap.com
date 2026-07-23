#!/usr/bin/env python3
"""Apply wider-spread Level 1-5 rewrites to batch-2 garden notes."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NOTES = ROOT / "content" / "english" / "notes"

LEVELS: dict[str, list[str]] = {
    "glorify-your-name": [
        "Level 1: Jesus prayed that God would look good through the hard thing ahead - not that He could skip it.",
        "Level 2: Like a runner who wants the coach honored at the finish line - not an exit ramp before the race ends.",
        "Level 3: When the costly hour arrives, glorifying the Father's name outweighs escape - obedience shows His glory, comfort does not.",
        "Level 4: When the hard hour arrives, pray that God is honored through your obedience - not that you can skip the cup.",
        "Level 5: [[Not My Will]] repeats the same surrender in Gethsemane; under [[Free Grace]] the cross is where the Father's name shines - not where you bargain out of cost.",
    ],
    "god-centered-design": [
        "Level 1: Do good so people thank God - like sharing lunch so others praise the cook, not clap for you.",
        "Level 2: Build and serve so people see God behind the work - like a sign that points to the source, not your face on the poster.",
        "Level 3: Visible good works aim glory upward - when the crowd applauds you instead of the Father, the design drifted off course.",
        "Level 4: Before you publish or plan, ask whether the work makes the Father visible - not whether it builds your name.",
        "Level 5: [[Seek the Kingdom First]] is the priority filter; [[Love Your Neighbor]] keeps it from becoming selfish spirituality.",
    ],
    "golden-rule-at-work": [
        "Level 1: Help coworkers the way you want help - step in, do not just stay out of the way.",
        "Level 2: The golden rule is active - do the helpful thing you would want done for you, like holding a door you would want held.",
        "Level 3: Passive fairness leaves people stuck - because you would want someone to act for you, the rule pushes you to act.",
        "Level 4: At work, ask what you would want if roles flipped - then do that helpful move instead of only keeping your head down.",
        "Level 5: [[The Golden Rule]] is the spine; at work it means stepping in on the tedious task, not just refusing to make things worse.",
    ],
    "goodness": [
        "Level 1: Goodness is doing the right thing so people think of God - like helping quietly so others thank Him.",
        "Level 2: Goodness is outward integrity that points people toward God - like a flashlight aimed at the sky, not at your own name tag.",
        "Level 3: Fruits of the Spirit pairs goodness with kindness - when goodness becomes a personal brand, the fruit rots into performance.",
        "Level 4: Do the right thing in a way that makes people notice God behind it - not your resume line.",
        "Level 5: [[Kindness]] is the soft strength beside goodness; [[Fruits of the Spirit]] keeps both aimed at others, not a nice-guy pose.",
    ],
    "grace": [
        "Level 1: God gives salvation free when you trust Him - like a prize you never earned by being best.",
        "Level 2: Salvation is a gift through belief - not a scoreboard of good deeds stacked high enough to win.",
        "Level 3: God gave His Son so belief decides eternal life - merit never earned the ticket; unbelief is the only rejection.",
        "Level 4: Receive eternal life by trusting Christ's promise - not by climbing a moral ladder you could never finish.",
        "Level 5: [[Mercy]] withholds what you deserve; [[Free Grace]] is grace applied to eternal life by faith alone - not wages you stacked.",
    ],
    "graph-view-analytics": [
        "Level 1: Check your notes map for lonely pages and pages with too many links - like toys nobody plays with and one everyone fights over.",
        "Level 2: Read the link map for orphan notes and over-linked hubs - like a city map showing dead streets and one overcrowded intersection.",
        "Level 3: Orphans and over-linked hubs skew the whole garden - spot them early or maintenance chases symptoms instead of causes.",
        "Level 4: Open the graph view and fix orphan notes and overloaded hubs before they distort how you navigate the garden.",
        "Level 5: [[Graph]] is the live map; [[Issues]] is where you fix what the analytics flagged - not vanity link counts.",
    ],
    "graph": [
        "Level 1: Find notes that connect everything, notes nobody links to, and notes that link to nothing - then fix those, not count links for fun.",
        "Level 2: The graph shows hubs, orphans, and dead-end notes - maintenance targets, like a map that marks crowded junctions and forgotten streets.",
        "Level 3: When one note collects every wikilink, navigation skews; when a note has zero inbound links, it rots unseen in the garden.",
        "Level 4: Open [/notes/graph/](/notes/graph/) and prune around top hubs, rescue orphans, and add body links where notes are dead ends.",
        "Level 5: Top twenty percent by wikilinks are anchors worth pruning around - bottom twenty percent and zero body links are where you spend maintenance time.",
    ],
    "grateful-obedience": [
        "Level 1: You obey God because you are already saved and grateful - like saying thank you with chores, not to buy your way in.",
        "Level 2: Obedience follows salvation as thanks - like a thank-you note after a gift, not payment to earn the gift.",
        "Level 3: Love shows up as keeping His commands - when obedience tries to buy standing, grace gets traded for wages.",
        "Level 4: Obey because grace already saved you - gratitude keeps commands from turning into a merit ladder.",
        "Level 5: [[Free Grace]] settled eternal life at faith; grateful obedience is the walk after - not the ticket in.",
    ],
    "great-commission": [
        "Level 1: Jesus told followers to go everywhere, welcome new believers, and teach them His way - with His power helping, not just to win arguments.",
        "Level 2: Go, baptize, teach obedience - like sending trained workers into every town, not just collecting names on a list.",
        "Level 3: The commission is make disciples, not collect debates - baptism and teaching obedience follow going, or the mission stalls at arrival.",
        "Level 4: Go where people are, welcome believers, and teach them to obey - under Christ's authority, not recruitment zeal.",
        "Level 5: [[Discipleship]] is the long obedience; [[Invest in the Few]] matches depth before scale - not chasing crowds without teaching.",
    ],
    "growth-mindset": [
        "Level 1: Missing three shots is counting what happened - saying you are bad at basketball sounds like you can never improve.",
        "Level 2: I am bad at this is a fixed label; I missed three is data you can train on - like a score sheet versus a name tag.",
        "Level 3: When one rough outing becomes identity, you stop collecting reps - mistakes stay verdicts instead of feedback you could use.",
        "Level 4: Replace I am bad at this with I missed three - then train the slice that broke.",
        "Level 5: [[Failure as Feedback]] only works when skill is trainable; [[Deliberate Practice]] is what you do with the data instead of fixing the ceiling.",
    ],
    "gtd-vs-para": [
        "Level 1: To-do lists belong in one place and learning notes in another - like groceries on the fridge list and recipes in a folder.",
        "Level 2: Tasks and knowledge need different homes - like mixing dirty dishes into your filing cabinet, one bucket turns both systems into junk.",
        "Level 3: GTD processes commitments; PARA organizes reference - when they share one bucket, neither system can run clean.",
        "Level 4: Keep actionable tasks in a trusted capture system and durable knowledge in PARA buckets - never the same inbox.",
        "Level 5: [[Getting Things Done]] owns next actions; [[PARA Method]] owns projects and resources - crossing the streams breeds rot.",
    ],
    "habit-formation": [
        "Level 1: Decide once to do the small thing daily until your body does it without a fresh pep talk each morning.",
        "Level 2: Make the decision once so you stop re-deciding every day - like setting an alarm once instead of debating wake-up time each morning.",
        "Level 3: Motivation fades; a single upfront choice turns the behavior into default instead of a daily negotiation you might lose.",
        "Level 4: Pick one small habit, decide once, and repeat until autopilot carries it - not until motivation returns.",
        "Level 5: [[Habit Stacking]] attaches new moves to anchors already on autopilot; [[Atomic Habits]] keeps the first rep small enough to repeat.",
    ],
    "habit-stacking": [
        "Level 1: Add a tiny new step right after something you already do - like writing one journal line after you pour coffee.",
        "Level 2: Stack a new small move onto a habit that already runs on autopilot - one anchor, one add-on, like chaining beads on a string.",
        "Level 3: The existing habit is the trigger; the new behavior rides its momentum instead of fighting for a fresh cue you might forget.",
        "Level 4: After your stable daily anchor, attach one tiny new step - do not bolt a whole routine onto nothing.",
        "Level 5: [[Habit Formation]] decides once; stacking is how you wire the new move without a separate reminder system.",
    ],
    "heart-righteousness": [
        "Level 1: God cares about anger and lust in your heart - not just whether you looked polite on the outside.",
        "Level 2: You can look fine outside while anger or lust inside still breaks the rule - like a clean shirt hiding a messy room.",
        "Level 3: Outward compliance without inward righteousness fails the standard - heart murder and heart adultery count before God, not just visible acts.",
        "Level 4: Treat anger and lust in the heart as guilt before God - polish on the outside does not erase it.",
        "Level 5: [[The Beatitudes]] and [[Judge Not]] both assume heart-level righteousness - external niceness is not the finish line.",
    ],
    "heed-every-near-miss": [
        "Level 1: A close call means something almost went wrong - treat it like a warning, not proof everything is safe.",
        "Level 2: When nobody gets injured, organizations often relax - near misses are signals, like smoke before a fire, not lucky free passes.",
        "Level 3: Ignoring near misses trains the system to wait for blood before it changes - the hazard was already present when luck blocked injury.",
        "Level 4: Log every near miss and act before injury proves you should have listened.",
        "Level 5: [[Incident Investigation]] stays blameless; [[Hierarchy of Controls]] asks what hazard to eliminate after the near miss, not who to blame.",
    ],
    "hierarchy-of-controls": [
        "Level 1: Remove the danger first - a guard rail beats a sign, and both beat helmets if you can fix the source.",
        "Level 2: Eliminate the hazard before warnings, admin, or PPE - like removing the pothole instead of posting a slow-down sign.",
        "Level 3: PPE is last because it depends on human compliance; elimination removes the risk at the root before anyone has to remember gear.",
        "Level 4: Ask whether you can eliminate or engineer out the hazard before you buy more signs and gloves.",
        "Level 5: [[Heed Every Near Miss]] feeds what to eliminate; admin controls and PPE are backups when the hazard cannot go away.",
    ],
    "honest-self-awareness": [
        "Level 1: Plans that ignore what you are actually like fall apart on an ordinary busy day - like shoes two sizes too small.",
        "Level 2: Transformation built on fantasy breaks on contact with Tuesday - real schedules expose fake starting lines like a scale under bright light.",
        "Level 3: When the plan assumes a person you are not, the first stressful week collapses the whole system - fantasy baselines cannot survive real load.",
        "Level 4: Build habits and goals from who you are this week - not from the ideal version you perform on paper.",
        "Level 5: [[Accept the Starting Line]] names the real baseline; [[Growth Mindset]] needs honest data before misses become trainable.",
    ],
    "humility-and-service": [
        "Level 1: In God's kingdom, the person who helps others is great - not the one who climbs over everyone to get on top.",
        "Level 2: Jesus came to serve and give His life - real greatness bends down like a parent tying a child's shoe, not climbing the worldly ladder.",
        "Level 3: Worldly rank climbs upward; kingdom greatness bends downward to serve and give - opposite directions, opposite rewards.",
        "Level 4: Measure greatness by who you served, not by who served your platform.",
        "Level 5: [[Servant Leadership]] and [[Follow Christ Then Lead]] keep the ladder inverted - influence without climbing over people.",
    ],
    "inbox-zero": [
        "Level 1: Open your inbox often, decide what to do with each message, and leave nothing sitting there to rot.",
        "Level 2: Work through every message on a schedule - decide the next step or archive it, like clearing dishes after each meal instead of letting them pile up.",
        "Level 3: An undeclared inbox becomes a todo graveyard - every message needs a next action or archive, or dread returns every Monday.",
        "Level 4: Touch each message once per processing pass: decide, delegate, defer with a date, or delete - then leave empty.",
        "Level 5: [[The Trusted Inbox]] is the capture lane; [[Getting Things Done]] processing keeps inbox zero from becoming performative tidying.",
    ],
    "incident-investigation": [
        "Level 1: After something breaks, ask what in the setup caused it - not only who was standing nearby when it happened.",
        "Level 2: Blameless tone keeps investigation on system causes - people fix processes when they are not scapegoated, like fixing the leaky pipe instead of yelling at the puddle.",
        "Level 3: Blame chases a name; investigation chases the condition that made failure possible - fix the layout, not just the person present.",
        "Level 4: Run post-incident reviews for system causes first - who was nearby is context, not the root.",
        "Level 5: [[Blameless After Action Review]] shares the tone; [[Heed Every Near Miss]] feeds hazards before incidents land.",
    ],
    "influence-without-title": [
        "Level 1: You are leading when people follow your direction - even if you never got the official job title.",
        "Level 2: Leadership is influence - if they are moving with you, you are leading; badge optional, like a captain nobody promoted but everyone listens to.",
        "Level 3: Title grants authority on org charts; influence moves behavior - when people act on your direction without a badge, you lead.",
        "Level 4: Lead by moving people toward a shared outcome - do not wait for a badge to start helping others win.",
        "Level 5: [[Leadership Is Influence]] is the headline; [[Title Without Influence]] warns when the badge moves nothing.",
    ],
    "information-diet": [
        "Level 1: Pick what news and videos you take in on purpose - what you scroll through shapes how you think.",
        "Level 2: Choose what you consume on purpose - feeds are not neutral background noise, like junk food left on the counter every day.",
        "Level 3: Passive scrolling trains attention and mood; curated intake shapes what feels normal by Friday - input becomes your inner weather.",
        "Level 4: Subscribe on purpose, unsubscribe on purpose - treat feeds like food you are willing to eat daily.",
        "Level 5: [[Signal vs Noise]] separates worth keeping; [[Digital Minimalism]] cuts pipes you cannot babysit.",
    ],
    "integrity-without-an-audience": [
        "Level 1: Do the right thing even when nobody is watching you - like cleaning your room when guests are not coming.",
        "Level 2: Do the honest work when there is no audience - applause is not what keeps the standard, like practicing alone before the game.",
        "Level 3: When integrity only shows up on stage, private corners still rot - character is what you do unseen, not what you perform.",
        "Level 4: Keep the same honest standard in private tasks you would defend in public.",
        "Level 5: [[Secret Devotion]] and [[Integrity]] both count obedience without an audience - [[Judgment Seat]] evaluates what nobody saw.",
    ],
    "integrity": [
        "Level 1: Your actions should match your words even when telling the truth slows you down or makes you look bad.",
        "Level 2: Integrity means your behavior still matches your words when honesty costs you speed or applause - like keeping a promise when breaking it would be easier.",
        "Level 3: When convenience bends the story, integrity breaks - alignment costs something every time, so shortcuts show up in the gap between claim and deed.",
        "Level 4: Keep words and deeds aligned even when honesty costs speed, comfort, or applause.",
        "Level 5: [[Plain Commitments at Work]] and [[Integrity Without an Audience]] split public promises from private corners - both must match.",
    ],
    "intellectual-sourcing": [
        "Level 1: Write down where an idea came from so you can find the book or article again and know you quoted it right.",
        "Level 2: Cite sources so you can trust what you wrote and find the original six months later - like labeling a box before you put it in storage.",
        "Level 3: Unsourced notes become guesses - a link or citation turns a half-remembered line back into evidence you can defend.",
        "Level 4: Attach the source when you capture the idea - future you should reach the original in one click.",
        "Level 5: [[Capture]] is where the source lands first; [[Active Knowledge Curation]] keeps citations from rotting into folklore.",
    ],
    "into-your-hands": [
        "Level 1: Jesus died trusting God to hold Him - like handing something precious to someone you know will take care of it.",
        "Level 2: His last recorded words to the Father trust the outcome - Father, into Your hands I commit My spirit, like releasing a rope when the climb is done.",
        "Level 3: Death arrives and Jesus commits His spirit to the Father - trust at the finish, not panic control, because surrender completes what the garden began.",
        "Level 4: At the end, commit the outcome to the Father's hands - echo Psalm 31:5 instead of clutching control.",
        "Level 5: [[Not My Will]] surrendered the cup; here surrender completes at death - trust holds when control is gone.",
    ],
    "invest-in-the-few": [
        "Level 1: Jesus spent real time with a small group before sending them out - depth with a few beats chasing a huge crowd.",
        "Level 2: Jesus picked twelve to stay close before He sent them - presence before platform, like training a few workers well before opening every branch.",
        "Level 3: Mass platform without presence produces spectators; time with a few produces sendable people - depth scales through people, not headcount alone.",
        "Level 4: Invest disproportionate presence in a small circle before you scale the message outward.",
        "Level 5: [[Great Commission]] sends widely; this note names the few who get presence first - depth before broadcast.",
    ],
    "issues": [
        "Level 1: Fix broken links and lonely notes in the garden without treating the writer like a failure.",
        "Level 2: Repair broken links and orphan notes without shaming whoever wrote them - like fixing a typo without calling the author careless.",
        "Level 3: Maintenance on orphans and dead links keeps the garden usable - shame about the author blocks fixes, so diagnose the graph, not the person.",
        "Level 4: Run the issues list on broken links and orphans - repair the graph, not the ego.",
        "Level 5: [[Graph]] shows where orphans live; [[Periodic Knowledge Review]] is when you batch-fix what issues flagged.",
    ],
    "it-is-written": [
        "Level 1: When Satan tempted Jesus, He answered with Bible verses He already knew - not words He had to look up in a hurry.",
        "Level 2: Each attack in the wilderness got It is written - Deuteronomy already loaded, not a panic search mid-temptation, like answers memorized before the test.",
        "Level 3: Temptation meets pre-loaded Scripture - scrambling for a verse mid-crisis loses to memory trained before the fight arrives.",
        "Level 4: Load Scripture before temptation arrives so It is written is ready without a panic lookup.",
        "Level 5: [[Jesus' Rhythms]] includes living in Scripture; wilderness answers show stored word, not improvised slogans.",
    ],
    "jesus-prayers": [
        "Level 1: One page tracks how often Jesus prayed; this page holds the exact words He said to God that the Bible records.",
        "Level 2: Rhythms track how often He prayed; this hub holds the verbatim prayers the Gospels record - like a schedule versus the speech transcript.",
        "Level 3: Rhythm notes frequency; this hub holds the recorded words - pattern and text are different layers, and both matter for imitation.",
        "Level 4: Use the rhythms hub for how often He prayed; use this hub for the verbatim prayers the Gospels preserve.",
        "Level 5: [[Withdraw to Pray]] is one rhythm; this index holds John 17, Gethsemane, and the cross - text you can review card by card.",
    ],
    "jesus-rhythms": [
        "Level 1: One section holds what Jesus taught; this section holds what the Bible shows He actually did day to day.",
        "Level 2: Eternal Principles holds what Jesus taught; this hub holds what the Gospels show Him doing - like a syllabus versus a daily log.",
        "Level 3: Teaching lane names commands; biography lane names recurring moves - prayer, Scripture, people, obedience on ordinary days, because pattern follows from what He did.",
        "Level 4: Track what the Gospels show Jesus doing daily - withdraw, Scripture, people, obedience - not a merit checklist.",
        "Level 5: Ground is still [[Free Grace]] - patterns are grateful imitation after faith; [[Atomic Notes]] below drill six cards each at [/notes/review/](/notes/review/).",
    ],
    "joy": [
        "Level 1: Joy is deep gladness that grows when you walk with God - not fake happiness you perform for other people.",
        "Level 2: Joy grows with love and peace as fruit of the Spirit - deeper than performing happiness for a crowd, like roots versus a painted smile.",
        "Level 3: Joy rooted in God survives bad weeks; performed happiness collapses when the audience leaves - circumstance cannot kill what the Spirit grows.",
        "Level 4: Look for gladness that stays when circumstances swing - not a smile you manufacture for the room.",
        "Level 5: [[Peace]] and [[Love]] sit beside joy in [[Fruits of the Spirit]] - joy is fruit, not a mood you fake on command.",
    ],
    "judge-not": [
        "Level 1: Fix your own big faults before you pick on someone else's small ones - you are not the final judge of their soul.",
        "Level 2: You are not the final judge of anyone's soul - deal with your own fault before you pick at theirs, like clearing your windshield before criticizing another driver.",
        "Level 3: Final judgment belongs to God - when you play judge, you skip your own plank and misread their speck, so hypocrisy blocks clear sight.",
        "Level 4: Deal with your plank first; leave final soul-judgment to God instead of nitpicking their speck.",
        "Level 5: [[Heart Righteousness]] keeps the standard inward; [[By Their Fruits]] reads evidence without replacing God's seat.",
    ],
    "judgment-seat": [
        "Level 1: Saved people will stand before Jesus to see what reward their good works earned - not to learn whether they get into heaven.",
        "Level 2: Believers face a reward review for what they did after salvation - not a second trial on who gets heaven, like an awards show after admission.",
        "Level 3: Eternal life was settled at faith; the bema weighs works for reward - categories must stay separate or panic follows when fire tests come.",
        "Level 4: Stand before Christ knowing salvation is settled - let the review weigh faithful works for reward, not standing.",
        "Level 5: [[Free Grace]] and [[Justification]] already decided forever; [[Loss of Reward]] keeps saved-through-fire distinct from unsaved.",
    ],
    "justification": [
        "Level 1: God declared the humble man right with Him - the proud man who bragged about his good deeds did not.",
        "Level 2: God declared the humble tax collector right with Him - the proud man who listed his deeds did not go home justified, like empty hands versus a trophy speech.",
        "Level 3: Justification is God's declarative yes on the humble - boasting about deeds did not buy the verdict, because the court measures trust, not performance.",
        "Level 4: Come to God with empty hands and receive the justified verdict - not a resume of religious performance.",
        "Level 5: [[Free Grace]] applies justification to eternal life; [[Sanctification]] is the walk after - do not merge the categories.",
    ],
    "kindness": [
        "Level 1: Kindness is gentle care for the real person in front of you - not acting polite just to look good.",
        "Level 2: Fruits of the Spirit names kindness beside goodness - soft strength toward actual people, like a hand on a shoulder, not a generic nice-guy pose.",
        "Level 3: Generic niceness performs for observers; kindness meets the person in front of you with soft strength - audience applause is not the aim.",
        "Level 4: Show gentle strength to the actual person in the room - not a polite pose for bystanders.",
        "Level 5: [[Goodness]] pairs with kindness in [[Fruits of the Spirit]] - both aim outward, not at a nice-guy brand.",
    ],
    "kingdom-on-the-road": [
        "Level 1: Jesus traveled town to town teaching, telling good news, and helping sick people - one life of service on the move.",
        "Level 2: He said He must preach the kingdom to other cities - teaching, preaching, healing on the road, like a doctor who goes to patients instead of waiting in one office.",
        "Level 3: The kingdom advance was mobile ministry - teaching, preaching, healing in every town, not one static stage, because people meet the kingdom where they live.",
        "Level 4: Take the kingdom to the next town - teach, proclaim, heal on the road instead of hoarding one audience.",
        "Level 5: [[Great Commission]] sends outward; this note is the Gospel biography of the same pattern - kingdom service in motion.",
    ],
    "layered-reading": [
        "Level 1: Read the same book more than once - first skim for the big picture, then mark parts, then write what you learned.",
        "Level 2: Read the same source in layers - skim first, mark what matters, then write it back, like peeling an onion one skin at a time.",
        "Level 3: One pass cannot extract structure, evidence, and your own words - each layer adds depth without pretending one read is enough.",
        "Level 4: Run the same source through skim, mark, and summarize passes before you claim you know it.",
        "Level 5: [[The Feynman Technique]] is the teach-it-back layer; [[Active Reading]] keeps highlights from dying in the margin.",
    ],
    "leadership-is-influence": [
        "Level 1: You are only leading if someone is coming with you - otherwise you are just walking alone.",
        "Level 2: You lead when people move with you - without followers you are walking alone, title or not, like a parade with no marchers.",
        "Level 3: Movement defines leadership - without followers, authority is a solo stroll, not influence, because direction only counts when others adopt it.",
        "Level 4: Check whether anyone is moving with you before you call it leadership.",
        "Level 5: [[Influence Without Title]] leads without a badge; [[Title Without Influence]] warns when the org chart moves nobody.",
    ],
    "leadership": [
        "Level 1: Good leaders make sure the people who depend on them still feel noticed when things get stressful.",
        "Level 2: Leadership shows up when your team still feels noticed after deadline pressure hits - like a captain who checks the crew when the storm rises.",
        "Level 3: When pressure spikes and people feel invisible, trust erodes - leadership is keeping them seen under load, because unseen people stop giving their best.",
        "Level 4: Under pressure, keep the people who depend on you feeling seen - not just the deliverable on track.",
        "Level 5: [[Servant Leadership]] bends toward service; [[Duty of Care]] names the protection they should feel when roles flip.",
    ],
    "lean-startup": [
        "Level 1: Try the smallest version first, see what happens, then improve - do not build the huge version before you know anyone wants it.",
        "Level 2: Ship a tiny version, watch what users do, learn, then grow - not the full build before anyone wants it, like tasting soup before cooking the pot.",
        "Level 3: Big builds before demand burn cash and morale - small tests produce learning loops cheap enough to repeat when the first guess is wrong.",
        "Level 4: Ship the smallest test, measure response, learn, then scale - never the full product on faith alone.",
        "Level 5: [[Practice Small Experiments]] keeps trials small; [[Ship It]] pushes the test out before perfection hoarding wins.",
    ],
    "learning-organizations": [
        "Level 1: Write down what went wrong and keep that note visible until the team fixes it or agrees to live with it.",
        "Level 2: The what broke line stays until fixed or accepted - like a sticky note on the fridge nobody removes until the leak is repaired.",
        "Level 3: Hidden failures repeat - a visible what broke line forces fix or explicit acceptance, because burying the miss guarantees the same miss returns.",
        "Level 4: Keep the what broke note on the board until the team fixes the system or documents why they accept the risk.",
        "Level 5: [[Incident Investigation]] feeds the line; [[Continuous Improvement]] closes it - not blame, system repair.",
    ],
    "let-your-light-shine": [
        "Level 1: Do good deeds where people can see them so they praise God - not so they praise you.",
        "Level 2: Good works on a hill point praise to the Father - visible on purpose, not to build your personal brand, like a lighthouse, not a billboard with your face.",
        "Level 3: Visible good works aim glory at the Father - when the audience applauds you instead, the light pointed the wrong way and the design failed.",
        "Level 4: Let good works be seen so observers glorify the Father - cut the moves that build your brand instead.",
        "Level 5: [[God Centered Design]] orders the same aim; [[Secret Devotion]] keeps private obedience in the ledger too.",
    ],
}

LEVEL_RE = re.compile(r"^  - Level [1-5]:.*$", re.MULTILINE)


def patch_note(slug: str, levels: list[str]) -> None:
    path = NOTES / f"{slug}.md"
    text = path.read_text(encoding="utf-8")
    found = LEVEL_RE.findall(text)
    assert len(found) == 5, f"{slug}: expected 5 level lines, found {len(found)}"
    it = iter(levels)
    new_text = LEVEL_RE.sub(lambda _: f"  - {next(it)}", text)
    assert "Level 6" not in new_text
    # ponytail: key_concept block only - no blank lines between bullets
    in_key = False
    cleaned: list[str] = []
    for line in new_text.splitlines():
        if line.startswith("key_concept:"):
            in_key = True
            cleaned.append(line)
            continue
        if in_key:
            if line and not line.startswith(" ") and not line.startswith("\t"):
                in_key = False
                cleaned.append(line)
                continue
            if line.strip() == "":
                continue
        cleaned.append(line)
    out = "\n".join(cleaned) + ("\n" if new_text.endswith("\n") else "")
    for level in levels:
        bad = re.search(r"\b\w+'(?:t|re|ve|ll|d)\b", level, re.I)
        assert not bad, f"{slug}: contraction in {level!r} ({bad.group()})"
    path.write_text(out, encoding="utf-8")
    print(f"patched {slug}")


def main() -> None:
    assert len(LEVELS) == 43, len(LEVELS)
    for slug, levels in LEVELS.items():
        assert len(levels) == 5, slug
        patch_note(slug, levels)
    print("done: 43 notes")


if __name__ == "__main__":
    main()
