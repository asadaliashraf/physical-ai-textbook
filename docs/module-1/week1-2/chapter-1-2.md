---
sidebar_position: 2
title: Chapter 1.2 - Nodes, Topics & Services
---

# Chapter 1.2: Nodes, Topics, and Services

**Learning Objectives:** Understand ROS 2 communication patterns for humanoid robots.

## 1. Topics for Humanoid Robots

Common robot topics:
- `/joint_states` → Current joint positions
- `/cmd_vel` → Velocity commands
- `/imu/data` → IMU sensor data
- `/camera/image_raw` → Camera images

### Joint State Publisher

```python
#!/usr/bin/env python3
import rclpy, math
from rclpy.node import Node
from sensor_msgs.msg import JointState

class JointStatePublisher(Node):
    def __init__(self):
        super().__init__('joint_state_publisher')
        self.pub = self.create_publisher(JointState, '/joint_states', 10)
        self.timer = self.create_timer(0.01, self.publish_state)
        self.t = 0.0
        self.joints = ['left_knee', 'right_knee', 'left_hip', 'right_hip']

    def publish_state(self):
        msg = JointState()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.name = self.joints
        msg.position = [0.3 * math.sin(2 * self.t + i * 0.5) for i in range(4)]
        self.pub.publish(msg)
        self.t += 0.01

def main(args=None):
    rclpy.init(args=args)
    rclpy.spin(JointStatePublisher())

if __name__ == '__main__':
    main()
```

## 2. Services for Robot Commands

```python
#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from example_interfaces.srv import SetBool

class GaitController(Node):
    def __init__(self):
        super().__init__('gait_controller')
        self.srv = self.create_service(SetBool, 'set_walking', self.gait_callback)
        self.is_walking = False

    def gait_callback(self, request, response):
        self.is_walking = request.data
        response.success = True
        response.message = 'Walking' if self.is_walking else 'Stopped'
        return response

def main(args=None):
    rclpy.init(args=args)
    rclpy.spin(GaitController())
```

## 3. QoS Settings

```python
from rclpy.qos import QoSProfile, QoSReliabilityPolicy

sensor_qos = QoSProfile(
    reliability=QoSReliabilityPolicy.BEST_EFFORT,
    depth=1
)
```

**Next**: [Chapter 1.3: Python Integration with rclpy](/docs/module-1/week1-2/chapter-1-3)
