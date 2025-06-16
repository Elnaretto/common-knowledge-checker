from flask import Flask, render_template_string, request
import os

app = Flask(__name__)
CK_THRESHOLD = 4

HTML_FORM = """
<!doctype html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Common Knowledge Checker</title>
  <style>
    body { font-family: Arial, sans-serif; margin: 40px; }
    input[type=text] { width: 100%; padding: 8px; margin-bottom: 10px; }
    button { padding: 10px 20px; }
    .result { margin-top: 20px; padding: 10px; border: 1px solid #ccc; }
  </style>
</head>
<body>
  <h2>Check if a fact is Common Knowledge (CK)</h2>
  <form method="POST">
    <label>Fact:</label><br>
    <input type="text" name="fact" required><br><br>

    {% for c in criteria %}
      <label><input type="checkbox" name="{{ c }}" value="true"> {{ c.replace('_', ' ').title() }}</label><br>
    {% endfor %}
    <br>
    <button type="submit">Check CK</button>
  </form>

  {% if result is not none %}
    <div class="result">
      <h3>Result:</h3>
      <p><strong>Fact:</strong> {{ fact }}</p>
      <p><strong>Criteria passed:</strong> {{ score }}/{{ total }}</p>
      <p><strong>Status:</strong> {{ "✅ Common Knowledge" if result else "❌ Not Common Knowledge" }}</p>
    </div>
  {% endif %}
</body>
</html>
"""

criteria_list = [
    "факт знают три поколения россиян (20 лет, 45 лет, 65 лет",
    "входит в школьную программу до 9 класса",
    "часто упоминается в СМИ",
    "представлен в поп-культуре",
    "мы знаем общественное мнение по этой теме",
    "национальный символ"
]

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    fact = ""
    score = 0
    total = len(criteria_list)

    if request.method == "POST":
        fact = request.form.get("fact", "")
        criteria_values = {c: (request.form.get(c) == "true") for c in criteria_list}
        score = sum(criteria_values.values())
        result = score >= CK_THRESHOLD

    return render_template_string(HTML_FORM, criteria=criteria_list, result=result, fact=fact, score=score, total=total)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
