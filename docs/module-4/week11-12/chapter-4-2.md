---
sidebar_position: 2
title: Chapter 4.2 - LLM Integration
---

# Chapter 4.2: LLM Integration for Cognitive Planning

## Gemini-Powered Robot Planner

```python
import google.generativeai as genai
import json

genai.configure(api_key="YOUR_GEMINI_API_KEY")
model = genai.GenerativeModel("gemini-1.5-flash")

SYSTEM_PROMPT = """You are a robot action planner.
Given a natural language command, output a JSON list of actions.
Available actions: navigate_to, pick_up, place_on, wait, speak
Output ONLY valid JSON."""

def plan_actions(command: str) -> list:
    response = model.generate_content(f"{SYSTEM_PROMPT}\n\nCommand: {command}")
    try:
        return json.loads(response.text)
    except:
        return [{"action": "speak", "params": {"text": "Could not understand command"}}]

# Example usage
actions = plan_actions("Pick up the coffee cup and put it on the table")
for action in actions:
    print(f"Execute: {action}")
```

## ROS 2 LLM Planning Node

```python
class LLMPlannerNode(Node):
    def __init__(self):
        super().__init__("llm_planner")
        genai.configure(api_key=self.declare_parameter("gemini_key", "").value)
        self.model = genai.GenerativeModel("gemini-1.5-flash")
        self.create_subscription(String, "/voice_commands", self.command_cb, 10)
        self.action_pub = self.create_publisher(String, "/robot_actions", 10)

    def command_cb(self, msg):
        actions = self.plan(msg.data)
        for action in actions:
            pub_msg = String()
            pub_msg.data = json.dumps(action)
            self.action_pub.publish(pub_msg)

    def plan(self, command):
        prompt = f"Plan robot actions for: {command}. Return JSON list."
        try:
            return json.loads(self.model.generate_content(prompt).text)
        except:
            return [{"action": "stand"}]
```

**Next**: [Chapter 4.3: Natural Language Commands](/docs/module-4/week11-12/chapter-4-3)
