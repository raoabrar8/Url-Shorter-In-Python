from flask import Flask, request, redirect, jsonify
import string
import random

app = Flask(__name__)

url_mapping = {}
base_url = "http://localhost:5000/"

def generate_short_id(num_chars=6):
    """Generate a random string of fixed length."""
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(num_chars))

@app.route('/shorten', methods=['POST'])
def shorten_url():
    """Endpoint to shorten a URL."""
    long_url = request.json['long_url']
    short_id = generate_short_id()
    
    while short_id in url_mapping:
        short_id = generate_short_id()

    url_mapping[short_id] = long_url
    short_url = base_url + short_id

    return jsonify({"short_url": short_url})

@app.route('/<short_id>', methods=['GET'])
def redirect_to_long_url(short_id):
    """Endpoint to redirect to the original URL."""
    long_url = url_mapping.get(short_id)
    if long_url:
        return redirect(long_url)
    else:
        return jsonify({"error": "URL not found"}), 404
    


if __name__ == '__main__':
    app.run(debug=True)
