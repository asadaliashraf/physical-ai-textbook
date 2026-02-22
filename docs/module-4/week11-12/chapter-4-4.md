---
sidebar_position: 4
title: Chapter 4.4 - Multi-modal Interaction
---

# Chapter 4.4: Multi-modal Interaction

## Vision-Language Understanding with Gemini

```python
import google.generativeai as genai
from PIL import Image
import io

genai.configure(api_key="YOUR_KEY")
model = genai.GenerativeModel("gemini-1.5-flash")

def analyze_scene(image_array, question: str = None) -> str:
    img = Image.fromarray(image_array)
    buf = io.BytesIO()
    img.save(buf, format="JPEG")
    buf.seek(0)
    prompt = question or "List all objects in this scene with their approximate positions."
    response = model.generate_content([prompt, img])
    return response.text
```

## Combined Voice + Vision ROS Node

```python
class MultiModalNode(Node):
    def __init__(self):
        super().__init__("multimodal")
        self.current_image = None
        self.create_subscription(String, "/voice_commands", self.voice_cb, 10)
        self.create_subscription(Image, "/camera/image_raw", self.image_cb, 10)
        self.response_pub = self.create_publisher(String, "/robot_response", 10)

    def image_cb(self, msg):
        bridge = CvBridge()
        self.current_image = bridge.imgmsg_to_cv2(msg, "rgb8")

    def voice_cb(self, msg):
        if self.current_image is not None:
            answer = analyze_scene(self.current_image, msg.data)
            response = String()
            response.data = answer
            self.response_pub.publish(response)
```

**Next**: [Chapter 4.5: Building the Autonomous Humanoid](/docs/module-4/week13/chapter-4-5)
