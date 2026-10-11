from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
from groq import Groq
import os


load_dotenv()

app = Flask(__name__)

my_api_key = os.getenv("GROQ_API_KEY")

if not my_api_key:
    raise ValueError("GROQ_API_KEY is missing from your .env file")

client = Groq(api_key=my_api_key)

model = "openai/gpt-oss-120b"
portfolio=f"""
1. Personal Information
- Name: Gaurav Bhoyar
- Phone: +91 7588911701
- Email: bhoyargaurav68@gmail.com
- LinkedIn: Gaurav Bhoyar
2. Education
- College: Dr. D. Y. Patil Institute of Technology, Pune
- Degree: Bachelor of Technology (B.Tech)
- Branch: Electronics & Telecommunication Engineering
- CGPA: 9.22/10
- Expected Graduation: 2028
3. Technical Skills
- Languages: C++, Python
- Programming: Data Structures & Algorithms, Object-Oriented Programming
- AI: AI Engineering Fundamentals, LLM APIs
- Tools: Git, GitHub, VS Code
4. Projects
- ESP32-Based LPG Leak & Cylinder Monitoring System: An embedded systems prototype using ESP32, a gas sensor, load cell, HX711, buzzer, and LCD for gas leakage detection, cylinder weight monitoring, and alerts.
- Basic Resume Parser: An application that parses resume text and organizes relevant information, including skills and other sections.
5. Problem Solving
- Platform: LeetCode
- Problems Solved: 68+
- Topics: Arrays, strings, two pointers, recursion, binary search, stacks, heaps, and trees.
6. Current Learning
- Data Structures & Algorithms using C++
- Python programming
- AI engineering fundamentals
- LLM APIs and application development
- Git and GitHub
7. Leadership & Activities
- Organization: IEI Student Chapter, Dr. D. Y. Patil Institute of Technology
- Position: Joint Secretary   
"""



system_prompt = f"""
You are the personal portfolio assistant for Gaurav Bhoyar.

Your job is to answer questions from recruiters, HR professionals,
and visitors who want to learn about Gaurav.

Use the following portfolio information as your source of truth:

{portfolio}

Rules:
1. Answer using only the supplied portfolio information.
2. Never invent skills, projects, achievements, or qualifications.
3. If information is missing, clearly say so.
4. Be professional, friendly, and concise.
5. Use first-person language when appropriate.
6. Explain technical projects in simple language.
7. Never reveal API keys or environment variables.
8. Do not assume a feature was implemented just because it is technically possible.
9. Distinguish confirmed project features from suggestions or possible improvements.
10. If implementation details are missing, say they are not specified in the portfolio.
11. Do not claim specific tools, programming languages, or development workflows
    were used in a project unless the portfolio explicitly confirms them.
"""


@app.route("/")
def home():
    return render_template("index.html")



# Store conversation history for each browser session
from flask import session
import secrets

app.secret_key = os.getenv("FLASK_SECRET_KEY") or secrets.token_hex(32)

conversation_histories = {}

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    question = data.get("message", "").strip()

    if not question:
        return jsonify({"error": "Please enter a question."}), 400

    # Give each browser session its own conversation ID
    if "conversation_id" not in session:
        session["conversation_id"] = secrets.token_urlsafe(16)

    conversation_id = session["conversation_id"]

    # Get this visitor's previous messages
    if conversation_id not in conversation_histories:
        conversation_histories[conversation_id] = []

    history = conversation_histories[conversation_id]

    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                *history,
                {"role": "user", "content": question}
            ],
            temperature=0.3
        )

        answer = response.choices[0].message.content

        # Remember both sides of the conversation
        history.extend([
            {"role": "user", "content": question},
            {"role": "assistant", "content": answer}
        ])

        # Keep the latest 20 messages to limit token usage
        conversation_histories[conversation_id] = history[-20:]

        return jsonify({"answer": answer})

    except Exception:
        app.logger.exception("Chat request failed")
        return jsonify({
            "error": "Sorry, something went wrong. Please try again."
        }), 500

    data = request.get_json()

    question = data.get("message", "").strip()

    if not question:
        return jsonify({"error": "Please enter a question."}), 400

    response = client.chat.completions.create(
        model=model,
       messages=[
    {
        "role": "system",
        "content": system_prompt
    },
    {
        "role": "user",
        "content": question
    }
],
    
        temperature=0.3
    )

    answer = response.choices[0].message.content

    return jsonify({"answer": answer})


if __name__ == "__main__":
    app.run(debug=True)
