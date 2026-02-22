---
sidebar_position: 3
title: Chapter 3.7 - Sim-to-Real Transfer
---

# Chapter 3.7: Sim-to-Real Transfer

## Domain Randomization

```python
import random

class RandomizedEnv:
    def reset(self):
        self.set_floor_friction(random.uniform(0.5, 1.5))
        self.set_joint_damping(random.uniform(0.5, 2.0))
        self.set_motor_strength(random.uniform(0.8, 1.2))
        return self.get_obs()
```

## Deploy Policy on Real Robot

```python
import torch, rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState
from std_msgs.msg import Float64MultiArray

class PolicyDeployment(Node):
    def __init__(self, model_path):
        super().__init__("policy_deployment")
        self.policy = torch.jit.load(model_path)
        self.policy.eval()
        self.create_subscription(JointState, "/joint_states", self.cb, 10)
        self.pub = self.create_publisher(Float64MultiArray, "/joint_commands", 10)

    def cb(self, msg):
        obs = torch.tensor(list(msg.position) + list(msg.velocity))
        with torch.no_grad():
            actions = self.policy(obs.unsqueeze(0)).squeeze()
        cmd = Float64MultiArray()
        cmd.data = actions.tolist()
        self.pub.publish(cmd)

def main(args=None):
    rclpy.init(args=args)
    rclpy.spin(PolicyDeployment("walking_policy.pt"))
```

## Module 3 Complete!

**Next Module**: [Module 4: Vision-Language-Action](/docs/module-4/intro)
