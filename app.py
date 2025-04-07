from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

@app.route("/reverse-image", methods=["GET"])
def reverse_image():
    image_url = request.args.get("image_url")
    api_key = os.getenv("SERPAPI_KEY")

    params = {
        "engine": "google_reverse_image",
        "image_url": image_url,
        "api_key": api_key
    }

    response = requests.get("https://serpapi.com/search", params=params)
    data = response.json()

    results = []
    for result in data.get("image_results", []):
        results.append({
            "title": result.get("title"),
            "link": result.get("link"),
            "thumbnail": result.get("thumbnail")
        })

    found_people = [img.get("title") for img in data.get("inline_images", []) if "title" in img]

    return jsonify({
        "results": results,
        "found_people": found_people
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
