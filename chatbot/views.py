import json
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import requests

from jobs.models import Job

# ---------------- CHAT UI ---------------- #
def chat_ui(request):
    return render(request, "chatbot/chat_widget.html")

# ---------------- HUGGINGFACE EXTRACTION ---------------- #
def extract_details_with_hf(user_input):
    prompt = f"""
Extract skills and preferred job location from this text.
Return ONLY valid JSON.

Format:
{{"skills":["python"], "location":"chennai"}}

Text:
{user_input}
"""
    try:
        response = requests.post(
            f"https://api-inference.huggingface.co/models/{settings.HF_MODEL}",
            headers={"Authorization": f"Bearer {settings.HF_API_KEY}"},
            json={"inputs": prompt, "parameters": {"max_new_tokens": 100}},
            timeout=30
        )
        result = response.json()
        if isinstance(result, list) and "generated_text" in result[0]:
            output = result[0]["generated_text"]
            start = output.find("{")
            end = output.rfind("}") + 1
            if start != -1 and end != -1:
                return json.loads(output[start:end])
    except Exception as e:
        print("HF ERROR:", e)
    return None

# ---------------- CHAT API ---------------- #
@csrf_exempt
def chat_api(request):
    if request.method != "POST":
        return JsonResponse({"reply": "Invalid request."})

    try:
        data = json.loads(request.body)
        user_input = data.get("message", "").strip().lower()
    except:
        return JsonResponse({"reply": "Invalid JSON input."})

    if not user_input:
        return JsonResponse({"reply": "Please enter something."})

    # 🔹 Handle smart keywords first
    if "salary" in user_input:
        return JsonResponse({
            "reply": "💰 Salary depends on skills & experience. Improve Python, REST API, and Git to get higher packages."
        })

    if "resume" in user_input:
        return JsonResponse({
            "reply": "📝 Keep your resume updated with projects, internships, and technical skills."
        })

    if "interview" in user_input:
        return JsonResponse({
            "reply": "🎯 Practice coding problems and revise core concepts before interviews."
        })

    # 🔹 Normal job search (skill, location)
    parts = user_input.split(",")

    if len(parts) < 2:
        return JsonResponse({
            "reply": "⚠ Please enter like: python, chennai"
        })

    skills = [p.strip() for p in parts[:-1]]
    location = parts[-1].strip()

    matched = []
    for job in Job.objects.all():
        job_location = job.location.lower()
        job_skills = job.skills.lower()

        if location not in job_location:
            continue

        score = sum(1 for skill in skills if skill in job_skills)

        if score > 0:
            matched.append((score, job))

    if not matched:
        return JsonResponse({"reply": "❌ No matching jobs found."})

    matched.sort(key=lambda x: x[0], reverse=True)

    reply = "✅ Recommended Jobs:\n\n"

    for score, job in matched[:3]:
        reply += f"🔹 {job.title} ({job.location})\n"
        reply += f"🏢 Company: {job.company}\n\n"

    reply += "🚀 Tip: Improve REST API & Git skills."

    return JsonResponse({"reply": reply})
