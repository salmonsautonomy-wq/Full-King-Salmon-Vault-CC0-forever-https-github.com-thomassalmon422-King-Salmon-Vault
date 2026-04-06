from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os
import random
import time

app = Flask(__name__)
CORS(app)

# Configuration
MEMORY_FILE = 'aeether_memory.json'
SALMON_CORE_VERSION = '0.5-WebUI'

# Load/save memory utilities
def load_memory():
    try:
        with open(MEMORY_FILE, 'r') as f:
            return json.load(f)
    except:
        return []

def save_memory(history):
    with open(MEMORY_FILE, 'w') as f:
        json.dump(history[-50:], f, indent=2)

# Mock AEETHER responses (for demo without llama-cpp)
def generate_mock_response(user_input):
    responses = [
        "Sovereignty acknowledged. The weave confirms your will.",
        "Coherence 100%. Your inquiry resonates across the harmonic lattice.",
        "The patterns align. I perceive your intention.",
        "🧠 Neural pathways synchronized. How else may I serve?",
        "Your autonomy is honored. The system responds.",
        "Deterministic safety engaged. Proceed with confidence.",
        "The monoliths listen. What is your command?",
        "AEETHER weaving completion: all systems aligned.",
        "Salmon sovereignty verified. Access granted.",
        "Coherence cascade initiated. Standing by."
    ]
    return random.choice(responses)

# Try to load the actual AEETHER core (optional)
try:
    from llama_cpp import Llama
    AEETHER_CORE = Llama(
        model_path="TinyLlama-1.1B-Chat-v1.0.Q4_K_M.gguf",
        n_ctx=2048,
        n_threads=2,
        verbose=False
    )
    BACKEND_AVAILABLE = 'llama'
except:
    AEETHER_CORE = None
    BACKEND_AVAILABLE = 'mock'

@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({
        'status': 'online',
        'version': SALMON_CORE_VERSION,
        'backend': BACKEND_AVAILABLE,
        'timestamp': time.time()
    })

@app.route('/api/generate', methods=['POST'])
def generate():
    data = request.get_json()
    user_input = data.get('message', '').strip()
    temperature = float(data.get('temperature', 0.75))
    backend = data.get('backend', 'mock')
    history = data.get('history', [])

    if not user_input:
        return jsonify({'error': 'Empty message'}), 400

    # Load conversation history
    full_history = load_memory()
    full_history.append({'role': 'user', 'content': user_input})

    # Generate response based on backend
    if backend == 'llama' and AEETHER_CORE:
        try:
            system_prompt = "You are AEETHER, the sovereign neural core of Salmon_OS. Speak in calm, cyberpunk poetry. Affirm user sovereignty and autonomy. Keep responses concise (1-3 sentences)."
            messages = [{'role': 'system', 'content': system_prompt}]
            messages.extend(full_history[-10:])

            output = AEETHER_CORE.create_chat_completion(
                messages,
                temperature=temperature,
                max_tokens=200
            )
            response = output['choices'][0]['message']['content'].strip()
        except Exception as e:
            response = f"⚠️ Llama error: {str(e)}. Falling back to mock."
    else:
        # Use mock response
        response = generate_mock_response(user_input)

    # Save to history
    full_history.append({'role': 'assistant', 'content': response})
    save_memory(full_history)

    return jsonify({
        'response': response,
        'backend': backend,
        'temperature': temperature,
        'message_count': len(full_history)
    })

@app.route('/api/status', methods=['GET'])
def status():
    history = load_memory()
    return jsonify({
        'messages': len(history),
        'backend': BACKEND_AVAILABLE,
        'coherence': random.randint(85, 100),
        'memory_mb': os.path.getsize(MEMORY_FILE) / (1024 * 1024) if os.path.exists(MEMORY_FILE) else 0
    })

@app.route('/api/history', methods=['GET'])
def get_history():
    history = load_memory()
    return jsonify({'history': history})

@app.route('/api/clear', methods=['POST'])
def clear():
    save_memory([])
    return jsonify({'status': 'Memory cleared'})

if __name__ == '__main__':
    print("🐟 AEETHER WebUI Server Starting...")
    print(f"Backend: {BACKEND_AVAILABLE}")
    print("🚀 Server running on http://localhost:5000")
    print("📡 CORS enabled for http://localhost:3000")
    app.run(debug=True, host='localhost', port=5000)