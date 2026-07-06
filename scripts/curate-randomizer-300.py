#!/usr/bin/env python3
"""Curate each randomizer collection to 300 entries, best first (rank 1 = top)."""
from __future__ import annotations

import re
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
YAML = ROOT / "data" / "randomizer.yaml"
TARGET = 300

# ponytail: maintainer script; run after bulk prompt edits

SCALE_CLUES_PIN = [
    "Things you'd want to do when you're very tired.",
    "Things to bring on a deserted island.",
    "Superpowers you'd actually want to have.",
    "Board games you'd bring to game night.",
    "Snacks you'd want during a movie at home.",
    "Foods you'd want for a comfort meal.",
    "Things that would cheer you up on a bad day.",
    "Things that would start a good conversation.",
    "Things that would be embarrassing to drop in public.",
    "Things you'd want when the Wi-Fi goes down at home.",
    "Things you'd want when you're bored at home.",
    "Things you'd want on a lazy Sunday morning.",
    "Things that would make a party more fun.",
    "Party games that work with any group size.",
    "Card games you'd teach in five minutes.",
    "Things that would end an awkward silence.",
    "Things you'd want when you can't find your keys.",
    "Things you'd want when you lock yourself out of a room.",
    "Things you'd want when your phone battery hits one percent.",
    "Things you'd want when you forget an umbrella.",
    "Things you'd want when you spill coffee on your shirt.",
    "Things that would make you laugh in a serious meeting.",
    "Things that would make a prank harmless and funny.",
    "Excuses for being late that might actually work.",
    "Things you'd love to find in your lunchbox.",
    "Things you'd hate to find in your lunchbox.",
    "Desserts you'd order if calories didn't matter.",
    "Foods you'd bring to a potluck.",
    "Breakfast foods that would wake you up.",
    "Drinks you'd want on a scorching day.",
    "Movies perfect for a family night.",
    "Movies perfect for a solo rainy afternoon.",
    "Songs you'd put on a road-trip playlist.",
    "TV shows you'd binge on a sick day.",
    "Superpowers perfect for a lazy person.",
    "Superpowers perfect for a helpful person.",
    "Time periods you'd visit with a time machine.",
    "Animals you'd want as an impossible pet.",
    "Things to bring if stranded in a forest overnight.",
    "Things to bring if the power went out for a week.",
    "Things you'd want if you could only carry one bag.",
    "Things you'd want if you had no internet for a month.",
    "Things you'd want during a power outage.",
    "Things you'd want when it's raining outside.",
    "Things you'd want when you're stuck indoors all day.",
    "Things you'd want during a snow day.",
    "Things you'd want during a long queue at the doctor.",
    "Things you'd want during a delayed flight.",
    "Things you'd want on a long flight.",
    "Things you'd want at a beach all day.",
]


def score_scale_clue(item: str) -> float:
    lower = item.lower()
    score = 50.0
    if len(item) > 95:
        score -= 18
    elif len(item) > 75:
        score -= 8
    if lower.count("if you had to") >= 1:
        score -= 14
    if lower.startswith("things you'd want when"):
        score -= 6
    if lower.startswith("things you'd want if you had to"):
        score -= 12
    if "superpower" in lower:
        score += 14
    if "embarrassing" in lower or "funny" in lower or "awkward" in lower:
        score += 12
    if "deserted island" in lower or "stranded" in lower:
        score += 14
    if "board game" in lower or "card game" in lower or "party game" in lower:
        score += 10
    if "snack" in lower or "comfort meal" in lower or "dessert" in lower:
        score += 8
    if "conversation" in lower or "party" in lower:
        score += 7
    if "wifi" in lower or "power outage" in lower or "internet" in lower:
        score += 8
    if "movie" in lower or "road-trip" in lower or "playlist" in lower:
        score += 6
    if "very tired" in lower or "bored at home" in lower:
        score += 10
    if "zombie" in lower or "socks kept disappearing" in lower:
        score -= 5
    return score


PERSONAL_PIN = [
    "How lazy are you?",
    "To what degree would you call yourself a sore loser?",
    "How competitive are you at board games?",
    "How hard is it for you to ignore your phone?",
    "How likely are you to gossip?",
    "How honest are you, even when it hurts?",
    "How dramatic are you?",
    "How stubborn are you?",
    "How much of a procrastinator are you?",
    "How funny do you think you are?",
    "How sarcastic are you?",
    "How impulsive are you?",
    "How jealous are you?",
    "How forgiving are you?",
    "How likely are you to hold a grudge?",
    "How likely are you to apologize first?",
    "How good are you at keeping secrets?",
    "How likely are you to return a shopping cart?",
    "How likely are you to eat food that fell on the floor?",
    "How likely are you to pretend you didn't see a message?",
    "How often do you replay awkward moments in your head?",
    "How likely are you to cry during a movie?",
    "How territorial are you about personal space?",
    "How comfortable are you eating alone in public?",
    "How comfortable are you with silence in conversation?",
    "How likely are you to include someone sitting alone?",
    "How likely are you to stand up for a friend?",
    "How calm are you when you lose a game?",
    "How gracious are you when you win?",
    "How tidy is your bedroom right now?",
    "How punctual are you?",
    "How adventurous are you with food?",
    "How picky are you about what you eat?",
    "How likely are you to overpack?",
    "How likely are you to get lost and not mind?",
    "How good are you at admitting when you're wrong?",
    "How good are you at winning arguments?",
    "How much do you enjoy being in charge?",
    "How much do you enjoy surprises?",
    "How much do you enjoy karaoke?",
    "How much do you enjoy trying local food when traveling?",
    "How likely are you to fact-check before sharing online?",
    "How environmentally conscious are you?",
    "How sentimental are you?",
    "How superstitious are you?",
    "How anxious are you in everyday life?",
    "How confident are you in new situations?",
    "How empathetic are you?",
    "How patient are you?",
    "How short-tempered are you?",
]

PERSONAL_NEW = [
    "How likely are you to double-dip at a party?",
    "How likely are you to borrow something and forget to return it?",
    "How likely are you to talk to yourself out loud?",
    "How likely are you to sing in the shower?",
    "How much do you care what strangers think of you?",
    "How much do you care what close friends think of you?",
    "How likely are you to read spoilers on purpose?",
    "How likely are you to peek at a gift before the day?",
    "How likely are you to rewatch the same show instead of starting something new?",
    "How likely are you to leave a group chat on read?",
    "How likely are you to laugh at your own joke?",
    "How likely are you to correct someone's grammar?",
    "How likely are you to finish a book you dislike?",
    "How likely are you to dog-ear a book page?",
    "How likely are you to use the last of something without replacing it?",
    "How likely are you to take the bigger slice of cake?",
    "How likely are you to save the best bite for last?",
    "How likely are you to eat straight from the container?",
    "How likely are you to wear pajamas on a video call?",
    "How likely are you to show up early to avoid being late?",
    "How likely are you to blame traffic when you left late?",
    "How likely are you to take credit for team work?",
    "How likely are you to deflect a compliment?",
    "How likely are you to remember a small detail someone mentioned once?",
    "How likely are you to send a voice note instead of typing?",
    "How likely are you to leave one dish in the sink overnight?",
    "How likely are you to reorganize a drawer when stressed?",
    "How likely are you to buy something because it is on sale?",
    "How likely are you to return an online purchase?",
    "How likely are you to keep tickets and receipts for years?",
    "How likely are you to name your plants or devices?",
    "How likely are you to talk to pets like people?",
    "How likely are you to wave back at someone who was waving at someone else?",
    "How likely are you to practice a conversation in your head beforehand?",
    "How likely are you to Google symptoms after a minor ache?",
    "How likely are you to skip the tutorial and figure it out?",
    "How likely are you to read instructions only after something fails?",
    "How likely are you to use all the browser tabs at once?",
    "How likely are you to clear notifications immediately?",
    "How likely are you to let notifications pile up?",
    "How likely are you to mute a group chat?",
    "How likely are you to finish someone else's sentence?",
    "How likely are you to interrupt when excited?",
    "How likely are you to stay quiet even when you disagree?",
    "How likely are you to play devil's advocate?",
    "How likely are you to change your opinion after a good argument?",
    "How likely are you to stick to your opinion out of pride?",
    "How likely are you to avoid conflict at all costs?",
    "How likely are you to address conflict directly?",
    "How likely are you to remember dreams?",
    "How likely are you to tell people about your dreams?",
    "How likely are you to believe in luck?",
    "How likely are you to have a lucky item or ritual?",
    "How likely are you to knock on wood or touch something for luck?",
    "How likely are you to feel guilty relaxing?",
    "How likely are you to reward yourself after small wins?",
    "How likely are you to celebrate your own birthday loudly?",
    "How likely are you to forget your own age for a moment?",
    "How likely are you to cry happy tears?",
    "How likely are you to get secondhand embarrassment for strangers?",
    "How likely are you to cringe at your old social posts?",
    "How likely are you to delete old photos?",
    "How likely are you to keep every photo forever?",
    "How likely are you to take photos of your food?",
    "How likely are you to post about a trip while still on it?",
    "How likely are you to wait until you are home to post?",
    "How likely are you to prefer texting over calling?",
    "How likely are you to let the phone ring and text back later?",
    "How likely are you to answer unknown numbers?",
    "How likely are you to use speakerphone in public?",
    "How likely are you to wear headphones to avoid small talk?",
    "How likely are you to chat with cashiers or baristas?",
    "How likely are you to tip generously?",
    "How likely are you to split a bill evenly no matter who ordered what?",
    "How likely are you to offer to pay for the whole table?",
    "How likely are you to save seats for friends who are late?",
    "How likely are you to give up your seat for someone else?",
    "How likely are you to hold the elevator?",
    "How likely are you to press the close-door button repeatedly?",
    "How likely are you to take the stairs when an elevator is right there?",
    "How likely are you to jaywalk?",
    "How likely are you to wait for the walk signal?",
    "How likely are you to speed up to make a yellow light?",
    "How likely are you to let someone merge in traffic?",
    "How likely are you to honk out of frustration?",
    "How likely are you to listen to the same song on repeat?",
    "How likely are you to judge a book by its cover?",
    "How likely are you to finish a series just to see the ending?",
    "How likely are you to walk out of a bad movie?",
    "How likely are you to read the menu online before arriving?",
    "How likely are you to order the same meal at a favorite restaurant?",
    "How likely are you to try the special you cannot pronounce?",
    "How likely are you to ask for substitutions?",
    "How likely are you to finish a plate even when full?",
    "How likely are you to take leftovers home?",
    "How likely are you to cook when you could order delivery?",
    "How likely are you to meal prep for the week?",
    "How likely are you to eat breakfast?",
    "How likely are you to skip lunch when busy?",
    "How likely are you to snack instead of eating a real meal?",
    "How likely are you to drink water before coffee?",
    "How likely are you to need caffeine to function in the morning?",
    "How likely are you to stay up too late despite being tired?",
    "How likely are you to nap when you have things to do?",
    "How likely are you to set multiple alarms?",
    "How likely are you to wake up before your alarm?",
    "How likely are you to hit snooze more than once?",
    "How likely are you to sleep with a fan or white noise?",
    "How likely are you to need complete darkness to sleep?",
    "How likely are you to scroll on your phone in bed?",
    "How likely are you to read before sleep?",
    "How likely are you to fall asleep during a movie?",
    "How likely are you to cry at a wedding?",
    "How likely are you to dance at weddings?",
    "How likely are you to give a toast when asked?",
    "How likely are you to avoid public speaking?",
    "How likely are you to volunteer answers in class or meetings?",
    "How likely are you to ask questions when confused?",
    "How likely are you to pretend you understood something?",
    "How likely are you to take notes by hand?",
    "How likely are you to color-code your notes or calendar?",
    "How likely are you to finish a project the night before it is due?",
    "How likely are you to start early and finish early?",
    "How likely are you to work better under pressure?",
    "How likely are you to clean before guests arrive?",
    "How likely are you to hide clutter in a closet before guests arrive?",
    "How likely are you to notice dust before guests do?",
    "How likely are you to rearrange furniture for a fresh feel?",
    "How likely are you to keep sentimental items you never use?",
    "How likely are you to donate clothes you still kind of like?",
    "How likely are you to fix something instead of replacing it?",
    "How likely are you to call a professional for home repairs?",
    "How likely are you to read reviews before every purchase?",
    "How likely are you to buy the extended warranty?",
    "How likely are you to regift something?",
    "How likely are you to write thank-you notes?",
    "How likely are you to remember to send a birthday message?",
    "How likely are you to prefer gifts you can use?",
    "How likely are you to prefer gifts with sentimental value?",
    "How likely are you to cry when saying goodbye at an airport?",
    "How likely are you to feel homesick on long trips?",
    "How likely are you to talk to seatmates on flights?",
    "How likely are you to use vacation days as soon as you earn them?",
    "How likely are you to hoard vacation days?",
    "How likely are you to plan every hour of a trip?",
    "How likely are you to wander with no plan on vacation?",
    "How likely are you to learn basic phrases before visiting a country?",
    "How likely are you to eat only familiar food while traveling?",
    "How likely are you to wake up early on vacation?",
    "How likely are you to sleep in on vacation every day?",
    "How likely are you to exercise on vacation?",
    "How likely are you to bring workout clothes you never use?",
    "How likely are you to feel competitive in casual games?",
    "How likely are you to let a child win on purpose?",
    "How likely are you to replay a game immediately after losing?",
    "How likely are you to read the rulebook before playing?",
    "How likely are you to house-rule a board game?",
    "How likely are you to prefer cooperative games over competitive ones?",
    "How likely are you to cheat in a friendly game?",
    "How likely are you to call out friendly cheating?",
    "How likely are you to keep score even when no one asked?",
    "How likely are you to forget the score on purpose?",
    "How likely are you to be the rule lawyer at game night?",
    "How likely are you to teach a game patiently?",
    "How likely are you to get impatient teaching rules?",
    "How likely are you to prefer short games over long ones?",
    "How likely are you to stay for one more round?",
    "How likely are you to be the last one to leave a party?",
    "How likely are you to leave a party without saying goodbye to everyone?",
    "How likely are you to ghost a group plan?",
    "How likely are you to commit to plans you are unsure about?",
    "How likely are you to cancel plans when something better comes up?",
    "How likely are you to reschedule instead of cancel?",
    "How likely are you to be the planner in your friend group?",
    "How likely are you to go along with whatever the group picks?",
    "How likely are you to suggest a new restaurant?",
    "How likely are you to order for the table if no one decides?",
    "How likely are you to split a dessert?",
    "How likely are you to get your own dessert?",
    "How likely are you to share passwords with a partner?",
    "How likely are you to keep some thoughts completely private?",
    "How likely are you to journal your feelings?",
    "How likely are you to talk through problems with friends?",
    "How likely are you to process emotions alone first?",
    "How likely are you to forgive yourself quickly?",
    "How likely are you to dwell on mistakes?",
    "How likely are you to ask for feedback at work or school?",
    "How likely are you to take criticism personally?",
    "How likely are you to celebrate others' wins genuinely?",
    "How likely are you to compare yourself to people online?",
    "How likely are you to take social media breaks?",
    "How likely are you to post about causes you care about?",
    "How likely are you to argue in comment sections?",
    "How likely are you to mute politics online?",
    "How likely are you to read long articles past the headline?",
    "How likely are you to listen to podcasts at faster speed?",
    "How likely are you to watch videos at double speed?",
    "How likely are you to finish every season you start?",
    "How likely are you to have multiple shows going at once?",
    "How likely are you to rewatch comfort shows?",
    "How likely are you to avoid horror movies?",
    "How likely are you to enjoy being scared on purpose?",
    "How likely are you to cover your eyes during scary scenes?",
    "How likely are you to read the plot summary before watching?",
    "How likely are you to avoid spoilers at all costs?",
    "How likely are you to recommend something you just discovered?",
    "How likely are you to gatekeep a favorite band or show?",
    "How likely are you to learn lyrics to songs you like?",
    "How likely are you to dance when no one is watching?",
    "How likely are you to dance when everyone is watching?",
    "How likely are you to sing along even when you do not know the words?",
    "How likely are you to play an instrument?",
    "How likely are you to wish you had learned an instrument younger?",
    "How likely are you to pick up hobbies in bursts?",
    "How likely are you to stick with one hobby for years?",
    "How likely are you to have unfinished craft projects?",
    "How likely are you to finish every DIY project you start?",
    "How likely are you to ask for help with assembly instructions?",
    "How likely are you to have extra screws after building furniture?",
    "How likely are you to read product manuals cover to cover?",
    "How likely are you to label storage boxes clearly?",
    "How likely are you to know exactly where your important documents are?",
    "How likely are you to misplace your wallet or bag weekly?",
    "How likely are you to pat your pockets before leaving?",
    "How likely are you to turn around mid-commute because you forgot something?",
    "How likely are you to pack the night before a trip?",
    "How likely are you to pack an hour before leaving?",
    "How likely are you to overprepare for bad weather?",
    "How likely are you to risk it without a jacket?",
    "How likely are you to trust the weather forecast completely?",
    "How likely are you to dress in layers no matter the forecast?",
    "How likely are you to wear sunglasses indoors?",
    "How likely are you to match socks deliberately?",
    "How likely are you to wear mismatched socks on purpose?",
    "How likely are you to keep clothes that no longer fit?",
    "How likely are you to donate clothes every season?",
    "How likely are you to buy clothes for who you want to be?",
    "How likely are you to buy clothes for comfort only?",
    "How likely are you to iron or steam clothes before wearing?",
    "How likely are you to wear wrinkled clothes without caring?",
    "How likely are you to notice fashion trends?",
    "How likely are you to keep the same style for years?",
    "How likely are you to compliment someone's outfit?",
    "How likely are you to remember people's clothing details?",
    "How likely are you to feel nervous before a first date?",
    "How likely are you to Google someone before meeting them?",
    "How likely are you to believe love at first sight?",
    "How likely are you to believe opposites attract?",
    "How likely are you to stay friends with exes?",
    "How likely are you to need alone time in a relationship?",
    "How likely are you to share everything with a partner?",
    "How likely are you to prefer quality time over gifts?",
    "How likely are you to prefer acts of service over words?",
    "How likely are you to say I love you first?",
    "How likely are you to wait for the other person to say it first?",
    "How likely are you to believe people can really change?",
    "How likely are you to give second chances?",
    "How likely are you to cut people off after one betrayal?",
    "How likely are you to stay loyal to friends from childhood?",
    "How likely are you to make friends easily as an adult?",
    "How likely are you to keep in touch with old classmates?",
    "How likely are you to be the friend who checks in first?",
    "How likely are you to wait for others to reach out?",
    "How likely are you to remember important dates without reminders?",
    "How likely are you to rely on calendar alerts for everything?",
    "How likely are you to be the emotional support friend?",
    "How likely are you to vent to friends often?",
    "How likely are you to offer advice when friends vent?",
    "How likely are you to just listen without fixing?",
    "How likely are you to feel drained after socializing?",
    "How likely are you to feel energized after socializing?",
    "How likely are you to need recovery time after big events?",
    "How likely are you to say yes to last-minute invites?",
    "How likely are you to prefer plans made days ahead?",
    "How likely are you to enjoy being the center of attention?",
    "How likely are you to avoid the spotlight?",
    "How likely are you to remember names after one introduction?",
    "How likely are you to reintroduce yourself because you forgot a name?",
    "How likely are you to feel awkward in elevators with strangers?",
    "How likely are you to make small talk in elevators?",
    "How likely are you to trust your gut over logic?",
    "How likely are you to need data before deciding?",
    "How likely are you to regret impulse purchases?",
    "How likely are you to return impulse purchases?",
    "How likely are you to stick to a shopping list?",
    "How likely are you to shop hungry and buy extras?",
    "How likely are you to try store samples?",
    "How likely are you to buy the checkout-line item?",
    "How likely are you to use coupons or loyalty apps?",
    "How likely are you to pay extra for convenience?",
    "How likely are you to choose generic brands?",
    "How likely are you to swear by one brand forever?",
    "How likely are you to read nutrition labels?",
    "How likely are you to eat organic when possible?",
    "How likely are you to skip meals when focused?",
    "How likely are you to stress-eat?",
    "How likely are you to lose appetite when stressed?",
    "How likely are you to exercise when stressed?",
    "How likely are you to skip workouts when busy?",
    "How likely are you to stretch daily?",
    "How likely are you to go to bed sore from sitting all day?",
    "How likely are you to take the long way for extra steps?",
    "How likely are you to track steps or workouts?",
    "How likely are you to compete with friends on fitness apps?",
    "How likely are you to try extreme sports?",
    "How likely are you to prefer gentle exercise?",
    "How likely are you to get competitive at the gym?",
    "How likely are you to compare your progress to others?",
    "How likely are you to celebrate personal records quietly?",
    "How likely are you to post workout achievements?",
    "How likely are you to believe you are a good driver?",
    "How likely are you to get road rage?",
    "How likely are you to sing along loudly while driving?",
    "How likely are you to talk on the phone while driving?",
    "How likely are you to let the tank run nearly empty?",
    "How likely are you to fill up at half a tank?",
    "How likely are you to wash your car regularly?",
    "How likely are you to ignore dashboard warning lights briefly?",
    "How likely are you to read every notification immediately?",
    "How likely are you to use Do Not Disturb often?",
    "How likely are you to keep your phone on the table during meals?",
    "How likely are you to put your phone away during conversations?",
    "How likely are you to feel naked without your phone?",
    "How likely are you to enjoy a full day without your phone?",
    "How likely are you to panic if you leave your charger behind?",
    "How likely are you to carry a portable battery?",
    "How likely are you to update apps right away?",
    "How likely are you to ignore software updates for months?",
    "How likely are you to customize your home screen?",
    "How likely are you to use default settings for everything?",
    "How likely are you to back up your photos?",
    "How likely are you to lose photos because you did not back up?",
    "How likely are you to use the same password everywhere?",
    "How likely are you to use unique passwords?",
    "How likely are you to enable two-factor authentication?",
    "How likely are you to click suspicious links by accident?",
    "How likely are you to fall for a harmless prank online?",
    "How likely are you to enjoy pranking friends?",
    "How likely are you to hate being pranked?",
    "How likely are you to plan elaborate surprises?",
    "How likely are you to spoil surprises by accident?",
    "How likely are you to keep a straight face when you know a secret?",
    "How likely are you to blurt secrets when excited?",
    "How likely are you to believe white lies are sometimes kind?",
    "How likely are you to always tell the full truth?",
    "How likely are you to avoid hurting feelings even if it means bending truth?",
    "How likely are you to value honesty over harmony?",
    "How likely are you to mediate arguments between friends?",
    "How likely are you to walk away from drama?",
    "How likely are you to stir drama without meaning to?",
    "How likely are you to be the peacemaker in your family?",
    "How likely are you to take sides in family disputes?",
    "How likely are you to enjoy family reunions?",
    "How likely are you to dread large family gatherings?",
    "How likely are you to get along with in-laws or partner's family?",
    "How likely are you to prefer holidays with friends over family?",
    "How likely are you to host holidays?",
    "How likely are you to travel for holidays every year?",
    "How likely are you to keep childhood traditions alive?",
    "How likely are you to invent new traditions as an adult?",
    "How likely are you to decorate early for holidays?",
    "How likely are you to decorate at the last minute?",
    "How likely are you to love gift wrapping?",
    "How likely are you to use gift bags to save time?",
    "How likely are you to save nice wrapping paper?",
    "How likely are you to tear wrapping paper aggressively?",
    "How likely are you to regift thoughtfully?",
    "How likely are you to keep gifts you will never use out of guilt?",
    "How likely are you to donate unused gifts?",
    "How likely are you to write wish lists?",
    "How likely are you to prefer surprise gifts?",
    "How likely are you to ask people what they want?",
    "How likely are you to remember what people like as gifts?",
    "How likely are you to procrastinate on gift shopping?",
    "How likely are you to buy gifts months early?",
    "How likely are you to feel competitive about gift-giving?",
    "How likely are you to prefer experiences over things?",
    "How likely are you to take photos instead of living the moment?",
    "How likely are you to put your phone away at concerts?",
    "How likely are you to know every lyric at a concert?",
    "How likely are you to arrive early to get a good spot?",
    "How likely are you to show up fashionably late?",
    "How likely are you to stay until the very end?",
    "How likely are you to leave before the encore?",
    "How likely are you to clap along even when you cannot keep rhythm?",
    "How likely are you to tear up at live performances?",
    "How likely are you to prefer museums alone?",
    "How likely are you to read every plaque in a museum?",
    "How likely are you to speed-walk through exhibits?",
    "How likely are you to visit tourist landmarks every trip?",
    "How likely are you to skip famous spots to avoid crowds?",
    "How likely are you to talk to locals for recommendations?",
    "How likely are you to eat only at highly rated places?",
    "How likely are you to try street food?",
    "How likely are you to get food poisoning fear but try anyway?",
    "How likely are you to pack snacks from home when traveling?",
    "How likely are you to buy souvenirs for everyone?",
    "How likely are you to buy souvenirs only for yourself?",
    "How likely are you to collect something when you travel?",
    "How likely are you to travel light with one bag?",
    "How likely are you to bring a book you never open on trips?",
    "How likely are you to finish a book on vacation?",
    "How likely are you to learn something new every year?",
    "How likely are you to feel stuck in your routines?",
    "How likely are you to reinvent yourself after a big life change?",
    "How likely are you to keep the same friend group forever?",
    "How likely are you to outgrow old friendships naturally?",
    "How likely are you to reach out to someone you miss first?",
    "How likely are you to assume others will contact you?",
    "How likely are you to feel like the responsible one in the group?",
    "How likely are you to feel like the chaotic one in the group?",
    "How likely are you to be the friend who remembers everyone's orders?",
    "How likely are you to forget what you wanted to order?",
    "How likely are you to tip on takeout?",
    "How likely are you to stiffen up during massages?",
    "How likely are you to fall asleep during relaxing activities?",
    "How likely are you to need background noise to focus?",
    "How likely are you to need silence to focus?",
    "How likely are you to work with music that has lyrics?",
    "How likely are you to use instrumental music only?",
    "How likely are you to clean while listening to podcasts?",
    "How likely are you to leave cleaning until you cannot ignore it?",
    "How likely are you to clean in one big session?",
    "How likely are you to clean a little every day?",
    "How likely are you to notice when a room smells off?",
    "How likely are you to burn food while multitasking?",
    "How likely are you to set timers when cooking?",
    "How likely are you to wing it with spices?",
    "How likely are you to follow recipes exactly?",
    "How likely are you to substitute ingredients confidently?",
    "How likely are you to panic if you are missing one ingredient?",
    "How likely are you to invite people over when the house is messy?",
    "How likely are you to cancel because the house is not ready?",
    "How likely are you to feel proud of small home improvements?",
    "How likely are you to compare your home to others online?",
    "How likely are you to enjoy home improvement shows?",
    "How likely are you to start projects you cannot finish?",
    "How likely are you to hire help instead of DIY?",
    "How likely are you to watch tutorial videos before trying?",
    "How likely are you to learn by breaking things first?",
    "How likely are you to read comments for hidden tips?",
    "How likely are you to trust online reviews completely?",
    "How likely are you to write reviews after good experiences?",
    "How likely are you to write reviews only after bad experiences?",
    "How likely are you to return to businesses that messed up once?",
    "How likely are you to hold grudges against brands?",
    "How likely are you to forgive bad service if the food was great?",
    "How likely are you to choose loyalty over trying new places?",
    "How likely are you to be the first to try a new restaurant?",
    "How likely are you to stick to two or three safe restaurants?",
    "How likely are you to order the weirdest item on the menu?",
    "How likely are you to ask the server for recommendations?",
    "How likely are you to lie that you like a meal you cooked for others?",
    "How likely are you to admit a recipe experiment failed?",
    "How likely are you to take pride in a simple meal done well?",
    "How likely are you to think you could win a cooking competition?",
    "How likely are you to think you could win a trivia night?",
    "How likely are you to shout answers at the TV during quizzes?",
    "How likely are you to guess confidently when unsure?",
    "How likely are you to stay quiet when unsure?",
    "How likely are you to bluff in casual games?",
    "How likely are you to call someone's bluff?",
    "How likely are you to enjoy strategy more than luck?",
    "How likely are you to enjoy luck more than strategy?",
    "How likely are you to believe you are unlucky?",
    "How likely are you to believe you are lucky?",
    "How likely are you to knock on wood after saying something good?",
    "How likely are you to feel uneasy about jinxing good news?",
    "How likely are you to celebrate small wins out loud?",
    "How likely are you to downplay your achievements?",
    "How likely are you to feel impostor syndrome at work or school?",
    "How likely are you to feel confident in your abilities?",
    "How likely are you to ask dumb questions on purpose?",
    "How likely are you to pretend you knew something all along?",
    "How likely are you to enjoy learning in public?",
    "How likely are you to hide when you are struggling?",
    "How likely are you to ask for help before you are desperate?",
    "How likely are you to offer help before being asked?",
    "How likely are you to feel annoyed when help is unsolicited?",
    "How likely are you to appreciate tough love?",
    "How likely are you to prefer gentle encouragement?",
    "How likely are you to motivate yourself with deadlines?",
    "How likely are you to motivate yourself with rewards?",
    "How likely are you to stick to habits for a full month?",
    "How likely are you to abandon habits after a week?",
    "How likely are you to restart habits after breaking them?",
    "How likely are you to feel guilty breaking a streak?",
    "How likely are you to not care about streaks at all?",
    "How likely are you to track habits in an app?",
    "How likely are you to rely on memory alone?",
    "How likely are you to believe willpower is enough?",
    "How likely are you to believe systems beat willpower?",
    "How likely are you to enjoy self-help content?",
    "How likely are you to roll your eyes at self-help content?",
    "How likely are you to recommend books that changed your thinking?",
    "How likely are you to finish self-help books?",
    "How likely are you to highlight or annotate books?",
    "How likely are you to lend books you care about?",
    "How likely are you to never get lent books back?",
    "How likely are you to buy books you never read?",
    "How likely are you to use the library for everything?",
    "How likely are you to judge people by their bookshelves?",
    "How likely are you to display books for looks?",
    "How likely are you to read before bed every night?",
    "How likely are you to fall asleep reading?",
    "How likely are you to read multiple books at once?",
    "How likely are you to finish one book before starting another?",
    "How likely are you to dog-ear library books?",
    "How likely are you to return library books late?",
    "How likely are you to pay fines without complaining?",
    "How likely are you to argue a late fee?",
    "How likely are you to feel personally attacked by fine print?",
    "How likely are you to read fine print for fun?",
    "How likely are you to sign up for free trials and cancel in time?",
    "How likely are you to forget and pay for subscriptions?",
    "How likely are you to audit subscriptions yearly?",
    "How likely are you to share streaming passwords?",
    "How likely are you to pay for your own accounts only?",
    "How likely are you to feel strongly about piracy?",
    "How likely are you to look the other way on gray-area downloads?",
    "How likely are you to pay artists directly when you can?",
    "How likely are you to tip creators online?",
    "How likely are you to believe kindness is your core trait?",
    "How likely are you to believe competence is your core trait?",
    "How likely are you to believe humor is your core trait?",
    "How likely are you to believe reliability is your core trait?",
]


def score_personal(item: str) -> float:
    lower = item.lower()
    score = 50.0
    if lower.startswith("how much do you enjoy"):
        score -= 12
    if lower.startswith("how good are you at"):
        score -= 4
    if "board game" in lower or "lazy" in lower or "gossip" in lower:
        score += 10
    if "phone" in lower or "procrastinat" in lower or "honest" in lower:
        score += 8
    if "sore loser" in lower or "dramatic" in lower or "stubborn" in lower:
        score += 9
    if lower.count("how calm are you") > 0:
        score -= 3
    if len(item) < 45:
        score += 3
    return score


SPECTRUM_PIN = [
    ("Hot", "Cold"),
    ("Overrated", "Underrated"),
    ("City life", "Country life"),
    ("Early bird", "Night owl"),
    ("Dog person", "Cat person"),
    ("Icebreaker", "Conversation ender"),
    ("Healthy choice", "Indulgent choice"),
    ("Formal event", "Casual hangout"),
    ("Window seat", "Aisle seat"),
    ("Text message", "Phone call"),
    ("Board game", "Video game"),
    ("Home cooking", "Restaurant meal"),
    ("Camping trip", "Hotel stay"),
    ("Beach vacation", "Mountain vacation"),
    ("Fiction book", "Nonfiction book"),
    ("Live music", "Recorded music"),
    ("Team sport", "Individual sport"),
    ("Ask for help", "Figure it out alone"),
    ("Digital detox", "Always connected"),
    ("Gift experiences", "Gift objects"),
    ("Harmless prank", "Cruel joke"),
    ("Time saver", "Time waster"),
    ("Stress relief", "Stress cause"),
    ("Low effort", "High effort"),
    ("Too spicy", "Too bland"),
    ("Too loud", "Too quiet"),
    ("Planned trip", "Spontaneous trip"),
    ("Minimal home", "Cozy clutter"),
    ("Eco-friendly", "Convenient"),
    ("Remote work", "Office work"),
    ("Video call", "In-person meeting"),
    ("Try new food", "Stick to favorites"),
    ("Repair item", "Replace item"),
    ("Cook from scratch", "Use shortcuts"),
    ("Group travel", "Solo travel"),
    ("Physical book", "E-book"),
    ("Dark mode", "Light mode"),
    ("Multitask", "Single task"),
    ("Hot shower", "Cold rinse"),
    ("DIY repair", "Call a pro"),
    ("Big party", "Small dinner"),
    ("Quiet library", "Busy cafe"),
    ("Strategy game", "Luck game"),
    ("Apologize first", "Wait for apology"),
    ("Stay late at party", "Leave early"),
    ("Morning news", "Morning music"),
    ("Sandwich", "Wrap"),
    ("Pancake", "Waffle"),
    ("Tea person", "Coffee person"),
    ("Sunrise watch", "Sunset watch"),
    ("Forest walk", "Beach walk"),
    ("Comedy show", "Drama show"),
]

SPECTRUM_NEW = [
    ("Cheap thrill", "Expensive hobby"),
    ("Loud restaurant", "Quiet restaurant"),
    ("Structured game", "Open-ended game"),
    ("Bookstore browse", "Online checkout"),
    ("Spontaneous gift", "Planned gift"),
    ("DIY haircut", "Salon cut"),
    ("Home movie night", "Theater night"),
    ("Open headphones", "Noise canceling"),
    ("Group photo", "Solo selfie"),
    ("Window open", "Window closed"),
    ("Firm mattress", "Soft mattress"),
    ("Fresh pizza", "Reheated pizza"),
    ("Quick shower", "Long bath"),
    ("Full calendar", "Blank weekend"),
    ("Paper map", "GPS navigation"),
    ("Handwritten list", "Phone notes"),
    ("Road trip music", "Drive podcast"),
    ("Comedy podcast", "True crime podcast"),
    ("Fancy coffee", "Instant coffee"),
    ("Meal kit", "Takeout order"),
    ("Farmers market", "Supermarket run"),
    ("Sunrise jog", "Sunset stroll"),
    ("Gym class", "Solo run"),
    ("Public praise", "Private thanks"),
    ("Detailed itinerary", "Rough outline"),
    ("Pack snacks", "Buy on the road"),
    ("Hotel buffet", "Corner café"),
    ("Museum guide", "Wander freely"),
    ("Theme park ride", "Nature trail"),
    ("Chocolate dessert", "Fruit dessert"),
    ("Classic board game", "Party card game"),
    ("Indie film", "Blockbuster"),
    ("Thrift find", "Brand new"),
    ("Shared appetizer", "Own entree"),
    ("Window shopping", "Purpose trip"),
    ("Camping stove meal", "Restaurant splurge"),
    ("Early checkout", "Late checkout"),
    ("Car karaoke", "Quiet drive"),
    ("Photo album", "Camera roll only"),
    ("Handwritten letter", "Quick text"),
    ("Board game teach", "Jump right in"),
    ("Strict budget", "Treat yourself"),
    ("Rainy day indoors", "Sunny day outdoors"),
    ("Morning workout", "Evening workout"),
    ("Cook for crowd", "Cook for one"),
    ("Learn by doing", "Learn by watching"),
    ("Keep mystery", "Spoil the ending"),
    ("Talk it out", "Sleep on it"),
    ("Big city noise", "Small town quiet"),
    ("Window plant", "Garden plot"),
]


def score_spectrum(left: str, right: str) -> float:
    score = 50.0
    if left.startswith("Better ") or right.startswith("Better "):
        score -= 10
    if left.startswith("Too ") and right.startswith("Too "):
        score -= 2
    if left.startswith("Low ") or left.startswith("High "):
        score -= 4
    ll, rl = len(left), len(right)
    if ll > 22 or rl > 22:
        score -= 6
    if ll < 16 and rl < 16:
        score += 4
    if "person" in left.lower() or "person" in right.lower():
        score += 6
    return score


def rank_unique(items: list[str], pin: list[str], scorer) -> list[str]:
    seen = set()
    ordered: list[str] = []
    for item in pin:
        if item not in seen:
            seen.add(item)
            ordered.append(item)
    rest = sorted(
        [i for i in items if i not in seen],
        key=lambda x: (-scorer(x), x),
    )
    for item in rest:
        if item not in seen:
            seen.add(item)
            ordered.append(item)
    return ordered


def rank_spectrums(pairs: list[dict], pin: list[tuple[str, str]], extra: list[tuple[str, str]]) -> list[dict]:
    existing = [(p["left"], p["right"]) for p in pairs]
    all_pairs = list(pin)
    seen = {(a.lower(), b.lower()) for a, b in all_pairs}
    seen |= {(b.lower(), a.lower()) for a, b in all_pairs}
    for src in extra + existing:
        key = (src[0].lower(), src[1].lower())
        rev = (src[1].lower(), src[0].lower())
        if key in seen or rev in seen:
            continue
        seen.add(key)
        all_pairs.append(src)
    pin_set = {(a.lower(), b.lower()) for a, b in pin}
    pin_set |= {(b.lower(), a.lower()) for a, b in pin}
    pinned = [p for p in all_pairs if (p[0].lower(), p[1].lower()) in pin_set or (p[1].lower(), p[0].lower()) in pin_set]
    pin_order = {p: i for i, p in enumerate(pin)}
    pinned.sort(
        key=lambda p: pin_order.get(p, pin_order.get((p[1], p[0]), 999)),
    )
    rest = [p for p in all_pairs if p not in pinned]
    rest.sort(key=lambda p: (-score_spectrum(p[0], p[1]), p[0], p[1]))
    ordered = pinned + rest
    return [{"left": l, "right": r} for l, r in ordered]


def yaml_quote(s: str) -> str:
    if re.search(r'[:#\[\]{},&*?|>!%@`]', s) or s.strip() != s:
        return '"' + s.replace('"', '\\"') + '"'
    return s


def dump_items(items: list[str]) -> str:
    return "\n".join(f"  - {yaml_quote(i)}" for i in items)


def dump_spectrums(pairs: list[dict]) -> str:
    lines = []
    for p in pairs:
        lines.append(f"  - left: {yaml_quote(p['left'])}")
        lines.append(f"    right: {yaml_quote(p['right'])}")
    return "\n".join(lines)


def replace_collection_block(text: str, col_id: str, new_block: str) -> str:
    pattern = rf"(- id: {re.escape(col_id)}\n.*?)(?=\n- id: |\Z)"
    if not re.search(pattern, text, flags=re.S):
        raise SystemExit(f"missing collection {col_id}")
    return re.sub(pattern, new_block.rstrip() + "\n", text, count=1, flags=re.S)


def main():
    data = yaml.safe_load(YAML.read_text())
    text = YAML.read_text()
    cols = {c["id"]: c for c in data["collections"]}

    scale = rank_unique(cols["scale-clues"]["items"], SCALE_CLUES_PIN, score_scale_clue)[:TARGET]
    personal_pool = cols["personal-scales"]["items"] + PERSONAL_NEW
    personal = rank_unique(personal_pool, PERSONAL_PIN, score_personal)[:TARGET]
    spectrum = rank_spectrums(cols["spectrum"]["spectrums"], SPECTRUM_PIN, SPECTRUM_NEW)[:TARGET]

    assert len(scale) == TARGET, len(scale)
    assert len(personal) == TARGET, len(personal)
    assert len(spectrum) == TARGET, len(spectrum)

    sc = cols["scale-clues"]
    block = (
        f"- id: scale-clues\n"
        f"  title: {sc['title']}\n"
        f"  mode: {sc['mode']}\n"
        f"  tagline: {sc['tagline']}\n"
        f"  play_hint: {sc['play_hint']}\n"
        f"  items:\n{dump_items(scale)}\n"
    )
    text = replace_collection_block(text, "scale-clues", block)

    ps = cols["personal-scales"]
    block = (
        f"- id: personal-scales\n"
        f"  title: {ps['title']}\n"
        f"  mode: {ps['mode']}\n"
        f"  tagline: {ps['tagline']}\n"
        f"  play_hint: {ps['play_hint']}\n"
        f"  scale_label: {ps['scale_label']}\n"
        f"  items:\n{dump_items(personal)}\n"
    )
    text = replace_collection_block(text, "personal-scales", block)

    sp = cols["spectrum"]
    block = (
        f"- id: spectrum\n"
        f"  title: {sp['title']}\n"
        f"  mode: {sp['mode']}\n"
        f"  tagline: {sp['tagline']}\n"
        f"  play_hint: {sp['play_hint']}\n"
        f"  spectrums:\n{dump_spectrums(spectrum)}\n"
    )
    text = replace_collection_block(text, "spectrum", block)

    YAML.write_text(text)
    print(f"scale-clues: {len(scale)} (top: {scale[0][:50]}...)")
    print(f"personal-scales: {len(personal)} (top: {personal[0]})")
    print(f"spectrum: {len(spectrum)} (top: {spectrum[0]['left']} | {spectrum[0]['right']})")


if __name__ == "__main__":
    main()
