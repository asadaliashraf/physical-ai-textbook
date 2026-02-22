---
sidebar_position: 2
title: Chapter 4.6 - System Integration
---

# Chapter 4.6: System Integration

## Full System Launch File

```python
# launch/complete_system.launch.py
from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import ExecuteProcess

def generate_launch_description():
    return LaunchDescription([
        ExecuteProcess(cmd=["gz", "sim", "-r", "humanoid_world.sdf"]),
        Node(package="ros_gz_bridge", executable="parameter_bridge",
             arguments=["/joint_states@sensor_msgs/msg/JointState[gz.msgs.Model"]),
        Node(package="my_humanoid_pkg", executable="voice_command_node"),
        Node(package="my_humanoid_pkg", executable="llm_planner_node",
             parameters=[{"gemini_key": "YOUR_KEY"}]),
        Node(package="my_humanoid_pkg", executable="autonomous_humanoid",
             parameters=[{"gemini_key": "YOUR_KEY"}]),
        Node(package="rviz2", executable="rviz2",
             arguments=["-d", "config/humanoid.rviz"]),
    ])
```

## Running the Full System

```bash
# One command to launch everything
ros2 launch my_humanoid_pkg complete_system.launch.py

# Then speak a command or publish one
ros2 topic pub /voice_commands std_msgs/String "{data: 'walk to the table'}" --once
```

**Next**: [Chapter 4.7: Capstone Project Guide](/docs/module-4/week13/chapter-4-7)
