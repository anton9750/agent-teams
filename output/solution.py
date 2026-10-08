from flask import Flask, request, jsonify
import redis
import json
import logging
from urllib.parse import urlparse

app = Flask(__name__)
redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)
logger = logging.getLogger(__name__)

@app.route('/process_image', methods=['POST'])
def process_image():
    data = request.json
    image_url = data.get('image_url')
    
    if not image_url:
        return jsonify({'error': 'Image URL is required'}), 400
    
    # Validate the image URL
    if not validate_image_url(image_url):
        return jsonify({'error': 'Invalid image URL'}), 400
    
    # Enqueue the image URL for processing
    try:
        redis_client.rpush('image_queue', json.dumps({'image_url': image_url}))
    except redis.RedisError as e:
        logger.error(f'Redis error: {e}')
        return jsonify({'error': 'Failed to enqueue image URL'}), 500
    
    return jsonify({'message': 'Image processing initiated'}), 202

def validate_image_url(url):
    # Implement URL validation logic
    # Example: Check if the URL is in a whitelist of allowed domains
    allowed_domains = ['example.com', 'another-example.com']
    parsed_url = urlparse(url)
    return parsed_url.netloc in allowed_domains

if __name__ == '__main__':
    app.run(debug=True)
