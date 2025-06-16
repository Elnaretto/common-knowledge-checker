from flask import Flask, request, render_template_string
import yaml

app = Flask(__name__)

HTML_FORM = """
<!doctype html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Common Knowledge Checker</title>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap" rel="stylesheet">
  <style>
    body {
      font-family: 'Inter', sans-serif;
      background: #f7f9fc;
      color: #333;
      padding: 40px;
      max-width: 600px;
      margin: auto;
    }
    h2 {
      color: #2c3e50;
    }
    input[type="text"] {
      width: 100%;
      padding: 10px;
      border-radius: 6px;
      border: 1px solid #ccc;
      margin-bottom: 20px;
      font-size: 16px;
    }
    label {
      display: block;
      margin-bottom: 10px;
      font-size: 16px;
    }
    button {
      background: #2ecc71;
      color: white;
      padding: 12px 20px;
      border: none;
      border-radius: 6px;
      font-size: 16px;
      cursor: pointer;
    }
    button:hover {
      background: #27ae60;
    }
    .result {
      margin-top: 30px;
      padding: 20px;
      background: white;
      border-radius: 8px;
      box-shadow: 0 0 10px rgba(0,0,0,0.05);
    }
  </style>
</head>
<body>
  <h2>🔍 Common Knowledge Checker</h2>
  <form method="post">
    <label>Факт:</label>
    <input type="text" name="fact" required>

    <label><input type="checkbox" name="criteria" value="generations_known"> Известно многим поколениям</label>
    <label><input type="checkbox" name="criteria" value="in_school_program"> В школьной программе</label>
    <label><input type="checkbox" name="criteria" value="media_frequency_high"> Часто упоминается в СМИ</label>
    <label><input type="checkbox" name="criteria" value="pop_culture_presence"> Присутствует в поп-культуре</label>
    <label><input type="checkbox" name="criteria" value="public_opinion_known"> Известно по опросам</label>
    <label><input type="checkbox" name="criteria" value="national_symbol"> Национальный символ</label>

    <br><br>
    <button type="submit">Проверить</button>
  </form>

  {% if result %}
    <div class="result">
      <h3>Результат:</h3>
      <p><strong>Факт:</strong> {{ fact }}</p>
      <p><strong>Критериев выполнено:</strong> {{ score }}/6</p>
      <p><strong>Вывод:</strong> {{ result }}</p>
    </div>
  {% endif %}
</body>
</html>
"""

CK_THRESHOLD = 4

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    fact = ""
    score = 0
    if request.method == "POST":
        fact = request.form.get("fact")
        selected_criteria = request.form.getlist("criteria")
        criteria_dict = {
            "generations_known": "generations_known" in selected_criteria,
            "in_school_program": "in_school_program" in selected_criteria,
            "media_frequency_high": "media_frequency_high" in selected_criteria,
            "pop_culture_presence": "pop_culture_presence" in selected_criteria,
            "public_opinion_known": "public_opinion_known" in selected_criteria,
            "national_symbol": "national_symbol" in selected_criteria
        }
        score = sum(criteria_dict.values())
        result = "✅ Это Common Knowledge" if score >= CK_THRESHOLD else "❌ Это не Common Knowledge"
    return render_template_string(HTML_FORM, result=result, fact=fact, score=score)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=10000)
