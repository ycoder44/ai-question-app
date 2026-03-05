from flask import Flask, request, render_template_string
from groq import Groq
import os

app = Flask(__name__)

client = Groq(
    api_key=os.environ.get("GROQ_API_KEY")
)

HTML = """
<h2>AI tạo câu hỏi</h2>

<form method="post">
<input name="topic">
<button type="submit">Tạo</button>
</form>

<pre>{{result}}</pre>
"""

@app.route("/", methods=["GET","POST"])
def index():

    result=""

    if request.method=="POST":

        topic=request.form.get("topic")

        try:

            chat = client.chat.completions.create(
                messages=[{
                    "role":"user",
                    "content":f"Tạo 3 câu hỏi tự luận về {topic}"
                }],
                model="llama3-8b-8192"
            )

            result = chat.choices[0].message.content

        except Exception as e:
            result = str(e)

    return render_template_string(HTML,result=result)

if __name__=="__main__":
    app.run(host="0.0.0.0",port=10000)
