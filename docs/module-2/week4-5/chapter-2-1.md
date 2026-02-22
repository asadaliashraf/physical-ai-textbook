---
sidebar_position: 1
title: Chapter 2.1 - Introduction to Gazebo
---

# Chapter 2.1: Introduction to Gazebo

## What is Gazebo?

**Gazebo** (formerly known as Gazebo Classic, now Gazebo Harmonic/Fortress) is an open-source robot simulation environment that provides:
- Accurate physics simulation (rigid body dynamics)
- Sensor simulation (cameras, LIDAR, IMU)
- ROS 2 integration via `ros_gz_bridge`
- Plugin system for custom behaviors

## Installing Gazebo

```bash
# Install Gazebo Harmonic (latest LTS)
sudo apt-get update
sudo apt-get install gz-harmonic -y

# Install ROS-Gazebo bridge
sudo apt install ros-humble-ros-gz -y

# Verify installation
gz sim --version
```

## Your First Gazebo World

```bash
# Launch an empty world
gz sim empty.sdf

# Or launch with a robot
gz sim -r ~/ros2_ws/src/my_robot/worlds/humanoid_world.sdf
```

## SDF: Simulation Description Format

Gazebo uses **SDF** (Simulation Description Format), an evolution of URDF with more features:

```xml
<?xml version="1.0"?>
<sdf version="1.9">
  <world name="humanoid_training">

    <!-- Physics configuration -->
    <physics name="fast_physics" type="ode">
      <max_step_size>0.001</max_step_size>
      <real_time_factor>1.0</real_time_factor>
      <real_time_update_rate>1000</real_time_update_rate>
    </physics>

    <!-- Environment lighting -->
    <light name="sun" type="directional">
      <pose>0 0 10 0 0 0</pose>
      <diffuse>1 1 1 1</diffuse>
      <specular>0.5 0.5 0.5 1</specular>
      <direction>-0.5 0.1 -0.9</direction>
    </light>

    <!-- Ground plane -->
    <model name="ground_plane">
      <static>true</static>
      <link name="link">
        <collision name="collision">
          <geometry>
            <plane><normal>0 0 1</normal></plane>
          </geometry>
        </collision>
        <visual name="visual">
          <geometry>
            <plane><normal>0 0 1</normal><size>100 100</size></plane>
          </geometry>
          <material>
            <ambient>0.8 0.8 0.8 1</ambient>
          </material>
        </visual>
      </link>
    </model>

    <!-- Include a robot model -->
    <include>
      <uri>model://my_humanoid</uri>
      <pose>0 0 1 0 0 0</pose>
    </include>

  </world>
</sdf>
```

## ROS 2 Integration

```bash
# Bridge Gazebo topics to ROS 2
ros2 run ros_gz_bridge parameter_bridge \
    /joint_states@sensor_msgs/msg/JointState[gz.msgs.Model \
    /camera/image@sensor_msgs/msg/Image[gz.msgs.Image \
    /lidar@sensor_msgs/msg/LaserScan[gz.msgs.LaserScan
```

## Launch File with Gazebo

```python
# launch/gazebo_humanoid.launch.py
from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import ExecuteProcess, IncludeLaunchDescription

def generate_launch_description():
    return LaunchDescription([
        # Start Gazebo
        ExecuteProcess(
            cmd=['gz', 'sim', 'humanoid_world.sdf'],
            output='screen'
        ),
        # Start ROS-Gazebo bridge
        Node(
            package='ros_gz_bridge',
            executable='parameter_bridge',
            arguments=['/joint_states@sensor_msgs/msg/JointState[gz.msgs.Model'],
        ),
        # Start your controller
        Node(
            package='my_humanoid_pkg',
            executable='joint_controller',
        ),
    ])
```

**Next**: [Chapter 2.2: Physics Simulation](/docs/module-2/week4-5/chapter-2-2)
