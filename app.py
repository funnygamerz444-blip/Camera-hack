import requests
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


@app.route('/')
def home():
  return 'Render Backend is Live!'


@app.route('/api/player')
def proxy_player():
  uid = request.args.get('uid')
  if not uid:
    return jsonify({'success': False, 'error': 'UID required'})

  # Working reliable endpoint
  target_url = f'https://mbf-api.demonsstore.workers.dev/?uid={uid}'
  try:
    response = requests.get(target_url, timeout=10)
    if response.status_code == 200:
      data = response.json()
      return jsonify({
          'success': True,
          'data': {
              'basicInfo': {
                  'nickname': data.get(
                      'name', data.get('nickname', 'Unknown')
                  ),
                  'level': data.get('level', 'N/A'),
                  'region': data.get('region', 'BD'),
                  'liked': data.get('likes', '0'),
              }
          },
      })
  except Exception as e:
    pass

  return jsonify({'success': False, 'error': 'Failed to fetch'})


if __name__ == '__main__':
  app.run(host='0.0.0.0', port=5000)
