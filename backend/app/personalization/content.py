"""Content personalization using Gemini REST API"""
import httpx
from app.config import settings

GEMINI_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"

PERSONALIZATION_PROMPTS = {
    "beginner": "You are personalizing robotics content for a BEGINNER. Use simple language and everyday analogies. Explain every technical term. Add 'Think of it like...' examples.",
    "intermediate": "You are personalizing robotics content for an INTERMEDIATE learner. Assume basic Python knowledge. Focus on practical implementation and best practices.",
    "advanced": "You are personalizing robotics content for an ADVANCED student. Use technical terminology freely. Include edge cases and advanced optimizations.",
}

HARDWARE_NOTES = {
    "none": "\n\n**Note**: Since you don't have hardware, focus on simulation. All examples work in Gazebo.",
    "basic": "\n\n**Note**: Examples are adapted for basic hardware. Watch performance considerations.",
    "jetson": "\n\n**Note**: You can run these examples on your Jetson! Check GPU acceleration tips.",
    "full_lab": "\n\n**Lab Note**: You have full hardware access! Try these on your real robot after simulation.",
}

async def _call_gemini(prompt: str) -> str:
    async with httpx.AsyncClient(timeout=60) as client:
        resp = await client.post(
            f"{GEMINI_URL}?key={settings.GEMINI_API_KEY}",
            json={"contents": [{"parts": [{"text": prompt}]}],
                  "generationConfig": {"temperature": 0.5, "maxOutputTokens": 4096}}
        )
        resp.raise_for_status()
        return resp.json()["candidates"][0]["content"]["parts"][0]["text"]

async def personalize_content(content: str, chapter_id: str, user_background: dict) -> str:
    exp_level = user_background.get("programming_experience", "beginner")
    robotics_exp = user_background.get("robotics_experience", "none")
    hardware = user_background.get("hardware_access", "none")
    goal = user_background.get("learning_goal", "overview")

    style = "advanced" if exp_level == "advanced" else ("beginner" if exp_level in ("none", "beginner") else "intermediate")
    system_prompt = PERSONALIZATION_PROMPTS[style]

    if goal == "project_based":
        system_prompt += " Emphasize HOW TO DO rather than theory."
    elif goal == "deep_dive":
        system_prompt += " Include deeper theoretical context."

    prompt = f"""{system_prompt}

The student has: Programming experience: {exp_level}, Robotics experience: {robotics_exp}, Hardware: {hardware}, Goal: {goal}

Rewrite/enhance the following chapter content to match this student's level.
Keep ALL code examples. Keep markdown formatting. Only ADD explanatory text.

Chapter content:
{content}

Personalized version:"""

    personalized = await _call_gemini(prompt)
    hw_note = HARDWARE_NOTES.get(hardware, "")
    return (hw_note + "\n\n" + personalized) if hw_note else personalized

async def get_adaptive_explanation(concept: str, user_background: dict) -> str:
    exp_level = user_background.get("programming_experience", "beginner")
    prompts = {
        "none": f"Explain '{concept}' in simple terms with everyday analogies.",
        "beginner": f"Explain '{concept}' for a programming beginner with a simple Python example.",
        "intermediate": f"Explain '{concept}' for an intermediate developer with practical examples.",
        "advanced": f"Give a technical explanation of '{concept}' with advanced details.",
    }
    return await _call_gemini(prompts.get(exp_level, prompts["beginner"]))
