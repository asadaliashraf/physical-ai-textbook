import type {SidebarsConfig} from '@docusaurus/plugin-content-docs';

const sidebars: SidebarsConfig = {
  tutorialSidebar: [
    {
      type: 'doc',
      id: 'intro',
      label: 'Welcome',
    },
    {
      type: 'category',
      label: 'Module 1: ROS 2 - The Robotic Nervous System',
      items: [
        'module-1/intro',
        {
          type: 'category',
          label: 'Week 1-2: ROS 2 Fundamentals',
          items: [
            'module-1/week1-2/chapter-1-1',
            'module-1/week1-2/chapter-1-2',
            'module-1/week1-2/chapter-1-3',
            'module-1/week1-2/chapter-1-4',
          ],
        },
        {
          type: 'category',
          label: 'Week 3: Advanced ROS 2',
          items: [
            'module-1/week3/chapter-1-5',
            'module-1/week3/chapter-1-6',
            'module-1/week3/chapter-1-7',
          ],
        },
      ],
    },
    {
      type: 'category',
      label: 'Module 2: Digital Twin - Gazebo & Unity',
      items: [
        'module-2/intro',
        {
          type: 'category',
          label: 'Week 4-5: Simulation Environments',
          items: [
            'module-2/week4-5/chapter-2-1',
            'module-2/week4-5/chapter-2-2',
            'module-2/week4-5/chapter-2-3',
            'module-2/week4-5/chapter-2-4',
          ],
        },
        {
          type: 'category',
          label: 'Week 6-7: Advanced Simulation',
          items: [
            'module-2/week6-7/chapter-2-5',
            'module-2/week6-7/chapter-2-6',
            'module-2/week6-7/chapter-2-7',
          ],
        },
      ],
    },
    {
      type: 'category',
      label: 'Module 3: AI-Robot Brain - NVIDIA Isaac™',
      items: [
        'module-3/intro',
        {
          type: 'category',
          label: 'Week 8-9: Isaac Platform',
          items: [
            'module-3/week8-9/chapter-3-1',
            'module-3/week8-9/chapter-3-2',
            'module-3/week8-9/chapter-3-3',
            'module-3/week8-9/chapter-3-4',
          ],
        },
        {
          type: 'category',
          label: 'Week 10: AI-Powered Robotics',
          items: [
            'module-3/week10/chapter-3-5',
            'module-3/week10/chapter-3-6',
            'module-3/week10/chapter-3-7',
          ],
        },
      ],
    },
    {
      type: 'category',
      label: 'Module 4: VLA - Vision-Language-Action',
      items: [
        'module-4/intro',
        {
          type: 'category',
          label: 'Week 11-12: Cognitive Robotics',
          items: [
            'module-4/week11-12/chapter-4-1',
            'module-4/week11-12/chapter-4-2',
            'module-4/week11-12/chapter-4-3',
            'module-4/week11-12/chapter-4-4',
          ],
        },
        {
          type: 'category',
          label: 'Week 13: Capstone Project',
          items: [
            'module-4/week13/chapter-4-5',
            'module-4/week13/chapter-4-6',
            'module-4/week13/chapter-4-7',
          ],
        },
      ],
    },
    {
      type: 'category',
      label: 'Appendices',
      items: [
        'appendices/hardware',
        'appendices/software-setup',
        'appendices/troubleshooting',
        'appendices/resources',
      ],
    },
  ],
};

export default sidebars;
