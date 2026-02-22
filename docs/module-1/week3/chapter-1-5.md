---
sidebar_position: 1
title: Chapter 1.5 - Building ROS 2 Packages
---

# Chapter 1.5: Building ROS 2 Packages

## ROS 2 Package Structure

```
my_humanoid_pkg/
├── package.xml          # Package metadata
├── setup.py             # Python package setup
├── setup.cfg            # Configuration
├── resource/
│   └── my_humanoid_pkg  # Ament index marker
└── my_humanoid_pkg/
    ├── __init__.py
    ├── joint_controller.py
    ├── gait_planner.py
    └── sensor_fusion.py
```

## Creating a Package

```bash
cd ~/ros2_ws/src
ros2 pkg create --build-type ament_python my_humanoid_pkg \
    --dependencies rclpy sensor_msgs geometry_msgs nav_msgs
```

## package.xml

```xml
<?xml version="1.0"?>
<package format="3">
  <name>my_humanoid_pkg</name>
  <version>0.1.0</version>
  <description>Humanoid robot control package</description>
  <maintainer email="you@email.com">Your Name</maintainer>
  <license>Apache-2.0</license>

  <depend>rclpy</depend>
  <depend>sensor_msgs</depend>
  <depend>geometry_msgs</depend>
  <depend>nav_msgs</depend>
  <depend>tf2_ros</depend>

  <test_depend>ament_copyright</test_depend>
  <test_depend>ament_flake8</test_depend>
  <test_depend>ament_pep257</test_depend>
  <test_depend>pytest</test_depend>

  <export>
    <build_type>ament_python</build_type>
  </export>
</package>
```

## setup.py

```python
from setuptools import find_packages, setup

package_name = 'my_humanoid_pkg'

setup(
    name=package_name,
    version='0.1.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        ('share/' + package_name + '/launch', ['launch/humanoid.launch.py']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    entry_points={
        'console_scripts': [
            'joint_controller = my_humanoid_pkg.joint_controller:main',
            'gait_planner = my_humanoid_pkg.gait_planner:main',
            'sensor_fusion = my_humanoid_pkg.sensor_fusion:main',
        ],
    },
)
```

## Building Your Package

```bash
cd ~/ros2_ws
colcon build --packages-select my_humanoid_pkg
source install/setup.bash

# Run your node
ros2 run my_humanoid_pkg joint_controller
```

**Next**: [Chapter 1.6: Launch Files & Parameters](/docs/module-1/week3/chapter-1-6)
