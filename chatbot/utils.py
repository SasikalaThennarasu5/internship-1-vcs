import re
from jobs.models import Job


# Predefined skill keywords
SKILLS = [
    "python", "django", "react", "java",
    "html", "css", "javascript", "sql"
]

# Basic greeting detection
def is_greeting(message):
    greetings = ["hi", "hello", "hey", "good morning", "good evening"]
    return any(word in message.lower() for word in greetings)


# Extract skill from message
def extract_skill(message):
    for skill in SKILLS:
        if skill in message.lower():
            return skill
    return None


# Extract location (basic)
def extract_location(message):
    words = message.lower().split()
    for word in words:
        if word.istitle():
            return word
    return None


# Generate chatbot response
def generate_response(message, user):
    message = message.lower()

    # Greeting
    if is_greeting(message):
        return f"Hello {user.username}! 👋 How can I help you today?"

    # Job search intent
    skill = extract_skill(message)

    if skill:
        jobs = Job.objects.filter(title__icontains=skill)[:5]

        if jobs.exists():
            response = f"I found {jobs.count()} {skill.title()} jobs 👇\n\n"
            for job in jobs:
                response += f"• {job.title} - {job.company_name}\n"
            return response
        else:
            return f"Sorry 😔 I couldn't find {skill.title()} jobs right now."

    return "I can help you find jobs. Try saying: 'Python jobs' or 'Django developer'."
