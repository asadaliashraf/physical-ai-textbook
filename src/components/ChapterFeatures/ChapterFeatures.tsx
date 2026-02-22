import React, { useState } from 'react';
import styles from './ChapterFeatures.module.css';

const API_BASE = process.env.NODE_ENV === 'production'
  ? 'https://physical-ai-backend-mocha.vercel.app'
  : 'http://localhost:8000';

interface ChapterFeaturesProps {
  chapterId: string;
  chapterContent?: string;
}

export default function ChapterFeatures({ chapterId, chapterContent = '' }: ChapterFeaturesProps) {
  const [isTranslated, setIsTranslated] = useState(false);
  const [translatedContent, setTranslatedContent] = useState('');
  const [isPersonalized, setIsPersonalized] = useState(false);
  const [personalizedContent, setPersonalizedContent] = useState('');
  const [loadingTranslation, setLoadingTranslation] = useState(false);
  const [loadingPersonalization, setLoadingPersonalization] = useState(false);
  const [error, setError] = useState('');

  const handleTranslate = async () => {
    if (isTranslated) {
      setIsTranslated(false);
      return;
    }

    if (translatedContent) {
      setIsTranslated(true);
      return;
    }

    setLoadingTranslation(true);
    setError('');

    try {
      const response = await fetch(`${API_BASE}/api/translate`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          chapter_id: chapterId,
          content: chapterContent || getPageContent(),
        }),
      });

      const data = await response.json();
      setTranslatedContent(data.translated);
      setIsTranslated(true);
    } catch (e) {
      setError('Translation requires the backend to be running. Please set up the backend first.');
    } finally {
      setLoadingTranslation(false);
    }
  };

  const handlePersonalize = async () => {
    if (isPersonalized) {
      setIsPersonalized(false);
      return;
    }

    if (personalizedContent) {
      setIsPersonalized(true);
      return;
    }

    const token = localStorage.getItem('auth_token');
    if (!token) {
      setError('Please sign in to personalize content based on your background.');
      return;
    }

    setLoadingPersonalization(true);
    setError('');

    try {
      const response = await fetch(`${API_BASE}/api/personalize`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`,
        },
        body: JSON.stringify({
          chapter_id: chapterId,
          content: chapterContent || getPageContent(),
        }),
      });

      if (!response.ok) {
        if (response.status === 401) {
          setError('Please sign in to personalize content.');
          return;
        }
        throw new Error('Personalization failed');
      }

      const data = await response.json();
      setPersonalizedContent(data.personalized);
      setIsPersonalized(true);
    } catch (e) {
      setError('Personalization requires the backend and authentication to be set up.');
    } finally {
      setLoadingPersonalization(false);
    }
  };

  const getPageContent = () => {
    // Fallback: get content from page
    const mainContent = document.querySelector('.markdown');
    return mainContent?.textContent?.slice(0, 3000) || '';
  };

  return (
    <div className={styles.container}>
      {/* Feature Buttons */}
      <div className={styles.buttonRow}>
        {/* Urdu Translation Button */}
        <button
          className={`${styles.featureBtn} ${isTranslated ? styles.active : ''}`}
          onClick={handleTranslate}
          disabled={loadingTranslation}
          title="Translate this chapter to Urdu"
        >
          {loadingTranslation ? (
            <span className={styles.spinner}></span>
          ) : (
            <>
              <span className={styles.btnIcon}>{isTranslated ? '🔤' : 'اردو'}</span>
              <span>{isTranslated ? 'Show English' : 'اردو میں پڑھیں'}</span>
            </>
          )}
        </button>

        {/* Personalization Button */}
        <button
          className={`${styles.featureBtn} ${isPersonalized ? styles.activeGreen : ''}`}
          onClick={handlePersonalize}
          disabled={loadingPersonalization}
          title="Personalize content based on your background"
        >
          {loadingPersonalization ? (
            <span className={styles.spinner}></span>
          ) : (
            <>
              <span className={styles.btnIcon}>{isPersonalized ? '✅' : '🎨'}</span>
              <span>{isPersonalized ? 'Original Version' : 'Personalize for Me'}</span>
            </>
          )}
        </button>
      </div>

      {/* Error Message */}
      {error && (
        <div className={styles.errorBanner}>
          ⚠️ {error}
          <button onClick={() => setError('')} className={styles.dismissBtn}>✕</button>
        </div>
      )}

      {/* Translated Content Display */}
      {isTranslated && translatedContent && (
        <div className={styles.translatedContent} dir="rtl">
          <div className={styles.contentHeader}>
            <span>🌐 اردو ترجمہ</span>
            <span className={styles.badge}>Powered by Gemini AI</span>
          </div>
          <div
            className={styles.translatedText}
            dangerouslySetInnerHTML={{ __html: translatedContent.replace(/\n/g, '<br>') }}
          />
        </div>
      )}

      {/* Personalized Content Display */}
      {isPersonalized && personalizedContent && (
        <div className={styles.personalizedContent}>
          <div className={styles.contentHeader}>
            <span>🎨 Personalized for You</span>
            <span className={styles.badge}>Based on your background</span>
          </div>
          <div
            className={styles.personalizedText}
            dangerouslySetInnerHTML={{ __html: personalizedContent.replace(/\n/g, '<br>') }}
          />
        </div>
      )}
    </div>
  );
}
