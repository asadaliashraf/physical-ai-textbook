---
sidebar_position: 1
title: Chapter 3.1 - Introduction to Isaac Sim
---

# Chapter 3.1: Introduction to NVIDIA Isaac Sim

## What is Isaac Sim?

**NVIDIA Isaac Sim** is a scalable, photorealistic simulation platform built on NVIDIA Omniverse. It enables robot developers to train, test, and validate AI-powered robots in physically accurate virtual environments before deploying to real hardware.

## Key Features

| Feature | Description |
|---------|-------------|
| **RTX Rendering** | Photorealistic visuals with ray tracing |
| **Physics** | PhysX 5 for accurate rigid body simulation |
| **Synthetic Data** | Generate labeled training data at scale |
| **ROS 2 Bridge** | Native integration with ROS 2 |
| **Isaac Lab** | RL training framework built-in |
| **Multi-robot** | Simulate hundreds of robots simultaneously |

## Installation

### Prerequisites

```bash
# NVIDIA Driver 525+
nvidia-smi  # Verify GPU

# CUDA 11.8+
nvcc --version

# Python 3.10
python3 --version
```

### Install via pip (Isaac Sim 4.x)

```bash
# Create virtual environment
python3 -m venv isaac_env
source isaac_env/bin/activate

# Install Isaac Sim Python package
pip install isaacsim --extra-index-url https://pypi.nvidia.com

# Install Isaac Lab
pip install isaacsim-rl --extra-index-url https://pypi.nvidia.com
```

### Verify Installation

```python
from isaacsim import SimulationApp
app = SimulationApp({"headless": False})

from pxr import Usd
print("Isaac Sim installed successfully!")
app.close()
```

## Your First Isaac Sim Scene

```python
#!/usr/bin/env python3
from isaacsim import SimulationApp

# Start simulation
app = SimulationApp({"headless": False, "width": 1920, "height": 1080})

import omni
from omni.isaac.core import World
from omni.isaac.core.objects import DynamicCuboid
import numpy as np

# Create world
world = World(stage_units_in_meters=1.0)
world.scene.add_default_ground_plane()

# Add a box that falls with gravity
box = world.scene.add(DynamicCuboid(
    prim_path="/World/Box",
    name="falling_box",
    position=np.array([0.0, 0.0, 1.0]),
    scale=np.array([0.2, 0.2, 0.2]),
    color=np.array([0.2, 0.4, 0.8]),
    mass=1.0
))

# Initialize and run simulation
world.reset()

print("Simulation started! Watching box fall...")
for i in range(1000):
    world.step(render=True)
    if i % 100 == 0:
        pos = box.get_world_pose()[0]
        print(f"Step {i}: Box position = {pos}")

app.close()
```

## Loading a Humanoid Robot

```python
from isaacsim import SimulationApp
app = SimulationApp({"headless": False})

from omni.isaac.core import World
from omni.isaac.core.robots import Robot
import omni.kit.commands
import numpy as np

world = World()
world.scene.add_default_ground_plane()

# Load robot from USD (Universal Scene Description)
omni.kit.commands.execute('CreateReference',
    usd_context=omni.usd.get_context(),
    prim_path='/World/Humanoid',
    asset_path='omniverse://localhost/Isaac/Robots/Unitree/H1/h1.usd'
)

# Create robot wrapper
robot = world.scene.add(Robot(
    prim_path="/World/Humanoid",
    name="h1_robot",
    position=np.array([0, 0, 1.05])
))

world.reset()
print(f"Robot joints: {robot.num_dof}")

for _ in range(2000):
    world.step(render=True)

app.close()
```

## Isaac Sim USD Format

Isaac Sim uses **USD** (Universal Scene Description) - Pixar's open-source 3D interchange format:

```python
from pxr import Usd, UsdGeom, UsdPhysics

# Open a stage
stage = Usd.Stage.CreateNew('/tmp/my_robot.usd')

# Create a mesh
mesh = UsdGeom.Mesh.Define(stage, '/World/Robot/Body')
mesh.CreatePointsAttr([(-1,-1,-1), (1,-1,-1), (1,1,-1), (-1,1,-1)])
mesh.CreateFaceVertexCountsAttr([4])
mesh.CreateFaceVertexIndicesAttr([0, 1, 2, 3])

# Add physics
rigid_body = UsdPhysics.RigidBodyAPI.Apply(mesh.GetPrim())
rigid_body.CreateRigidBodyEnabledAttr(True)

stage.GetRootLayer().Save()
print("USD scene saved!")
```

**Next**: [Chapter 3.2: Photorealistic Simulation](/docs/module-3/week8-9/chapter-3-2)
