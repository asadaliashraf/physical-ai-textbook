import React, { useState, useRef, useEffect, useCallback, forwardRef, useImperativeHandle } from 'react';
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

export interface ChatWidgetHandle {
  openWithQuery: (query: string, selectedText: string) => void;
}

const ChatWidget = forwardRef<ChatWidgetHandle, ChatWidgetProps>(({ chapterId }, ref) => {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState<Message[]>([
    {
      role: 'assistant',
      content: '👋 Hello! I\'m your AI tutor for this Physical AI & Humanoid Robotics textbook. Ask me anything about the content, or select text and click "Explain This"!',
      timestamp: new Date(),
    }
  ]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [selectedText, setSelectedText] = useState('');
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLTextAreaElement>(null);
  const pendingSendRef = useRef(false);

  // Expose openWithQuery to parent via ref
  useImperativeHandle(ref, () => ({
    openWithQuery: (query: string, sel: string) => {
      setSelectedText(sel);
      setInput(query);
      setIsOpen(true);
      pendingSendRef.current = true;
    },
  }));

  // Auto-send when opened via Explain button
  useEffect(() => {
    if (pendingSendRef.current && isOpen && input && selectedText) {
      pendingSendRef.current = false;
      const q = input;
      const s = selectedText;
      setTimeout(() => {
        doSend(q, s);
      }, 300);
    }
  }, [isOpen, input, selectedText]);

  // Scroll to bottom on new messages
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const doSend = async (queryText: string, selText: string) => {
    if (!queryText.trim() || isLoading) return;

    const displayContent = selText
      ? `About this text: "${selText.substring(0, 100)}..."\n\n${queryText}`
      : queryText;

    const userMessage: Message = {
      role: 'user',
      content: displayContent,
      timestamp: new Date(),
    };

    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setSelectedText('');
    setIsLoading(true);

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
          query: queryText,
          chapter_id: chapterId,
          selected_text: selText || undefined,
          conversation_history: messages.slice(-6).map(m => ({
            role: m.role,
            content: m.content,
          })),
        }),
      });

      if (!response.ok) throw new Error('API request failed');

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
          content: '⚠️ Sorry, I encountered an error. Please try again.',
        };
        return newMessages;
      });
    } finally {
      setIsLoading(false);
    }
  };

  const sendMessage = useCallback(() => {
    doSend(input, selectedText);
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
            💡 Select text in the book, then click "Explain This"
          </div>
        </div>
      )}
    </>
  );
});

ChatWidget.displayName = 'ChatWidget';
export default ChatWidget;
