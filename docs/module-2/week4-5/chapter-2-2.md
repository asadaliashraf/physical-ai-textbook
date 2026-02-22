---
sidebar_position: 2
title: Chapter 2.2 - Physics Simulation
---

# Chapter 2.2: Physics Simulation

## Physics Engines in Gazebo

| Engine | Best For | Notes |
|--------|----------|-------|
| **ODE** | General robotics | Default, stable |
| **Bullet** | Soft bodies | Complex collisions |
| **DART** | Humanoids | Best for bipedal robots |

## Configuring DART for Humanoids

```xml
<physics name="dart_physics" type="dart">
  <max_step_size>0.001</max_step_size>
  <real_time_factor>1.0</real_time_factor>
</physics>
```

## Contact Physics

```xml
<!-- Configure foot-ground contact -->
<surface>
  <contact>
    <ode>
      <kp>1000000.0</kp>   <!-- Stiffness -->
      <kd>100.0</kd>        <!-- Damping -->
      <mu>0.8</mu>          <!-- Friction coefficient -->
    </ode>
  </contact>
</surface>
```

## Simulating Balance

```python
def compute_center_of_mass(link_masses, link_positions):
    total_mass = sum(link_masses)
    com = sum(m * p for m, p in zip(link_masses, link_positions)) / total_mass
    return com
```

## Gravity Compensation

```python
import math

def gravity_compensation(joint_angles, link_masses, link_lengths):
    torques = []
    for angle, mass, length in zip(joint_angles, link_masses, link_lengths):
        torque = mass * 9.81 * length * 0.5 * math.cos(angle)
        torques.append(torque)
    return torques
```

**Next**: [Chapter 2.3: Unity for Robotics](/docs/module-2/week4-5/chapter-2-3)
