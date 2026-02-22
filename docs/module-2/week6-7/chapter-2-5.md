---
sidebar_position: 1
title: Chapter 2.5 - URDF and SDF Formats
---

# Chapter 2.5: URDF and SDF Formats

## URDF vs SDF

| Feature | URDF | SDF |
|---------|------|-----|
| **Purpose** | Robot description | World + Robot description |
| **Simulation** | Gazebo (via conversion) | Gazebo native |
| **Sensors** | Limited | Full sensor support |
| **Multiple robots** | One robot | Multiple robots |
| **World elements** | No | Yes |

## Advanced URDF with XACRO

```xml
<?xml version="1.0"?>
<robot xmlns:xacro="http://www.ros.org/wiki/xacro" name="full_humanoid">
  
  <xacro:property name="body_mass" value="20.0"/>
  <xacro:property name="leg_mass" value="5.0"/>
  <xacro:property name="upper_leg_length" value="0.4"/>
  <xacro:property name="lower_leg_length" value="0.35"/>

  <!-- Reusable leg macro -->
  <xacro:macro name="leg" params="prefix side_sign">
    <!-- Upper leg -->
    <link name="${prefix}_upper_leg">
      <visual>
        <origin xyz="0 0 -${upper_leg_length/2}"/>
        <geometry>
          <cylinder length="${upper_leg_length}" radius="0.05"/>
        </geometry>
        <material name="${prefix}_color">
          <color rgba="${(side_sign+1)/2} 0.3 ${(-side_sign+1)/2} 1"/>
        </material>
      </visual>
      <inertial>
        <mass value="${leg_mass}"/>
        <inertia ixx="${leg_mass * upper_leg_length**2 / 12}" ixy="0" ixz="0"
                 iyy="${leg_mass * upper_leg_length**2 / 12}" iyz="0"
                 izz="0.005"/>
      </inertial>
    </link>

    <!-- Hip joint -->
    <joint name="${prefix}_hip_pitch" type="revolute">
      <parent link="base_link"/>
      <child link="${prefix}_upper_leg"/>
      <origin xyz="${side_sign * 0.1} 0 -0.25"/>
      <axis xyz="0 1 0"/>
      <limit lower="-1.5" upper="1.0" effort="100" velocity="2.0"/>
      <dynamics damping="1.0" friction="0.1"/>
    </joint>
    
    <!-- Lower leg -->
    <link name="${prefix}_lower_leg">
      <visual>
        <origin xyz="0 0 -${lower_leg_length/2}"/>
        <geometry>
          <cylinder length="${lower_leg_length}" radius="0.04"/>
        </geometry>
      </visual>
      <inertial>
        <mass value="${leg_mass * 0.6}"/>
        <inertia ixx="0.04" ixy="0" ixz="0" iyy="0.04" iyz="0" izz="0.003"/>
      </inertial>
    </link>

    <!-- Knee joint -->
    <joint name="${prefix}_knee" type="revolute">
      <parent link="${prefix}_upper_leg"/>
      <child link="${prefix}_lower_leg"/>
      <origin xyz="0 0 -${upper_leg_length}"/>
      <axis xyz="0 1 0"/>
      <limit lower="-1.57" upper="0.0" effort="80" velocity="2.0"/>
    </joint>
  </xacro:macro>

  <!-- Use the macro for both legs -->
  <xacro:leg prefix="left" side_sign="-1"/>
  <xacro:leg prefix="right" side_sign="1"/>

</robot>
```

## Convert XACRO to URDF

```bash
ros2 run xacro xacro humanoid.xacro > humanoid.urdf
check_urdf humanoid.urdf
```

## Complete SDF World File

```xml
<?xml version="1.0"?>
<sdf version="1.9">
  <world name="humanoid_lab">
    <!-- DART physics for accurate humanoid simulation -->
    <physics name="dart" type="dart">
      <max_step_size>0.001</max_step_size>
      <real_time_factor>1.0</real_time_factor>
    </physics>
    
    <!-- Gravity -->
    <gravity>0 0 -9.81</gravity>
    
    <!-- Lighting -->
    <light name="sun" type="directional">
      <pose>0 0 10 0 0 0</pose>
      <diffuse>1 1 1 1</diffuse>
      <specular>0.2 0.2 0.2 1</specular>
      <direction>-0.5 0.1 -0.9</direction>
      <cast_shadows>true</cast_shadows>
    </light>
    
    <!-- Ground -->
    <model name="ground">
      <static>true</static>
      <link name="link">
        <collision name="col">
          <geometry>
            <plane><normal>0 0 1</normal></plane>
          </geometry>
          <surface>
            <friction>
              <ode><mu>0.8</mu><mu2>0.8</mu2></ode>
            </friction>
          </surface>
        </collision>
        <visual name="vis">
          <geometry>
            <plane><normal>0 0 1</normal><size>20 20</size></plane>
          </geometry>
        </visual>
      </link>
    </model>
  </world>
</sdf>
```

**Next**: [Chapter 2.6: Building Custom Worlds](/docs/module-2/week6-7/chapter-2-6)
