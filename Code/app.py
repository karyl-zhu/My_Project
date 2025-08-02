from flask import Flask, request, jsonify, render_template
import requests

app = Flask(__name__)

GOOGLE_MAPS_API_KEY = "你的_API_KEY"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/restaurants")
def get_restaurants():
    lat = request.args.get("lat")
    lng = request.args.get("lng")
    if not lat or not lng:
        return jsonify({"error": "缺少經緯度參數"}), 400

    url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
    params = {
        "location": f"{lat},{lng}",
        "radius": 5000,  # 公里範圍
        "type": "restaurant",
        "key": GOOGLE_MAPS_API_KEY
    }

    response = requests.get(url, params=params)
    data = response.json()
    return jsonify(data)

if __name__ == "__main__":
    app.run(debug=True)
