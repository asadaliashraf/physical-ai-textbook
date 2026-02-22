---
sidebar_position: 3
title: Chapter 2.7 - Real-world Physics
---

# Chapter 2.7: Real-world Physics

## Achieving Sim-to-Real Transfer

The biggest challenge in robot simulation is the **reality gap**: behaviors that work in simulation often fail on real hardware. This chapter covers techniques to minimize this gap.

## Key Physical Phenomena to Model

### 1. Actuator Dynamics

Real motors don't respond instantaneously:

```python
class ActuatorModel:
    def __init__(self, max_torque=200, time_constant=0.05):
        self.max_torque = max_torque
        self.time_constant = time_constant
        self.current_torque = 0

    def step(self, commanded_torque, dt):
        # First-order actuator model
        error = commanded_torque - self.current_torque
        self.current_torque += (error / self.time_constant) * dt
        # Clamp to motor limits
        self.current_torque = max(-self.max_torque,
                                   min(self.max_torque, self.current_torque))
        return self.current_torque
```

### 2. Contact and Ground Reaction Forces

```python
def compute_ground_reaction_force(foot_pos, foot_vel, stiffness=10000, damping=100):
    """Compute ground reaction force using spring-damper model"""
    if foot_pos[2] > 0:  # Foot above ground
        return [0, 0, 0]
    
    # Penetration depth
    penetration = -foot_pos[2]
    
    # Spring-damper force (upward)
    force_z = stiffness * penetration - damping * foot_vel[2]
    
    # Friction forces (horizontal)
    friction_coeff = 0.8
    force_x = -friction_coeff * abs(force_z) * foot_vel[0]
    force_y = -friction_coeff * abs(force_z) * foot_vel[1]
    
    return [force_x, force_y, max(0, force_z)]
```

### 3. Sensor Noise Modeling

```python
import numpy as np

class IMUWithNoise:
    def __init__(self):
        # Typical IMU noise parameters
        self.gyro_noise_std = 0.002   # rad/s
        self.accel_noise_std = 0.02   # m/s²
        self.gyro_bias = np.random.normal(0, 0.001, 3)  # Constant bias
        self.accel_bias = np.random.normal(0, 0.01, 3)

    def measure(self, true_angular_vel, true_linear_accel):
        # Add bias and noise
        gyro = (true_angular_vel + self.gyro_bias +
                np.random.normal(0, self.gyro_noise_std, 3))
        accel = (true_linear_accel + self.accel_bias +
                 np.random.normal(0, self.accel_noise_std, 3))
        return gyro, accel
```

### 4. Communication Delays

```python
from collections import deque

class DelayedActuator:
    def __init__(self, delay_steps=5):  # ~50ms at 100Hz
        self.buffer = deque(maxlen=delay_steps)
        # Fill buffer with zeros
        for _ in range(delay_steps):
            self.buffer.append(0.0)

    def command(self, value):
        self.buffer.append(value)
        return self.buffer[0]  # Return oldest command
```

## Measuring Sim-to-Real Gap

```python
def evaluate_sim_to_real_gap(sim_policy, real_robot_data):
    """Compare simulation predictions vs real robot behavior"""
    
    metrics = {
        'position_rmse': 0,
        'velocity_rmse': 0,
        'force_rmse': 0
    }
    
    for sim_state, real_state in zip(sim_policy.states, real_robot_data):
        metrics['position_rmse'] += (sim_state['position'] - real_state['position'])**2
        metrics['velocity_rmse'] += (sim_state['velocity'] - real_state['velocity'])**2
    
    n = len(real_robot_data)
    metrics = {k: (v/n)**0.5 for k, v in metrics.items()}
    return metrics
```

## Module 2 Complete! 🎉

You've mastered digital twin creation. You can now:
✅ Set up Gazebo simulation environments
✅ Configure physics engines for humanoid robots
✅ Integrate ROS 2 with simulation
✅ Simulate all types of sensors
✅ Build realistic world environments
✅ Model real-world physics phenomena

**Next Module**: [Module 3: The AI-Robot Brain (NVIDIA Isaac™)](/docs/module-3/intro)
