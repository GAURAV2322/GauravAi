import os
from pathlib import Path
from time import sleep
from dotenv import load_dotenv
from groq import Groq

load_dotenv()
my_api_key=os.getenv("GROQ_API_KEY")

if not my_api_key:
    raise ValueError("API key kaha hai beeee")
client=Groq(api_key=my_api_key)
model="openai/gpt-oss-120b"

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


def ask_ai(question):
    messages = [
        {"role": "system", "content": system_prompt}
    ]

    messages.extend(conversation_history)

    messages.append({
        "role": "user",
        "content": question
    })

    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0.3
    )

    answer = response.choices[0].message.content

    conversation_history.append({
        "role": "user",
        "content": question
    })

    conversation_history.append({
        "role": "assistant",
        "content": answer
    })

    return answer



conversation_history = []    
while True:
 
    question = input("You: ").strip()

    if question.lower() == "exit":
        print("Assistant: Thank you for visiting!")
        break

    if not question:
        continue

    answer = ask_ai(question)
    print(f"\nAssistant: {answer}\n")