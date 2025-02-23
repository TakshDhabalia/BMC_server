from flask import Flask, request, jsonify
from flask_cors import CORS
import your_ml_model  # Replace with your actual ML model

app = Flask(__name__)
CORS(app)  # Allows requests from any origin (use specific origins in production)

@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.json  # Get JSON data from request
        text_input = data.get("text", "")  # Extract input text
        
        if not text_input:
            return jsonify({"error": "No input provided"}), 400

        # Process input through your ML model
        model_output = your_ml_model.run_inference(text_input)  # Replace with actual inference function

        return jsonify({"prediction": model_output})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)  # Run on port 8000
