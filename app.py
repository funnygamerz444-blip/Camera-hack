import requests
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


@app.route('/')
def home():
  return 'Render Backend is Live with New API!'


@app.route('/api/player')
def proxy_player():
  uid = request.args.get('uid')
  if not uid:
    return jsonify({'success': False, 'error': 'UID required'}), 400

  # নতুন এপিআই লিংক এখানে সেট করা হলো
  target_url = f'https://nirob-x-info.vercel.app/info?uid={uid.strip()}'
  try:
    response = requests.get(target_url, timeout=15)
    if response.status_code == 200:
      data = response.json()

      # নতুন এপিআই-এর ফরম্যাট অনুযায়ী ডাটা রিড করা
      info = data.get('data') or data
      name = info.get('name') or info.get('nickname') or info.get('UserName')
      level = info.get('level') or info.get('Level') or 'N/A'
      region = info.get('region') or info.get('Server') or 'BD'
      likes = info.get('likes') or info.get('Liked') or '0'

      if name:
        return jsonify({
            'success': True,
            'data': {
                'basicInfo': {
                    'nickname': name,
                    'level': level,
                    'region': region,
                    'liked': likes,
                }
            },
        })
  except Exception as e:
    pass

  return jsonify({'success': False, 'error': 'Failed to fetch'}), 500


if __name__ == '__main__':
  app.run(host='0.0.0.0', port=5000)
