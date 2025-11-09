import spacy
from flask import Flask, request, jsonify

# 1. Set up the Flask app
app = Flask(__name__)

# 2. Load our trained model
model_dir = "model_output"
print(f"Loading model from {model_dir}...")
try:
    nlp = spacy.load(model_dir)
    print("✅ Model loaded successfully.")
except Exception as e:
    print(f"❌ ERROR: Could not load model. {e}")
    nlp = None

# 3. Define the "/parse" endpoint
@app.route("/parse", methods=["POST"])
def parse_text():
    if not nlp:
        return jsonify({"error": "Model is not loaded"}), 500

    # Get the JSON data from the request (our Swift app will send this)
    data = request.get_json()

    if not data or "text" not in data:
        return jsonify({"error": "No 'text' field provided"}), 400

    text = data.get("text")

    # 4. Use our model to find entities
    doc = nlp(text)

    # 5. Format the entities into a clean JSON response
    entities = []
    for ent in doc.ents:
        entities.append({
            "text": ent.text,
            "label": ent.label_
        })

    print(f"Processed text, found {len(entities)} entities.")

    # Send the list of entities back to our Swift app
    return jsonify({"entities": entities})

# 6. Run the server
if __name__ == "__main__":
    print("Starting Flask server on http://127.0.0.1:5000 ...")
    # 'host="0.0.0.0"' makes it accessible on your local network
    # We use 127.0.0.1 (localhost) for our Swift app
    app.run(port=5000, host="127.0.0.1")