from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Function to get a quantum random number (0-255)
def get_quantum_random_number():
    response = requests.get("https://qrng.anu.edu.au/API/jsonI.php?length=1&type=uint8")
    if response.status_code == 200:
        data = response.json()
        return data['data'][0]
    else:
        # Fall back to classical randomness if API fails
        import random
        return random.randint(0, 255)

# Function to map a value from 0-255 to any min-max range
def map_number(value, from_min, from_max, to_min, to_max):
    return int((value - from_min) * (to_max - to_min) / (from_max - from_min) + to_min)

@app.route('/random', methods=['GET'])
def random_number():
    min_val = int(request.args.get('min', 0))
    max_val = int(request.args.get('max', 100))
    if min_val > max_val:
        return jsonify({"error": "min cannot be greater than max"}), 400

    q_random = get_quantum_random_number()
    mapped = map_number(q_random, 0, 255, min_val, max_val)
    return jsonify({"random_number": mapped})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)