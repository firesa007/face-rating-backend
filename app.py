from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI
import base64
import os

# Initialize OpenAI client with the new v1.0+ syntax
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app = Flask(__name__)
CORS(app)

@app.route('/api/rate', methods=['POST'])
def rate_face():
    if 'image' not in request.files:
        return jsonify({'error': 'No image uploaded'}), 400

    image_file = request.files['image']
    image_bytes = image_file.read()
    base64_image = base64.b64encode(image_bytes).decode('utf-8')

    try:
        # Use the new OpenAI API syntax
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "What is the hair color in this image? One word answer."},
                        {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}
                    ],
                }
            ],
            max_tokens=10
        )
        
        rating = response.choices[0].message.content.strip()
        return jsonify({'rating': rating})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)