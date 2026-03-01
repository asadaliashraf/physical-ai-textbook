import React, { useState, useEffect, useCallback, useRef } from 'react';
import { useLocation } from '@docusaurus/router';
import ChatWidget from '../components/ChatBot/ChatWidget';
import AuthModal from '../components/Auth/AuthModal';

// Helper to get chapter ID from path
function getChapterId(pathname: string): string | undefined {
  const match = pathname.match(/\/docs\/(.+)/);
  return match ? match[1] : undefined;
}

// Navbar Auth Button (injected globally via portal)
function NavbarAuth({ onOpenModal }: { onOpenModal: () => void }) {
  const [user, setUser] = useState<any>(null);

  useEffect(() => {
    const stored = localStorage.getItem('user');
    if (stored) {
      try { setUser(JSON.parse(stored)); } catch {}
    }
  }, []);

  useEffect(() => {
    const handler = () => {
      const stored = localStorage.getItem('user');
      if (stored) {
        try { setUser(JSON.parse(stored)); } catch {}
      } else {
        setUser(null);
      }
    };
    window.addEventListener('auth-changed', handler);
    return () => window.removeEventListener('auth-changed', handler);
  }, []);

  const handleLogout = () => {
    localStorage.removeItem('auth_token');
    localStorage.removeItem('user');
    setUser(null);
    window.dispatchEvent(new Event('auth-changed'));
  };

  if (user) {
    return (
      <div style={{
        display: 'flex',
        alignItems: 'center',
        gap: '0.5rem',
        fontSize: '0.875rem',
        color: '#4b5563',
        marginRight: '0.5rem',
      }}>
        <span style={{
          width: '32px', height: '32px',
          borderRadius: '50%',
          background: 'linear-gradient(135deg, #2563eb, #7c3aed)',
          color: 'white',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          fontWeight: '700',
          fontSize: '0.85rem',
        }}>
          {user.name?.charAt(0)?.toUpperCase() || '?'}
        </span>
        <span style={{ fontWeight: '600', maxWidth: '100px', overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>
          {user.name?.split(' ')[0]}
        </span>
        <button
          onClick={handleLogout}
          style={{
            background: 'none',
            border: '1px solid #d1d5db',
            borderRadius: '0.4rem',
            padding: '0.25rem 0.6rem',
            cursor: 'pointer',
            fontSize: '0.8rem',
            color: '#6b7280',
            fontFamily: 'inherit',
          }}
        >
          Sign Out
        </button>
      </div>
    );
  }

  return (
    <button
      onClick={onOpenModal}
      style={{
        padding: '0.4rem 1.2rem',
        background: 'linear-gradient(135deg, #2563eb, #7c3aed)',
        color: 'white',
        border: 'none',
        borderRadius: '0.5rem',
        cursor: 'pointer',
        fontWeight: '600',
        fontSize: '0.875rem',
        fontFamily: 'inherit',
        marginRight: '0.5rem',
        whiteSpace: 'nowrap',
      }}
    >
      Sign In
    </button>
  );
}

// Portal to inject auth into navbar
function NavbarAuthPortal({ onOpenModal }: { onOpenModal: () => void }) {
  const [container, setContainer] = useState<HTMLElement | null>(null);
  const location = useLocation();
  const injectedRef = useRef(false);

  useEffect(() => {
    const PORTAL_ID = 'navbar-auth-portal';
    injectedRef.current = false;

    const inject = () => {
      if (injectedRef.current) return;
      const existing = document.getElementById(PORTAL_ID);
      if (existing) {
        setContainer(existing);
        injectedRef.current = true;
        return;
      }
      const navRight = document.querySelector('.navbar__items--right');
      if (navRight) {
        const div = document.createElement('div');
        div.id = PORTAL_ID;
        div.style.display = 'flex';
        div.style.alignItems = 'center';
        navRight.prepend(div);
        setContainer(div);
        injectedRef.current = true;
      }
    };

    // Try immediately
    inject();

    // Retry with interval for SSR hydration timing
    if (!injectedRef.current) {
      const interval = setInterval(() => {
        inject();
        if (injectedRef.current) clearInterval(interval);
      }, 500);
      return () => clearInterval(interval);
    }
  }, [location.pathname]);

  // Re-inject if navbar gets re-rendered (Docusaurus client-side nav)
  useEffect(() => {
    const PORTAL_ID = 'navbar-auth-portal';
    const observer = new MutationObserver((mutations) => {
      // Only act if our portal was actually removed
      if (!document.getElementById(PORTAL_ID)) {
        injectedRef.current = false;
        const navRight = document.querySelector('.navbar__items--right');
        if (navRight) {
          const div = document.createElement('div');
          div.id = PORTAL_ID;
          div.style.display = 'flex';
          div.style.alignItems = 'center';
          navRight.prepend(div);
          setContainer(div);
          injectedRef.current = true;
        }
      }
    });
    // Only observe the navbar, not the entire body
    const navbar = document.querySelector('.navbar');
    if (navbar) {
      observer.observe(navbar, { childList: true, subtree: true });
    }
    return () => observer.disconnect();
  }, []);

  if (!container) return null;

  const ReactDOM = require('react-dom');
  return ReactDOM.createPortal(<NavbarAuth onOpenModal={onOpenModal} />, container);
}

// Floating "Explain" button on text selection
function SelectionExplainButton({ chatWidgetRef }: { chatWidgetRef: React.RefObject<any> }) {
  const [show, setShow] = useState(false);
  const [position, setPosition] = useState({ top: 0, left: 0 });
  const [text, setText] = useState('');

  useEffect(() => {
    const handleSelection = () => {
      const selection = window.getSelection();
      const selectedText = selection?.toString().trim();

      if (selectedText && selectedText.length > 10) {
        const range = selection!.getRangeAt(0);
        const rect = range.getBoundingClientRect();
        setText(selectedText);
        setPosition({
          top: rect.top + window.scrollY - 45,
          left: rect.left + window.scrollX + (rect.width / 2),
        });
        setShow(true);
      } else {
        setShow(false);
      }
    };

    const handleMouseDown = (e: MouseEvent) => {
      const target = e.target as HTMLElement;
      if (target.closest('#explain-btn')) return;
      setTimeout(() => {
        const sel = window.getSelection()?.toString().trim();
        if (!sel || sel.length < 10) {
          setShow(false);
        }
      }, 200);
    };

    document.addEventListener('mouseup', handleSelection);
    document.addEventListener('mousedown', handleMouseDown);
    return () => {
      document.removeEventListener('mouseup', handleSelection);
      document.removeEventListener('mousedown', handleMouseDown);
    };
  }, []);

  if (!show) return null;

  return (
    <button
      id="explain-btn"
      onClick={() => {
        if (chatWidgetRef.current) {
          chatWidgetRef.current.openWithQuery('Explain this in simple terms:', text);
        }
        setShow(false);
        window.getSelection()?.removeAllRanges();
      }}
      style={{
        position: 'absolute',
        top: `${position.top}px`,
        left: `${position.left}px`,
        transform: 'translateX(-50%)',
        zIndex: 9999,
        background: 'linear-gradient(135deg, #2563eb, #7c3aed)',
        color: 'white',
        border: 'none',
        borderRadius: '2rem',
        padding: '0.4rem 1rem',
        fontSize: '0.85rem',
        fontWeight: '600',
        cursor: 'pointer',
        boxShadow: '0 4px 15px rgba(37, 99, 235, 0.4)',
        display: 'flex',
        alignItems: 'center',
        gap: '0.35rem',
        fontFamily: 'inherit',
        whiteSpace: 'nowrap',
        animation: 'fadeInUp 0.2s ease-out',
      }}
    >
      💡 Explain This
    </button>
  );
}

export default function Root({ children }: { children: React.ReactNode }) {
  const location = useLocation();
  const chapterId = getChapterId(location.pathname);
  const [showAuthModal, setShowAuthModal] = useState(false);
  const chatWidgetRef = useRef<any>(null);

  const handleAuthSuccess = useCallback((userData: any) => {
    window.dispatchEvent(new Event('auth-changed'));
    setShowAuthModal(false);
  }, []);

  return (
    <>
      {children}

      {/* Selection Explain Button */}
      <SelectionExplainButton chatWidgetRef={chatWidgetRef} />

      {/* Global ChatBot */}
      <ChatWidget chapterId={chapterId} ref={chatWidgetRef} />

      {/* Inject Auth button into navbar */}
      <NavbarAuthPortal onOpenModal={() => setShowAuthModal(true)} />

      {/* Auth Modal */}
      {showAuthModal && (
        <AuthModal
          onClose={() => setShowAuthModal(false)}
          onSuccess={handleAuthSuccess}
        />
      )}

      {/* Global animation styles */}
      <style>{`
        @keyframes fadeInUp {
          from { opacity: 0; transform: translate(-50%, 8px); }
          to { opacity: 1; transform: translate(-50%, 0); }
        }
      `}</style>
    </>
  );
}
