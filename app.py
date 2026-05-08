from flask import Flask, request
import google.generativeai as genai
import requests
import os

app = Flask(__name__)
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

def analyze_food_image(image_url):
    model = genai.GenerativeModel('gemini-1.5-flash')
    img_data = requests.get(image_url).content
    prompt = "حلل الصورة دي وقولي الطبق فيه كام سعر حراري وكام جرام بروتين. رد في سطرين بالعربي بس."
    response = model.generate_content([prompt, {"mime_type": "image/jpeg", "data": img_data}])
    return response.text

@app.route("/")
def home():
    return "Bot is running"

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json
    if data.get("type") == "image":
        image_url = data["image"]["url"]
        result = analyze_food_image(image_url)
        return {"reply": f"{result}\n\nعاش، سجلتهولك 💪"}
    return {"reply": "ابعتلي صورة الأكل بس"}

if __name__ == "__main__":
    app.run()
