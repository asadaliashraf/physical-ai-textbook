---
sidebar_position: 3
title: Appendix C - Troubleshooting
---

# Appendix C: Troubleshooting Guide

## ROS 2 Issues

**ros2: command not found**
```bash
source /opt/ros/humble/setup.bash
```

**Nodes not connecting**
```bash
export ROS_DOMAIN_ID=0
ros2 daemon stop && ros2 daemon start
```

**Build errors**
```bash
cd ~/ros2_ws && colcon build --cmake-clean-cache
```

## Gazebo Issues

**Slow performance**
- Reduce physics rate: `<real_time_update_rate>500</real_time_update_rate>`
- Use headless: `gz sim -r world.sdf --headless-rendering`

## AI/API Issues

**Gemini rate limit**
- Use `gemini-1.5-flash` (faster, cheaper)
- Add exponential backoff retry logic

**Whisper too slow**
- Use smaller model: `whisper.load_model("tiny")`
- Run on GPU: model runs on CUDA automatically if available
