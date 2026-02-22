"""Content personalization based on user background"""
import google.generativeai as genai
from app.config import settings

genai.configure(api_key=settings.GEMINI_API_KEY)

PERSONALIZATION_PROMPTS = {
    "beginner": """You are personalizing robotics content for an ABSOLUTE BEGINNER.
    - Use very simple language and everyday analogies
    - Explain every technical term when first used
    - Add "Think of it like..." examples
    - Encourage the student frequently
    - Add extra context about WHY each concept matters""",

    "intermediate": """You are personalizing robotics content for an INTERMEDIATE learner.
    - Assume basic Python knowledge
    - Focus on practical implementation
    - Include best practices
    - Add performance tips and common pitfalls""",

    "advanced": """You are personalizing robotics content for an ADVANCED student.
    - Use technical terminology freely
    - Include research context and citations
    - Mention edge cases and advanced optimizations
    - Add links to related advanced topics""",
}

HARDWARE_NOTES = {
    "none": "\n\n📝 **Note**: Since you don't have hardware, focus on simulation. All examples work in Gazebo.",
    "basic": "\n\n💻 **Note**: Examples are adapted for Jetson Nano. Watch performance considerations.",
    "jetson": "\n\n🚀 **Note**: You can run these examples on your Jetson Orin! Check GPU acceleration tips.",
    "full_lab": "\n\n🔬 **Lab Note**: You have full hardware access! Try these on your real robot after simulation.",
}

async def personalize_content(
    content: str,
    chapter_id: str,
    user_background: dict
) -> str:
    """Rewrite/enhance content based on user background"""

    exp_level = user_background.get("programming_experience", "beginner")
    robotics_exp = user_background.get("robotics_experience", "none")
    hardware = user_background.get("hardware_access", "none")
    goal = user_background.get("learning_goal", "overview")

    # Determine personalization level
    if exp_level in ["none", "beginner"]:
        personalization_style = "beginner"
    elif exp_level == "advanced":
        personalization_style = "advanced"
    else:
        personalization_style = "intermediate"

    system_prompt = PERSONALIZATION_PROMPTS[personalization_style]

    # Add goal context
    if goal == "project_based":
        system_prompt += "\n- Emphasize HOW TO DO rather than theory"
    elif goal == "deep_dive":
        system_prompt += "\n- Include deeper theoretical context"

    model = genai.GenerativeModel(
        "gemini-1.5-flash",
        generation_config={"temperature": 0.5, "max_output_tokens": 4096}
    )

    prompt = f"""{system_prompt}

The student has:
- Programming experience: {exp_level}
- Robotics experience: {robotics_exp}
- Hardware access: {hardware}
- Learning goal: {goal}

Rewrite/enhance the following chapter content to match this student's level.
Keep ALL code examples. Keep markdown formatting.
Only ADD explanatory text, don't remove technical content.

Chapter content:
{content}

Personalized version:"""

    response = model.generate_content(prompt)
    personalized = response.text

    # Add hardware note
    hw_note = HARDWARE_NOTES.get(hardware, "")
    personalized = hw_note + "\n\n" + personalized if hw_note else personalized

    return personalized

async def get_adaptive_explanation(concept: str, user_background: dict) -> str:
    """Get an explanation of a concept tailored to the user"""
    exp_level = user_background.get("programming_experience", "beginner")

    prompts = {
        "none": f"Explain '{concept}' in simple terms for someone with no technical background. Use everyday analogies.",
        "beginner": f"Explain '{concept}' for a programming beginner. Include a simple Python example.",
        "intermediate": f"Explain '{concept}' for an intermediate Python developer. Include practical examples.",
        "advanced": f"Give a technical explanation of '{concept}' including advanced details and optimizations.",
    }

    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(prompts.get(exp_level, prompts["beginner"]))
    return response.text
