"""
EventSniffer Training Data v2.0
Goal: 200+ diverse, real-world examples for 95%+ accuracy
"""

import re

# ============================================================================
# COMPREHENSIVE TRAINING DATA - ORGANIZED BY CATEGORY
# ============================================================================

SIMPLE_DATA = [
    # ===== CATEGORY 1: EXPLICIT FORMAL MEETINGS (30 examples) =====
    ("Let's schedule a meeting for tomorrow at 3pm", [("meeting", "EVENT"), ("tomorrow", "DATE"), ("at 3pm", "TIME")]),
    ("Team standup next Monday at 9:30am", [("Team standup", "EVENT"), ("next Monday", "DATE"), ("at 9:30am", "TIME")]),
    ("All hands meeting on Friday at 10am in Conference Room A", [("All hands meeting", "EVENT"), ("Friday", "DATE"), ("at 10am", "TIME"), ("Conference Room A", "LOCATION")]),
    ("Q4 planning session next Wednesday from 2-4pm", [("Q4 planning session", "EVENT"), ("next Wednesday", "DATE"), ("2-4pm", "TIME")]),
    ("Client demo tomorrow at 1:30pm on Zoom", [("Client demo", "EVENT"), ("tomorrow", "DATE"), ("at 1:30pm", "TIME"), ("Zoom", "LOCATION")]),
    ("Weekly sync every Thursday at 3pm", [("Weekly sync", "EVENT"), ("every Thursday", "DATE"), ("at 3pm", "TIME")]),
    ("Retrospective meeting on 12/15 at 4pm", [("Retrospective meeting", "EVENT"), ("12/15", "DATE"), ("at 4pm", "TIME")]),
    ("Sprint planning next Tuesday 10am-12pm", [("Sprint planning", "EVENT"), ("next Tuesday", "DATE"), ("10am-12pm", "TIME")]),
    ("1:1 with Sarah next Friday at 2pm", [("1:1 with Sarah", "EVENT"), ("next Friday", "DATE"), ("at 2pm", "TIME")]),
    ("Design review tomorrow morning at 11", [("Design review", "EVENT"), ("tomorrow morning", "DATE"), ("at 11", "TIME")]),
    
    ("Product demo on Wednesday at 3:30pm via Google Meet", [("Product demo", "EVENT"), ("Wednesday", "DATE"), ("at 3:30pm", "TIME"), ("Google Meet", "LOCATION")]),
    ("Engineering sync next Monday at 9am", [("Engineering sync", "EVENT"), ("next Monday", "DATE"), ("at 9am", "TIME")]),
    ("Board meeting on the 20th at 2pm", [("Board meeting", "EVENT"), ("the 20th", "DATE"), ("at 2pm", "TIME")]),
    ("Kickoff call tomorrow 10:30am Zoom", [("Kickoff call", "EVENT"), ("tomorrow", "DATE"), ("10:30am", "TIME"), ("Zoom", "LOCATION")]),
    ("Town hall next Friday at 4pm in the auditorium", [("Town hall", "EVENT"), ("next Friday", "DATE"), ("at 4pm", "TIME"), ("auditorium", "LOCATION")]),
    ("Performance review scheduled for 11/25 at 3pm", [("Performance review", "EVENT"), ("11/25", "DATE"), ("at 3pm", "TIME")]),
    ("Training session on Tuesday from 1-3pm", [("Training session", "EVENT"), ("Tuesday", "DATE"), ("1-3pm", "TIME")]),
    ("Interview with candidate tomorrow at 2:30pm", [("Interview with candidate", "EVENT"), ("tomorrow", "DATE"), ("at 2:30pm", "TIME")]),
    ("Sales call next Wednesday at 11am", [("Sales call", "EVENT"), ("next Wednesday", "DATE"), ("at 11am", "TIME")]),
    ("Marketing sync Friday at 1pm via Teams", [("Marketing sync", "EVENT"), ("Friday", "DATE"), ("at 1pm", "TIME"), ("Teams", "LOCATION")]),
    
    ("Architecture review meeting on 12/10 at 3pm", [("Architecture review meeting", "EVENT"), ("12/10", "DATE"), ("at 3pm", "TIME")]),
    ("Budget planning session next Thursday 2-5pm", [("Budget planning session", "EVENT"), ("next Thursday", "DATE"), ("2-5pm", "TIME")]),
    ("Offsite planning on January 15th at 9am", [("Offsite planning", "EVENT"), ("January 15th", "DATE"), ("at 9am", "TIME")]),
    ("Quarterly business review next Monday at 10am", [("Quarterly business review", "EVENT"), ("next Monday", "DATE"), ("at 10am", "TIME")]),
    ("Team lunch on Friday at noon at Chipotle", [("Team lunch", "EVENT"), ("Friday", "DATE"), ("at noon", "TIME"), ("Chipotle", "LOCATION")]),
    ("Webinar on Wednesday at 1pm", [("Webinar", "EVENT"), ("Wednesday", "DATE"), ("at 1pm", "TIME")]),
    ("Workshop next week on Tuesday at 10am", [("Workshop", "EVENT"), ("next week on Tuesday", "DATE"), ("at 10am", "TIME")]),
    ("Scrum of scrums tomorrow at 9:15am", [("Scrum of scrums", "EVENT"), ("tomorrow", "DATE"), ("at 9:15am", "TIME")]),
    ("Code review session on Thursday at 2pm", [("Code review session", "EVENT"), ("Thursday", "DATE"), ("at 2pm", "TIME")]),
    ("Team building event next Friday afternoon", [("Team building event", "EVENT"), ("next Friday afternoon", "DATE")]),
    
    # ===== CATEGORY 2: CASUAL SOCIAL PLANS (25 examples) =====
    ("Wanna grab coffee tomorrow?", [("grab coffee", "EVENT"), ("tomorrow", "DATE")]),
    ("Let's get lunch next Tuesday", [("get lunch", "EVENT"), ("next Tuesday", "DATE")]),
    ("Dinner on Friday at 7pm?", [("Dinner", "EVENT"), ("Friday", "DATE"), ("at 7pm", "TIME")]),
    ("Drinks after work on Thursday?", [("Drinks after work", "EVENT"), ("Thursday", "DATE")]),
    ("Coffee at Starbucks tomorrow at 3", [("Coffee", "EVENT"), ("Starbucks", "LOCATION"), ("tomorrow", "DATE"), ("at 3", "TIME")]),
    ("Lunch at Joe's Pizza on Wednesday around noon", [("Lunch", "EVENT"), ("Joe's Pizza", "LOCATION"), ("Wednesday", "DATE"), ("around noon", "TIME")]),
    ("Grabbing dinner tonight at 8", [("Grabbing dinner", "EVENT"), ("tonight", "DATE"), ("at 8", "TIME")]),
    ("Brunch this Sunday at 11am", [("Brunch", "EVENT"), ("this Sunday", "DATE"), ("at 11am", "TIME")]),
    ("Happy hour Friday at 5:30", [("Happy hour", "EVENT"), ("Friday", "DATE"), ("at 5:30", "TIME")]),
    ("Movie on Saturday evening?", [("Movie", "EVENT"), ("Saturday evening", "DATE")]),
    
    ("Gym session tomorrow morning at 6am", [("Gym session", "EVENT"), ("tomorrow morning", "DATE"), ("at 6am", "TIME")]),
    ("Tennis match on Sunday at 2pm", [("Tennis match", "EVENT"), ("Sunday", "DATE"), ("at 2pm", "TIME")]),
    ("Study group next Wednesday at 4pm in the library", [("Study group", "EVENT"), ("next Wednesday", "DATE"), ("at 4pm", "TIME"), ("library", "LOCATION")]),
    ("Game night on Friday at my place", [("Game night", "EVENT"), ("Friday", "DATE"), ("my place", "LOCATION")]),
    ("Hiking trip next Saturday morning", [("Hiking trip", "EVENT"), ("next Saturday morning", "DATE")]),
    ("Book club meeting on the 18th at 7pm", [("Book club meeting", "EVENT"), ("the 18th", "DATE"), ("at 7pm", "TIME")]),
    ("BBQ at Sarah's place on Sunday at 4", [("BBQ", "EVENT"), ("Sarah's place", "LOCATION"), ("Sunday", "DATE"), ("at 4", "TIME")]),
    ("Yoga class tomorrow at 6pm", [("Yoga class", "EVENT"), ("tomorrow", "DATE"), ("at 6pm", "TIME")]),
    ("Cooking together next Friday night", [("Cooking together", "EVENT"), ("next Friday night", "DATE")]),
    ("Video game session on Saturday afternoon", [("Video game session", "EVENT"), ("Saturday afternoon", "DATE")]),
    
    ("Birthday party on December 20th at 8pm", [("Birthday party", "EVENT"), ("December 20th", "DATE"), ("at 8pm", "TIME")]),
    ("Wine tasting next Thursday at 7", [("Wine tasting", "EVENT"), ("next Thursday", "DATE"), ("at 7", "TIME")]),
    ("Karaoke night on Friday at 9pm", [("Karaoke night", "EVENT"), ("Friday", "DATE"), ("at 9pm", "TIME")]),
    ("Picnic this weekend in Central Park", [("Picnic", "EVENT"), ("this weekend", "DATE"), ("Central Park", "LOCATION")]),
    ("Concert on Saturday at 8pm at The Venue", [("Concert", "EVENT"), ("Saturday", "DATE"), ("at 8pm", "TIME"), ("The Venue", "LOCATION")]),
    
    # ===== CATEGORY 3: ABBREVIATED/CASUAL CHAT (30 examples) =====
    ("sync tmrw 10a", [("sync", "EVENT"), ("tmrw", "DATE"), ("10a", "TIME")]),
    ("coffee weds?", [("coffee", "EVENT"), ("weds", "DATE")]),
    ("meet fri 3p zoom", [("meet", "EVENT"), ("fri", "DATE"), ("3p", "TIME"), ("zoom", "LOCATION")]),
    ("call mon 2pm", [("call", "EVENT"), ("mon", "DATE"), ("2pm", "TIME")]),
    ("lunch tues noon", [("lunch", "EVENT"), ("tues", "DATE"), ("noon", "TIME")]),
    ("standup tmr 9:30", [("standup", "EVENT"), ("tmr", "DATE"), ("9:30", "TIME")]),
    ("1on1 thurs 4p", [("1on1", "EVENT"), ("thurs", "DATE"), ("4p", "TIME")]),
    ("drinks tonite?", [("drinks", "EVENT"), ("tonite", "DATE")]),
    ("gym tmrw AM", [("gym", "EVENT"), ("tmrw AM", "DATE")]),
    ("demo next week tues", [("demo", "EVENT"), ("next week tues", "DATE")]),
    
    ("catchup call wed 11a", [("catchup call", "EVENT"), ("wed", "DATE"), ("11a", "TIME")]),
    ("quick sync in 10 min", [("quick sync", "EVENT"), ("in 10 min", "TIME")]),
    ("mtg 2pm conf rm B", [("mtg", "EVENT"), ("2pm", "TIME"), ("conf rm B", "LOCATION")]),
    ("review session tmrw afternoon", [("review session", "EVENT"), ("tmrw afternoon", "DATE")]),
    ("planning call next mon 10:30", [("planning call", "EVENT"), ("next mon", "DATE"), ("10:30", "TIME")]),
    ("breakfast meeting tues 8a", [("breakfast meeting", "EVENT"), ("tues", "DATE"), ("8a", "TIME")]),
    ("debrief fri EOD", [("debrief", "EVENT"), ("fri EOD", "DATE")]),
    ("workshop sat morning", [("workshop", "EVENT"), ("sat morning", "DATE")]),
    ("team dinner thurs 7p", [("team dinner", "EVENT"), ("thurs", "DATE"), ("7p", "TIME")]),
    ("sync w/ John tomorrow", [("sync w/ John", "EVENT"), ("tomorrow", "DATE")]),
    
    ("check-in call next week", [("check-in call", "EVENT"), ("next week", "DATE")]),
    ("status update wed AM", [("status update", "EVENT"), ("wed AM", "DATE")]),
    ("retro fri 3pm", [("retro", "EVENT"), ("fri", "DATE"), ("3pm", "TIME")]),
    ("kickoff mon morning", [("kickoff", "EVENT"), ("mon morning", "DATE")]),
    ("brainstorm sesh tues 2p", [("brainstorm sesh", "EVENT"), ("tues", "DATE"), ("2p", "TIME")]),
    ("progress review thurs", [("progress review", "EVENT"), ("thurs", "DATE")]),
    ("sprint demo next fri 11a", [("sprint demo", "EVENT"), ("next fri", "DATE"), ("11a", "TIME")]),
    ("team sync every tues 10am", [("team sync", "EVENT"), ("every tues", "DATE"), ("10am", "TIME")]),
    ("all-hands next wed 2pm", [("all-hands", "EVENT"), ("next wed", "DATE"), ("2pm", "TIME")]),
    ("office hours mon 1-3p", [("office hours", "EVENT"), ("mon", "DATE"), ("1-3p", "TIME")]),
    
    # ===== CATEGORY 4: APPOINTMENTS/ERRANDS (20 examples) =====
    ("Doctor appointment on 12/5 at 2:30pm", [("Doctor appointment", "EVENT"), ("12/5", "DATE"), ("at 2:30pm", "TIME")]),
    ("Dentist visit next Thursday at 10am", [("Dentist visit", "EVENT"), ("next Thursday", "DATE"), ("at 10am", "TIME")]),
    ("Hair cut on Saturday at 3pm", [("Hair cut", "EVENT"), ("Saturday", "DATE"), ("at 3pm", "TIME")]),
    ("Car service appointment tomorrow at 9am", [("Car service appointment", "EVENT"), ("tomorrow", "DATE"), ("at 9am", "TIME")]),
    ("Vet appointment for Max on Friday at 4pm", [("Vet appointment", "EVENT"), ("Friday", "DATE"), ("at 4pm", "TIME")]),
    ("Eye exam on 11/20 at 1pm", [("Eye exam", "EVENT"), ("11/20", "DATE"), ("at 1pm", "TIME")]),
    ("Physical therapy session next Tuesday at 5pm", [("Physical therapy session", "EVENT"), ("next Tuesday", "DATE"), ("at 5pm", "TIME")]),
    ("Massage appointment on Wednesday at 6:30pm", [("Massage appointment", "EVENT"), ("Wednesday", "DATE"), ("at 6:30pm", "TIME")]),
    ("Bank meeting tomorrow at noon", [("Bank meeting", "EVENT"), ("tomorrow", "DATE"), ("at noon", "TIME")]),
    ("Tax prep appointment on January 10th at 2pm", [("Tax prep appointment", "EVENT"), ("January 10th", "DATE"), ("at 2pm", "TIME")]),
    
    ("Home inspection next Friday at 10am", [("Home inspection", "EVENT"), ("next Friday", "DATE"), ("at 10am", "TIME")]),
    ("Lawyer consultation on Thursday at 3pm", [("Lawyer consultation", "EVENT"), ("Thursday", "DATE"), ("at 3pm", "TIME")]),
    ("Insurance review meeting next week", [("Insurance review meeting", "EVENT"), ("next week", "DATE")]),
    ("Financial advisor meeting on 12/12 at 11am", [("Financial advisor meeting", "EVENT"), ("12/12", "DATE"), ("at 11am", "TIME")]),
    ("Property viewing on Saturday at 2pm at 123 Main St", [("Property viewing", "EVENT"), ("Saturday", "DATE"), ("at 2pm", "TIME"), ("123 Main St", "LOCATION")]),
    ("Pickup package at post office tomorrow", [("Pickup package", "EVENT"), ("post office", "LOCATION"), ("tomorrow", "DATE")]),
    ("Drop off car for repairs on Monday morning", [("Drop off car for repairs", "EVENT"), ("Monday morning", "DATE")]),
    ("Pick up dry cleaning on Wednesday afternoon", [("Pick up dry cleaning", "EVENT"), ("Wednesday afternoon", "DATE")]),
    ("Grocery shopping this weekend", [("Grocery shopping", "EVENT"), ("this weekend", "DATE")]),
    ("Pharmacy pickup tomorrow at 5pm", [("Pharmacy pickup", "EVENT"), ("tomorrow", "DATE"), ("at 5pm", "TIME")]),
    
    # ===== CATEGORY 5: DEADLINES/SUBMISSIONS (15 examples) =====
    ("Project due next Friday", [("Project due", "EVENT"), ("next Friday", "DATE")]),
    ("Report deadline on 11/30", [("Report deadline", "EVENT"), ("11/30", "DATE")]),
    ("Submit proposal by EOD tomorrow", [("Submit proposal", "EVENT"), ("EOD tomorrow", "DATE")]),
    ("Code freeze on Thursday at 5pm", [("Code freeze", "EVENT"), ("Thursday", "DATE"), ("at 5pm", "TIME")]),
    ("Final submission due December 15th", [("Final submission due", "EVENT"), ("December 15th", "DATE")]),
    ("Timesheet deadline this Friday", [("Timesheet deadline", "EVENT"), ("this Friday", "DATE")]),
    ("Expense report due by end of month", [("Expense report due", "EVENT"), ("end of month", "DATE")]),
    ("Performance review self-assessment due next Monday", [("Performance review self-assessment due", "EVENT"), ("next Monday", "DATE")]),
    ("Budget proposal deadline on 12/1", [("Budget proposal deadline", "EVENT"), ("12/1", "DATE")]),
    ("Contract renewal by next Wednesday", [("Contract renewal", "EVENT"), ("next Wednesday", "DATE")]),
    
    ("Manuscript submission deadline January 20th", [("Manuscript submission deadline", "EVENT"), ("January 20th", "DATE")]),
    ("Application deadline on 11/15 at 11:59pm", [("Application deadline", "EVENT"), ("11/15", "DATE"), ("at 11:59pm", "TIME")]),
    ("Registration closes next Friday at noon", [("Registration closes", "EVENT"), ("next Friday", "DATE"), ("at noon", "TIME")]),
    ("Tax filing deadline April 15th", [("Tax filing deadline", "EVENT"), ("April 15th", "DATE")]),
    ("Grant proposal due by end of quarter", [("Grant proposal due", "EVENT"), ("end of quarter", "DATE")]),
    
    # ===== CATEGORY 6: QUESTIONS/VAGUE REQUESTS (15 examples) =====
    ("Are you free tomorrow?", [("tomorrow", "DATE")]),
    ("What about next Tuesday?", [("next Tuesday", "DATE")]),
    ("Can we meet sometime next week?", [("meet", "EVENT"), ("next week", "DATE")]),
    ("How's Friday at 3?", [("Friday", "DATE"), ("at 3", "TIME")]),
    ("Free for a quick call?", [("quick call", "EVENT")]),
    ("Got time for coffee?", [("coffee", "EVENT")]),
    ("Available on Wednesday?", [("Wednesday", "DATE")]),
    ("When works for you next week?", [("next week", "DATE")]),
    ("Can you make it to the meeting?", [("meeting", "EVENT")]),
    ("Are you around tomorrow afternoon?", [("tomorrow afternoon", "DATE")]),
    
    ("Free anytime this week?", [("this week", "DATE")]),
    ("Would Monday work?", [("Monday", "DATE")]),
    ("How about 2pm?", [("2pm", "TIME")]),
    ("Want to grab lunch soon?", [("grab lunch", "EVENT")]),
    ("Got a minute to chat?", [("chat", "EVENT")]),
    
    # ===== CATEGORY 7: COMPLEX/MULTI-PART (15 examples) =====
    ("Let's meet Tuesday or Wednesday, whatever works", [("meet", "EVENT"), ("Tuesday", "DATE"), ("Wednesday", "DATE")]),
    ("Coffee tomorrow at 3, or Thursday at 2 if that's better", [("Coffee", "EVENT"), ("tomorrow", "DATE"), ("at 3", "TIME"), ("Thursday", "DATE"), ("at 2", "TIME")]),
    ("Sync next week, preferably Monday or Tuesday morning", [("Sync", "EVENT"), ("next week", "DATE"), ("Monday", "DATE"), ("Tuesday morning", "DATE")]),
    ("Available for a call between 2-4pm on Friday?", [("call", "EVENT"), ("2-4pm", "TIME"), ("Friday", "DATE")]),
    ("Meeting got moved from Tuesday to Thursday at 3pm", [("Meeting", "EVENT"), ("Tuesday", "DATE"), ("Thursday", "DATE"), ("at 3pm", "TIME")]),
    ("Let's reschedule the 1:1 from tomorrow to next Monday", [("1:1", "EVENT"), ("tomorrow", "DATE"), ("next Monday", "DATE")]),
    ("Demo is now on Wednesday at 2pm instead of Tuesday", [("Demo", "EVENT"), ("Wednesday", "DATE"), ("at 2pm", "TIME"), ("Tuesday", "DATE")]),
    ("Can we do Monday at 10 or Tuesday at 11?", [("Monday", "DATE"), ("at 10", "TIME"), ("Tuesday", "DATE"), ("at 11", "TIME")]),
    ("Planning session next week, likely Wednesday or Thursday afternoon", [("Planning session", "EVENT"), ("next week", "DATE"), ("Wednesday", "DATE"), ("Thursday afternoon", "DATE")]),
    ("Interview scheduled for 12/5 at 1pm, might shift to 2pm", [("Interview", "EVENT"), ("12/5", "DATE"), ("at 1pm", "TIME"), ("2pm", "TIME")]),
    
    ("Team lunch on Friday around noon, maybe 12:30", [("Team lunch", "EVENT"), ("Friday", "DATE"), ("around noon", "TIME"), ("12:30", "TIME")]),
    ("Standup at 9:30 tomorrow unless we move it to 10", [("Standup", "EVENT"), ("at 9:30", "TIME"), ("tomorrow", "DATE"), ("10", "TIME")]),
    ("Office hours Tuesday 2-4pm or Wednesday 1-3pm", [("Office hours", "EVENT"), ("Tuesday", "DATE"), ("2-4pm", "TIME"), ("Wednesday", "DATE"), ("1-3pm", "TIME")]),
    ("Review meeting next Monday at 3, might go until 5", [("Review meeting", "EVENT"), ("next Monday", "DATE"), ("at 3", "TIME"), ("5", "TIME")]),
    ("Coffee at Starbucks or Peet's, either Tuesday or Wednesday afternoon", [("Coffee", "EVENT"), ("Starbucks", "LOCATION"), ("Peet's", "LOCATION"), ("Tuesday", "DATE"), ("Wednesday afternoon", "DATE")]),
    
    # ===== CATEGORY 8: NEGATIVE EXAMPLES (40 examples - CRITICAL!) =====
    ("That's a great idea", []),
    ("I agree with you", []),
    ("What time is it?", []),
    ("I'm heading out now", []),
    ("The weather is nice today", []),
    ("I finished the project yesterday", []),
    ("That was a good meeting", []),
    ("Thanks for the update", []),
    ("I'll send it over later", []),
    ("Let me know what you think", []),
    
    ("The deadline was last week", []),
    ("I was at the office on Monday", []),
    ("She lives in San Francisco", []),
    ("The cafe is on Main Street", []),
    ("Zoom is a great tool", []),
    ("I use Google Calendar for events", []),
    ("Tomorrow is a holiday", []),
    ("I'm busy all next week", []),
    ("That time doesn't work for me", []),
    ("I can't make it", []),
    
    ("The meeting happened yesterday", []),
    ("We met last Tuesday", []),
    ("I was free at 3pm", []),
    ("My old office was downtown", []),
    ("Coffee is my favorite drink", []),
    ("Lunch was delicious", []),
    ("The project started in January", []),
    ("I'm on vacation next week", []),
    ("See you around", []),
    ("Take care", []),
    
    ("What's the address?", []),
    ("How long does it take?", []),
    ("Where is the office?", []),
    ("Who is coming?", []),
    ("Why did that happen?", []),
    ("I don't remember when that was", []),
    ("Do you have any availability?", []),
    ("What's on your calendar?", []),
    ("I need to schedule something", []),
    ("Let me check my schedule", []),
]


def get_training_data():
    """
    Automatically calculate character positions for entities
    """
    TRAIN_DATA = []
    
    for text, entities in SIMPLE_DATA:
        ents_list = []
        
        # Sort by length (longest first) to avoid substring issues
        sorted_entities = sorted(entities, key=lambda x: len(x[0]), reverse=True)
        
        for ent_text, label in sorted_entities:
            # Find all occurrences
            matches = list(re.finditer(re.escape(ent_text), text, re.IGNORECASE))
            
            if matches:
                match = matches[0]
                start = match.start()
                end = match.end()
                ents_list.append((start, end, label))
            else:
                print(f"WARNING: '{ent_text}' not found in '{text}'")
        
        TRAIN_DATA.append((text, {"entities": ents_list}))
    
    return TRAIN_DATA


# Export
TRAIN_DATA = get_training_data()

if __name__ == "__main__":
    print(f"✅ Generated {len(TRAIN_DATA)} training examples")
    print(f"   Events: ~{sum(1 for _, a in TRAIN_DATA if any(e[2] == 'EVENT' for e in a['entities']))}")
    print(f"   Dates: ~{sum(1 for _, a in TRAIN_DATA if any(e[2] == 'DATE' for e in a['entities']))}")
    print(f"   Times: ~{sum(1 for _, a in TRAIN_DATA if any(e[2] == 'TIME' for e in a['entities']))}")
    print(f"   Locations: ~{sum(1 for _, a in TRAIN_DATA if any(e[2] == 'LOCATION' for e in a['entities']))}")
    print(f"   Negative: {sum(1 for _, a in TRAIN_DATA if len(a['entities']) == 0)}")
