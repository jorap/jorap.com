#!/usr/bin/env python3
"""Maintain data/randomizer.yaml — build decks, curate rankings, refresh spectrum."""
from __future__ import annotations

import argparse
import re
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
YAML = ROOT / "data" / "randomizer.yaml"
TARGET = 300
SPECTRUM_TARGET = 200

# ponytail: maintainer tool; re-run after bulk prompt/spectrum edits

WYR_META = {
    "id": "would-you-rather",
    "title": "Either-or dilemmas",
    "mode": "ranked-prompts",
    "tagline": "Two options, one choice. Pick a side and say why.",
    "play_hint": (
        "Read both options aloud. Everyone picks one, no middle ground. "
        "Best argument wins."
    ),
}

TABLE_META = {
    "id": "table-topics",
    "title": "Conversation starters",
    "mode": "ranked-prompts",
    "tagline": "Open prompts to swap stories and opinions. No scoring.",
    "play_hint": (
        "Take turns. There is no right answer; stories beat one-word replies."
    ),
}

WYR_ITEMS: list[str] = [
    "Always be ten minutes early, or always be ten minutes late?",
    "Always have perfect weather on vacation, or always get the best seat at home?",
    "Always know the plot of a movie before you watch it, or never know anything about it?",
    "Always laugh at your own jokes, or never laugh at your own jokes?",
    "Always remember names, or always remember faces?",
    "Always sleep eight hours but wake up groggy, or sleep six hours and wake up refreshed?",
    "Always speak your mind, or always think before you speak?",
    "Always win at board games, or always have the most fun losing?",
    "Be able to fly but only two feet off the ground, or be invisible but only when nobody is looking?",
    "Be famous for one amazing thing, or be unknown but great at many things?",
    "Be the funniest person in the room, or the kindest person in the room?",
    "Be the best player on a losing team, or the worst player on a winning team?",
    "Be the first to arrive at every party, or the last to leave every party?",
    "Be the person who plans every trip, or the person who happily follows along?",
    "Be able to talk to animals, or speak every human language fluently?",
    "Be able to pause time for one minute a day, or rewind one minute a day?",
    "Be stuck in summer forever, or stuck in winter forever?",
    "Eat only breakfast foods for a year, or eat only dinner foods for a year?",
    "Eat the same perfect meal every day, or never eat the same meal twice?",
    "Give up music forever, or give up movies forever?",
    "Give up salty snacks forever, or give up sweet snacks forever?",
    "Have a rewind button for conversations, or a pause button for awkward moments?",
    "Have a personal chef, or have a personal driver?",
    "Have a photographic memory for faces, or for places?",
    "Have free flights anywhere forever, or free meals anywhere forever?",
    "Have more free time, or have more spending money?",
    "Have one extra hour every morning, or one extra hour every night?",
    "Have super hearing, or super smell?",
    "Have the ability to find anything you lose, or never lose anything again?",
    "Have unlimited books, or unlimited board games?",
    "Have wifi everywhere you go, or never need wifi again?",
    "Know every language but only read them, or speak one language perfectly but write poorly?",
    "Know the ending of every book before you start, or never know how a story ends?",
    "Live in a house with a huge yard and a small home, or a huge home and no yard?",
    "Live in a treehouse, or live on a houseboat?",
    "Live next door to your best friend, or live next door to your favorite restaurant?",
    "Live without air conditioning, or live without heating?",
    "Lose your phone for a day, or lose your keys for a day?",
    "Never do laundry again, or never wash dishes again?",
    "Never get a mosquito bite again, or never get sunburned again?",
    "Never have to wait in line, or never hit traffic?",
    "Never need an alarm clock, or never feel tired during the day?",
    "Never use a microwave again, or never use an oven again?",
    "Only eat food you cook, or only eat food someone else cooks?",
    "Only listen to one song on repeat for a month, or only listen to new songs for a month?",
    "Only travel by train, or only travel by plane?",
    "Only watch cartoons, or only watch documentaries?",
    "Read minds but only happy thoughts, or read minds but only worried thoughts?",
    "Read one book a week forever, or watch one movie a week forever?",
    "Ride a bike everywhere, or walk everywhere?",
    "Share one bathroom with five tidy people, or have five messy bathrooms to yourself?",
    "Shower in the morning only, or shower at night only?",
    "Sing every time you speak, or dance every time you walk?",
    "Skip every Monday, or skip every Friday?",
    "Sleep in a hammock, or sleep on a giant beanbag?",
    "Talk to your past self for ten minutes, or your future self for ten minutes?",
    "Trade places with your pet for a day, or trade places with your favorite teacher for a day?",
    "Travel to the past for a week, or travel to the future for a week?",
    "Use only pencils, or use only pens?",
    "Wake up early on weekends, or sleep in on weekdays too?",
    "Watch only live sports, or play only sports and never watch them?",
    "Wear formal clothes every day, or wear pajamas every day?",
    "Win a small prize every day, or win one huge prize once?",
    "Always have cold drinks, or always have hot drinks?",
    "Always have snacks in your pocket, or always have tissues in your pocket?",
    "Always hear background music, or always hear gentle ocean sounds?",
    "Always know when someone is lying, or always know when someone needs help?",
    "Always take the scenic route, or always take the fastest route?",
    "Be able to breathe underwater, or be able to survive in extreme cold?",
    "Be able to draw perfectly, or be able to sing perfectly?",
    "Be able to run as fast as a bike, or bike as comfortably as walking?",
    "Be allergic to chocolate, or be allergic to cheese?",
    "Be great at telling stories, or be great at remembering facts?",
    "Be stuck with dial-up internet for a day, or no phone for a day?",
    "Be the captain of every team, or the cheerleader for every team?",
    "Be the best gift-giver, or be the best thank-you-note writer?",
    "Be the person who picks the restaurant, or the person who always enjoys whatever is picked?",
    "Be too hot all the time, or too cold all the time?",
    "Eat dessert before dinner every night, or never eat dessert again?",
    "Eat pizza every Friday, or eat tacos every Tuesday?",
    "Get a surprise party every year, or plan the perfect party for someone else every year?",
    "Get free tickets to every concert, or free passes to every museum?",
    "Give up all social media, or give up all streaming services?",
    "Give up coffee, or give up tea?",
    "Go camping every month, or go to the beach every month?",
    "Go to space for an hour, or explore the deepest ocean trench for an hour?",
    "Have a clone to do chores, or have a robot to do homework?",
    "Have a home library that restocks itself, or a kitchen that cooks one perfect meal daily?",
    "Have a magic backpack that fits anything, or shoes that never wear out?",
    "Have a pet dragon the size of a cat, or a pet elephant the size of a dog?",
    "Have a phone battery that lasts a week, or a car that never needs gas?",
    "Have a room that cleans itself, or laundry that folds itself?",
    "Have a week with no homework, or a week with no chores?",
    "Have an endless supply of your favorite candy, or your favorite fruit?",
    "Have every Friday off school or work, or have every Wednesday off?",
    "Have perfect handwriting, or type twice as fast?",
    "Have snow on your birthday every year, or sunshine on your birthday every year?",
    "Have the world's best memory for birthdays, or for favorite foods?",
    "Have to whisper for a day, or have to speak in rhyme for a day?",
    "Have your favorite meal once a week, or a pretty good meal every day?",
    "Keep one childhood toy forever, or keep one childhood photo album forever?",
    "Know how to fix any bike, or know how to cook any meal?",
    "Know the history of every place you visit, or know the best food in every place you visit?",
    "Live above a bakery, or live above a bookstore?",
    "Live in a city with great public transit, or live in a town where you can bike everywhere?",
    "Live where it rains every afternoon, or where it is sunny every afternoon?",
    "Lose the ability to taste sweet, or lose the ability to taste salty?",
    "Never eat ice cream again, or never eat french fries again?",
    "Never get hiccups again, or never get the hiccups from laughing too hard?",
    "Never have to set an alarm, or never have to charge your devices?",
    "Never step on a LEGO brick again, or never stub your toe again?",
    "Only eat with chopsticks, or only eat with a spoon?",
    "Only play outside games, or only play inside games?",
    "Only use paper maps, or only use voice directions?",
    "Ride a roller coaster every week, or watch fireworks every week?",
    "See every sunrise for a year, or see every sunset for a year?",
    "Share your room with a sibling who is tidy, or have your own room that is always messy?",
    "Shop only at small local stores, or shop only at huge supermarkets?",
    "Speak every language for one day, or play every instrument for one day?",
    "Spend a day as a zookeeper, or spend a day as a park ranger?",
    "Spend a day in the 1800s, or spend a day in the 2200s?",
    "Spend a week without TV, or spend a week without music?",
    "Swap lives with a cartoon character for a day, or with a historical figure for a day?",
    "Take a photo that lasts forever, or take a trip that lasts one perfect day?",
    "Take only baths, or take only showers?",
    "Talk to plants and hear them reply, or talk to books and hear their stories?",
    "Travel by hot-air balloon, or travel by speedboat?",
    "Use only stairs for a month, or only elevators for a month?",
    "Visit every continent once, or revisit your favorite place ten times?",
    "Wake up to birdsong, or wake up to your favorite song?",
    "Watch a movie with no sound, or listen to a movie with no picture?",
    "Wear socks with sandals confidently, or never wear sandals again?",
    "Win a year of free ice cream, or win a year of free movie tickets?",
    "Always find a parking spot, or always find a seat on public transit?",
    "Always get the last slice of pizza, or always get the first fresh batch?",
    "Always have clean socks, or always have a charged phone?",
    "Always have good hair days, or always have good outfit days?",
    "Always know the shortest line at the store, or always know the fastest checkout clerk?",
    "Be able to jump as high as a basketball hoop, or run as fast as a scooter?",
    "Be able to talk to babies and understand them, or talk to grandparents and hear their best stories?",
    "Be famous on a talent show, or be famous for helping your community?",
    "Be the best at charades, or be the best at riddles?",
    "Be the designated photographer, or be the person who never appears in photos?",
    "Be the friend who remembers birthdays, or the friend who always brings snacks?",
    "Be the teacher's helper for a day, or the coach's helper for a day?",
    "Be too tall for doorways, or too short to reach top shelves?",
    "Bring lunch from home every day, or eat cafeteria food every day?",
    "Build the world's tallest sandcastle, or find the coolest seashell on the beach?",
    "Camp in the mountains, or camp by the ocean?",
    "Carry a huge umbrella always, or never need an umbrella?",
    "Celebrate every holiday twice, or invent one new holiday each year?",
    "Clean your room in five minutes magically, or keep it tidy without thinking?",
    "Climb a real mountain, or kayak a real river?",
    "Cook one meal perfectly, or bake one dessert perfectly?",
    "Dance in public without embarrassment, or sing karaoke without embarrassment?",
    "Discover a new planet, or discover a new species in your backyard?",
    "Do homework in half the time, or chores in half the time?",
    "Drink only smoothies for a week, or only soup for a week?",
    "Eat breakfast for every meal, or dinner for every meal?",
    "Explore a cave, or explore a coral reef?",
    "Find a hidden door in your house, or find a secret garden behind your school?",
    "Fix any broken toy, or build any toy from scratch?",
    "Fly a kite in a storm safely, or sail a boat on a calm lake?",
    "Get a hundred small compliments, or one huge heartfelt compliment?",
    "Get free popcorn at every movie, or free toppings on every ice cream?",
    "Get stickers on every assignment, or get high-fives from every teacher?",
    "Give up video games for a month, or give up board games for a month?",
    "Go on a road trip with no map, or go on a road trip with a strict schedule?",
    "Go to bed at sunset, or go to bed at midnight every night?",
    "Grow the perfect garden, or grow the perfect treehouse?",
    "Have a birthday party every month, or one epic birthday party every year?",
    "Have a bubble machine follow you, or have confetti fall when you enter a room?",
    "Have a friendly ghost as a roommate, or a friendly robot as a roommate?",
    "Have a magic eraser for mistakes, or a magic pencil that never dulls?",
    "Have a pet that can talk, or a plant that gives advice?",
    "Have a slide instead of stairs at home, or a trampoline in the living room?",
    "Have a snow day every week in winter, or a pool day every week in summer?",
    "Have a tree that grows any fruit you want, or a garden that grows any vegetable?",
    "Have an endless supply of markers, or an endless supply of building blocks?",
    "Have every book read to you by a great narrator, or read every book yourself silently?",
    "Have homework that grades itself, or chores that complete themselves?",
    "Have lunch with your favorite athlete, or lunch with your favorite author?",
    "Have matching outfits with your best friend, or never match accidentally again?",
    "Have more snowball fights, or have more water balloon fights?",
    "Have pancakes every morning, or have waffles every morning?",
    "Have pizza delivered by drone, or by bicycle with a bell choir?",
    "Have super sticky shoes for climbing, or super bouncy shoes for jumping?",
    "Have the best seat at every concert, or meet the band after every show?",
    "Have the loudest laugh in the room, or the most contagious smile?",
    "Have the power to make anyone laugh, or the power to calm anyone down?",
    "Have the world's best tree fort, or the world's best blanket fort?",
    "Have to eat with your non-dominant hand, or write with your non-dominant hand?",
    "Have to wear a cape everywhere, or wear a hat everywhere?",
    "Have unlimited craft supplies, or unlimited sports equipment?",
    "Have your favorite animal as a pet, or your favorite vehicle as a toy?",
    "Hear every song before it is released, or read every book before it is published?",
    "Help build a playground, or help plant a community garden?",
    "Hold a snake calmly, or hold a tarantula calmly?",
    "Host a game show at school, or host a cooking show at home?",
    "Jump into a pile of leaves every day, or jump into a pile of pillows every day?",
    "Keep a diary that writes back, or keep a photo album that plays sounds?",
    "Keep every ticket stub forever, or keep every seashell from every beach?",
    "Learn magic tricks, or learn juggling?",
    "Live in a castle with no heating, or a cabin with perfect heating?",
    "Live in a neighborhood with every friend nearby, or live where the food is amazing?",
    "Live where it snows on holidays, or where it is warm on holidays?",
    "Lose power for a day with candles and board games, or lose internet for a day with books?",
    "Make the world's best paper airplane, or make the world's best origami crane?",
    "Meet a dinosaur safely, or meet an astronaut on the moon safely?",
    "Never brush your teeth again but have perfect teeth, or brush twice daily forever?",
    "Never get lost, or never lose your belongings?",
    "Never run out of hot water, or never run out of battery on game night?",
    "Only drink milkshakes, or only drink lemonade?",
    "Only eat finger foods, or only eat foods you eat with a fork?",
    "Only play team sports, or only play solo sports?",
    "Only read comic books, or only read chapter books?",
    "Only use crayons, or only use colored pencils?",
    "Open a lemonade stand that never runs out, or a bake sale that never runs out?",
    "Paint a mural on your school wall, or paint a mural on your bedroom wall?",
    "Pat a penguin, or feed a giraffe?",
    "Pick teams always, or never have to pick teams?",
    "Play hide-and-seek in a museum after hours, or play tag in a giant mall after hours?",
    "Play in the rain without getting cold, or play in the snow without getting wet?",
    "Play one instrument amazingly, or play every instrument a little?",
    "Play outside until dark every day, or play board games inside until dark every day?",
    "Play the hero in every story, or play the clever sidekick in every story?",
    "Read under the covers with a flashlight, or read in a sunny window seat?",
    "Ride a camel, or ride a horse on the beach?",
    "Ride the tallest slide, or ride the longest zip line?",
    "Run a marathon slowly, or sprint a hundred meters incredibly fast?",
    "See a whale up close, or see the northern lights up close?",
    "See your favorite band live once, or see a great unknown band ten times?",
    "Share one giant pizza, or everyone gets their own personal pizza?",
    "Sing in a choir, or play in a band?",
    "Sit in the front row at a show, or sit in the back with the best view?",
    "Skip rope for an hour, or hula hoop for an hour?",
    "Sleep in a tent every weekend, or sleep in a fancy hotel every weekend?",
    "Slide down a banister safely, or swing on a rope swing over a lake?",
    "Smell every flower in a garden, or taste every fruit in an orchard?",
    "Speak to crowds confidently, or perform on stage confidently?",
    "Spend a day at an amusement park alone, or spend a day at a water park with friends?",
    "Spend a day building with LEGO, or spend a day painting?",
    "Spend a night in a museum, or spend a night on a ship?",
    "Start a club at school, or join every club at school?",
    "Stay up late on New Year's Eve every year, or wake up early for sunrise every New Year?",
    "Swim with dolphins, or snorkel with colorful fish?",
    "Take a horse-drawn carriage ride, or take a gondola ride?",
    "Take the window seat on every flight, or take the aisle seat on every flight?",
    "Talk to your favorite fictional character, or talk to your favorite historical hero?",
    "Throw the best surprise party, or receive the best surprise party?",
    "Trade desserts at lunch every day, or keep your desserts secret?",
    "Travel by camel across a desert, or travel by sled across snow?",
    "Use a time machine once, or use a teleporter once?",
    "Visit a volcano safely, or visit a glacier safely?",
    "Visit every zoo in your country, or visit every national park?",
    "Volunteer at an animal shelter, or volunteer at a food bank?",
    "Wake up to pancakes on your birthday only, or wake up to pancakes every Saturday?",
    "Walk on stilts well, or ride a unicycle well?",
    "Watch a meteor shower every month, or watch a rainbow every week?",
    "Watch cartoons from the 1990s, or watch cartoons made this year?",
    "Watch only funny movies, or watch only adventure movies?",
    "Wear a costume to school every Friday, or wear pajamas to school one day a year?",
    "Wear goggles that see underwater, or boots that walk on water?",
    "Win a spelling bee, or win a science fair?",
    "Win at rock-paper-scissors every time, or win at coin flips every time?",
    "Write a bestselling children's book, or illustrate a bestselling children's book?",
    "Always have perfect picnic weather, or always have perfect stargazing weather?",
    "Always pick the right line at the grocery store, or always pick the ripest fruit?",
    "Be able to smell when cookies are done, or hear when the kettle is ready?",
    "Be friends with someone who tells great jokes, or someone who gives great hugs?",
    "Be the fastest reader in class, or the fastest runner at recess?",
    "Bring your pet to school one day, or bring your favorite toy to show-and-tell every week?",
    "Build a robot that does homework, or build a robot that tells jokes?",
    "Catch every ball in a game, or throw every ball perfectly?",
    "Celebrate your birthday in summer every year, or in winter every year?",
    "Choose the music on every car ride, or choose the snacks on every car ride?",
    "Climb the tallest tree in town, or dive into the deepest pool in town?",
    "Collect stamps, or collect interesting rocks?",
    "Color inside the lines perfectly, or draw freestyle masterpieces?",
    "Compete in a friendly talent show, or host the talent show?",
    "Curl up with a cat, or play fetch with a dog?",
    "Dance in the rain, or build a snowman in fresh snow?",
    "Discover buried treasure in your yard, or discover a time capsule at school?",
    "Drink hot cocoa with marshmallows every day, or iced tea every day?",
    "Eat a giant pretzel at a fair, or eat cotton candy at a fair?",
    "Find a four-leaf clover every week, or find a lucky penny every week?",
    "Get a standing ovation once, or make one person deeply happy every day?",
    "Get free ice cream on hot days, or free hot chocolate on cold days?",
    "Go sledding every winter day, or go swimming every summer day?",
    "Grow flowers that change color, or grow vegetables that taste like dessert?",
    "Have a backpack that organizes itself, or shoes that tie themselves?",
    "Have a birthday cake that never runs out for one party, or candles that never melt?",
    "Have a favorite pen that never runs dry, or a favorite notebook that never fills up?",
    "Have a magic carpet for short trips, or roller skates that work on grass?",
    "Have a phone that translates any language instantly, or a map that shows secret paths?",
    "Have a robot that walks your dog, or a dog that fetches your homework?",
    "Have a secret handshake with your best friend, or a secret code for notes?",
    "Have an extra day off every month, or an extra hour of recess every day?",
    "Have dessert first at every restaurant, or never wait for a table?",
    "Have fireworks on your birthday, or balloons everywhere on your birthday?",
    "Have matching pajamas with your family on holidays, or matching hats?",
    "Have more cousins visit often, or visit more cousins often?",
    "Have perfect eyesight, or perfect hearing?",
    "Have the best Halloween costume every year, or the best Christmas sweater every year?",
    "Have the power to freeze a moment for photos, or rewind one embarrassing moment?",
    "Have unlimited stickers, or unlimited temporary tattoos?",
    "Have your bedroom redecorated magically once a year, or pick one perfect theme forever?",
    "Hear a joke that never gets old, or hear a song that never gets old?",
    "Help animals find homes, or help neighbors with groceries?",
    "Jump on a pogo stick across town, or skateboard across town?",
    "Keep a fish that sings, or a bird that tells jokes?",
    "Learn to surf, or learn to ski?",
    "Live near the ocean, or live near the mountains?",
    "Lose one hour of sleep but gain one hour of play, or keep sleep and lose one hour of play?",
    "Make the world's biggest bubble, or the world's longest domino chain?",
    "Meet every Disney character, or meet every superhero?",
    "Never have a bad hair day at school photos, or never have a stain on your shirt?",
    "Only celebrate birthdays, or only celebrate half-birthdays too?",
    "Only play card games, or only play dice games?",
    "Open presents slowly one by one, or open everything at once?",
    "Paint your room any color weekly, or keep one perfect color forever?",
    "Pat every dog you see, or high-five every kid on your team?",
    "Pick the movie every family night, or pick the snacks every family night?",
    "Play chess with a grandmaster, or play soccer with a pro?",
    "Play in a marching band, or cheer from the best spot in the stadium?",
    "Read five short books, or read one long book?",
    "Ride in a parade float, or ride a fire truck with sirens?",
    "Run a lemonade stand that earns enough for a bike, or a bake sale that earns enough for a trip?",
    "See every animal at the zoo in one day, or spend all day with one favorite animal?",
    "Send a message to the whole world for one minute, or send a private message to anyone in history?",
    "Share your favorite snack with the class, or keep a secret stash forever?",
    "Sing the national anthem at a game, or lead a pep rally?",
    "Sit by the campfire every night, or watch the stars from a rooftop every night?",
    "Sleep in on Sundays only, or sleep in on every school holiday?",
    "Slide into home plate safely every time, or hit a home run once?",
    "Spend a day as principal, or spend a day as lunch chef?",
    "Spend a week on a farm, or spend a week in a big city?",
    "Start every morning with stretches, or start every morning with jokes?",
    "Swim in a lake, or swim in a pool?",
    "Take care of a class pet for a month, or adopt a plant for the classroom?",
    "Take photos that always look professional, or draw pictures that always look professional?",
    "Throw a perfect spiral every time, or catch a perfect spiral every time?",
    "Trade lunches with a friend daily, or always pack the perfect lunch?",
    "Travel by scooter everywhere, or travel by skateboard everywhere?",
    "Visit a lighthouse, or visit a windmill?",
    "Wake up to snow on the ground, or wake up to flowers blooming?",
    "Walk your neighbor's dog, or water your neighbor's plants?",
    "Watch a play on stage, or act in a play on stage?",
    "Watch the sunrise from a hill, or watch the sunset from a pier?",
    "Win a friendly debate, or win a friendly race?",
    "Write with your left hand for a day, or hop on one foot for a day?",
]

TABLE_CATEGORIES: list[dict] = [
    {
        "id": "growing-up",
        "title": "Growing up",
        "items": [
            "A rule from childhood you still follow.",
            "A toy or game you wish you still had.",
            "A smell that instantly takes you back to childhood.",
            "A sound from your neighborhood growing up.",
            "A food you loved as a kid that you still love.",
            "A food you hated as a kid that you like now.",
            "A holiday tradition you looked forward to every year.",
            "A chore you actually did not mind doing.",
            "A chore you tried hard to avoid.",
            "A time you got lost and how it turned out.",
            "A teacher who changed how you see something.",
            "A friend from childhood you still think about.",
            "A playground game you could play for hours.",
            "A birthday party you still remember clearly.",
            "A gift you were thrilled to receive as a kid.",
            "A skill you learned young and still use.",
            "A family road trip story worth retelling.",
            "A time you stood up for someone at school.",
            "A time someone stood up for you.",
            "A book you read over and over as a kid.",
            "A cartoon or show that shaped your sense of humor.",
            "A song your family played on repeat.",
            "A nickname you had and whether you liked it.",
            "A superstition or ritual you had as a kid.",
            "A time you were braver than you expected.",
            "A time you were more scared than you expected.",
            "A pet or animal that was part of your childhood.",
            "A tree, hill, or corner of town that felt like yours.",
            "A time you moved homes or schools and what helped.",
            "A hobby you picked up young and dropped.",
            "A hobby you picked up young and kept.",
            "A time you lied and still feel guilty about.",
            "A time you told the truth when it was hard.",
            "A prize or ribbon you earned and what it meant.",
            "A time you failed at something and tried again.",
            "A time you quit something and were glad you did.",
            "A relative who told the best stories.",
            "A meal that only tasted right at someone's house.",
            "A time you shared a room and what you learned.",
            "A time you had your own space and what you did with it.",
            "A weather day you remember: snow, rain, or heat.",
            "A time you built something with your hands.",
            "A time you broke something and had to fix it.",
            "A time you laughed so hard you could not stop.",
            "A time you cried and who comforted you.",
            "A piece of clothing you wore until it fell apart.",
            "A time you felt proud of a sibling or cousin.",
            "A time you felt jealous of a sibling or cousin.",
            "A school project you still remember.",
            "A time you helped a neighbor without being asked.",
        ],
    },
    {
        "id": "places-travel",
        "title": "Places and travel",
        "items": [
            "A place that surprised you when you finally visited.",
            "A place you would take a visitor on their first day in your town.",
            "A trip that did not go as planned but turned out fine.",
            "A trip that went better than planned.",
            "A city you could wander without a map.",
            "A country you want to visit for the food.",
            "A country you want to visit for nature.",
            "A country you want to visit for history.",
            "A beach memory, good or bad.",
            "A mountain or hill climb worth the effort.",
            "A museum exhibit that stuck with you.",
            "A market or fair you loved browsing.",
            "A long flight story, good seat or bad seat.",
            "A train or bus ride you still remember.",
            "A road trip snack tradition.",
            "A souvenir you actually kept and use.",
            "A souvenir you bought and immediately regretted.",
            "A photo from a trip you still look at.",
            "A place you would return to again and again.",
            "A place you would visit once and never need to return.",
            "A hotel or hostel story.",
            "A camping memory: tent, cabin, or backyard.",
            "A time you got wonderfully lost in a new place.",
            "A local food you tried abroad and loved.",
            "A local food you tried abroad and could not finish.",
            "A language barrier moment that became funny.",
            "A time a stranger was kind while you traveled.",
            "A weather surprise on vacation.",
            "A sunrise or sunset you watched on a trip.",
            "A body of water you swam in and remember.",
            "A hike you would recommend to a friend.",
            "A hike you would not recommend.",
            "A theme park ride you would wait in line for again.",
            "A quiet place you found in a busy city.",
            "A festival or parade you stumbled into.",
            "A border or customs story.",
            "A time you traveled light and were glad.",
            "A time you overpacked and paid for it.",
            "A favorite street to walk with no destination.",
            "A view you would paint if you could.",
            "A place that felt peaceful within an hour.",
            "A place that felt overwhelming at first.",
            "A national park or protected area you loved.",
            "A small town that charmed you.",
            "A big city that energized you.",
            "A travel mistake that taught you something.",
            "A travel tip you give everyone.",
            "A place you visited as a kid you want your kids to see.",
            "A bucket-list trip you have not done yet.",
            "A trip you would repeat exactly as it happened.",
        ],
    },
    {
        "id": "food-kitchen",
        "title": "Food and kitchen",
        "items": [
            "A dish you could eat every week without getting tired of it.",
            "A dish you only want on special occasions.",
            "A recipe someone taught you that you still make.",
            "A recipe you ruined the first time you tried.",
            "A food that smells better than it tastes for you.",
            "A food that tastes better than it smells for you.",
            "A comfort food when you are sick.",
            "A comfort food when you are celebrating.",
            "A snack you hide from other people.",
            "A snack you happily share with everyone.",
            "A restaurant you would recommend to anyone.",
            "A restaurant you would not send your worst enemy to.",
            "A street food you would travel for.",
            "A breakfast you could eat any time of day.",
            "A dinner that always makes you sleepy.",
            "A dessert you cannot resist.",
            "A dessert you do not understand the hype for.",
            "A fruit you wait for in season.",
            "A vegetable you learned to like as an adult.",
            "A spice or sauce that changed your cooking.",
            "A kitchen tool you use more than people expect.",
            "A kitchen tool you bought and never use.",
            "A cooking smell that makes a house feel like home.",
            "A food from another culture you love.",
            "A food combination that sounds weird but works.",
            "A food you eat in a specific way every time.",
            "A drink order that says something about you.",
            "A potluck dish you are known for.",
            "A potluck dish you avoid bringing.",
            "A time you cooked for someone and they loved it.",
            "A time you cooked for someone and it went wrong.",
            "A meal you ate alone and enjoyed.",
            "A meal you shared that felt special.",
            "A picnic that was perfect.",
            "A picnic that was a disaster.",
            "A food you tried once and never again.",
            "A food you refused as a kid and love now.",
            "A lunchbox item you still think about.",
            "A midnight snack you are not proud of.",
            "A holiday dish your family argues about.",
            "A baking success you brag about.",
            "A baking failure you laugh about now.",
            "A food you eat differently at home vs. in public.",
            "A condiment you put on almost everything.",
            "A condiment you think is overrated.",
            "A meal that is worth the long wait.",
            "A fast food order you will defend.",
            "A home-cooked meal that beats any restaurant.",
            "A food memory tied to a specific person.",
            "A food you want to learn to cook well.",
        ],
    },
    {
        "id": "hobbies-fun",
        "title": "Hobbies and fun",
        "items": [
            "A hobby you picked up during a boring season of life.",
            "A hobby you quit and sometimes miss.",
            "A game you could play every game night.",
            "A game you refuse to play again.",
            "A sport or activity you are bad at but enjoy.",
            "A sport or activity you are good at but find stressful.",
            "A song you put on when you need energy.",
            "A song you put on when you need calm.",
            "A movie you have seen more than five times.",
            "A movie you walked out of or almost did.",
            "A TV show you recommend to everyone.",
            "A book you gave as a gift.",
            "A book someone gave you that mattered.",
            "A craft or project sitting half-finished at home.",
            "A craft or project you finished and still display.",
            "A concert or live show you still talk about.",
            "A podcast topic you never get tired of.",
            "A board game role you always end up playing.",
            "A video game world you would live in for a week.",
            "A card game you learned as a kid.",
            "A puzzle type you love: jigsaw, crossword, or other.",
            "A collection you had as a kid: cards, rocks, stickers.",
            "A talent you would perform at a school talent show.",
            "A talent you absolutely would not perform.",
            "A hobby that costs more than people think.",
            "A hobby that costs almost nothing.",
            "A weekend activity that never gets old.",
            "A weekend activity you are tired of.",
            "A rainy-day indoor activity you recommend.",
            "A sunny-day outdoor activity you recommend.",
            "A hobby you do alone to recharge.",
            "A hobby you only enjoy with other people.",
            "A instrument you wish you had learned.",
            "A language you wish you had learned.",
            "A YouTube rabbit hole you fall into.",
            "A meme or joke format you still find funny.",
            "A holiday craft or decoration you enjoy making.",
            "A party game that works with any group.",
            "A party game that needs exactly the right group.",
            "A place you go to think: park, café, library.",
            "A creative block you pushed through.",
            "A time you taught someone a game or skill.",
            "A time someone taught you something that stuck.",
            "A competition you won and still smile about.",
            "A competition you lost and still smile about.",
            "A fandom you were deep into.",
            "A character from fiction you relate to.",
            "A hobby you want to try this year.",
            "A hobby you want your kids or nieces to try.",
            "A simple pleasure you wish you did more often.",
        ],
    },
    {
        "id": "family-friends",
        "title": "Family and friends",
        "items": [
            "A friend who feels like family.",
            "A family member who feels like a friend.",
            "A tradition your friend group invented.",
            "A tradition your family refuses to change.",
            "A time a friend made you laugh when you needed it.",
            "A time you made a friend laugh when they needed it.",
            "A piece of advice a parent or elder gave you that stuck.",
            "A piece of advice you give younger people.",
            "A sibling or cousin story that still comes up at reunions.",
            "A reunion moment you look forward to.",
            "A reunion moment you dread a little.",
            "A gift you gave that someone still uses.",
            "A gift you received that surprised you.",
            "A handwritten note or card you kept.",
            "A text or message you re-read sometimes.",
            "A time you apologized and meant it.",
            "A time someone apologized to you and it mattered.",
            "A friend you lost touch with but think of fondly.",
            "A friend you reconnected with and were glad.",
            "A neighbor who made your block better.",
            "A pet that brought your household together.",
            "A pet story your family tells too often.",
            "A meal where everyone talked at once.",
            "A meal where comfortable silence was enough.",
            "A time you hosted and it went well.",
            "A time you hosted and learned a lesson.",
            "A time you were a guest and felt welcomed.",
            "A inside joke only your family understands.",
            "A inside joke only your friends understand.",
            "A time you helped a friend move or fix something.",
            "A time a friend helped you without being asked.",
            "A wedding or celebration you loved attending.",
            "A milestone you are proud someone close achieved.",
            "A hard conversation you are glad you had.",
            "A hard conversation you are still avoiding.",
            "A compliment you remember years later.",
            "A compliment you give easily.",
            "A time you felt like the responsible one in the group.",
            "A time you felt like the chaotic one in the group.",
            "A friend who challenges you to grow.",
            "A friend who helps you relax.",
            "A family recipe or ritual passed down.",
            "A holiday where your people are all in one place.",
            "A long-distance friendship that still works.",
            "A group chat that is mostly memes.",
            "A group chat that is mostly logistics.",
            "A time you met a friend as an adult unexpectedly.",
            "A mentor outside your family who mattered.",
            "A kid in your life who makes you laugh.",
            "A way you stay in touch that actually works.",
        ],
    },
    {
        "id": "stories-surprises",
        "title": "Stories and surprises",
        "items": [
            "A small kindness from a stranger you still remember.",
            "A time you were in the right place at the right time.",
            "A coincidence that still feels unreal.",
            "A dream you remember vividly.",
            "A nightmare that stuck with you.",
            "A near miss (car, bike, kitchen, sports) that taught you something.",
            "A time you found money or lost money in a memorable way.",
            "A prank you pulled that went perfectly.",
            "A prank that backfired on you.",
            "A surprise that made your week.",
            "A surprise you would not want repeated.",
            "A rumor you believed as a kid.",
            "A fact you learned that changed a conversation.",
            "A question a kid asked you that stopped you cold.",
            "A question you wish more people asked.",
            "A time you said yes without knowing what you agreed to.",
            "A time you said no and were relieved.",
            "A costume or outfit you wore proudly.",
            "A costume or outfit you regret.",
            "A weather event you lived through: storm, flood, heat wave.",
            "A power outage story.",
            "A time the internet went out and you did something better.",
            "A thing you believed until embarrassingly late in life.",
            "A superstition you still half believe.",
            "A lucky charm or ritual before big moments.",
            "A unlucky day that became a funny story.",
            "A time you met someone famous or almost did.",
            "A autograph, ticket stub, or keepsake you saved.",
            "A time you were on the news, radio, or school announcement.",
            "A time you helped in an emergency, big or small.",
            "A fear you overcame.",
            "A fear you still have and manage.",
            "A prediction you made that came true.",
            "A prediction you made that failed spectacularly.",
            "A time you guessed someone's secret correctly.",
            "A time your secret got out.",
            "A object you almost threw away and were glad you kept.",
            "A object you kept too long and finally let go.",
            "A sound in your home that still startles you.",
            "A smell in your home that means comfort.",
            "A time you laughed at the wrong moment.",
            "A time silence was the right response.",
            "A rule you break on purpose every time.",
            "A rule you follow even when nobody is watching.",
            "A headline you still think about.",
            "A local legend or story from your town.",
            "A travel story you tell at every dinner party.",
            "A story you shorten every time you tell it.",
            "A story that gets better with every retelling.",
            "A plot twist in your own life you did not see coming.",
        ],
    },
]
def table_topic_items() -> list[str]:
    items: list[str] = []
    for cat in TABLE_CATEGORIES:
        items.extend(cat["items"])
    return items


def build_table_block() -> str:
    items = table_topic_items()
    if len(items) != TARGET:
        raise SystemExit(f"table-topics: need {TARGET} items, have {len(items)}")
    if len(set(items)) != len(items):
        raise SystemExit("table-topics: duplicate items")
    m = TABLE_META
    return (
        f"- id: {m['id']}\n"
        f"  title: {m['title']}\n"
        f"  mode: {m['mode']}\n"
        f"  tagline: {m['tagline']}\n"
        f"  play_hint: {m['play_hint']}\n"
        f"  items:\n{dump_items(items)}\n"
    )


def build_wyr_block() -> str:
    items = WYR_ITEMS[:TARGET]
    if len(items) < TARGET:
        raise SystemExit(f"would-you-rather: need {TARGET}, have {len(items)}")
    if len(set(items)) != len(items):
        raise SystemExit("would-you-rather: duplicate items")
    m = WYR_META
    return (
        f"- id: {m['id']}\n"
        f"  title: {m['title']}\n"
        f"  mode: {m['mode']}\n"
        f"  tagline: {m['tagline']}\n"
        f"  play_hint: {m['play_hint']}\n"
        f"  items:\n{dump_items(items)}\n"
    )


def replace_or_append(text: str, col_id: str, block: str) -> str:
    pattern = rf"- id: {re.escape(col_id)}\n.*?(?=\n- id: |\Z)"
    if re.search(pattern, text, flags=re.S):
        return re.sub(pattern, block.rstrip() + "\n", text, count=1, flags=re.S)
    return text.rstrip() + "\n\n" + block
SCALE_CLUES_PIN = [
    "Things you'd want to do when you're very tired.",
    "Things to bring on a deserted island.",
    "Superpowers you'd actually want to have.",
    "Games that need no equipment at all.",
    "Snacks you'd want during a movie at home.",
    "Foods you'd want for a comfort meal.",
    "Things that would cheer you up on a bad day.",
    "Things that would start a good conversation.",
    "Things that would be embarrassing to drop in public.",
    "Things you'd want when the Wi-Fi goes down at home.",
    "Things you'd want when you're bored at home.",
    "Things that would make a party more fun.",
    "Card games everyone already knows.",
    "Games you could explain in one sentence.",
    "Things that would end an awkward silence.",
    "Things that would make you giggle when you should stay quiet.",
    "Things you'd want when playing hide-and-seek.",
    "Things you'd want when playing musical chairs.",
    "Things you'd want when playing Simon says.",
    "Things you'd want when playing rock paper scissors.",
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
    if re.search(
        r"\b(meeting|new job|team meeting|as an adult|age thirty|livestream|submarine|"
        r"space station|first colony|volcano erupted|sign a kid|kids actually|"
        r"curious teenager|important meeting|pharmacy run|dollar store|"
        r"hiking trail|charity livestream|five-year-old|teenager)\b",
        lower,
    ):
        score -= 40
    if "grandparent" in lower and "child and a grandparent" not in lower:
        score -= 20
    if re.search(
        r"\b(board games? you'd|party games? that|card games? you'd teach|non-gamers?|"
        r"game night|bluffing|mixed ages|rules are easy|teams up against|drawing skills|"
        r"under twenty minutes|luck matters more|duck duck goose|mother may i|musical statues|"
        r"capture the flag|leapfrog|follow the leader)\b",
        lower,
    ):
        score -= 35
    if re.search(
        r"\bwhen playing (hide-and-seek|tag|musical chairs|simon says|rock paper scissors|"
        r"charades|hot potato|tic-tac-toe|hopscotch|jump rope|catch|twenty questions)\b",
        lower,
    ):
        score += 14
    if re.search(
        r"\bwhen playing (dodgeball|tug of war|freeze tag|freeze dance|arm wrestling|thumb war)\b",
        lower,
    ):
        score += 6
    if lower.startswith("things you'd want when the family "):
        score -= 10
    if lower.startswith("things you'd want if "):
        score -= 3
    if "board game" in lower or "party game" in lower:
        score -= 15
    if lower.startswith("card games everyone") or lower.startswith("games that need no"):
        score += 12
    if lower.startswith("games you could explain") or lower.startswith("games a child"):
        score += 8
    if lower.startswith("games everyone") or lower.startswith("games that are fun"):
        score += 8
    if "superpower" in lower:
        score += 14
    if "deserted island" in lower:
        score += 18
    if "very tired" in lower:
        score += 16
    if "stranded" in lower:
        score += 12
    if "embarrassing" in lower or "funny" in lower or "awkward" in lower or "giggle" in lower:
        score += 12
    if "snack" in lower or "comfort meal" in lower or "dessert" in lower:
        score += 8
    if "conversation" in lower or "party" in lower or "picnic" in lower:
        score += 7
    if "wifi" in lower or "power outage" in lower or "internet" in lower:
        score += 6
    if "movie" in lower or "road-trip" in lower or "playlist" in lower:
        score += 6
    if "bored at home" in lower or "bad day" in lower:
        score += 10
    if any(w in lower for w in ("any age", "group project", "speaking in front")):
        score += 8
    if re.search(r"\b(sandstorm|elevators only|volcano|homework graded|shrunk to the size)\b", lower):
        score -= 8
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
    if len(item) > 58:
        score -= 10
    elif len(item) < 38:
        score += 4
    if lower in ("how lazy are you?", "how dramatic are you?", "how stubborn are you?"):
        score += 18
    if "sore loser" in lower:
        score += 16
    if "competitive are you at board games" in lower:
        score += 15
    if lower == "how likely are you to gossip?":
        score += 14
    if "honest are you, even when it hurts" in lower:
        score += 14
    if "procrastinator" in lower:
        score += 12
    if "ignore your phone" in lower:
        score += 12
    if "eat food that fell on the floor" in lower:
        score += 12
    if "return a shopping cart" in lower:
        score += 11
    if "sing in the shower" in lower:
        score += 10
    if "cry during a movie" in lower:
        score += 10
    if "double-dip at a party" in lower:
        score += 10
    if "sarcastic" in lower or "impulsive" in lower:
        score += 9
    if "replay awkward moments" in lower:
        score += 9
    if "include someone sitting alone" in lower:
        score += 8
    if "how funny do you think you are" in lower:
        score += 8
    if "apologize first" in lower:
        score += 8
    if "scroll on your phone in bed" in lower:
        score += 7
    if lower.startswith("how much do you enjoy"):
        score -= 14
    if lower.startswith("how good are you at"):
        score -= 6
    if lower.startswith("how good a "):
        score -= 4
    if "how calm are you" in lower:
        score -= 6
    if re.search(
        r"\b(wedding|while driving|road rage|jaywalk|raise or promotion|"
        r"google someone before meeting|comment sections|tip creators|"
        r"ghost a group plan|speakerphone in public|vacation days|"
        r"mute politics|house-rule a board game|rule lawyer|workaholic|"
        r"vengeful|argue a late fee|unique passwords|dog-ear library|"
        r"extreme sports|eating alone in public|wear headphones to avoid)\b",
        lower,
    ):
        score -= 14
    if re.match(
        r"^how (adventurous|ambitious|athletic|brave|cautious|coordinated|"
        r"diplomatic|easygoing|nostalgic|rebellious|romantic) are you\?$",
        lower,
    ):
        score -= 8
    if "like your food" in lower or "like your drinks" in lower:
        score -= 5
    return score


SPECTRUM_TAGLINE = (
    "Two poles on one line. "
    "Someone picks a hidden spot; you give one clue that lands there."
)
SPECTRUM_PLAY_HINT = (
    "Give a single clue for where the target lands. "
    "Works near either pole, not only the middle. Expect friendly debate."
)

# Wavelength-grade pairs: one sliding axis, many placeable clues (best first).
SPECTRUM_CURATED = [
    ('Hot', 'Cold'),
    ('Overrated', 'Underrated'),
    ('Boring', 'Exciting'),
    ('Smells bad', 'Smells good'),
    ('Rough', 'Smooth'),
    ('Cheap', 'Expensive'),
    ('Easy', 'Hard'),
    ('Safe', 'Dangerous'),
    ('Common', 'Rare'),
    ('Simple', 'Complex'),
    ('Quiet', 'Loud'),
    ('Mild', 'Spicy'),
    ('Useless', 'Useful'),
    ('Predictable', 'Surprising'),
    ('Relaxing', 'Stressful'),
    ('Polite', 'Rude'),
    ('Healthy', 'Unhealthy'),
    ('Old-fashioned', 'Modern'),
    ('Local', 'Exotic'),
    ('Calm', 'Chaotic'),
    ('Forgiving', 'Strict'),
    ('Obvious', 'Subtle'),
    ('Big', 'Small'),
    ('Fast', 'Slow'),
    ('Bright', 'Dim'),
    ('Sweet', 'Savory'),
    ('Soft', 'Firm'),
    ('Light', 'Heavy'),
    ('Clean', 'Dirty'),
    ('Full', 'Empty'),
    ('Shallow', 'Deep'),
    ('Narrow', 'Wide'),
    ('Sharp', 'Dull'),
    ('Fresh', 'Stale'),
    ('Patient', 'Impatient'),
    ('Brave', 'Timid'),
    ('Honest', 'Deceptive'),
    ('Serious', 'Silly'),
    ('Formal', 'Casual'),
    ('Private', 'Public'),
    ('Temporary', 'Permanent'),
    ('Literal', 'Figurative'),
    ('Fact', 'Opinion'),
    ('Introvert', 'Extrovert'),
    ('Beginner', 'Expert'),
    ('Childish', 'Mature'),
    ('Optimistic', 'Pessimistic'),
    ('Lazy', 'Driven'),
    ('Pointless', 'Essential'),
    ('Weak', 'Powerful'),
    ('Fragile', 'Durable'),
    ('Gentle', 'Aggressive'),
    ('Passive', 'Assertive'),
    ('Flexible', 'Rigid'),
    ('Minimal', 'Extravagant'),
    ('Ordinary', 'Extraordinary'),
    ('Mainstream', 'Underground'),
    ('Natural', 'Artificial'),
    ('Handmade', 'Mass-produced'),
    ('Crowded', 'Empty'),
    ('Sandwich', 'Not a sandwich'),
    ('Sport', 'Not a sport'),
    ('Vegetable', 'Not a vegetable'),
    ('Art', 'Science'),
    ('Job', 'Career'),
    ('Tool', 'Toy'),
    ('Pet', 'Pest'),
    ('Fantasy', 'Sci-fi'),
    ('Sad song', 'Happy song'),
    ('Fiction', 'Nonfiction'),
    ('Comedy', 'Drama'),
    ('Indoor activity', 'Outdoor activity'),
    ('Gift', 'Not a gift'),
    ('Dessert', 'Not dessert'),
    ('Breakfast food', 'Dinner food'),
    ('Game', 'Not a game'),
    ('Snack', 'Meal'),
    ('Joke', 'Not a joke'),
    ('Exercise', 'Not exercise'),
    ('Holiday', 'Not a holiday'),
    ('Harmless prank', 'Cruel joke'),
    ('Icebreaker', 'Conversation ender'),
    ('Time saver', 'Time waster'),
    ('Stress relief', 'Stress cause'),
    ('Healthy choice', 'Indulgent choice'),
    ('Selfish choice', 'Generous choice'),
    ('Confidence boost', 'Confidence drain'),
    ('Team builder', 'Team divider'),
    ('Low effort', 'High effort'),
    ('Mild habit', 'Risky habit'),
    ('Simple skill', 'Impressive skill'),
    ('Cheap thrill', 'Expensive hobby'),
    ('Overhyped', 'Underrated gem'),
    ('Guilty pleasure', 'Proud favorite'),
    ('Comfort zone', 'Challenge'),
    ('Nostalgia', 'Novelty'),
    ('Classic', 'Trending'),
    ('Comfort food', 'Adventurous food'),
    ('Underdone', 'Overdone'),
    ('Overexplained', 'Mysterious'),
    ('Quiet hobby', 'Loud hobby'),
    ('Solo hobby', 'Group hobby'),
    ('Low-key hangout', 'Big night out'),
    ('Quick errand', 'All-day outing'),
    ('Short walk', 'Long hike'),
    ('Quick shower', 'Long bath'),
    ('Light snack', 'Full meal'),
    ('Power nap', 'Deep sleep'),
    ('Mini vacation', 'Dream trip'),
    ('Quick game', 'Epic campaign'),
    ('Casual sport', 'Competitive sport'),
    ('Practice round', 'Championship'),
    ('Chore', 'Hobby'),
    ('Routine', 'Adventure'),
    ('Stay home', 'Go out'),
    ('Rest day', 'Training day'),
    ('Window shopping', 'Big purchase'),
    ('Budget meal', 'Fine dining'),
    ('Instant reply', 'Thoughtful reply'),
    ('Quick fix', 'Long-term fix'),
    ('Last minute', 'Planned ahead'),
    ('Rough draft', 'Final version'),
    ('Warm-up', 'Main event'),
    ('Appetizer', 'Main course'),
    ('Trailer', 'Feature film'),
    ('Tutorial', 'Boss fight'),
    ('Whisper', 'Shout'),
    ('Shy greeting', 'Bold introduction'),
    ('Listen', 'Talk'),
    ('Follow', 'Lead'),
    ('Play it safe', 'Take a risk'),
    ('Overthink', 'Go with gut'),
    ('Trust easily', 'Trust slowly'),
    ('Open book', 'Hard to read'),
    ('Forgive quickly', 'Hold a grudge'),
    ('Ask permission', 'Take initiative'),
    ('Overshare', 'Keep mystery'),
    ('Early bird', 'Night owl'),
    ('Summer mood', 'Winter mood'),
    ('Rainy day', 'Sunny day'),
    ('School day', 'Weekend'),
    ('Work mode', 'Vacation mode'),
    ('Screen time', 'Outside time'),
    ('Homework', 'Passion project'),
    ('Background music', 'Live concert'),
    ('Short video', 'Feature film'),
    ('Cartoon', 'Documentary'),
    ('Rewatch', 'First watch'),
    ('Spoiler', 'Surprise twist'),
    ('Happy ending', 'Tragic ending'),
    ('Formal event', 'Casual hangout'),
    ('City life', 'Country life'),
    ('Planned trip', 'Spontaneous trip'),
    ('Minimal home', 'Cozy clutter'),
    ('Packing light', 'Packing heavy'),
    ('Deep research', 'Quick search'),
    ('Fresh pizza', 'Reheated pizza'),
    ('Firm mattress', 'Soft mattress'),
    ('Indie film', 'Blockbuster'),
    ('Thrift find', 'Brand new'),
    ('Learn by doing', 'Learn by watching'),
    ('Strict budget', 'Treat yourself'),
    ('Big city noise', 'Small town quiet'),
    ('Whole foods', 'Processed foods'),
    ('Gentle ride', 'Thrill ride'),
    ('Overprepared', 'Underprepared'),
    ('Detailed itinerary', 'Rough outline'),
    ('Inbox zero', 'Inbox backlog'),
    ('Early arrival', 'Fashionably late'),
    ('Strategy game', 'Luck game'),
    ('Loud restaurant', 'Quiet restaurant'),
    ('Home cooking', 'Restaurant meal'),
    ('Camping trip', 'Hotel stay'),
    ('Beach vacation', 'Mountain vacation'),
    ('Group travel', 'Solo travel'),
    ('Remote work', 'Office work'),
    ('Video call', 'In-person meeting'),
    ('Ask for help', 'Figure it out alone'),
    ('Digital detox', 'Always connected'),
    ('Physical book', 'E-book'),
    ('DIY repair', 'Call a pro'),
    ('Repair item', 'Replace item'),
    ('Cook from scratch', 'Use shortcuts'),
    ('Morning workout', 'Evening workout'),
    ('Car karaoke', 'Quiet drive'),
    ('Home movie night', 'Theater night'),
    ('Spontaneous gift', 'Planned gift'),
    ('Farmers market', 'Supermarket run'),
    ('Bookstore browse', 'Online checkout'),
    ('Theme park ride', 'Nature trail'),
    ('Tent camping', 'Cabin stay'),
    ('Hotel buffet', 'Corner café'),
    ('Guided tour', 'Self-guided tour'),
    ('City break', 'Nature retreat'),
    ('Board game', 'Video game'),
    ('Live music', 'Recorded music'),
    ('Comedy podcast', 'True crime podcast'),
    ('Kid movie', 'Grown-up movie'),
    ('Instant coffee', 'Fancy coffee'),
    ('Fruit dessert', 'Chocolate dessert'),
]


# Parallel-alternative pairs that fail the pole test (preference forks, not gradients).
SPECTRUM_WEAK = {
    "sandwich", "wrap", "pancake", "waffle", "tea person", "coffee person",
    "morning news", "morning music", "sunrise watch", "sunset watch",
    "forest walk", "beach walk", "apple orchard", "apple bag",
    "escalator", "stairs", "elevator", "bike errand", "car errand",
    "cash payment", "card payment", "charades act", "charades guess",
    "hot cocoa mug", "hot tea mug", "remember faces", "remember names",
    "dog person", "cat person", "window seat", "aisle seat",
}



def score_spectrum(left: str, right: str) -> float:
    score = 50.0
    ll, rl = left.lower(), right.lower()
    if left.startswith("Better ") or right.startswith("Better "):
        score -= 20
    if left.startswith("Too ") and right.startswith("Too "):
        score -= 8
    if (left.startswith("Low ") and right.startswith("High ")) or (
        left.startswith("High ") and right.startswith("Low ")
    ):
        score -= 6
    if ll in SPECTRUM_WEAK or rl in SPECTRUM_WEAK:
        score -= 15
    if " person" in f" {ll}" or " person" in f" {rl}":
        score -= 10
    if "not a " in ll or "not a " in rl or "not " in ll or "not " in rl:
        score += 8  # fuzzy-boundary cards clue well in Wavelength
    if len(left) > 22 or len(right) > 22:
        score -= 6
    if len(left) < 14 and len(right) < 14:
        score += 5
    return score


def rank_unique(items: list[str], pin: list[str], scorer) -> list[str]:
    pool = set(items)
    seen = set()
    ordered: list[str] = []
    for item in pin:
        if item in pool and item not in seen:
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


def rank_scale_clues(items: list[str]) -> list[str]:
    """Best prompt first — pure score order."""
    return sorted(items, key=lambda x: (-score_scale_clue(x), x))


def rank_personal_scales(items: list[str]) -> list[str]:
    """Best icebreaker first — pure score order."""
    return sorted(items, key=lambda x: (-score_personal(x), x))


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

def cmd_build() -> None:
    text = YAML.read_text()
    text = replace_or_append(text, "would-you-rather", build_wyr_block())
    text = replace_or_append(text, "table-topics", build_table_block())
    YAML.write_text(text)
    data = yaml.safe_load(text)
    cols = {c["id"]: c for c in data["collections"]}
    wyr = cols["would-you-rather"]["items"]
    topics = cols["table-topics"]["items"]
    print(f"would-you-rather: {len(wyr)}")
    print(f"table-topics: {len(topics)}")

def cmd_curate(only: str | None = None) -> None:
    data = yaml.safe_load(YAML.read_text())
    text = YAML.read_text()
    cols = {c["id"]: c for c in data["collections"]}
    touch = {"scale-clues", "personal-scales", "spectrum"} if only is None else {only}

    if "scale-clues" in touch:
        scale = rank_scale_clues(cols["scale-clues"]["items"])[:TARGET]
        assert len(scale) == TARGET, len(scale)
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

    if "personal-scales" in touch:
        personal_pool = list(cols["personal-scales"]["items"])
        if len(personal_pool) < TARGET:
            seen = set(personal_pool)
            personal_pool.extend(x for x in PERSONAL_NEW if x not in seen)
        personal = rank_personal_scales(personal_pool)[:TARGET]
        assert len(personal) == TARGET, len(personal)
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

    if "spectrum" in touch:
        spectrum = [{"left": l, "right": r} for l, r in SPECTRUM_CURATED[:SPECTRUM_TARGET]]
        assert len(spectrum) == SPECTRUM_TARGET, len(spectrum)
        sp = cols["spectrum"]
        block = (
            f"- id: spectrum\n"
            f"  title: {sp['title']}\n"
            f"  mode: {sp['mode']}\n"
            f"  tagline: {SPECTRUM_TAGLINE}\n"
            f"  play_hint: {SPECTRUM_PLAY_HINT}\n"
            f"  spectrums:\n{dump_spectrums(spectrum)}\n"
        )
        text = replace_collection_block(text, "spectrum", block)

    YAML.write_text(text)
    if "scale-clues" in touch:
        print(f"scale-clues: {len(scale)} (top: {scale[0][:50]}...)")
    if "personal-scales" in touch:
        print(f"personal-scales: {len(personal)} (top: {personal[0]})")
    if "spectrum" in touch:
        print(f"spectrum: {len(spectrum)} (top: {spectrum[0]['left']} | {spectrum[0]['right']})")

def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="cmd", required=True)
    sub.add_parser("build", help="Rebuild would-you-rather + table-topics").set_defaults(
        run=lambda _a: cmd_build()
    )
    cp = sub.add_parser("curate", help="Rank scale-clues, personal-scales, spectrum")
    cp.add_argument(
        "--only",
        choices=["scale-clues", "personal-scales", "spectrum"],
        help="One collection only (default: all three)",
    )
    cp.set_defaults(run=lambda a: cmd_curate(a.only))
    sub.add_parser("spectrum", help="Alias: curate --only spectrum").set_defaults(
        run=lambda _a: cmd_curate("spectrum")
    )
    args = parser.parse_args()
    args.run(args)

if __name__ == "__main__":
    main()
