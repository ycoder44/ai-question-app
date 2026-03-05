from flask import Flask, request, render_template_string
from groq import Groq
import os

app = Flask(__name__)

client = Groq(
    api_key=os.environ.get("GROQ_API_KEY")
)

HTML = """
<!DOCTYPE html>
<html>
<head>
<title>AI Essay Question Generator</title>
</head>
<body>

<h2>AI tạo câu hỏi tự luận</h2>

<form method="post">
<input name="topic" placeholder="Nhập chủ đề..." required>
<button type="submit">Tạo câu hỏi</button>
</form>

{% if result %}
<h3>Kết quả:</h3>
<pre>{{ result }}</pre>
{% endif %}

</body>
</html>
"""

@app.route("/", methods=["GET","POST"])
def home():
    result = ""

    if request.method == "POST":
        topic = request.form["topic"]

        prompt = f"""
Tạo 3 câu hỏi tự luận về chủ đề: {topic}

Sau mỗi câu hỏi hãy viết:
- Gợi ý đáp án
"""

        completion = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        result = completion.choices[0].message.content

    return render_template_string(HTML, result=result)

if __name__ == "__main__":
    app.run()
