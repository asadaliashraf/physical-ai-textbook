---
sidebar_position: 3
title: Chapter 2.3 - Unity for Robotics
---

# Chapter 2.3: Unity for Robotics

## Unity Robotics Hub

Unity provides photorealistic environments for:
- Training visual perception models
- Testing human-robot interaction
- Creating realistic training data

## Setup

1. Install Unity 2022 LTS from https://unity.com/download
2. Add the ROS-TCP-Connector package via Package Manager:
   `https://github.com/Unity-Technologies/ROS-TCP-Connector.git`

## ROS 2 Bridge

```bash
ros2 run ros_tcp_endpoint default_server_endpoint \
    --ros-args -p ROS_IP:=127.0.0.1
```

## Unity C# Script for Robot Visualization

```csharp
using UnityEngine;
using Unity.Robotics.ROSTCPConnector;
using RosMessageTypes.Sensor;

public class RobotVisualizer : MonoBehaviour
{
    ROSConnection ros;

    void Start()
    {
        ros = ROSConnection.GetOrCreateInstance();
        ros.Subscribe<JointStateMsg>("/joint_states", OnJointState);
    }

    void OnJointState(JointStateMsg msg)
    {
        for (int i = 0; i < msg.name.Length; i++)
        {
            float angle = (float)msg.position[i] * Mathf.Rad2Deg;
            Transform joint = transform.Find(msg.name[i]);
            if (joint != null)
                joint.localRotation = Quaternion.Euler(0, angle, 0);
        }
    }
}
```

## Photorealistic Training Data

Unity generates diverse scenarios:
- Different indoor environments
- Various lighting conditions
- Moving people and vehicles
- Weather variations

**Next**: [Chapter 2.4: Sensor Simulation](/docs/module-2/week4-5/chapter-2-4)
