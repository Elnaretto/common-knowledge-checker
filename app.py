from flask import Flask, render_template, request
import yaml

app = Flask(__name__)

CK_THRESHOLD = 4

def is_common_knowledge(criteria):
    return sum(criteria.values()) >= CK_THRESHOLD

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    if request.method == "POST":
        fact = request.form.get("fact", "")
        
        # Collect criteria as booleans from form inputs
        criteria = {
            "generations_known": request.form.get("generations_known") == "on",
            "in_school_program": request.form.get("in_school_program") == "on",
            "media_frequency_high": request.form.get("media_frequency_high") == "on",
            "pop_culture_presence": request.form.get("pop_culture_presence") == "on",
            "public_opinion_known": request.form.get("public_opinion_known") == "on",
            "national_symbol": request.form.get("national_symbol") == "on",
        }

        score = sum(criteria.values())
        ck = is_common_knowledge(criteria)
        result = {
            "fact": fact,
            "score": score,
            "criteria": criteria,
            "is_ck": ck
        }

    return render_template("index.html", result=result)

if __name__ == "__main__":
    app.run(debug=True)
