
from flask import Flask, jsonify

app = Flask(__name__)

# Sample data for listings
listings = [
    {'id': 1, 'title': 'Listing 1', 'description': 'Description 1'},
    {'id': 2, 'title': 'Listing 2', 'description': 'Description 2'},
]

@app.route('/api/listings', methods=['GET'])
def get_listings():
    return jsonify(listings), 200

@app.route('/api/listings/<int:id>', methods=['GET'])
def get_listing(id):
    listing = next((listing for listing in listings if listing['id'] == id), None)
    if listing:
        return jsonify(listing), 200
    else:
        return jsonify({'error': 'Listing not found'}), 404

if __name__ == '__main__':
    app.run(debug=True, port=5001)  # Changed to port 5001
