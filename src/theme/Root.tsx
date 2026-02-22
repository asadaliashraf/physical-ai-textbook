import React, { useState, useEffect } from 'react';
import { useLocation } from '@docusaurus/router';
import dynamic from '@docusaurus/router';
import ChatWidget from '../components/ChatBot/ChatWidget';
import AuthModal from '../components/Auth/AuthModal';

// Helper to get chapter ID from path
function getChapterId(pathname: string): string | undefined {
  const match = pathname.match(/\/docs\/(.+)/);
  return match ? match[1] : undefined;
}

// Navbar Auth Button (injected globally)
function NavbarAuth() {
  const [user, setUser] = useState<any>(null);
  const [showModal, setShowModal] = useState(false);

  useEffect(() => {
    const stored = localStorage.getItem('user');
    if (stored) {
      setUser(JSON.parse(stored));
    }
  }, []);

  const handleLogout = () => {
    localStorage.removeItem('auth_token');
    localStorage.removeItem('user');
    setUser(null);
    window.location.reload();
  };

  const handleSuccess = (userData: any) => {
    setUser(userData);
  };

  if (user) {
    return (
      <div style={{
        display: 'flex',
        alignItems: 'center',
        gap: '0.5rem',
        fontSize: '0.875rem',
        color: '#4b5563',
      }}>
        <span style={{
          width: '30px', height: '30px',
          borderRadius: '50%',
          background: 'linear-gradient(135deg, #2563eb, #7c3aed)',
          color: 'white',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          fontWeight: '700',
          fontSize: '0.8rem',
        }}>
          {user.name?.charAt(0)?.toUpperCase() || '?'}
        </span>
        <span style={{ fontWeight: '600' }}>{user.name?.split(' ')[0]}</span>
        <button
          onClick={handleLogout}
          style={{
            background: 'none',
            border: '1px solid #e5e7eb',
            borderRadius: '0.4rem',
            padding: '0.2rem 0.6rem',
            cursor: 'pointer',
            fontSize: '0.8rem',
            color: '#6b7280',
          }}
        >
          Sign Out
        </button>
      </div>
    );
  }

  return (
    <>
      <button
        onClick={() => setShowModal(true)}
        style={{
          padding: '0.4rem 1rem',
          background: 'linear-gradient(135deg, #2563eb, #7c3aed)',
          color: 'white',
          border: 'none',
          borderRadius: '0.4rem',
          cursor: 'pointer',
          fontWeight: '600',
          fontSize: '0.875rem',
          fontFamily: 'inherit',
        }}
      >
        Sign In
      </button>
      {showModal && (
        <AuthModal
          onClose={() => setShowModal(false)}
          onSuccess={handleSuccess}
        />
      )}
    </>
  );
}

export default function Root({ children }: { children: React.ReactNode }) {
  const location = useLocation();
  const chapterId = getChapterId(location.pathname);
  const isDocPage = location.pathname.startsWith('/docs');

  return (
    <>
      {children}

      {/* Global ChatBot */}
      <ChatWidget chapterId={chapterId} />

      {/* Inject Auth button into navbar */}
      <NavbarAuthPortal />
    </>
  );
}

// Portal to inject auth into navbar
function NavbarAuthPortal() {
  const [mounted, setMounted] = useState(false);
  const [container, setContainer] = useState<Element | null>(null);

  useEffect(() => {
    setMounted(true);
    // Find navbar items container
    const navbarItems = document.querySelector('.navbar__items--right');
    if (navbarItems) {
      const div = document.createElement('div');
      div.style.display = 'flex';
      div.style.alignItems = 'center';
      navbarItems.prepend(div);
      setContainer(div);
    }
  }, []);

  if (!mounted || !container) return null;

  const ReactDOM = require('react-dom');
  return ReactDOM.createPortal(<NavbarAuth />, container);
}
