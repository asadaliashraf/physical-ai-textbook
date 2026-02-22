---
sidebar_position: 2
title: Chapter 2.6 - Building Custom Worlds
---

# Chapter 2.6: Building Custom Worlds

## Design Principles for Training Environments

A good simulation environment for humanoid training:
1. **Represents real-world variety** (different floors, obstacles, lighting)
2. **Is computationally efficient** (fast rendering = more training)
3. **Has randomizable elements** (domain randomization)
4. **Provides accurate contact physics**

## Building an Apartment Environment

```xml
<?xml version="1.0"?>
<sdf version="1.9">
  <world name="apartment">
    <physics type="dart">
      <max_step_size>0.001</max_step_size>
    </physics>
    
    <!-- Walls -->
    <model name="walls">
      <static>true</static>
      <!-- North wall -->
      <link name="north_wall">
        <pose>0 5 1.5 0 0 0</pose>
        <collision name="col">
          <geometry><box><size>10 0.2 3</size></box></geometry>
        </collision>
        <visual name="vis">
          <geometry><box><size>10 0.2 3</size></box></geometry>
          <material>
            <ambient>0.9 0.9 0.9 1</ambient>
          </material>
        </visual>
      </link>
      <!-- Add more walls similarly -->
    </model>
    
    <!-- Furniture -->
    <model name="table">
      <static>true</static>
      <pose>2 2 0 0 0 0</pose>
      <link name="tabletop">
        <pose>0 0 0.75 0 0 0</pose>
        <collision name="col">
          <geometry><box><size>1.2 0.8 0.05</size></box></geometry>
        </collision>
        <visual name="vis">
          <geometry><box><size>1.2 0.8 0.05</size></box></geometry>
          <material><ambient>0.6 0.4 0.2 1</ambient></material>
        </visual>
      </link>
    </model>
    
    <!-- Dynamic obstacles (can be moved by robot) -->
    <model name="cup">
      <pose>2 2 0.8 0 0 0</pose>
      <link name="body">
        <inertial><mass>0.3</mass></inertial>
        <collision name="col">
          <geometry><cylinder><radius>0.04</radius><length>0.12</length></cylinder></geometry>
        </collision>
        <visual name="vis">
          <geometry><cylinder><radius>0.04</radius><length>0.12</length></cylinder></geometry>
          <material><ambient>0.2 0.4 0.8 1</ambient></material>
        </visual>
      </link>
    </model>
    
  </world>
</sdf>
```

## Domain Randomization

For robust sim-to-real transfer, randomize environment parameters:

```python
#!/usr/bin/env python3
import subprocess
import random

def randomize_world():
    """Generate a world SDF with randomized parameters"""
    
    # Randomize floor friction
    floor_friction = random.uniform(0.5, 1.2)
    
    # Randomize lighting
    light_intensity = random.uniform(0.7, 1.3)
    
    # Randomize obstacle positions
    table_x = random.uniform(1.0, 3.0)
    table_y = random.uniform(1.0, 3.0)
    
    world_sdf = f"""<?xml version="1.0"?>
<sdf version="1.9">
  <world name="randomized_apartment">
    <physics type="dart">
      <max_step_size>0.001</max_step_size>
    </physics>
    <light name="sun" type="directional">
      <diffuse>{light_intensity} {light_intensity} {light_intensity} 1</diffuse>
    </light>
    <model name="table">
      <static>true</static>
      <pose>{table_x} {table_y} 0 0 0 {random.uniform(0, 3.14)}</pose>
      <!-- table links... -->
    </model>
  </world>
</sdf>"""
    
    with open('/tmp/randomized_world.sdf', 'w') as f:
        f.write(world_sdf)
    
    return '/tmp/randomized_world.sdf'

# Run 100 training episodes with different worlds
for episode in range(100):
    world_file = randomize_world()
    print(f"Episode {episode}: Training in randomized world")
    subprocess.run(['gz', 'sim', world_file])
```

**Next**: [Chapter 2.7: Real-world Physics](/docs/module-2/week6-7/chapter-2-7)
