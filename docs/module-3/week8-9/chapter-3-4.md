---
sidebar_position: 4
title: Chapter 3.4 - Nav2 Navigation
---

# Chapter 3.4: Nav2 Path Planning for Humanoid Robots

## What is Nav2?

**Nav2** (Navigation 2) is the ROS 2 navigation framework providing:
- Global path planning (A*, Dijkstra)
- Local path planning (DWB, MPPI)
- Obstacle avoidance
- Recovery behaviors

## Nav2 Architecture

```
Goal Pose
    ↓
[BT Navigator] (Behavior Tree)
    ↓
[Planner Server] → Global Path
    ↓
[Controller Server] → Velocity Commands
    ↓
[Costmap 2D] (Obstacle map)
    ↓
[Robot Base]
```

## Configure Nav2 for Humanoid

```yaml
# nav2_params.yaml
bt_navigator:
  ros__parameters:
    global_frame: map
    robot_base_frame: base_link
    odom_topic: /odom
    bt_loop_duration: 10
    default_server_timeout: 20
    default_nav_to_pose_bt_xml: navigate_w_replanning_and_recovery.xml

planner_server:
  ros__parameters:
    planner_plugins: ["GridBased"]
    GridBased:
      plugin: "nav2_navfn_planner/NavfnPlanner"
      tolerance: 0.5
      use_astar: true
      allow_unknown: true

controller_server:
  ros__parameters:
    controller_plugins: ["FollowPath"]
    FollowPath:
      plugin: "dwb_core::DWBLocalPlanner"
      max_vel_x: 0.5        # Max forward speed
      min_vel_x: -0.1       # Allow slight backward
      max_vel_theta: 1.0    # Max rotation speed
      min_speed_xy: 0.0
      max_speed_xy: 0.5

costmap_common_params:
  robot_radius: 0.35      # Humanoid footprint radius
  inflation_radius: 0.55
  obstacle_range: 2.5
  raytrace_range: 3.0
```

## Sending Navigation Goals

```python
#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient
from nav2_msgs.action import NavigateToPose
from geometry_msgs.msg import PoseStamped
import math

class HumanoidNavigator(Node):
    def __init__(self):
        super().__init__('humanoid_navigator')
        self._client = ActionClient(self, NavigateToPose, 'navigate_to_pose')

    def navigate_to(self, x, y, theta=0.0):
        """Send robot to position (x, y) facing angle theta"""
        self.get_logger().info(f'Navigating to ({x:.2f}, {y:.2f})')
        
        goal = NavigateToPose.Goal()
        goal.pose.header.frame_id = 'map'
        goal.pose.header.stamp = self.get_clock().now().to_msg()
        goal.pose.pose.position.x = x
        goal.pose.pose.position.y = y
        goal.pose.pose.position.z = 0.0
        
        # Convert angle to quaternion
        goal.pose.pose.orientation.z = math.sin(theta / 2)
        goal.pose.pose.orientation.w = math.cos(theta / 2)
        
        self._client.wait_for_server()
        future = self._client.send_goal_async(
            goal, feedback_callback=self.feedback_cb
        )
        future.add_done_callback(self.goal_response_cb)

    def feedback_cb(self, feedback):
        dist = feedback.feedback.distance_remaining
        self.get_logger().info(f'Distance remaining: {dist:.2f}m')

    def goal_response_cb(self, future):
        goal_handle = future.result()
        if goal_handle.accepted:
            self.get_logger().info('Goal accepted!')
            result_future = goal_handle.get_result_async()
            result_future.add_done_callback(self.result_cb)
        else:
            self.get_logger().warn('Goal rejected!')

    def result_cb(self, future):
        self.get_logger().info('Navigation complete!')

def main(args=None):
    rclpy.init(args=args)
    navigator = HumanoidNavigator()
    navigator.navigate_to(2.0, 1.5, math.pi/2)
    rclpy.spin(navigator)

if __name__ == '__main__':
    main()
```

**Next**: [Chapter 3.5: Perception Systems](/docs/module-3/week10/chapter-3-5)
