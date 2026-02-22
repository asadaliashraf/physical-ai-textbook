---
sidebar_position: 3
title: Chapter 1.3 - Python with rclpy
---

# Chapter 1.3: Python Integration with rclpy

## rclpy Fundamentals

`rclpy` is the Python client library for ROS 2. It provides all the tools needed to create nodes, publish messages, and interact with the ROS 2 ecosystem.

## Node Communication Patterns

### Asynchronous Service Calls

```python
#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from rclpy.callback_groups import ReentrantCallbackGroup
from example_interfaces.srv import AddTwoInts

class AsyncServiceClient(Node):
    def __init__(self):
        super().__init__('async_client')
        self.cb_group = ReentrantCallbackGroup()
        self.client = self.create_client(
            AddTwoInts, 'add_two_ints',
            callback_group=self.cb_group
        )

    async def send_request(self, a, b):
        request = AddTwoInts.Request()
        request.a = a
        request.b = b
        response = await self.client.call_async(request)
        return response.sum
```

## Parameters in ROS 2

```python
class ConfigurableNode(Node):
    def __init__(self):
        super().__init__('configurable_node')
        self.declare_parameter('walk_speed', 0.5)
        self.declare_parameter('step_height', 0.1)
        self.declare_parameter('robot_name', 'humanoid_01')

        speed = self.get_parameter('walk_speed').value
        self.get_logger().info(f'Walk speed: {speed}')
```

## Timers and Callbacks

```python
class MultiTimerNode(Node):
    def __init__(self):
        super().__init__('multi_timer')
        # 100 Hz control loop
        self.create_timer(0.01, self.control_callback)
        # 1 Hz status update
        self.create_timer(1.0, self.status_callback)

    def control_callback(self):
        pass  # High-frequency control

    def status_callback(self):
        self.get_logger().info('System OK')
```

## Logging System

```python
self.get_logger().debug('Debug message')
self.get_logger().info('Information')
self.get_logger().warn('Warning!')
self.get_logger().error('Error occurred!')
self.get_logger().fatal('Fatal error!')
```

## Exercise: Build a Robot Monitor

Create a node that:
1. Subscribes to `/joint_states` and `/imu/data`
2. Checks if joint velocities are within safe limits
3. Publishes a safety status to `/robot_safety`
4. Logs warnings when limits are exceeded

**Next**: [Chapter 1.4: URDF for Humanoid Robots](/docs/module-1/week1-2/chapter-1-4)
