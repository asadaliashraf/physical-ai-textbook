---
sidebar_position: 3
title: Chapter 4.3 - Natural Language Commands
---

# Chapter 4.3: Natural Language Command Processing

## Command Parser

```python
class CommandParser:
    ACTION_MAP = {
        "walk": "start_walking",
        "go": "navigate_to",
        "pick up": "pick_object",
        "grab": "pick_object",
        "place": "place_object",
        "put": "place_object",
        "stop": "stop_all",
        "sit": "sit_down",
        "stand": "stand_up",
    }

    def parse(self, command: str) -> dict:
        for keyword, action in self.ACTION_MAP.items():
            if keyword in command.lower():
                return {"action": action, "raw": command, "confidence": 0.9}
        return {"action": "unknown", "raw": command, "confidence": 0.0}
```

## Multi-turn Conversation

```python
class ConversationalRobot:
    def __init__(self, api_key: str):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel("gemini-1.5-flash")
        self.chat = self.model.start_chat(history=[])

    def talk(self, user_msg: str) -> str:
        prompt = f"You control a humanoid robot. User says: {user_msg}"
        return self.chat.send_message(prompt).text

    def run(self):
        print("Robot ready! Give commands:")
        while True:
            user = input("You: ").strip()
            if user.lower() in ["quit", "exit"]:
                break
            print(f"Robot: {self.talk(user)}")
```

**Next**: [Chapter 4.4: Multi-modal Interaction](/docs/module-4/week11-12/chapter-4-4)
