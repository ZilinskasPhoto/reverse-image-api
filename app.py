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

    # Debug: spausdink visą SerpAPI atsakymą
    print("SERPAPI RAW RESPONSE:")
    print(data)

    results = []
    found_people = []

    # 1. Tikrink knowledge graph (pvz. žinomi žmonės)
    if "knowledge_graph" in data and "title" in data["knowledge_graph"]:
        found_people.append(data["knowledge_graph"]["title"])

    # 2. Inline images (dažnai su thumbnail'ais ir pavadinimais)
    if "inline_images" in data:
        for item in data["inline_images"]:
            if "title" in item:
                found_people.append(item["title"])

    # 3. Įprasti rezultatai su nuorodomis
    if "image_results" in data:
        for result in data["image_results"]:
            results.append({
                "title": result.get("title"),
                "link": result.get("link"),
                "thumbnail": result.get("thumbnail")
            })

    return jsonify({
        "results": results,
        "found_people": found_people
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
