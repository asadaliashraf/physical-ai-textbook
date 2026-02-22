---
sidebar_position: 2
title: Chapter 1.6 - Launch Files & Parameters
---

# Chapter 1.6: Launch Files & Parameters

## ROS 2 Launch Files

Launch files start multiple nodes simultaneously with a single command.

## Python Launch File

```python
# launch/humanoid.launch.py
from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration

def generate_launch_description():
    # Declare arguments
    robot_name_arg = DeclareLaunchArgument(
        'robot_name', default_value='humanoid_01',
        description='Name of the robot'
    )
    walk_speed_arg = DeclareLaunchArgument(
        'walk_speed', default_value='0.5',
        description='Walking speed (0.0-1.0)'
    )

    return LaunchDescription([
        robot_name_arg,
        walk_speed_arg,

        # Joint State Publisher
        Node(
            package='my_humanoid_pkg',
            executable='joint_controller',
            name='joint_controller',
            parameters=[{
                'robot_name': LaunchConfiguration('robot_name'),
                'walk_speed': LaunchConfiguration('walk_speed'),
            }],
            output='screen',
        ),

        # Gait Planner
        Node(
            package='my_humanoid_pkg',
            executable='gait_planner',
            name='gait_planner',
            remappings=[
                ('/cmd_vel', '/robot/cmd_vel'),
            ],
        ),

        # RViz2 for visualization
        Node(
            package='rviz2',
            executable='rviz2',
            name='rviz2',
            arguments=['-d', 'config/humanoid_view.rviz'],
        ),
    ])
```

## Running Launch Files

```bash
# Basic launch
ros2 launch my_humanoid_pkg humanoid.launch.py

# With arguments
ros2 launch my_humanoid_pkg humanoid.launch.py \
    robot_name:=robot_alpha \
    walk_speed:=0.8
```

## Parameter Files (YAML)

```yaml
# config/robot_params.yaml
joint_controller:
  ros__parameters:
    robot_name: "humanoid_01"
    walk_speed: 0.5
    joint_limits:
      left_knee: [-1.57, 0.0]
      right_knee: [-1.57, 0.0]
      left_hip: [-0.8, 0.8]
    control_frequency: 100.0
    use_sim_time: false
```

```python
# Load YAML parameters in launch
Node(
    package='my_humanoid_pkg',
    executable='joint_controller',
    parameters=['config/robot_params.yaml'],
)
```

## Dynamic Parameter Updates

```python
from rcl_interfaces.msg import SetParametersResult

class AdaptiveController(Node):
    def __init__(self):
        super().__init__('adaptive_controller')
        self.declare_parameter('kp', 1.0)
        self.add_on_set_parameters_callback(self.param_callback)

    def param_callback(self, params):
        for param in params:
            if param.name == 'kp':
                self.kp = param.value
                self.get_logger().info(f'Updated kp to {self.kp}')
        return SetParametersResult(successful=True)
```

```bash
# Update parameters at runtime
ros2 param set /adaptive_controller kp 2.5
```

**Next**: [Chapter 1.7: Practical Project](/docs/module-1/week3/chapter-1-7)
