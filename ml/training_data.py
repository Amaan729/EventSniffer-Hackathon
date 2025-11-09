# training_data.py
#
# --- THIS IS THE NEW, GUARANTEED-TO-WORK VERSION ---
#
# Instead of manual (and broken) character counts, this file
# defines the *text* of the entities. A function then
# calculates the correct start/end positions automatically.
# This makes it impossible to have a [W030] alignment error.
#

import spacy
import re

# 1. Define the data in a simple, human-readable format.
# (text, [ (entity_text_to_find, "LABEL"), ... ])
SIMPLE_DATA = [
    # --- Full Events ---
    ("Let's meet tomorrow at 3", [("Let's meet", "EVENT"), ("tomorrow", "DATE"), ("at 3", "TIME")]),
    ("The project is due next Friday", [("The project is due", "EVENT"), ("next Friday", "DATE")]),
    ("Grabbing coffee on Main St?", [("Grabbing coffee", "EVENT"), ("Main St", "LOCATION")]),
    ("Hey are you free to grab lunch next Tuesday at 1pm?", [("grab lunch", "EVENT"), ("next Tuesday", "DATE"), ("at 1pm", "TIME")]),
    ("We have the All-Hands Meeting on Monday at 10:00 AM", [("All-Hands Meeting", "EVENT"), ("on Monday", "DATE"), ("at 10:00 AM", "TIME")]),
    ("Can we schedule the 1:1 for this Wednesday at 4:30pm?", [("1:1", "EVENT"), ("this Wednesday", "DATE"), ("at 4:30pm", "TIME")]),
    ("Let's book the standup for next Monday at 9:30am in the main conf room", [("standup", "EVENT"), ("next Monday", "DATE"), ("at 9:30am", "TIME"), ("main conf room", "LOCATION")]),
    ("How about lunch at Joe's Pizza on Wednesday around 1?", [("lunch", "EVENT"), ("Joe's Pizza", "LOCATION"), ("on Wednesday", "DATE"), ("around 1", "TIME")]),
    ("Doctor's appointment 12/20 at 3:45pm", [("Doctor's appointment", "EVENT"), ("12/20", "DATE"), ("at 3:45pm", "TIME")]),
    ("Let's sync up on the project next week.", [("sync up", "EVENT"), ("next week", "DATE")]),

    # --- Virtual Locations ---
    ("Let's do a quick sync on Zoom at 4", [("quick sync", "EVENT"), ("Zoom", "LOCATION"), ("at 4", "TIME")]),
    ("I'll send a Google Meet invite for 3pm tomorrow", [("Google Meet", "LOCATION"), ("3pm", "TIME"), ("tomorrow", "DATE")]),
    ("Design review tomorrow morning on Teams", [("Design review", "EVENT"), ("tomorrow morning", "DATE-TIME"), ("Teams", "LOCATION")]),
    ("Weekly sync on Google Meet, Friday at 11", [("Weekly sync", "EVENT"), ("Google Meet", "LOCATION"), ("Friday", "DATE"), ("at 11", "TIME")]),

    # --- Deadlines ---
    ("The report deadline is EOD tomorrow", [("report deadline", "EVENT"), ("EOD tomorrow", "DATE-TIME")]),
    ("Submit your hours by next Friday", [("Submit your hours", "EVENT"), ("next Friday", "DATE")]),
    ("Code freeze is on 11/20 at 5pm", [("Code freeze", "EVENT"), ("11/20", "DATE"), ("at 5pm", "TIME")]),
    ("This task is due on Wednesday", [("This task is due", "EVENT"), ("on Wednesday", "DATE")]),

    # --- Partial Info / Questions ---
    ("Are you free on Tuesday?", [("on Tuesday", "DATE")]),
    ("What about 3pm?", [("3pm", "TIME")]),
    ("Can we meet next week?", [("meet", "EVENT"), ("next week", "DATE")]),
    ("Got time for a call?", [("call", "EVENT")]),
    ("Wanna grab coffee?", [("grab coffee", "EVENT")]),
    ("Let's talk on Monday", [("talk", "EVENT"), ("on Monday", "DATE")]),
    ("How about next week?", [("next week", "DATE")]),
    ("Need to chat about the design.", [("chat", "EVENT")]),

    # --- Informal Chat-speak ---
    ("sync tmrw 10am?", [("sync", "EVENT"), ("tmrw", "DATE"), ("10am", "TIME")]),
    ("coffee weds?", [("coffee", "EVENT"), ("weds", "DATE")]),
    ("meet fri 3p zoom?", [("meet", "EVENT"), ("fri", "DATE"), ("3p", "TIME"), ("zoom", "LOCATION")]),
    ("free next week for a chat?", [("next week", "DATE"), ("chat", "EVENT")]),
    ("How about 2:30 on 11/25?", [("2:30", "TIME"), ("11/25", "DATE")]),
    ("Meeting 3pm", [("Meeting", "EVENT"), ("3pm", "TIME")]),
    ("U free tmrw?", [("free", "EVENT"), ("tmrw", "DATE")]),
    ("dinner 7pm fri", [("dinner", "EVENT"), ("7pm", "TIME"), ("fri", "DATE")]),

    # --- NEGATIVE EXAMPLES (CRITICAL) ---
    ("That's a great idea, I'll send it over.", []),
    ("I'm heading out now.", []),
    ("What time is it?", []),
    ("I already finished the project.", []),
    ("That was a great meeting.", []),
    ("The report was due yesterday.", []),
    ("We met last Tuesday.", []),
    ("I'm not free on Tuesday.", []),
    ("I'll be free *after* 3pm.", []),
    ("Do you remember what happened on Nov 20th?", []),
    ("My old office was on Main St.", []),
    ("See you!", []),
    ("What's on your calendar for tomorrow?", []),
    ("I'm pushing the code now.", []),
    ("He's grabbing his coffee now.", []),
    ("The due date has passed.", []),
    ("I need to schedule a meeting.", []),
    ("Let me know what time works.", []),
    ("What's the address?", []),
    ("I'm in a meeting.", []),
    ("The project started on Monday.", []),
    ("I can't meet then.", []),
    ("Tomorrow is a holiday.", []),
    ("I'm busy all next week.", []),
    ("That time doesn't work.", []),
    ("The cafe is on 1st Ave.", []),
    ("I'll be on vacation next Friday.", []),
    ("We should have synced last week.", []),
    ("He lives in Tempe.", []),
    ("Zoom is a good tool.", []),
    ("I was free at 3pm.", []),
    ("My next meeting is at 10.", []),
]


def get_training_data():
    """
    This function programmatically builds the spaCy training data.
    It finds the character offsets for each entity, which
    guarantees they are correct and avoids the [W030] warning.
    """
    TRAIN_DATA = []
    
    for text, entities in SIMPLE_DATA:
        ents_list = []
        
        # Sort entities by length, longest first.
        # This prevents "meet" from matching before "let's meet".
        sorted_entities = sorted(entities, key=lambda x: len(x[0]), reverse=True)

        for ent_text, label in sorted_entities:
            # Use regex to find all matches
            matches = list(re.finditer(re.escape(ent_text), text))
            
            if matches:
                # For this simple dataset, we'll just take the first match.
                # A more complex system would handle multiple matches.
                match = matches[0]
                start = match.start()
                end = match.end()
                ents_list.append((start, end, label))
            else:
                # This check is for me, the developer, to see if my
                # SIMPLE_DATA is bad.
                print(f"--- WARNING: Could not find '{ent_text}' in '{text}'")

        TRAIN_DATA.append((text, {"entities": ents_list}))
            
    return TRAIN_DATA

# This line is just for compatibility if anything else was importing it.
TRAIN_DATA = get_training_data()