import React, { useState, useRef, useEffect, useCallback } from 'react';
import styles from './ChatWidget.module.css';

const API_BASE = process.env.NODE_ENV === 'production'
  ? 'https://physical-ai-backend-mocha.vercel.app'
  : 'http://localhost:8000';

interface Message {
  role: 'user' | 'assistant';
  content: string;
  timestamp: Date;
}

interface ChatWidgetProps {
  chapterId?: string;
}

export default function ChatWidget({ chapterId }: ChatWidgetProps) {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState<Message[]>([
    {
      role: 'assistant',
      content: '👋 Hello! I\'m your AI tutor for this Physical AI & Humanoid Robotics textbook. Ask me anything about the content, or select text and ask me to explain it!',
      timestamp: new Date(),
    }
  ]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [selectedText, setSelectedText] = useState('');
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLTextAreaElement>(null);

  // Scroll to bottom on new messages
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  // Listen for text selection
  useEffect(() => {
    const handleSelection = () => {
      const selection = window.getSelection();
      const text = selection?.toString().trim();
      if (text && text.length > 20) {
        setSelectedText(text);
      }
    };

    document.addEventListener('mouseup', handleSelection);
    document.addEventListener('touchend', handleSelection);
    return () => {
      document.removeEventListener('mouseup', handleSelection);
      document.removeEventListener('touchend', handleSelection);
    };
  }, []);

  const sendMessage = useCallback(async () => {
    if (!input.trim() || isLoading) return;

    const userMessage: Message = {
      role: 'user',
      content: selectedText
        ? `About this text: "${selectedText.substring(0, 100)}..."\n\n${input}`
        : input,
      timestamp: new Date(),
    };

    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setSelectedText('');
    setIsLoading(true);

    // Add placeholder for streaming response
    const assistantMessage: Message = {
      role: 'assistant',
      content: '',
      timestamp: new Date(),
    };
    setMessages(prev => [...prev, assistantMessage]);

    try {
      const token = localStorage.getItem('auth_token');
      const endpoint = token ? '/api/chat/authenticated' : '/api/chat';

      const response = await fetch(`${API_BASE}${endpoint}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          ...(token ? { 'Authorization': `Bearer ${token}` } : {}),
        },
        body: JSON.stringify({
          query: input,
          chapter_id: chapterId,
          selected_text: selectedText || undefined,
          conversation_history: messages.slice(-6).map(m => ({
            role: m.role,
            content: m.content,
          })),
        }),
      });

      if (!response.ok) throw new Error('API request failed');

      // Stream the response
      const reader = response.body?.getReader();
      const decoder = new TextDecoder();
      let fullContent = '';

      while (reader) {
        const { done, value } = await reader.read();
        if (done) break;

        const text = decoder.decode(value);
        const lines = text.split('\n');

        for (const line of lines) {
          if (line.startsWith('data: ')) {
            const data = line.slice(6);
            if (data === '[DONE]') break;

            try {
              const parsed = JSON.parse(data);
              if (parsed.content) {
                fullContent += parsed.content;
                setMessages(prev => {
                  const newMessages = [...prev];
                  newMessages[newMessages.length - 1] = {
                    ...newMessages[newMessages.length - 1],
                    content: fullContent,
                  };
                  return newMessages;
                });
              }
            } catch {
              // Skip malformed JSON
            }
          }
        }
      }
    } catch (error) {
      setMessages(prev => {
        const newMessages = [...prev];
        newMessages[newMessages.length - 1] = {
          ...newMessages[newMessages.length - 1],
          content: '⚠️ Sorry, I encountered an error. Please make sure the backend is running and try again.',
        };
        return newMessages;
      });
    } finally {
      setIsLoading(false);
    }
  }, [input, selectedText, chapterId, messages, isLoading]);

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  return (
    <>
      {/* Floating Chat Button */}
      <button
        className={`${styles.chatButton} ${isOpen ? styles.chatButtonOpen : ''}`}
        onClick={() => setIsOpen(!isOpen)}
        title="Ask AI Tutor"
      >
        {isOpen ? '✕' : '🤖'}
        {!isOpen && <span className={styles.chatButtonLabel}>Ask AI</span>}
      </button>

      {/* Chat Window */}
      {isOpen && (
        <div className={styles.chatWindow}>
          {/* Header */}
          <div className={styles.chatHeader}>
            <div className={styles.chatHeaderInfo}>
              <span className={styles.chatHeaderIcon}>🤖</span>
              <div>
                <div className={styles.chatHeaderTitle}>AI Tutor</div>
                <div className={styles.chatHeaderSubtitle}>Physical AI Expert</div>
              </div>
            </div>
            <button
              className={styles.chatCloseBtn}
              onClick={() => setIsOpen(false)}
            >
              ✕
            </button>
          </div>

          {/* Selected Text Banner */}
          {selectedText && (
            <div className={styles.selectedTextBanner}>
              <span>📌 Selected: "{selectedText.substring(0, 80)}..."</span>
              <button onClick={() => setSelectedText('')}>✕</button>
            </div>
          )}

          {/* Messages */}
          <div className={styles.messages}>
            {messages.map((msg, i) => (
              <div
                key={i}
                className={`${styles.message} ${msg.role === 'user' ? styles.userMessage : styles.assistantMessage}`}
              >
                <div className={styles.messageAvatar}>
                  {msg.role === 'user' ? '👤' : '🤖'}
                </div>
                <div className={styles.messageContent}>
                  <div
                    className={styles.messageText}
                    dangerouslySetInnerHTML={{
                      __html: msg.content
                        .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
                        .replace(/\*(.*?)\*/g, '<em>$1</em>')
                        .replace(/`(.*?)`/g, '<code>$1</code>')
                        .replace(/\n/g, '<br>')
                    }}
                  />
                  {isLoading && i === messages.length - 1 && msg.role === 'assistant' && !msg.content && (
                    <div className={styles.typingIndicator}>
                      <span></span><span></span><span></span>
                    </div>
                  )}
                </div>
              </div>
            ))}
            <div ref={messagesEndRef} />
          </div>

          {/* Input Area */}
          <div className={styles.inputArea}>
            <textarea
              ref={inputRef}
              className={styles.input}
              value={input}
              onChange={e => setInput(e.target.value)}
              onKeyDown={handleKeyDown}
              placeholder={selectedText ? 'Ask about selected text...' : 'Ask about robotics, ROS 2, Isaac...'}
              rows={2}
              disabled={isLoading}
            />
            <button
              className={styles.sendBtn}
              onClick={sendMessage}
              disabled={!input.trim() || isLoading}
            >
              {isLoading ? '⏳' : '➤'}
            </button>
          </div>

          <div className={styles.chatFooter}>
            💡 Tip: Select text in the book to ask about it specifically
          </div>
        </div>
      )}
    </>
  );
}
