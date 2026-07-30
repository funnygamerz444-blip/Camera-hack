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
    return jsonify(
        {'success': False, 'error': 'UID required', 'name': 'API Data Not Found'}
    )

  # Using a reliable alternative endpoint
  target_url = f'https://mbf-api.demonsstore.workers.dev/?uid={uid}'
  try:
    response = requests.get(target_url, timeout=10)
    if response.status_code == 200:
      data = response.json()
      # Map fields correctly to match your panel layout
      return jsonify({
          'name': data.get('name', 'Unknown Player'),
          'level': data.get('level', 'N/A'),
          'region': data.get('region', 'BD'),
          'likes': data.get('likes', '0'),
      })
  except Exception as e:
    pass

  return jsonify({
      'name': 'API Data Not Found',
      'level': 'N/A',
      'region': 'BD',
      'likes': '0',
  })


if __name__ == '__main__':
  app.run(host='0.0.0.0', port=5000)
