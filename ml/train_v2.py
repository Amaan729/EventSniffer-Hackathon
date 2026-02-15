"""
EventSniffer Training Script v2.0
Optimized for maximum accuracy
"""

import spacy
from spacy.training import Example
import random
from pathlib import Path

# Import our enhanced training data
import sys
sys.path.insert(0, '/tmp')
from training_data_v2 import get_training_data


def train_model(iterations=50, dropout=0.35):
    """
    Train NER model with optimized hyperparameters
    
    Args:
        iterations: Number of training iterations (more = better, up to a point)
        dropout: Regularization to prevent overfitting (0.3-0.5 range)
    """
    print("=" * 60)
    print("🚀 EventSniffer Model Training v2.0")
    print("=" * 60)
    
    # Load base model
    print("\n1️⃣ Loading base model (en_core_web_lg)...")
    try:
        nlp = spacy.load("en_core_web_lg")
        print("✅ Base model loaded")
    except OSError:
        print("❌ en_core_web_lg not found. Installing...")
        import subprocess
        subprocess.run(["python", "-m", "spacy", "download", "en_core_web_lg"])
        nlp = spacy.load("en_core_web_lg")
    
    # Setup NER pipe
    if "ner" not in nlp.pipe_names:
        ner = nlp.add_pipe("ner", last=True)
    else:
        ner = nlp.get_pipe("ner")
    
    # Load training data
    print("\n2️⃣ Loading training data...")
    TRAIN_DATA = get_training_data()
    print(f"✅ Loaded {len(TRAIN_DATA)} training examples")
    
    # Add labels
    labels = set()
    for _, annotations in TRAIN_DATA:
        for ent in annotations.get("entities", []):
            labels.add(ent[2])
            ner.add_label(ent[2])
    
    print(f"✅ Labels: {', '.join(sorted(labels))}")
    
    # Create training examples
    print("\n3️⃣ Preparing training examples...")
    examples = []
    for text, annotations in TRAIN_DATA:
        try:
            doc = nlp.make_doc(text)
            example = Example.from_dict(doc, annotations)
            examples.append(example)
        except Exception as e:
            print(f"⚠️  Skipping: '{text[:50]}...' - {e}")
    
    print(f"✅ Created {len(examples)} valid examples")
    
    if not examples:
        print("❌ No valid examples! Check training_data_v2.py")
        return
    
    # Training configuration
    print(f"\n4️⃣ Training configuration:")
    print(f"   Iterations: {iterations}")
    print(f"   Dropout: {dropout}")
    print(f"   Batch size: 8")
    
    # Train
    print("\n5️⃣ Starting training...")
    print("-" * 60)
    
    # Disable other pipes during training
    other_pipes = [pipe for pipe in nlp.pipe_names if pipe != "ner"]
    
    with nlp.select_pipes(disable=other_pipes):
        optimizer = nlp.initialize()
        
        best_loss = float('inf')
        patience = 10
        no_improvement = 0
        
        for itn in range(iterations):
            random.shuffle(examples)
            losses = {}
            
            # Train in batches
            batches = spacy.util.minibatch(examples, size=8)
            for batch in batches:
                nlp.update(
                    batch,
                    drop=dropout,
                    sgd=optimizer,
                    losses=losses
                )
            
            current_loss = losses.get('ner', 0.0)
            
            # Print progress
            if (itn + 1) % 5 == 0 or itn == 0:
                print(f"Iteration {itn + 1:3d}/{iterations} | Loss: {current_loss:8.4f}")
            
            # Early stopping check
            if current_loss < best_loss:
                best_loss = current_loss
                no_improvement = 0
            else:
                no_improvement += 1
            
            # Stop if no improvement
            if no_improvement >= patience and itn > 20:
                print(f"\n⚠️  Early stopping at iteration {itn + 1} (no improvement for {patience} iterations)")
                break
    
    print("-" * 60)
    print(f"✅ Training complete! Final loss: {best_loss:.4f}")
    
    # Save model
    output_dir = Path("model_output_v2")
    output_dir.mkdir(exist_ok=True)
    nlp.to_disk(output_dir)
    print(f"\n6️⃣ Model saved to '{output_dir}'")
    
    # Quick test
    print("\n7️⃣ Quick validation:")
    print("-" * 60)
    
    test_texts = [
        "Let's sync tomorrow at 10am on Zoom",
        "sync tmrw 10a",
        "Coffee next Tuesday?",
        "Doctor appointment on 12/5 at 2:30pm",
        "That's a great idea",  # Should find nothing
    ]
    
    nlp_trained = spacy.load(output_dir)
    for text in test_texts:
        doc = nlp_trained(text)
        if doc.ents:
            ents_str = ", ".join([f"{e.text}({e.label_})" for e in doc.ents])
            print(f"✅ '{text}' → {ents_str}")
        else:
            print(f"⚪ '{text}' → (no entities)")
    
    print("\n" + "=" * 60)
    print("🎉 DONE! Run validation with:")
    print(f"   python validate_model.py {output_dir}")
    print("=" * 60)


if __name__ == "__main__":
    train_model(iterations=50, dropout=0.35)
