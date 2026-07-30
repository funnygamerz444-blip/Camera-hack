import requests
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


@app.route('/')
def home():
  return 'Render Backend Server is Live and Running for Yeaxin Panel!'


@app.route('/api/player')
def proxy_player():
  uid = request.args.get('uid')
  if not uid:
    return jsonify({'success': False, 'error': 'UID required'})

  target_url = f'https://star-info-api.lovable.app/functions/v1/info-api/accinfo?uid={uid}'
  try:
    response = requests.get(target_url, timeout=10)
    if response.status_code == 200:
      api_data = response.json()
      # Directly return the parsed fields to match JS keys
      return jsonify(api_data)
  except Exception as e:
    pass

  return jsonify({'success': False, 'error': 'Failed to fetch'})


if __name__ == '__main__':
  app.run(host='0.0.0.0', port=5000)
