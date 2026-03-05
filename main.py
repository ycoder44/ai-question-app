from flask import Flask, request, render_template_string
import google.generativeai as genai
import os

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

app = Flask(__name__)

def tao_cau_hoi(chu_de):
    try:
        model = genai.GenerativeModel("models/gemini-2.5-flash")

        prompt = f"""
        Viết đầy đủ nội dung theo định dạng sau.

        Câu hỏi:
        (1 câu hỏi tự luận về chủ đề)

        Gợi ý đáp án:
        (gạch đầu dòng rõ ràng)

        Chủ đề: {chu_de}
        """

        response = model.generate_content(
            prompt,
            generation_config={
                "temperature": 0.5,
                "max_output_tokens": 2048
            }
        )

        return response.text

    except Exception as e:
        return f"Lỗi: {str(e)}"

HTML = """
<!DOCTYPE html>
<html>
<head>
<title>AI Tạo Câu Hỏi</title>
</head>
<body>
<h2>Nhập chủ đề</h2>
<form method="post">
<input name="chu_de" required>
<button>Tạo</button>
</form>
{% if ket_qua %}
<h3>Kết quả:</h3>
<textarea rows="20" cols="80">{{ ket_qua }}</textarea>
{% endif %}
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def home():
    ket_qua = None
    if request.method == "POST":
        ket_qua = tao_cau_hoi(request.form["chu_de"])
    return render_template_string(HTML, ket_qua=ket_qua)

# KHÔNG cần app.run() khi deploy