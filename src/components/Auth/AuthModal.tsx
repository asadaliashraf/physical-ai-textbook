import React, { useState } from 'react';
import styles from './AuthModal.module.css';

const API_BASE = process.env.NODE_ENV === 'production'
  ? 'https://physical-ai-backend.vercel.app'
  : 'http://localhost:8000';

interface AuthModalProps {
  onClose: () => void;
  onSuccess: (user: any) => void;
}

export default function AuthModal({ onClose, onSuccess }: AuthModalProps) {
  const [mode, setMode] = useState<'login' | 'register'>('login');
  const [step, setStep] = useState(1); // 1: credentials, 2: background (register only)
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const [formData, setFormData] = useState({
    email: '',
    name: '',
    password: '',
    confirmPassword: '',
    background: {
      programming_experience: 'beginner',
      robotics_experience: 'none',
      hardware_access: 'none',
      learning_goal: 'overview',
      preferred_language: 'english',
    }
  });

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const { name, value } = e.target;
    if (name.startsWith('bg_')) {
      const bgKey = name.replace('bg_', '');
      setFormData(prev => ({
        ...prev,
        background: { ...prev.background, [bgKey]: value }
      }));
    } else {
      setFormData(prev => ({ ...prev, [name]: value }));
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');

    if (mode === 'register' && step === 1) {
      if (formData.password !== formData.confirmPassword) {
        setError('Passwords do not match');
        return;
      }
      setStep(2);
      return;
    }

    setLoading(true);

    try {
      const endpoint = mode === 'login' ? '/auth/login' : '/auth/register';
      const body = mode === 'login'
        ? { email: formData.email, password: formData.password }
        : {
            email: formData.email,
            name: formData.name,
            password: formData.password,
            background: formData.background
          };

      const response = await fetch(`${API_BASE}${endpoint}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(body),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || 'Authentication failed');
      }

      localStorage.setItem('auth_token', data.access_token);
      localStorage.setItem('user', JSON.stringify(data.user));
      onSuccess(data.user);
      onClose();

    } catch (err: any) {
      setError(err.message || 'Something went wrong. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className={styles.overlay} onClick={onClose}>
      <div className={styles.modal} onClick={e => e.stopPropagation()}>
        {/* Header */}
        <div className={styles.header}>
          <div className={styles.logo}>🤖</div>
          <h2 className={styles.title}>
            {mode === 'login' ? 'Welcome Back!' : 'Join Physical AI'}
          </h2>
          <p className={styles.subtitle}>
            {mode === 'login'
              ? 'Sign in to access personalized content'
              : step === 1 ? 'Create your account' : 'Tell us about your background'}
          </p>
          <button className={styles.closeBtn} onClick={onClose}>✕</button>
        </div>

        {/* Step indicator for registration */}
        {mode === 'register' && (
          <div className={styles.steps}>
            <div className={`${styles.step} ${step >= 1 ? styles.stepActive : ''}`}>
              1. Account
            </div>
            <div className={styles.stepLine}></div>
            <div className={`${styles.step} ${step >= 2 ? styles.stepActive : ''}`}>
              2. Background
            </div>
          </div>
        )}

        <form className={styles.form} onSubmit={handleSubmit}>
          {/* Step 1: Credentials */}
          {(mode === 'login' || step === 1) && (
            <>
              {mode === 'register' && (
                <div className={styles.field}>
                  <label>Full Name</label>
                  <input
                    type="text"
                    name="name"
                    value={formData.name}
                    onChange={handleChange}
                    placeholder="Your name"
                    required
                  />
                </div>
              )}
              <div className={styles.field}>
                <label>Email Address</label>
                <input
                  type="email"
                  name="email"
                  value={formData.email}
                  onChange={handleChange}
                  placeholder="you@example.com"
                  required
                />
              </div>
              <div className={styles.field}>
                <label>Password</label>
                <input
                  type="password"
                  name="password"
                  value={formData.password}
                  onChange={handleChange}
                  placeholder="••••••••"
                  required
                  minLength={6}
                />
              </div>
              {mode === 'register' && (
                <div className={styles.field}>
                  <label>Confirm Password</label>
                  <input
                    type="password"
                    name="confirmPassword"
                    value={formData.confirmPassword}
                    onChange={handleChange}
                    placeholder="••••••••"
                    required
                  />
                </div>
              )}
            </>
          )}

          {/* Step 2: Background (registration only) */}
          {mode === 'register' && step === 2 && (
            <>
              <div className={styles.backgroundInfo}>
                <span>ℹ️</span>
                <p>We'll use this to personalize content for your level</p>
              </div>

              <div className={styles.field}>
                <label>Programming Experience</label>
                <select name="bg_programming_experience" onChange={handleChange}
                        value={formData.background.programming_experience}>
                  <option value="none">None / Complete beginner</option>
                  <option value="beginner">Beginner (basic Python)</option>
                  <option value="intermediate">Intermediate (classes, modules)</option>
                  <option value="advanced">Advanced (professional developer)</option>
                </select>
              </div>

              <div className={styles.field}>
                <label>Robotics Experience</label>
                <select name="bg_robotics_experience" onChange={handleChange}
                        value={formData.background.robotics_experience}>
                  <option value="none">No experience</option>
                  <option value="hobbyist">Hobbyist (Arduino, Raspberry Pi)</option>
                  <option value="student">Student (some ROS experience)</option>
                  <option value="professional">Professional roboticist</option>
                </select>
              </div>

              <div className={styles.field}>
                <label>Hardware Access</label>
                <select name="bg_hardware_access" onChange={handleChange}
                        value={formData.background.hardware_access}>
                  <option value="none">No hardware (simulation only)</option>
                  <option value="basic">Basic PC / Laptop</option>
                  <option value="jetson">NVIDIA Jetson kit</option>
                  <option value="full_lab">Full robotics lab access</option>
                </select>
              </div>

              <div className={styles.field}>
                <label>Learning Goal</label>
                <select name="bg_learning_goal" onChange={handleChange}
                        value={formData.background.learning_goal}>
                  <option value="overview">General overview of Physical AI</option>
                  <option value="deep_dive">Deep technical understanding</option>
                  <option value="project_based">Build practical projects</option>
                </select>
              </div>

              <div className={styles.field}>
                <label>Preferred Language</label>
                <select name="bg_preferred_language" onChange={handleChange}
                        value={formData.background.preferred_language}>
                  <option value="english">English</option>
                  <option value="urdu">اردو (Urdu)</option>
                  <option value="both">Both English and Urdu</option>
                </select>
              </div>
            </>
          )}

          {/* Error message */}
          {error && <div className={styles.error}>⚠️ {error}</div>}

          {/* Submit button */}
          <button type="submit" className={styles.submitBtn} disabled={loading}>
            {loading ? (
              <span className={styles.btnSpinner}></span>
            ) : mode === 'login' ? 'Sign In' :
              step === 1 ? 'Continue →' : '🚀 Create Account'}
          </button>

          {/* Back button for step 2 */}
          {mode === 'register' && step === 2 && (
            <button
              type="button"
              className={styles.backBtn}
              onClick={() => setStep(1)}
            >
              ← Back
            </button>
          )}
        </form>

        {/* Toggle between login/register */}
        <div className={styles.toggle}>
          {mode === 'login' ? (
            <>
              Don't have an account?{' '}
              <button onClick={() => { setMode('register'); setStep(1); setError(''); }}>
                Sign up free
              </button>
            </>
          ) : (
            <>
              Already have an account?{' '}
              <button onClick={() => { setMode('login'); setStep(1); setError(''); }}>
                Sign in
              </button>
            </>
          )}
        </div>
      </div>
    </div>
  );
}
