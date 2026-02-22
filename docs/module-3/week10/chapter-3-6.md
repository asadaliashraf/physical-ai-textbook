---
sidebar_position: 2
title: Chapter 3.6 - Reinforcement Learning
---

# Chapter 3.6: Reinforcement Learning for Locomotion

## PPO for Humanoid Walking

Proximal Policy Optimization (PPO) is the gold standard for humanoid locomotion training.

```python
import torch
import torch.nn as nn

class ActorCritic(nn.Module):
    def __init__(self, obs_dim, act_dim):
        super().__init__()
        self.shared = nn.Sequential(
            nn.Linear(obs_dim, 256), nn.ELU(),
            nn.Linear(256, 128), nn.ELU()
        )
        self.actor = nn.Sequential(nn.Linear(128, act_dim), nn.Tanh())
        self.critic = nn.Linear(128, 1)

    def forward(self, obs):
        shared = self.shared(obs)
        return self.actor(shared), self.critic(shared)
```

## Reward Function Design

```python
def compute_reward(base_vel, actions, base_height):
    vel_reward = -abs(base_vel[0] - 0.5)    # Target: 0.5 m/s forward
    lateral = -0.5 * abs(base_vel[1])        # Penalize sideways motion
    energy = -0.001 * sum(a**2 for a in actions)  # Energy efficiency
    fall = -100.0 if base_height < 0.5 else 0.0   # Fall penalty
    return vel_reward + lateral + energy + fall
```

## Training in Isaac Lab

```bash
# Train with 4096 parallel environments
python train.py --task H1-Walk --num_envs 4096 --headless

# Monitor training
tensorboard --logdir logs/
```

**Next**: [Chapter 3.7: Sim-to-Real Transfer](/docs/module-3/week10/chapter-3-7)
