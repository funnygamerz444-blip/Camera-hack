import requests
from flask import Flask, jsonify, request

app = Flask(__name__)


@app.route('/api/player')
def proxy_player():
  uid = request.args.get('uid')
  if not uid:
    return jsonify({'success': False, 'error': 'UID required'})

  target_url = f'https://star-info-api.lovable.app/functions/v1/info-api/accinfo?uid={uid}'
  try:
    response = requests.get(target_url, timeout=10)
    if response.status_code == 200:
      return jsonify({'success': True, 'data': response.json()})
  except Exception as e:
    pass

  return jsonify({'success': False, 'error': 'Failed to fetch'})
