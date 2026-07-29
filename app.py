from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import requests

app = Flask(__name__, template_folder='.')
CORS(app)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/player', methods=['GET'])
def get_player_info():
    uid = request.args.get('uid')
    if not uid:
        return jsonify({"success": False, "error": "UID is required"}), 400
    
    try:
        target_api = f"https://info.killersharmabot.online/player-info?uid={uid}"
        response = requests.get(target_api, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            return jsonify({"success": True, "data": data})
        else:
            return jsonify({"success": False, "error": "Failed to fetch from external API"}), 500
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
