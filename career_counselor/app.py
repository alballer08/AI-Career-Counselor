from flask import Flask, render_template, request
import google.generativeai as genai
import os

app = Flask(__name__)

# Load API key from environment variable
API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    raise ValueError("Please set the GEMINI_API_KEY environment variable")

genai.configure(api_key=API_KEY)

# Use Gemini 2.5 Flash (fast, good for real-time apps)
model = genai.GenerativeModel("models/gemini-2.5-flash-preview-05-20")

@app.route('/', methods=['GET', 'POST'])
def index():
    suggestions = None
    if request.method == 'POST':
        name = request.form.get('name', '')
        interests = request.form.get('interests', '')
        skills = request.form.get('skills', '')
        education = request.form.get('education', '')

        prompt = f"""
You are a career counselor AI. A user has provided the following background:

Name: {name}
Interests: {interests}
Skills: {skills}
Education: {education}

Based on this information, suggest 3–5 potential career paths. For each, include:
- Job title
- Why it's a good fit
- Suggested next steps to pursue that career
"""

        try:
            response = model.generate_content(prompt)
            suggestions = response.text
        except Exception as e:
            suggestions = f"Error generating suggestions: {e}"

    return render_template('index.html', suggestions=suggestions)

if __name__ == '__main__':
    app.run(debug=True)
