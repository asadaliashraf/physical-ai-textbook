---
sidebar_position: 4
title: Chapter 2.4 - Sensor Simulation
---

# Chapter 2.4: Sensor Simulation (LIDAR, Cameras, IMUs)

## Sensor Types in Robotics

### 1. LIDAR

```xml
<sensor name="lidar" type="gpu_lidar">
  <pose>0 0 0.5 0 0 0</pose>
  <update_rate>10</update_rate>
  <lidar>
    <scan>
      <horizontal>
        <samples>1080</samples>
        <min_angle>-3.14159</min_angle>
        <max_angle>3.14159</max_angle>
      </horizontal>
    </scan>
    <range>
      <min>0.1</min>
      <max>100.0</max>
    </range>
  </lidar>
</sensor>
```

### 2. Depth Camera

```xml
<sensor name="depth_camera" type="depth_camera">
  <camera>
    <horizontal_fov>1.047</horizontal_fov>
    <image>
      <width>640</width>
      <height>480</height>
    </image>
    <clip>
      <near>0.1</near>
      <far>10.0</far>
    </clip>
  </camera>
  <update_rate>30</update_rate>
</sensor>
```

### 3. IMU

```xml
<sensor name="imu" type="imu">
  <imu>
    <angular_velocity>
      <x><noise type="gaussian"><stddev>0.0002</stddev></noise></x>
    </angular_velocity>
    <linear_acceleration>
      <x><noise type="gaussian"><stddev>0.017</stddev></noise></x>
    </linear_acceleration>
  </imu>
  <update_rate>200</update_rate>
</sensor>
```

## Processing Sensor Data in ROS 2

```python
import math
from sensor_msgs.msg import LaserScan, Imu

class SensorFusion(Node):
    def __init__(self):
        super().__init__('sensor_fusion')
        self.create_subscription(LaserScan, '/lidar', self.lidar_cb, 10)
        self.create_subscription(Imu, '/imu/data', self.imu_cb, 10)

    def lidar_cb(self, msg):
        valid = [r for r in msg.ranges if not math.isnan(r) and r > 0]
        if valid and min(valid) < 0.5:
            self.get_logger().warn(f'Obstacle at {min(valid):.2f}m!')

    def imu_cb(self, msg):
        ax = msg.linear_acceleration.x
        ay = msg.linear_acceleration.y
        az = msg.linear_acceleration.z
        roll = math.atan2(ay, az)
        pitch = math.atan2(-ax, math.sqrt(ay**2 + az**2))
        self.get_logger().debug(
            f'Roll: {math.degrees(roll):.1f} Pitch: {math.degrees(pitch):.1f}'
        )
```

**Next**: [Chapter 2.5: URDF and SDF Formats](/docs/module-2/week6-7/chapter-2-5)
