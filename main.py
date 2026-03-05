from flask import Flask, request, render_template_string
from groq import Groq
import os

app = Flask(__name__)

# API KEY (Render sẽ đọc từ Environment Variable)
client = Groq(
    api_key=os.environ.get("GROQ_API_KEY")
)

# HTML giao diện
HTML = """
<!DOCTYPE html>
<html>
<head>
<title>AI Tạo Câu Hỏi</title>
<style>
body{
    font-family: Arial;
    margin:40px;
}
input{
    padding:10px;
    width:300px;
}
button{
    padding:10px;
}
.result{
    margin-top:20px;
    white-space: pre-wrap;
}
</style>
</head>

<body>

<h2>AI tạo câu hỏi tự luận</h2>

<form method="post">
<input name="topic" placeholder="Nhập chủ đề">
<button type="submit">Tạo câu hỏi</button>
</form>

<div class="result">
{{result}}
</div>

</body>
</html>
"""


@app.route("/", methods=["GET","POST"])
def index():

    result = ""

    if request.method == "POST":

        topic = request.form.get("topic")

        prompt = f"""
Tạo 3 câu hỏi tự luận về chủ đề: {topic}

Sau đó đưa ra gợi ý đáp án ngắn.
"""

        chat = client.chat.completions.create(
            messages=[
                {"role": "user", "content": prompt}
            ],
            model="llama3-8b-8192",
            max_tokens=800
        )

        result = chat.choices[0].message.content

    return render_template_string(HTML, result=result)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
