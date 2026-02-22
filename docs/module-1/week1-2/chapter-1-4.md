---
sidebar_position: 4
title: Chapter 1.4 - URDF for Humanoid Robots
---

# Chapter 1.4: URDF for Humanoid Robots

## What is URDF?

**URDF** (Unified Robot Description Format) is an XML format that describes a robot's physical structure — its links (rigid bodies) and joints (connections between links).

## URDF Structure

```xml
<?xml version="1.0"?>
<robot name="simple_humanoid">

  <!-- Base Link (torso) -->
  <link name="base_link">
    <visual>
      <geometry>
        <box size="0.3 0.2 0.5"/>
      </geometry>
      <material name="blue">
        <color rgba="0.2 0.4 0.8 1.0"/>
      </material>
    </visual>
    <collision>
      <geometry>
        <box size="0.3 0.2 0.5"/>
      </geometry>
    </collision>
    <inertial>
      <mass value="20.0"/>
      <inertia ixx="0.1" ixy="0" ixz="0" iyy="0.1" iyz="0" izz="0.05"/>
    </inertial>
  </link>

  <!-- Head Link -->
  <link name="head_link">
    <visual>
      <geometry>
        <sphere radius="0.12"/>
      </geometry>
    </visual>
    <inertial>
      <mass value="3.0"/>
      <inertia ixx="0.02" ixy="0" ixz="0" iyy="0.02" iyz="0" izz="0.02"/>
    </inertial>
  </link>

  <!-- Neck Joint -->
  <joint name="neck_joint" type="revolute">
    <parent link="base_link"/>
    <child link="head_link"/>
    <origin xyz="0 0 0.31" rpy="0 0 0"/>
    <axis xyz="0 0 1"/>
    <limit lower="-1.57" upper="1.57" effort="10" velocity="1.0"/>
  </joint>

  <!-- Left Upper Leg -->
  <link name="left_upper_leg">
    <visual>
      <geometry>
        <cylinder length="0.4" radius="0.05"/>
      </geometry>
    </visual>
    <inertial>
      <mass value="5.0"/>
      <inertia ixx="0.07" ixy="0" ixz="0" iyy="0.07" iyz="0" izz="0.005"/>
    </inertial>
  </link>

  <!-- Left Hip Joint -->
  <joint name="left_hip_pitch" type="revolute">
    <parent link="base_link"/>
    <child link="left_upper_leg"/>
    <origin xyz="0.1 0 -0.25" rpy="0 0 0"/>
    <axis xyz="0 1 0"/>
    <limit lower="-1.5" upper="1.0" effort="100" velocity="2.0"/>
  </joint>

</robot>
```

## Joint Types

| Type | Description | Example |
|------|-------------|---------|
| `revolute` | Rotates around an axis with limits | Knee, Hip |
| `continuous` | Rotates without limits | Wheel |
| `prismatic` | Slides along an axis | Linear actuator |
| `fixed` | No movement | Sensor mount |
| `floating` | 6-DOF free motion | Base link |

## Visualizing URDF in RViz2

```bash
# Install urdf tutorial
sudo apt install ros-humble-urdf-tutorial

# Launch visualization
ros2 launch urdf_tutorial display.launch.py model:=my_robot.urdf
```

## XACRO: Better URDF

XACRO adds macros to URDF, reducing repetition:

```xml
<?xml version="1.0"?>
<robot xmlns:xacro="http://www.ros.org/wiki/xacro" name="humanoid">

  <!-- Define reusable macro for a leg segment -->
  <xacro:macro name="leg_segment" params="prefix length mass">
    <link name="${prefix}_segment">
      <visual>
        <geometry>
          <cylinder length="${length}" radius="0.05"/>
        </geometry>
      </visual>
      <inertial>
        <mass value="${mass}"/>
        <inertia ixx="${mass * length * length / 12}"
                 ixy="0" ixz="0"
                 iyy="${mass * length * length / 12}"
                 iyz="0" izz="0.005"/>
      </inertial>
    </link>
  </xacro:macro>

  <!-- Use the macro -->
  <xacro:leg_segment prefix="left_upper" length="0.4" mass="5.0"/>
  <xacro:leg_segment prefix="right_upper" length="0.4" mass="5.0"/>
  <xacro:leg_segment prefix="left_lower" length="0.35" mass="3.0"/>
  <xacro:leg_segment prefix="right_lower" length="0.35" mass="3.0"/>

</robot>
```

## Validate Your URDF

```bash
# Check for errors
check_urdf my_robot.urdf

# Convert xacro to URDF
ros2 run xacro xacro my_robot.xacro > my_robot.urdf
```

**Next**: [Chapter 1.5: Building ROS 2 Packages](/docs/module-1/week3/chapter-1-5)
