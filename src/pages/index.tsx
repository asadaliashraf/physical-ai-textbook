import React from 'react';
import clsx from 'clsx';
import Link from '@docusaurus/Link';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import Layout from '@theme/Layout';
import styles from './index.module.css';

function HomepageHeader() {
  const {siteConfig} = useDocusaurusContext();
  return (
    <header className={clsx('hero hero--primary', styles.heroBanner)}>
      <div className="container">
        <h1 className="hero__title">{siteConfig.title}</h1>
        <p className="hero__subtitle">{siteConfig.tagline}</p>
        <p className={styles.heroDescription}>
          Learn to bridge the gap between digital intelligence and physical embodiment.
          Master ROS 2, Gazebo, NVIDIA Isaac, and Vision-Language-Action systems to build
          the next generation of humanoid robots.
        </p>
        <div className={styles.buttons}>
          <Link
            className="button button--primary button--lg"
            to="/docs/intro">
            Start Learning 📚
          </Link>
          <Link
            className="button button--secondary button--lg"
            to="/docs/intro"
            style={{marginLeft: '1rem'}}>
            View Curriculum →
          </Link>
        </div>
      </div>
    </header>
  );
}

function FeatureCard({title, description, icon}: {title: string; description: string; icon: string}) {
  return (
    <div className={clsx('col col--3')}>
      <div className="card" style={{height: '100%', textAlign: 'center'}}>
        <div className="card__header">
          <div style={{fontSize: '3rem', marginBottom: '1rem'}}>{icon}</div>
          <h3>{title}</h3>
        </div>
        <div className="card__body">
          <p>{description}</p>
        </div>
      </div>
    </div>
  );
}

function Features() {
  return (
    <section className={styles.features}>
      <div className="container">
        <h2 className={styles.sectionTitle}>What You'll Learn</h2>
        <div className="row" style={{marginBottom: '3rem'}}>
          <FeatureCard
            icon="🤖"
            title="ROS 2 Mastery"
            description="Build the robotic nervous system with nodes, topics, and services for humanoid control."
          />
          <FeatureCard
            icon="🌐"
            title="Digital Twins"
            description="Create photorealistic simulations with Gazebo and Unity for safe robot testing."
          />
          <FeatureCard
            icon="🧠"
            title="NVIDIA Isaac"
            description="Leverage AI-powered perception, navigation, and sim-to-real transfer."
          />
          <FeatureCard
            icon="👁️"
            title="Vision-Language-Action"
            description="Integrate LLMs for natural language control and cognitive planning."
          />
        </div>

        <h2 className={styles.sectionTitle}>Course Structure</h2>
        <div className="row">
          <div className="col col--6">
            <div className="card" style={{marginBottom: '1.5rem'}}>
              <div className="card__header">
                <h3>📖 4 Comprehensive Modules</h3>
              </div>
              <div className="card__body">
                <ul>
                  <li><strong>Module 1:</strong> The Robotic Nervous System (ROS 2)</li>
                  <li><strong>Module 2:</strong> The Digital Twin (Gazebo & Unity)</li>
                  <li><strong>Module 3:</strong> The AI-Robot Brain (NVIDIA Isaac™)</li>
                  <li><strong>Module 4:</strong> Vision-Language-Action (VLA)</li>
                </ul>
              </div>
            </div>
          </div>
          <div className="col col--6">
            <div className="card" style={{marginBottom: '1.5rem'}}>
              <div className="card__header">
                <h3>⏱️ 13 Weeks of Learning</h3>
              </div>
              <div className="card__body">
                <ul>
                  <li>Week 1-3: ROS 2 Fundamentals & Advanced Topics</li>
                  <li>Week 4-7: Simulation with Gazebo & Unity</li>
                  <li>Week 8-10: NVIDIA Isaac Platform</li>
                  <li>Week 11-13: VLA & Capstone Project</li>
                </ul>
              </div>
            </div>
          </div>
        </div>

        <div className="row" style={{marginTop: '3rem'}}>
          <div className="col col--12">
            <div className={styles.highlightBox}>
              <h2 style={{marginBottom: '1rem'}}>🎯 Capstone Project: Autonomous Humanoid</h2>
              <p style={{fontSize: '1.1rem', marginBottom: '0'}}>
                Build a simulated humanoid robot that receives voice commands, plans paths,
                navigates obstacles, identifies objects using computer vision, and manipulates
                them—all while understanding natural language instructions.
              </p>
            </div>
          </div>
        </div>

        <div className="row" style={{marginTop: '3rem', textAlign: 'center'}}>
          <div className="col col--12">
            <h2 className={styles.sectionTitle}>Why Physical AI Matters</h2>
            <p style={{fontSize: '1.1rem', maxWidth: '800px', margin: '0 auto 2rem', color: '#4b5563'}}>
              Humanoid robots are poised to excel in our human-centered world because they share
              our physical form and can be trained with abundant data from interacting in human
              environments. This represents a significant transition from AI models confined to
              digital environments to embodied intelligence that operates in physical space.
            </p>
            <Link
              className="button button--primary button--lg"
              to="/docs/intro">
              Begin Your Journey →
            </Link>
          </div>
        </div>
      </div>
    </section>
  );
}

export default function Home(): JSX.Element {
  const {siteConfig} = useDocusaurusContext();
  return (
    <Layout
      title={`Welcome`}
      description="Master Physical AI and Humanoid Robotics - A comprehensive course on embodied intelligence">
      <HomepageHeader />
      <main>
        <Features />
      </main>
    </Layout>
  );
}
