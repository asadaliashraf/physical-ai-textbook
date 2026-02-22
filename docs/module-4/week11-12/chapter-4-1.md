---
sidebar_position: 1
title: Chapter 4.1 - Voice-to-Action
---

# Chapter 4.1: Voice-to-Action Systems

## OpenAI Whisper for Speech Recognition

```bash
pip install openai-whisper sounddevice scipy
```

## ROS 2 Voice Command Node

```python
#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import whisper
import sounddevice as sd
import numpy as np

class VoiceCommandNode(Node):
    def __init__(self):
        super().__init__("voice_command_node")
        self.pub = self.create_publisher(String, "/voice_commands", 10)
        self.model = whisper.load_model("base")
        self.sample_rate = 16000
        self.get_logger().info("Listening for voice commands...")
        self.create_timer(3.0, self.listen_once)

    def listen_once(self):
        audio = sd.rec(int(3 * self.sample_rate),
                      samplerate=self.sample_rate, channels=1)
        sd.wait()
        result = self.model.transcribe(audio.flatten().astype(np.float32))
        text = result["text"].strip()
        if text:
            msg = String()
            msg.data = text
            self.pub.publish(msg)
            self.get_logger().info(f"Heard: {text}")

def main(args=None):
    rclpy.init(args=args)
    rclpy.spin(VoiceCommandNode())
```

**Next**: [Chapter 4.2: LLM Integration](/docs/module-4/week11-12/chapter-4-2)
