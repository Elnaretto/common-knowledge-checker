from flask import Flask, render_template, request
import yaml

app = Flask(__name__)

CK_THRESHOLD = 4

criteria_keys = [
    "generations_known",
    "in_school_program",
    "media_frequency_high",
    "pop_culture_presence",
    "public_opinion_known",
    "national_symbol"
]

def is_common_knowledge(criteria: dict) -> bool:
    return sum(criteria.values()) >= CK_THRESHOLD

@app.route("/", methods=["GET", "POST"])
def index():
    result = ""
    error = ""

    if request.method == "POST":
        fact = request.form.get("fact", "").strip()
        selected_criteria = request.form.getlist("criteria")

        if not fact:
            error = "⚠️ Please enter a fact."
        elif not selected_criteria:
            error = "⚠️ Please select at least one criterion."
        else:
            criteria = {key: (key in selected_criteria) for key in criteria_keys}
            ck = is_common_knowledge(criteria)
            result = f"✅ Yes, this is common knowledge!" if ck else "❌ Not common knowledge."

    return render_template("index.html", result=result, error=error, criteria_keys=criteria_keys)

if __name__ == "__main__":
    app.run(debug=True)
