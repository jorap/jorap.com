#!/usr/bin/env python3
"""Regenerate curated spectrum pairs into data/randomizer.yaml."""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
YAML = ROOT / "data" / "randomizer.yaml"

# ponytail: one-off maintainer script; run manually when expanding spectrums

def load_pairs():
    # Inline pair list — curated opposites only (no adjective×noun templates)
    pairs = []

    def add(l, r):
        if l != r:
            pairs.append((l, r))

    concepts = """
Hot|Cold
Quiet activity|Active sport
Healthy snack|Treat food
Mild habit|Risky habit
Simple skill|Impressive skill
Selfish choice|Generous choice
Formal event|Casual hangout
Art|Craft
Simple gift|Fancy gift
Overrated|Underrated
City life|Country life
Planned trip|Spontaneous trip
Early bird|Night owl
Minimal home|Cozy clutter
Text message|Phone call
Better alone|Better with others
Better in theory|Better in practice
Better for kids|Better for adults
Better indoors|Better outdoors
Better hot|Better cold
Better fresh|Better preserved
Better handmade|Better factory-made
Better saved|Better spent
Better planned|Better improvised
Better quiet|Better lively
Better small|Better large
Better short|Better long
Better sweet|Better savory
Better mild|Better bold
Better plain|Better fancy
Better familiar|Better exotic
Harmless prank|Cruel joke
Healthy choice|Indulgent choice
Eco-friendly|Convenient
Time saver|Time waster
Stress relief|Stress cause
Confidence boost|Confidence drain
Team builder|Team divider
Icebreaker|Conversation ender
Low effort|High effort
Low cost|High cost
Low risk|High risk
Low noise|High noise
Low skill|High skill
Low maintenance|High maintenance
Window seat|Aisle seat
Front row|Back row
Packing light|Packing heavy
Early arrival|Fashionably late
Overprepared|Underprepared
Too spicy|Too bland
Too sweet|Too bitter
Too crowded|Too empty
Too formal|Too casual
Too strict|Too lenient
Too loud|Too quiet
Too bright|Too dim
Too fast|Too slow
Too big|Too small
Too serious|Too silly
Too cautious|Too reckless
Too frugal|Too generous
Too organized|Too spontaneous
Breakfast food|Dinner food
Summer activity|Winter activity
Solo hobby|Group hobby
Desk job|Physical job
Team sport|Individual sport
Board game|Video game
Fiction book|Nonfiction book
Comedy show|Drama show
Live music|Recorded music
Home cooking|Restaurant meal
Walking commute|Driving commute
Public transport|Private car
Camping trip|Hotel stay
Beach vacation|Mountain vacation
City break|Nature retreat
Guided tour|Self-guided tour
Group travel|Solo travel
Physical book|E-book
Handwritten note|Typed message
Cash payment|Card payment
Shopping in store|Shopping online
New clothes|Secondhand clothes
Bright colors|Neutral colors
Comfort shoes|Dress shoes
Home workout|Gym workout
Team meeting|One-on-one chat
Strict deadline|Flexible deadline
Big celebration|Quiet acknowledgment
Public speech|Private conversation
Remote work|Office work
Video call|In-person meeting
Deep research|Quick search
Ask for help|Figure it out alone
Speak up|Stay quiet
Try new food|Stick to favorites
Split the bill|Treat everyone
Repair item|Replace item
Cook from scratch|Use shortcuts
Daily routine|Mix it up
Family dinner|Solo dinner
Hot drink|Iced drink
Sweet treat|Savory treat
Watching sports|Playing sports
Short hike|Long trek
Packed schedule|Open schedule
Digital detox|Always connected
Paper to-do list|App to-do list
Heavy blanket|Light sheet
Live plants|Artificial plants
Dog person|Cat person
Gift experiences|Gift objects
Carpool|Drive solo
Dark mode|Light mode
Multitask|Single task
Vegetarian meal|Meat meal
Hot shower|Cold rinse
Umbrella carry|Hoodie only
DIY repair|Call a pro
Group study|Solo study
Front of class|Back of class
Sandwich|Wrap
Pancake|Waffle
Tea person|Coffee person
City museum|Science museum
Tent camping|Cabin stay
Mountain view|Ocean view
Quiet library|Busy cafe
Online course|In-person class
Big party|Small dinner
Cook together|Cook alone
Table chat|TV dinner
Host duties|Guest relax
Morning news|Morning music
Night read|Night stream
Window shopping|Purpose shopping
Thrift treasure|Retail new
Minimal wallet|Stuffed wallet
Budget plan|Spend freely
Cloud sync|Local file
Public post|Private diary
Fiction escape|Nonfiction learn
Paint canvas|Sketch pad
Campfire song|Indoor playlist
Sunrise watch|Sunset watch
Snow angel|Sand castle
Forest walk|Beach walk
Indoor pool|Outdoor pool
Strategy game|Luck game
Potluck dish|Store-bought dish
Meal prep|Cook daily
Alarm snooze|Up on first ring
Fan sleep|AC sleep
Open curtain|Blackout curtain
Weekly deep clean|Daily light tidy
Scented candle|Unscented air
Pet on furniture|Pet off furniture
Volunteer often|Volunteer rarely
Vote every election|Vote sometimes
Apologize first|Wait for apology
Trust strangers|Trust slowly
Gift handmade card|Store card
Stay late at party|Leave early
Bike helmet|No helmet
Dark mode app|Light mode app
Standing desk|Sitting desk
Inbox zero|Inbox backlog
Sick day rest|Work while sick
Whole foods|Processed foods
Annual checkup|Go when needed
Weather app check|Look outside
Emergency kit|Figure it out
Coupon hunting|Pay full price
Library book|Owned book
Teach to learn|Learn quietly
School club|Free afternoon
Prom attend|Skip dance
Summer camp|Summer home
Borrow tools|Own every tool
Adopt rescue|Buy from breeder
Donate monthly|Donate once a year
Debate for fun|Avoid debates
Sing at parties|Watch others dance
Remember faces|Remember names
RSVP promptly|RSVP last minute
Offer a ride|Find your own way
Wash car often|Wash when dirty
Phone until it dies|New phone yearly
Read privacy policy|Accept quickly
Work music|Work silence
Vacation unplugged|Vacation online
Doctor visit|Home rest
Gym membership|Home exercise
Hot lunchbox|Cold lunchbox
Grill outside|Pan inside
Park bench|Kitchen table
Escalator|Stairs
Elevator|Walk up
Raincoat|Hoodie
Layer many|One warm layer
Welcome mat|Bare step
Neighbor chat|Quick wave
Book lend|Library only
Classic film|New blockbuster
Small venue|Big arena
Home colors|Visiting colors
Sticker reward|Word praise
Screen time earn|Screen time free
Bedtime story|Bedtime solo
Compost bin|Trash bin
Herb garden|Store herbs
File folder|Pile stack
Bullet journal|Blank notebook
Laptop couch|Desk proper
Headset mic|Laptop mic
Password book|Memory only
Keep box|Recycle box
Emergency fund big|Month to month
Food bank drop|Pantry buy
Tree plant day|Water tree
Birthday big|Birthday small
Postcard send|Text photo
Farm visit|Petting zoo
Lego set|Free build
Open mic|Shower concert
Language flashcards|Phrase book
Garage sale|Online listing
Apple orchard|Apple bag
Gentle ride|Thrill ride
Pool noodle|Free swim
Spa day|Home mask
Goal vision board|Goal list
Calendar block deep work|Open calendar
Say no politely|Say yes often
Walking meeting|Desk meeting
Blog post|Private note
Review honest|Review skip
Reusable cup|Disposable cup
Bike errand|Car errand
Walk to school|Drive to school
Charades act|Charades guess
Trivia teams|Trivia solo
Victory lap|Quiet exit
Train harder|Rest more
Indoor court|Outdoor court
Bleacher seat|Field edge
Save for bike|Spend now
Share toy|Mine toy
Camp in yard|Camp in room
Catch release|Catch keep
Hot cocoa mug|Hot tea mug
Remote start|Bundle first
Hydrate sports|Drink when dry
Lucky socks|Any socks
Halftime adjust|Same plan
Clutch shot|Pass clutch
""".strip().splitlines()
    for line in concepts:
        l, r = line.split("|", 1)
        add(l.strip(), r.strip())

    # Dedupe preserve order
    seen = set()
    unique = []
    for l, r in pairs:
        key = (l.lower(), r.lower())
        rev = (r.lower(), l.lower())
        if key in seen or rev in seen:
            continue
        seen.add(key)
        unique.append((l, r))
    return unique


def main():
    pairs = load_pairs()
    assert pairs, "no spectrum pairs"
    text = YAML.read_text()
    block = "- id: spectrum\n  title: Concept spectrums\n  mode: spectrum\n"
    block += (
        "  tagline: Two poles on one line. "
        "Someone picks a hidden spot; you give one clue that lands there.\n"
    )
    block += (
        "  play_hint: Give a single clue for where the target lands. "
        "Works near either pole, not only the middle. Expect friendly debate.\n"
    )
    block += "  spectrums:\n"
    for l, r in pairs:
        block += f"  - left: {l}\n    right: {r}\n"
    new_text = re.sub(r"- id: spectrum\n.*\Z", block.rstrip() + "\n", text, count=1, flags=re.S)
    YAML.write_text(new_text)
    print(f"wrote {len(pairs)} spectrums")


if __name__ == "__main__":
    main()
