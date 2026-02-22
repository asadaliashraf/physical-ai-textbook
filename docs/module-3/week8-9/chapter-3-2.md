---
sidebar_position: 2
title: Chapter 3.2 - Photorealistic Simulation
---

# Chapter 3.2: Photorealistic Simulation & Synthetic Data

## Why Photorealistic Simulation?

Training computer vision models requires vast amounts of labeled data. Real-world collection is:
- Expensive and time-consuming
- Dangerous for certain scenarios
- Hard to control/label

**Isaac Sim generates unlimited, perfectly labeled synthetic data!**

## Synthetic Data Generation

```python
from isaacsim import SimulationApp
app = SimulationApp({"headless": True})

from omni.isaac.core import World
from omni.replicator.core import ReplicatorCore
import omni.replicator.core as rep

world = World()

# Set up the scene with a robot and objects
with rep.new_layer():
    # Create camera
    camera = rep.create.camera(position=(0, -3, 1.5))
    
    # Random object placement
    objects = rep.create.from_usd(
        'omniverse://localhost/Isaac/Props/household_objects/*.usd',
        count=10
    )
    
    # Randomize parameters each frame
    with rep.randomizer.register_randomizer():
        # Random object positions on table
        rep.randomize.pose(
            objects,
            position=rep.distribution.uniform((-0.5, -0.5, 0.75), (0.5, 0.5, 0.85))
        )
        
        # Random lighting
        rep.randomize.light(
            lights=rep.create.light(light_type='sphere', count=3),
            intensity=rep.distribution.uniform(500, 2000),
            color=rep.distribution.uniform((0.8, 0.8, 0.8), (1.0, 1.0, 1.0))
        )
        
        # Random camera angle
        rep.randomize.pose(
            camera,
            position=rep.distribution.uniform((-1, -4, 1), (1, -2, 2.5)),
            look_at=(0, 0, 0.8)
        )

# Generate 1000 training images
render_product = rep.create.render_product(camera, (640, 480))

writer = rep.WriterRegistry.get("BasicWriter")
writer.initialize(
    output_dir="/tmp/synthetic_data",
    rgb=True,
    bounding_box_2d_tight=True,  # Object detection labels
    semantic_segmentation=True,   # Segmentation masks
    depth=True
)

writer.attach([render_product])

for i in range(1000):
    rep.orchestrator.step()
    print(f"Generated image {i+1}/1000")

print("Dataset generation complete!")
app.close()
```

## Material Randomization

```python
# Randomize robot appearance for sim-to-real
with rep.randomizer.register_randomizer():
    robot_materials = rep.create.material_omnipbr(
        diffuse=rep.distribution.choice([
            (0.3, 0.3, 0.3),   # Dark gray
            (0.8, 0.8, 0.8),   # Light gray
            (0.2, 0.4, 0.8),   # Blue
        ]),
        roughness=rep.distribution.uniform(0.1, 0.9),
        metallic=rep.distribution.uniform(0.0, 0.5)
    )
```

## RTX Rendering Modes

| Mode | Use Case | Speed |
|------|----------|-------|
| **RTX Real-Time** | Training, fast iteration | Fast |
| **RTX Interactive** | Visual debugging | Medium |
| **RTX Accurate** | Final dataset generation | Slow |
| **Path Tracing** | Research-quality | Very slow |

```python
# Set render mode
from omni.isaac.core.utils.render_product import RenderProduct

render_product = RenderProduct(camera_prim, (1920, 1080))
render_product.hydra_texture.set_updates_enabled(True)

# Switch to path tracing for high quality
import carb
carb.settings.get_settings().set('/rtx/rendermode', 'PathTracing')
```

**Next**: [Chapter 3.3: Isaac ROS & VSLAM](/docs/module-3/week8-9/chapter-3-3)
