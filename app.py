import os
import json
from flask import Flask, request, jsonify, render_template
import base64
from google import genai
from google.genai import types
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Configure Gemini API
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("Missing GEMINI_API_KEY. Set it as an environment variable.")

# Initialize Gemini client
client = genai.Client(api_key=GEMINI_API_KEY)

# Model configuration
MODEL_NAME = "gemini-2.0-flash"
GENERATION_CONFIG = types.GenerateContentConfig(
    temperature=1,
    top_p=0.95,
    top_k=40,
    max_output_tokens=8192,
    response_mime_type="text/plain",
)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/generate", methods=["POST"])
def generate_meal_plan():
    try:
        data = request.json
        print("\n📩 Received Data:", json.dumps(data, indent=4))  # ✅ Print received input

        # Construct user prompt
        user_prompt = f"""
        Generate a detailed meal plan considering the following:
        - Age: {data.get('age')}
        - Gender: {data.get('gender')}
        - Weight: {data.get('weight')} kg
        - Height: {data.get('height')} cm
        - Activity Level: {data.get('activity')}
        - Diet Restrictions: {", ".join(data.get('diet_restrictions', []))}
        - Custom Diet: {data.get('custom_diet')}
        - Allergies: {data.get('allergies')}
        - Health Conditions: {data.get('health')}
        - Goal: {data.get('goal')}
        - Preferred Cuisine: {data.get('cuisine')}
        - Number of Meals per Day: {data.get('meals')}
        - Foods to Include: {data.get('include_foods')}
        - Foods to Avoid: {data.get('avoid_foods')}
        
        Provide meal recommendations with recipes for breakfast, lunch, dinner, and snacks.
        """

        # Prepare request content
        contents = [
            types.Content(
                role="user",
                parts=[types.Part.from_text(text=user_prompt)],
            )
        ]

        # Generate AI response
        response_text = ""
        for chunk in client.models.generate_content_stream(
            model=MODEL_NAME,
            contents=contents,
            config=GENERATION_CONFIG,
        ):
            response_text += chunk.text

        print("\n📝 AI Generated Meal Plan:\n", response_text)  # ✅ Print response to terminal

        return jsonify({"meal_plan": response_text.strip()})  # Send response to frontend

    except Exception as e:
        print("\n❌ Error:", str(e))  # ✅ Print errors
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
