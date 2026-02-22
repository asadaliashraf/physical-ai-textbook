---
sidebar_position: 1
title: Chapter 1.1 - Introduction to ROS 2
---

# Chapter 1.1: Introduction to ROS 2

## Overview

Welcome to your first hands-on chapter with ROS 2! In this chapter, you'll install ROS 2, understand its architecture, and create your first robotic node.

**Learning Objectives:**
- Install ROS 2 Humble on Ubuntu 22.04
- Understand the ROS 2 architectural patterns
- Create and run your first ROS 2 node
- Explore the ros2 command-line interface

**Estimated Time:** 2-3 hours

---

## 1. Installing ROS 2 Humble

### System Requirements

- **OS**: Ubuntu 22.04 (Jammy Jellyfish)
- **Architecture**: x86_64 (AMD64)
- **Disk Space**: At least 5 GB free
- **Internet**: Required for package downloads

### Step 1: Set Locale

```bash
locale  # Check current locale
sudo apt update && sudo apt install locales
sudo locale-gen en_US en_US.UTF-8
sudo update-locale LC_ALL=en_US.UTF-8 LANG=en_US.UTF-8
export LANG=en_US.UTF-8
```

### Step 2: Setup Sources

```bash
# Ensure Ubuntu Universe repository is enabled
sudo apt install software-properties-common
sudo add-apt-repository universe

# Add ROS 2 GPG key
sudo apt update && sudo apt install curl -y
sudo curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.key -o /usr/share/keyrings/ros-archive-keyring.gpg

# Add repository to sources list
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] http://packages.ros.org/ros2/ubuntu $(. /etc/os-release && echo $UBUNTU_CODENAME) main" | sudo tee /etc/apt/sources.list.d/ros2.list > /dev/null
```

### Step 3: Install ROS 2 Packages

```bash
# Update package index
sudo apt update

# Install ROS 2 Humble Desktop (recommended)
sudo apt install ros-humble-desktop -y

# Or install ROS 2 Humble Base (minimal)
# sudo apt install ros-humble-ros-base -y
```

This will take 10-15 minutes depending on your internet speed.

### Step 4: Environment Setup

```bash
# Source ROS 2 environment
source /opt/ros/humble/setup.bash

# Add to .bashrc for automatic sourcing
echo "source /opt/ros/humble/setup.bash" >> ~/.bashrc
```

### Step 5: Install Development Tools

```bash
# Install colcon (build tool)
sudo apt install python3-colcon-common-extensions -y

# Install rosdep (dependency management)
sudo apt install python3-rosdep2 -y

# Initialize rosdep
sudo rosdep init
rosdep update
```

### Verify Installation

```bash
# Check ROS 2 version
ros2 --version

# Expected output:
# ros2 cli version: X.X.X
```

✅ **Checkpoint**: If you see the version number, ROS 2 is successfully installed!

---

## 2. Understanding ROS 2 Architecture

### The Core Components

ROS 2 architecture is based on a **graph** of processes (nodes) communicating over named channels (topics).

```
┌─────────────────────────────────────────┐
│         ROS 2 Computational Graph       │
├─────────────────────────────────────────┤
│                                         │
│  ┌──────┐    topic    ┌──────┐         │
│  │Node A├────────────>│Node B│         │
│  └──────┘             └──────┘         │
│                                         │
│  ┌──────┐   service   ┌──────┐         │
│  │Node C├─────────────│Node D│         │
│  └──────┘             └──────┘         │
│                                         │
│  ┌──────┐   action    ┌──────┐         │
│  │Node E├─────────────│Node F│         │
│  └──────┘             └──────┘         │
│                                         │
└─────────────────────────────────────────┘
            ↓
        Built on DDS
(Data Distribution Service)
```

### Key Architectural Patterns

#### 1. **No Master Node** (Unlike ROS 1)
In ROS 2, there is no central `roscore`. Nodes discover each other automatically using DDS discovery protocol.

**Advantages:**
- More robust (no single point of failure)
- Better for distributed systems
- Easier multi-robot coordination

#### 2. **Quality of Service (QoS)**
Fine-grained control over communication reliability, latency, and resource usage.

**QoS Policies:**
- **Reliability**: Best effort vs. reliable
- **Durability**: Volatile vs. transient local
- **History**: Keep last N messages vs. keep all
- **Deadline**: Maximum time between messages

#### 3. **Security by Default**
ROS 2 supports DDS-Security for authentication, encryption, and access control.

---

## 3. Your First ROS 2 Node

### Hello, Robot! (Publisher Example)

Let's create a simple node that publishes "Hello, Robot!" messages.

#### Step 1: Create a Python File

```bash
mkdir -p ~/ros2_ws/src
cd ~/ros2_ws/src
mkdir hello_robot
cd hello_robot
```

Create `hello_publisher.py`:

```python
#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class HelloPublisher(Node):
    def __init__(self):
        super().__init__('hello_publisher')
        self.publisher_ = self.create_publisher(String, 'robot_message', 10)
        self.timer = self.create_timer(1.0, self.timer_callback)
        self.counter = 0
        self.get_logger().info('Hello Publisher has started!')

    def timer_callback(self):
        msg = String()
        msg.data = f'Hello, Robot! Count: {self.counter}'
        self.publisher_.publish(msg)
        self.get_logger().info(f'Publishing: "{msg.data}"')
        self.counter += 1


def main(args=None):
    rclpy.init(args=args)
    node = HelloPublisher()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
```

#### Step 2: Make it Executable

```bash
chmod +x hello_publisher.py
```

#### Step 3: Run the Node

```bash
# Source ROS 2
source /opt/ros/humble/setup.bash

# Run the node
python3 hello_publisher.py
```

**Expected Output:**
```
[INFO] [hello_publisher]: Hello Publisher has started!
[INFO] [hello_publisher]: Publishing: "Hello, Robot! Count: 0"
[INFO] [hello_publisher]: Publishing: "Hello, Robot! Count: 1"
[INFO] [hello_publisher]: Publishing: "Hello, Robot! Count: 2"
...
```

🎉 **Congratulations!** You've created your first ROS 2 node!

---

## 4. Understanding the Code

Let's break down what's happening:

### Importing Libraries

```python
import rclpy  # ROS 2 Python client library
from rclpy.node import Node  # Base class for ROS 2 nodes
from std_msgs.msg import String  # Standard message type
```

### Creating a Node Class

```python
class HelloPublisher(Node):
    def __init__(self):
        super().__init__('hello_publisher')  # Node name
```

Every ROS 2 node inherits from the `Node` class and must have a unique name.

### Creating a Publisher

```python
self.publisher_ = self.create_publisher(
    String,           # Message type
    'robot_message',  # Topic name
    10                # Queue size (QoS depth)
)
```

### Creating a Timer

```python
self.timer = self.create_timer(
    1.0,                 # Period in seconds
    self.timer_callback  # Callback function
)
```

This timer calls `timer_callback()` every 1 second.

### Publishing Messages

```python
def timer_callback(self):
    msg = String()
    msg.data = f'Hello, Robot! Count: {self.counter}'
    self.publisher_.publish(msg)
```

### Spinning the Node

```python
rclpy.spin(node)
```

This keeps the node running and processing callbacks.

---

## 5. Creating a Subscriber

Now let's create a node that listens to our messages!

Create `hello_subscriber.py`:

```python
#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class HelloSubscriber(Node):
    def __init__(self):
        super().__init__('hello_subscriber')
        self.subscription = self.create_subscription(
            String,
            'robot_message',
            self.listener_callback,
            10
        )
        self.get_logger().info('Hello Subscriber has started!')

    def listener_callback(self, msg):
        self.get_logger().info(f'Received: "{msg.data}"')


def main(args=None):
    rclpy.init(args=args)
    node = HelloSubscriber()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
```

### Run Both Nodes

**Terminal 1:**
```bash
python3 hello_publisher.py
```

**Terminal 2:**
```bash
python3 hello_subscriber.py
```

You should see:
- **Terminal 1**: Publishing messages
- **Terminal 2**: Receiving and logging the same messages

---

## 6. Exploring with ros2 CLI

The `ros2` command-line tool is essential for debugging and exploring ROS 2 systems.

### List All Running Nodes

```bash
ros2 node list
```

**Output:**
```
/hello_publisher
/hello_subscriber
```

### Get Node Information

```bash
ros2 node info /hello_publisher
```

**Output shows:**
- Subscribers
- Publishers (robot_message)
- Services
- Actions

### List All Topics

```bash
ros2 topic list
```

**Output:**
```
/robot_message
/rosout
/parameter_events
```

### Echo a Topic

```bash
ros2 topic echo /robot_message
```

This displays all messages published to the topic in real-time.

### Topic Information

```bash
ros2 topic info /robot_message
```

**Output shows:**
- Message type: std_msgs/msg/String
- Publisher count: 1
- Subscription count: 1

### Topic Bandwidth

```bash
ros2 topic bw /robot_message
```

Shows messages/second and bytes/second.

### Topic Frequency

```bash
ros2 topic hz /robot_message
```

Shows publish frequency (should be ~1 Hz in our example).

---

## 7. Visualizing with rqt_graph

`rqt_graph` provides a visual representation of your ROS 2 system.

### Install rqt_graph

```bash
sudo apt install ros-humble-rqt-graph -y
```

### Run rqt_graph

```bash
ros2 run rqt_graph rqt_graph
```

You'll see a graphical representation:
- Nodes as ovals
- Topics as arrows connecting nodes

---

## 8. Hands-On Exercises

### Exercise 1: Modify the Message

Change the publisher to send "Greetings from ROS 2!" instead of "Hello, Robot!".

<details>
<summary>Solution</summary>

```python
msg.data = f'Greetings from ROS 2! Count: {self.counter}'
```
</details>

### Exercise 2: Change the Publishing Rate

Modify the publisher to send messages every 0.5 seconds.

<details>
<summary>Solution</summary>

```python
self.timer = self.create_timer(0.5, self.timer_callback)
```
</details>

### Exercise 3: Create a New Topic

Create a second publisher in the same node that publishes to a topic called `/robot_status` with the message "System OK".

<details>
<summary>Hint</summary>

Create another publisher with `create_publisher()` and publish to it in the same timer callback.
</details>

---

## 9. Key Takeaways

✅ ROS 2 uses a distributed architecture with no master node
✅ Nodes communicate via topics, services, and actions
✅ `rclpy` is the Python client library for ROS 2
✅ Publishers and subscribers use a pub/sub pattern
✅ The `ros2` CLI is essential for debugging
✅ `rqt_graph` provides visual insights into your system

---

## 10. Common Issues and Solutions

### Issue: "ros2: command not found"

**Solution:**
```bash
source /opt/ros/humble/setup.bash
```

### Issue: Publisher and Subscriber don't connect

**Solution:**
- Check both nodes are running
- Verify topic names match exactly
- Check QoS compatibility with `ros2 topic info`

### Issue: Permission denied when running Python script

**Solution:**
```bash
chmod +x your_script.py
```

---

## 11. Additional Resources

- [ROS 2 Humble Documentation](https://docs.ros.org/en/humble/)
- [rclpy API Reference](https://docs.ros2.org/latest/api/rclpy/)
- [ROS 2 Tutorials](https://docs.ros.org/en/humble/Tutorials.html)
- [ROS 2 Design Docs](https://design.ros2.org/)

---

## Quiz

Test your understanding:

1. What is the main advantage of ROS 2 over ROS 1?
2. What does DDS stand for and what is its role?
3. What are the three main communication patterns in ROS 2?
4. How often does our publisher send messages? (Answer: Every 1 second)
5. What command shows all running nodes?

<details>
<summary>Answers</summary>

1. No master node, better real-time support, built-in security, cross-platform
2. Data Distribution Service - it's the middleware ROS 2 is built on
3. Topics (pub/sub), Services (request/response), Actions (long-running tasks)
4. 1 Hz (once per second)
5. `ros2 node list`
</details>

---

## Next Steps

In the next chapter, we'll dive deeper into **Topics, Services, and the message system**.

**Next**: [Chapter 1.2: Nodes, Topics, and Services](/docs/module-1/week1-2/chapter-1-2) →

:::tip Practice Makes Perfect
Before moving on, try modifying the code examples. Change message types, add multiple publishers, experiment with different timer rates. The best way to learn ROS 2 is by doing!
:::
