---
sidebar_position: 1
title: Chapter 4.5 - Autonomous Humanoid
---

# Chapter 4.5: Building the Autonomous Humanoid

## Complete System Architecture

```
Voice Input → [Whisper ASR] → Text
Camera → [YOLOv8] → Detections
LIDAR → [Obstacle Detector] → Safe zones

Text + Detections → [Gemini LLM Planner] → Action Plan
Action Plan → [ROS 2 Action Executor] → Robot Movement
```

## Complete Implementation

```python
#!/usr/bin/env python3
import rclpy, json, threading
from rclpy.node import Node
from std_msgs.msg import String
from sensor_msgs.msg import LaserScan
import google.generativeai as genai

class AutonomousHumanoid(Node):
    def __init__(self):
        super().__init__("autonomous_humanoid")
        genai.configure(api_key=self.declare_parameter("gemini_key", "").value)
        self.llm = genai.GenerativeModel("gemini-1.5-flash")
        self.obstacle_detected = False
        self.task_queue = []

        self.create_subscription(String, "/voice_commands", self.voice_cb, 10)
        self.create_subscription(LaserScan, "/lidar", self.lidar_cb, 10)
        self.action_pub = self.create_publisher(String, "/robot_actions", 10)
        self.status_pub = self.create_publisher(String, "/robot_status", 10)
        self.get_logger().info("Autonomous Humanoid Online!")

    def voice_cb(self, msg):
        self.get_logger().info(f"Command: {msg.data}")
        actions = self.plan(msg.data)
        self.task_queue.extend(actions)
        threading.Thread(target=self.execute, daemon=True).start()

    def plan(self, command: str) -> list:
        prompt = f"Plan actions for: '{command}'. Return JSON list with action and params."
        try:
            return json.loads(self.llm.generate_content(prompt).text)
        except:
            return [{"action": "speak", "params": {"text": "Command unclear"}}]

    def lidar_cb(self, msg):
        valid = [r for r in msg.ranges if 0.1 < r < 10.0]
        self.obstacle_detected = bool(valid and min(valid) < 0.5)

    def execute(self):
        for task in self.task_queue:
            while self.obstacle_detected:
                self.get_logger().warn("Waiting for obstacle to clear...")
                import time
                time.sleep(0.5)
            action_msg = String()
            action_msg.data = json.dumps(task)
            self.action_pub.publish(action_msg)
        self.task_queue.clear()
        done = String()
        done.data = "Task complete!"
        self.status_pub.publish(done)

def main(args=None):
    rclpy.init(args=args)
    rclpy.spin(AutonomousHumanoid())
```

**Next**: [Chapter 4.6: System Integration](/docs/module-4/week13/chapter-4-6)
