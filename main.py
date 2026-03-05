from flask import Flask, request, render_template
from groq import Groq
import os

app = Flask(__name__)

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

@app.route("/", methods=["GET", "POST"])
def index():
    result = ""

    if request.method == "POST":
        topic = request.form.get("topic")

        try:
            completion = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "user", "content": f"Tạo 3 câu hỏi tự luận về {topic}"}
                ]
            )

            result = completion.choices[0].message.content

        except Exception as e:
            result = f"Lỗi API: {e}"

    return render_template("index.html", result=result)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
