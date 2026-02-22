---
sidebar_position: 2
title: Appendix B - Software Setup
---

# Appendix B: Complete Software Setup Guide

## Ubuntu 22.04

Download: https://ubuntu.com/download/desktop

## ROS 2 Humble

```bash
sudo apt install curl gnupg
sudo curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.key \
    -o /usr/share/keyrings/ros-archive-keyring.gpg

echo "deb [arch=$(dpkg --print-architecture) \
    signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] \
    http://packages.ros.org/ros2/ubuntu jammy main" \
    | sudo tee /etc/apt/sources.list.d/ros2.list > /dev/null

sudo apt update && sudo apt install ros-humble-desktop -y
echo "source /opt/ros/humble/setup.bash" >> ~/.bashrc
```

## Python Dependencies

```bash
pip install google-generativeai openai-whisper ultralytics
pip install torch torchvision fastapi uvicorn qdrant-client asyncpg
```

## Gazebo Harmonic

```bash
sudo apt-get install gz-harmonic
sudo apt install ros-humble-ros-gz -y
```
