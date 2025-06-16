from flask import Flask, render_template, request
import yaml
import os

app = Flask(__name__)

CK_THRESHOLD = 4

def is_common_knowledge(criteria: dict) -> bool:
    return sum(criteria.values()) >= CK_THRESHOLD

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    score = 0
    if request.method == "POST":
        criteria = {
            "generations_known": request.form.get("generations_known") == "on",
            "in_school_program": request.form.get("in_school_program") == "on",
            "media_frequency_high": request.form.get("media_frequency_high") == "on",
            "pop_culture_presence": request.form.get("pop_culture_presence") == "on",
            "public_opinion_known": request.form.get("public_opinion_known") == "on",
            "national_symbol": request.form.get("national_symbol") == "on",
        }
        score = sum(criteria.values())
        result = is_common_knowledge(criteria)
    return render_template("index.html", result=result, score=score)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
