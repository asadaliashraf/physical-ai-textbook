---
sidebar_position: 3
title: Chapter 3.3 - Isaac ROS & VSLAM
---

# Chapter 3.3: Isaac ROS & Visual SLAM

## Isaac ROS

**Isaac ROS** provides hardware-accelerated ROS 2 packages that run on NVIDIA GPUs and Jetson platforms. Key packages:

| Package | Function |
|---------|----------|
| `isaac_ros_visual_slam` | GPU-accelerated SLAM |
| `isaac_ros_image_segmentation` | Real-time semantic segmentation |
| `isaac_ros_depth_image_proc` | Depth image processing |
| `isaac_ros_nvblox` | Real-time 3D scene reconstruction |
| `isaac_ros_object_detection` | Hardware-accelerated object detection |

## Visual SLAM (VSLAM)

VSLAM estimates robot position by tracking visual features across camera frames.

```
Camera Frames → Feature Extraction → Tracking → Pose Estimation → Map
                     (GPU)              (GPU)         (GPU)
```

### Setup Isaac ROS Visual SLAM

```bash
# Install Isaac ROS VSLAM
sudo apt install ros-humble-isaac-ros-visual-slam -y
```

### Launch VSLAM

```python
# launch/vslam.launch.py
from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import DeclareLaunchArgument

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='isaac_ros_visual_slam',
            executable='visual_slam_node',
            name='visual_slam',
            parameters=[{
                'denoise_input_images': False,
                'rectified_images': True,
                'enable_debug_mode': False,
                'enable_slam_visualization': True,
                'num_cameras': 1,
                'min_num_images': 2,
                'enable_localization_n_mapping': True,
            }],
            remappings=[
                ('stereo_camera/left/image', '/camera/image_rect'),
                ('stereo_camera/left/camera_info', '/camera/camera_info'),
            ]
        ),
    ])
```

## Processing VSLAM Output in Python

```python
#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from nav_msgs.msg import Odometry
from geometry_msgs.msg import PoseWithCovarianceStamped
import numpy as np

class VSLAMProcessor(Node):
    def __init__(self):
        super().__init__('vslam_processor')
        
        # Subscribe to VSLAM pose output
        self.create_subscription(
            PoseWithCovarianceStamped,
            '/visual_slam/tracking/odometry',
            self.pose_callback,
            10
        )
        
        # Publish processed odometry
        self.odom_pub = self.create_publisher(Odometry, '/odom', 10)
        
        self.position_history = []
        self.get_logger().info('VSLAM Processor ready!')

    def pose_callback(self, msg):
        pos = msg.pose.pose.position
        self.get_logger().info(
            f'Robot position: x={pos.x:.3f}, y={pos.y:.3f}, z={pos.z:.3f}'
        )
        
        # Track position history
        self.position_history.append([pos.x, pos.y, pos.z])
        
        # Compute distance traveled
        if len(self.position_history) > 1:
            prev = np.array(self.position_history[-2])
            curr = np.array(self.position_history[-1])
            distance = np.linalg.norm(curr - prev)
            self.get_logger().info(f'Step distance: {distance:.4f}m')

def main(args=None):
    rclpy.init(args=args)
    rclpy.spin(VSLAMProcessor())

if __name__ == '__main__':
    main()
```

**Next**: [Chapter 3.4: Nav2 Navigation](/docs/module-3/week8-9/chapter-3-4)
