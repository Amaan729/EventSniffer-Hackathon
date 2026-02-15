"""
Hybrid Event Parser: NER Model + Rule-Based Post-Processing
Combines ML predictions with deterministic rules for maximum accuracy
"""

import spacy
import re
from datetime import datetime
from typing import List, Dict, Any


class HybridEventParser:
    """
    Two-stage parser:
    1. Use spaCy NER model for entity extraction
    2. Apply rule-based post-processing to fix/enhance results
    """
    
    def __init__(self, model_path="model_output_v2"):
        """Load the trained NER model"""
        print(f"Loading model from {model_path}...")
        self.nlp = spacy.load(model_path)
        print("✅ Model loaded")
        
        # Date patterns
        self.date_patterns = [
            # Relative dates
            (r'\b(today|tonight|tn|tonite)\b', 'DATE'),
            (r'\b(tomorrow|tmrw|tmr|tmw)\b', 'DATE'),
            (r'\b(yesterday)\b', 'DATE'),
            (r'\b(next|this)\s+(week|month|year)\b', 'DATE'),
            (r'\b(next|this)\s+(mon|monday|tues|tuesday|wed|wednesday|thurs|thursday|fri|friday|sat|saturday|sun|sunday)\b', 'DATE'),
            (r'\b(mon|monday|tues|tuesday|wed|wednesday|thurs|thursday|fri|friday|sat|saturday|sun|sunday)\b', 'DATE'),
            
            # Absolute dates
            (r'\b\d{1,2}/\d{1,2}(/\d{2,4})?\b', 'DATE'),  # 12/5, 12/5/24
            (r'\b(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[a-z]*\s+\d{1,2}(st|nd|rd|th)?\b', 'DATE'),  # Dec 5th
            (r'\b\d{1,2}(st|nd|rd|th)?\s+(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[a-z]*\b', 'DATE'),  # 5th Dec
        ]
        
        # Time patterns
        self.time_patterns = [
            # Standard times
            (r'\b\d{1,2}:\d{2}\s*(am|pm|AM|PM)?\b', 'TIME'),  # 3:30pm
            (r'\b\d{1,2}\s*(am|pm|AM|PM|a|p)\b', 'TIME'),  # 3pm, 3p
            (r'\b(at|@)\s*\d{1,2}(:\d{2})?\s*(am|pm|AM|PM|a|p)?\b', 'TIME'),  # at 3, @ 3pm
            
            # Time ranges
            (r'\b\d{1,2}(:\d{2})?\s*-\s*\d{1,2}(:\d{2})?\s*(am|pm|AM|PM)?\b', 'TIME'),  # 2-4pm
            (r'\b(from|between)\s+\d{1,2}.*?\d{1,2}\s*(am|pm|AM|PM)\b', 'TIME'),
            
            # Relative times
            (r'\b(noon|midnight|EOD|end of day)\b', 'TIME'),
            (r'\b(morning|afternoon|evening|night)\b', 'TIME'),
            (r'\bin\s+\d+\s+(min|minutes|mins|hour|hours|hr|hrs)\b', 'TIME'),
        ]
        
        # Location patterns
        self.location_patterns = [
            # Virtual
            (r'\b(zoom|teams|google meet|slack|webex|skype)\b', 'LOCATION'),
            (r'https?://\S+', 'LOCATION'),  # URLs
            
            # Physical markers
            (r'\bat\s+[A-Z][a-z]+\'?s\b', 'LOCATION'),  # at Joe's
            (r'\b(conference room|conf room|room)\s+[A-Z0-9]+\b', 'LOCATION'),
            (r'\bon\s+[A-Z][a-z]+\s+(st|street|ave|avenue|rd|road|blvd|boulevard)\b', 'LOCATION'),
        ]
    
    def parse(self, text: str) -> Dict[str, Any]:
        """
        Parse text for calendar events
        
        Returns:
            {
                'entities': [...],  # Raw NER entities
                'enhanced': {...},  # Enhanced with rules
                'confidence': float,  # Overall confidence
                'calendar_event': {...} or None  # Ready-to-use event
            }
        """
        # Stage 1: NER extraction
        doc = self.nlp(text)
        ner_entities = []
        for ent in doc.ents:
            ner_entities.append({
                'text': ent.text,
                'label': ent.label_,
                'start': ent.start_char,
                'end': ent.end_char
            })
        
        # Stage 2: Rule-based enhancement
        enhanced_entities = self._apply_rules(text, ner_entities)
        
        # Stage 3: Build calendar event
        calendar_event = self._build_calendar_event(enhanced_entities, text)
        
        # Stage 4: Calculate confidence
        confidence = self._calculate_confidence(enhanced_entities, calendar_event)
        
        return {
            'entities': ner_entities,
            'enhanced': enhanced_entities,
            'confidence': confidence,
            'calendar_event': calendar_event
        }
    
    def _apply_rules(self, text: str, ner_entities: List[Dict]) -> Dict[str, List[str]]:
        """Apply regex rules to catch what NER missed"""
        enhanced = {
            'EVENT': [],
            'DATE': [],
            'TIME': [],
            'LOCATION': []
        }
        
        # Add NER findings
        for ent in ner_entities:
            if ent['label'] in enhanced:
                enhanced[ent['label']].append(ent['text'])
        
        # Apply date rules
        for pattern, label in self.date_patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                val = match.group(0)
                if val not in enhanced['DATE']:
                    enhanced['DATE'].append(val)
        
        # Apply time rules
        for pattern, label in self.time_patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                val = match.group(0)
                if val not in enhanced['TIME']:
                    enhanced['TIME'].append(val)
        
        # Apply location rules
        for pattern, label in self.location_patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                val = match.group(0)
                if val not in enhanced['LOCATION']:
                    enhanced['LOCATION'].append(val)
        
        return enhanced
    
    def _build_calendar_event(self, entities: Dict, text: str) -> Dict:
        """Try to build a complete calendar event"""
        if not entities.get('EVENT') and not entities.get('DATE'):
            return None  # No event detected
        
        # Infer event title
        title = entities.get('EVENT', ['New Event'])[0] if entities.get('EVENT') else "Event"
        
        # Get date/time
        date_str = entities.get('DATE', [None])[0]
        time_str = entities.get('TIME', [None])[0]
        location = entities.get('LOCATION', [None])[0]
        
        return {
            'title': title.title(),
            'date': date_str,
            'time': time_str,
            'location': location,
            'original_text': text
        }
    
    def _calculate_confidence(self, entities: Dict, event: Dict) -> float:
        """Calculate confidence score 0-1"""
        if not event:
            return 0.0
        
        score = 0.0
        
        # Has event name: +0.4
        if entities.get('EVENT'):
            score += 0.4
        
        # Has date: +0.3
        if entities.get('DATE'):
            score += 0.3
        
        # Has time: +0.2
        if entities.get('TIME'):
            score += 0.2
        
        # Has location: +0.1
        if entities.get('LOCATION'):
            score += 0.1
        
        return min(score, 1.0)


# Demo usage
if __name__ == "__main__":
    parser = HybridEventParser("model_output_v2")
    
    test_cases = [
        "Let's sync tomorrow at 10am on Zoom",
        "sync tmrw 10a",
        "Coffee next Tuesday?",
        "Meeting @ 3pm",
        "Doctor appointment on 12/5 at 2:30pm",
        "That's a great idea",  # Should return None
    ]
    
    print("\n" + "=" * 80)
    print("🔍 HYBRID PARSER DEMO")
    print("=" * 80)
    
    for text in test_cases:
        print(f"\nInput: '{text}'")
        result = parser.parse(text)
        
        if result['calendar_event']:
            print(f"✅ Event detected (confidence: {result['confidence']:.0%})")
            event = result['calendar_event']
            print(f"   Title: {event['title']}")
            print(f"   Date: {event['date'] or 'N/A'}")
            print(f"   Time: {event['time'] or 'N/A'}")
            print(f"   Location: {event['location'] or 'N/A'}")
        else:
            print(f"⚪ No event detected")
