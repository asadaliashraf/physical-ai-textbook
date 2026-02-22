---
sidebar_position: 3
title: Chapter 1.7 - Practical Project
---

# Chapter 1.7: Practical Project - Simple Humanoid Controller

## Project Overview

Build a complete ROS 2 system that simulates a simple humanoid robot with:
- Joint state publishing (simulated walking)
- IMU data simulation
- Balance estimation
- A gait control service
- Full visualization in RViz2

## Project Architecture

```
[imu_simulator] ──/imu/data──▶ [balance_estimator] ──/balance_state──▶
[joint_sim] ─────/joint_states──▶ [gait_controller]
                                          │
                                    /set_gait (service)
```

## Complete Implementation

```python
# gait_controller.py
#!/usr/bin/env python3
import rclpy, math
from rclpy.node import Node
from sensor_msgs.msg import JointState, Imu
from std_msgs.msg import String
from example_interfaces.srv import SetBool

class HumanoidGaitController(Node):
    def __init__(self):
        super().__init__('humanoid_gait_controller')

        # State
        self.gait = 'stand'
        self.t = 0.0
        self.joints = [
            'left_hip_pitch', 'left_knee', 'left_ankle_pitch',
            'right_hip_pitch', 'right_knee', 'right_ankle_pitch',
        ]

        # Publishers
        self.joint_pub = self.create_publisher(JointState, '/joint_states', 10)
        self.status_pub = self.create_publisher(String, '/gait_status', 10)

        # Services
        self.create_service(SetBool, '/start_walking', self.walk_service_cb)

        # Timer - 100 Hz control loop
        self.create_timer(0.01, self.control_loop)
        self.get_logger().info('Humanoid Gait Controller Ready!')

    def walk_service_cb(self, request, response):
        self.gait = 'walk' if request.data else 'stand'
        response.success = True
        response.message = f'Gait set to: {self.gait}'
        self.get_logger().info(f'Gait changed to: {self.gait}')
        return response

    def control_loop(self):
        msg = JointState()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.name = self.joints

        if self.gait == 'walk':
            # Sinusoidal walking pattern
            phase = 2 * math.pi * self.t
            msg.position = [
                0.3 * math.sin(phase),           # left_hip_pitch
                max(0, 0.4 * math.sin(phase)),    # left_knee
                -0.2 * math.sin(phase),           # left_ankle
                0.3 * math.sin(phase + math.pi),  # right_hip_pitch
                max(0, 0.4 * math.sin(phase + math.pi)),  # right_knee
                -0.2 * math.sin(phase + math.pi), # right_ankle
            ]
            self.t += 0.01
        else:
            msg.position = [0.0] * 6  # Stand still

        msg.velocity = [0.0] * 6
        msg.effort = [0.0] * 6
        self.joint_pub.publish(msg)

        # Status
        status = String()
        status.data = f'Gait: {self.gait} | t={self.t:.2f}s'
        self.status_pub.publish(status)

def main(args=None):
    rclpy.init(args=args)
    rclpy.spin(HumanoidGaitController())

if __name__ == '__main__':
    main()
```

## Running the Project

```bash
# Terminal 1: Start controller
ros2 run my_humanoid_pkg gait_controller

# Terminal 2: Start walking
ros2 service call /start_walking example_interfaces/srv/SetBool "{data: true}"

# Terminal 3: Watch joint states
ros2 topic echo /joint_states

# Terminal 4: Open RViz2
ros2 run rviz2 rviz2
```

## Congratulations!

You've completed **Module 1: The Robotic Nervous System**. You now know how to:
- Create ROS 2 nodes, publishers, subscribers, services
- Describe robots with URDF
- Build and launch ROS 2 packages
- Build a basic humanoid controller

**Next Module**: [Module 2: The Digital Twin (Gazebo & Unity)](/docs/module-2/intro)
