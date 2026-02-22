---
sidebar_position: 1
title: Module 1 Overview
---

# Module 1: The Robotic Nervous System (ROS 2)

## Introduction

Just as the human nervous system transmits signals between the brain and body, **ROS 2** (Robot Operating System 2) serves as the communication infrastructure for robots. It's the middleware that allows different parts of a robotic system to talk to each other seamlessly.

## What is ROS 2?

ROS 2 is not an operating system in the traditional sense—it's a **middleware framework** that provides:

- 📡 **Communication protocols** for distributed systems
- 🔧 **Tools** for building, debugging, and visualizing robotic applications
- 📦 **Libraries** for common robotic tasks (navigation, manipulation, perception)
- 🌐 **Ecosystem** of packages from the robotics community

### Why ROS 2 (not ROS 1)?

ROS 2 was redesigned from the ground up to address limitations of ROS 1:

| Feature | ROS 1 | ROS 2 |
|---------|-------|-------|
| **Real-time capable** | ❌ No | ✅ Yes |
| **Multi-robot systems** | ⚠️ Difficult | ✅ Native support |
| **Security** | ❌ Minimal | ✅ Built-in (DDS Security) |
| **Cross-platform** | 🐧 Linux only | ✅ Linux, Windows, macOS |
| **Production ready** | ⚠️ Research-focused | ✅ Industrial-grade |
| **Python 3** | ❌ Python 2.7 | ✅ Python 3.6+ |

## Module Learning Objectives

By the end of Module 1, you will:

✅ Understand ROS 2 architecture and core concepts
✅ Build and run ROS 2 nodes in Python
✅ Implement publishers, subscribers, services, and actions
✅ Create robot descriptions using URDF
✅ Develop custom ROS 2 packages
✅ Use launch files for complex system startup
✅ Debug and visualize ROS 2 systems

## Module Structure

### Week 1-2: ROS 2 Fundamentals
- **Chapter 1.1**: Introduction to ROS 2
- **Chapter 1.2**: Nodes, Topics, and Services
- **Chapter 1.3**: Python Integration with rclpy
- **Chapter 1.4**: URDF for Humanoid Robots

### Week 3: Advanced ROS 2
- **Chapter 1.5**: Building ROS 2 Packages
- **Chapter 1.6**: Launch Files & Parameters
- **Chapter 1.7**: Practical Project - Simple Humanoid Controller

## Key Concepts

### Nodes
Independent processes that perform specific computations. Each sensor, actuator, or algorithm typically runs in its own node.

```
Example: camera_node, motor_controller_node, path_planner_node
```

### Topics
Named buses for asynchronous, many-to-many communication using publish/subscribe pattern.

```
Node A (Publisher)  --(topic)--> Node B (Subscriber)
                    --(topic)--> Node C (Subscriber)
```

### Services
Synchronous request/response communication for actions that need acknowledgment.

```
Client Node --[request]--> Server Node
Client Node <--[response]-- Server Node
```

### Actions
For long-running tasks with feedback and ability to cancel.

```
Client --> [Goal] --> Action Server
Client <-- [Feedback] <-- Action Server
Client <-- [Result] <-- Action Server
```

## The ROS 2 Ecosystem

ROS 2 is built on top of **DDS** (Data Distribution Service), an industry-standard protocol for real-time systems. This gives ROS 2:

- 🔒 **Security**: Encryption and authentication
- ⚡ **Performance**: Low latency, high throughput
- 🌐 **Quality of Service (QoS)**: Configure reliability, history, and more
- 🔗 **Interoperability**: Work with non-ROS DDS systems

## Practical Applications

### In Humanoid Robotics
- **Sensor Integration**: IMU, cameras, force sensors all publish to topics
- **Motion Control**: Joint controllers subscribe to command topics
- **Behavior Coordination**: Higher-level planners use services and actions
- **Simulation**: Gazebo communicates via ROS 2 topics

### Real-World Example: Walking Control

```
Vision Node --|IMU Node|-- State Estimator
              |Joint Encoders|
                     |
                     v
              Balance Controller
                     |
                     v
          [Gait Generator Action]
                     |
          +----------+----------+
          |          |          |
      Left Leg   Right Leg   Arms
      Motor Control
```

## Prerequisites for This Module

- **Python**: Basic to intermediate (functions, classes)
- **Linux**: Comfortable with terminal and bash commands
- **C++**: Optional (we'll use Python, but understanding C++ helps)

## Installation Overview

You'll need:
1. **Ubuntu 22.04 LTS** (Jammy Jellyfish)
2. **ROS 2 Humble Hawksbill** (LTS release)
3. **Python 3.10+**
4. **colcon** (ROS 2 build tool)

:::tip Setup Guide
Full installation instructions are in [Appendix B: Software Setup](/docs/appendices/software-setup). We recommend installing ROS 2 Humble as it's the Long Term Support (LTS) version.
:::

## Tools You'll Master

- **ros2**: Command-line interface for ROS 2
- **rviz2**: 3D visualization tool
- **rqt**: Qt-based GUI tools
- **rosbag2**: Recording and playback of topic data
- **colcon**: Build system for ROS 2 packages

## Hands-On Philosophy

This module is **highly practical**. Each concept is followed by:

1. 💻 **Code Example**: Working code you can run
2. 🔬 **Experiment**: Modify the code and observe changes
3. ✍️ **Exercise**: Build something from scratch
4. 🎯 **Quiz**: Test your understanding

## Project Preview: Simple Humanoid Controller

By the end of this module, you'll build a ROS 2 system that:

- Reads IMU sensor data
- Publishes joint angle commands
- Uses a service to change gaits (walk, run, stand)
- Visualizes the robot in RViz2
- Launches everything with a single command

## Common Pitfalls (and How to Avoid Them)

### ❌ Not sourcing the setup file
**Problem**: `ros2: command not found`

**Solution**: Always source ROS 2:
```bash
source /opt/ros/humble/setup.bash
```

Add to `~/.bashrc` for persistence.

### ❌ Mixing ROS 1 and ROS 2 concepts
**Problem**: Trying to use `roscore` (ROS 1) in ROS 2

**Solution**: ROS 2 has no central master. Nodes discover each other automatically via DDS.

### ❌ Not understanding QoS
**Problem**: Publisher and subscriber don't connect

**Solution**: Match QoS settings (reliability, durability, history)

## Resources

- [ROS 2 Official Documentation](https://docs.ros.org/en/humble/)
- [ROS 2 Design Documents](https://design.ros2.org/)
- [DDS Foundation](https://www.dds-foundation.org/)

---

## Ready to Start?

In the next chapter, we'll install ROS 2 and create our first "Hello, Robot!" node.

**Next**: [Chapter 1.1: Introduction to ROS 2](/docs/module-1/week1-2/chapter-1-1) →

:::note Module Duration
Plan for **3 weeks** to complete this module. Each week requires approximately 8-10 hours of study and hands-on practice.
:::
