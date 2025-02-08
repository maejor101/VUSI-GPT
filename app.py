from flask import Flask, request, jsonify, render_template
import subprocess
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return render_template('index.html')  

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        message = data.get('message')

        if not message:
            return jsonify({'error': 'No message provided'}), 400  
        result = subprocess.run(
            ['ollama', 'run', 'deepseek-coder', message], 
            capture_output=True, 
            text=True,
            encoding='utf-8'  
        )

        print(f"STDOUT: {result.stdout}")
        print(f"STDERR: {result.stderr}")

        if result.returncode != 0:
            return jsonify({'error': 'Failed to get a response from the model'}), 500

        response = result.stdout.strip() if result.stdout else "No response from the model"
        return jsonify({'response': response}), 200

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': 'An error occurred while processing your request'}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5001)
