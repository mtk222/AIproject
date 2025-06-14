import openai
from flask import Flask, request, render_template_string
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")  # removed my key for now

TEMPLATE = """
<!doctype html>
<title>Customer Profile Curator</title>
<h1>Describe your retail business or goals:</h1>
<form method=post>
  <textarea name=prompt rows=4 cols=50>{{ prompt }}</textarea><br><br>
  <input type=submit value=Get Profiles>
</form>
{% if ideas %}
  <h2>Typical Customer Profiles:</h2>
  <ul>
  {% for idea in ideas %}
    <li>{{ idea }}</li>
  {% endfor %}
  </ul>
{% endif %}
"""

@app.route("/", methods=["GET", "POST"])
def home():
    ideas = []
    prompt = ""
    if request.method == "POST":
        prompt = request.form["prompt"]
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a market analyst helping retail businesses understand customer segments."},
                {"role": "user", "content": f"As a retailer, I want to understand my typical customer. Here is some info about my business: {prompt}. Can you provide 5 example customer profiles with details like demographics, behaviors, and motivations?"}
            ]
        )
        content = response.choices[0].message.content
        ideas = content.split("\n")
        ideas = [idea.strip("- ") for idea in ideas if idea.strip()]
    return render_template_string(TEMPLATE, ideas=ideas, prompt=prompt)

if __name__ == "__main__":
    app.run(debug=True)
