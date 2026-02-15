"""
EventSniffer Model Validation Suite
Tests model accuracy and identifies failure modes
"""

import spacy
from typing import Dict, List, Tuple
import json

# Test suite with expected outputs
VALIDATION_SUITE = [
    # Format: (text, expected_entities_dict)
    ("Let's meet tomorrow at 3pm", {"EVENT": ["meet"], "DATE": ["tomorrow"], "TIME": ["3pm"]}),
    ("sync tmrw 10a zoom", {"EVENT": ["sync"], "DATE": ["tmrw"], "TIME": ["10a"], "LOCATION": ["zoom"]}),
    ("Coffee on Main St next Tuesday", {"EVENT": ["Coffee"], "LOCATION": ["Main St"], "DATE": ["next Tuesday"]}),
    ("Doctor appointment on 12/5 at 2:30pm", {"EVENT": ["Doctor appointment"], "DATE": ["12/5"], "TIME": ["2:30pm"]}),
    ("That's a great idea", {}),  # Negative
    ("I finished the project yesterday", {}),  # Negative
    ("Are you free tomorrow?", {"DATE": ["tomorrow"]}),  # Partial
    ("Team lunch on Friday at noon at Chipotle", {"EVENT": ["Team lunch"], "DATE": ["Friday"], "TIME": ["noon"], "LOCATION": ["Chipotle"]}),
    ("wanna grab lunch fri?", {"EVENT": ["grab lunch"], "DATE": ["fri"]}),
    ("Meeting got moved from Tuesday to Thursday at 3pm", {"EVENT": ["Meeting"], "DATE": ["Tuesday", "Thursday"], "TIME": ["3pm"]}),
]


def evaluate_model(model_path: str) -> Dict:
    """
    Evaluate model on validation suite
    Returns accuracy metrics
    """
    print(f"\n🔍 Loading model from {model_path}...")
    try:
        nlp = spacy.load(model_path)
    except:
        print(f"❌ Model not found at {model_path}")
        return None
    
    results = {
        "total": len(VALIDATION_SUITE),
        "correct": 0,
        "partial": 0,
        "missed": 0,
        "false_positive": 0,
        "details": []
    }
    
    for i, (text, expected) in enumerate(VALIDATION_SUITE):
        doc = nlp(text)
        
        # Extract actual entities
        actual = {}
        for ent in doc.ents:
            if ent.label_ not in actual:
                actual[ent.label_] = []
            actual[ent.label_].append(ent.text.lower())
        
        # Normalize expected
        expected_norm = {k: [v.lower() for v in vals] for k, vals in expected.items()}
        
        # Check if match
        is_correct = True
        is_partial = False
        
        # Check for missing entities
        for label, expected_vals in expected_norm.items():
            if label not in actual:
                is_correct = False
                is_partial = False
                results["missed"] += 1
            else:
                # Check if all expected values found
                actual_vals = actual[label]
                if not all(any(exp in act for act in actual_vals) for exp in expected_vals):
                    is_correct = False
                    if any(any(exp in act for act in actual_vals) for exp in expected_vals):
                        is_partial = True
        
        # Check for false positives
        for label in actual:
            if label not in expected_norm:
                is_correct = False
                results["false_positive"] += 1
        
        # Update counters
        if is_correct:
            results["correct"] += 1
            status = "✅"
        elif is_partial:
            results["partial"] += 1
            status = "⚠️"
        else:
            status = "❌"
        
        # Store details
        results["details"].append({
            "text": text,
            "expected": expected,
            "actual": {k: list(set(v)) for k, v in actual.items()},
            "status": status
        })
        
        print(f"{status} Test {i+1}/{len(VALIDATION_SUITE)}: {text[:50]}")
    
    # Calculate accuracy
    accuracy = (results["correct"] / results["total"]) * 100
    partial_accuracy = ((results["correct"] + results["partial"]) / results["total"]) * 100
    
    print(f"\n📊 RESULTS:")
    print(f"   Accuracy: {accuracy:.1f}% ({results['correct']}/{results['total']})")
    print(f"   Partial:  {partial_accuracy:.1f}% (including partial matches)")
    print(f"   Missed:   {results['missed']} entities")
    print(f"   False+:   {results['false_positive']} false positives")
    
    return results


if __name__ == "__main__":
    # Test if model exists
    import sys
    model_path = sys.argv[1] if len(sys.argv) > 1 else "model_output"
    evaluate_model(model_path)
