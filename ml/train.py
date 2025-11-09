# train.py
# --- THIS IS THE CORRECTED VERSION ---

import spacy
from spacy.tokens import DocBin
from spacy.training import Example
import random

# **** THIS IS THE FIX ****
# We are now importing the function, not the old variable
from training_data import get_training_data

def train_model(iterations=30):
    print("Loading base model (en_core_web_lg)...")
    nlp = spacy.load("en_core_web_lg")
    
    if "ner" not in nlp.pipe_names:
        ner = nlp.add_pipe("ner", last=True)
    else:
        ner = nlp.get_pipe("ner")

    # Load the data from our function
    TRAIN_DATA = get_training_data()

    # Add our custom labels (EVENT, DATE, TIME, LOCATION)
    for _, annotations in TRAIN_DATA:
        for ent in annotations.get("entities"):
            ner.add_label(ent[2])

    print("Preparing training data...")
    
    db = DocBin()
    examples = []
    
    # **** THIS IS THE FIX ****
    # We are now iterating over the correct data
    for text, annotations in TRAIN_DATA:
        try:
            doc = nlp.make_doc(text)
            example = Example.from_dict(doc, annotations)
            examples.append(example)
        except ValueError as e:
            print(f"Error processing data: {e} - Skipping example: '{text}'")

    # Check if we actually have examples
    if not examples:
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        print("ERROR: No training data was loaded. Check 'training_data.py'.")
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        return

    print(f"Loaded {len(examples)} valid training examples.")
        
    db.to_disk("./train.spacy")
    
    print(f"--- Starting training ({iterations} iterations) ---")

    pipe_exceptions = ["ner"]
    unaffected_pipes = [pipe for pipe in nlp.pipe_names if pipe not in pipe_exceptions]
    
    with nlp.select_pipes(disable=unaffected_pipes):
        optimizer = nlp.initialize()
        
        for itn in range(iterations):
            random.shuffle(examples)
            losses = {}
            
            for batch in spacy.util.minibatch(examples, size=8):
                nlp.update(
                    batch,
                    drop=0.3,
                    sgd=optimizer,
                    losses=losses
                )
            
            if (itn + 1) % 5 == 0:
                print(f"Iteration {itn + 1}/{iterations} | Loss: {losses.get('ner', 0.0)}")

    print("--- Training finished! ---")
    
    output_dir = "model_output"
    nlp.to_disk(output_dir)
    print(f"✅ Model saved to '{output_dir}'")
    
    print("\n--- Testing model on examples ---")
    nlp_trained = spacy.load(output_dir)
    
    test_texts = [
        "Let's have a quick sync tomorrow at 10am on Zoom",
        "The project is due next Monday",
        "I'm free this afternoon",
        "What about coffee at the cafe?",
        "That was a great presentation."
    ]
    
    for text in test_texts:
        print(f"\nText: '{text}'")
        doc = nlp_trained(text)
        if not doc.ents:
            print("  -> No entities found.")
        else:
            for ent in doc.ents:
                print(f"  -> Found: '{ent.text}' ({ent.label_})")

if __name__ == "__main__":
    train_model(iterations=30)