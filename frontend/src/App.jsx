import { useEffect, useMemo, useState } from 'react';

const starterPrompts = [
  'How do I enable S3 versioning?',
  'What is the difference between IAM roles and policies?',
  'How does Lambda work with triggers?',
];

function App() {
  const [messages, setMessages] = useState([
    {
      role: 'assistant',
      content: 'Hello! I can help you explore core AWS services and documentation. Ask me about S3, Lambda, IAM, VPC, DynamoDB, or Bedrock.',
    },
  ]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [streamingText, setStreamingText] = useState('');
  const [streamingIndex, setStreamingIndex] = useState(0);

  const apiBaseUrl = useMemo(() => import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000', []);

  async function handleSubmit(event) {
    event.preventDefault();
    const trimmedInput = input.trim();
    if (!trimmedInput || loading) return;

    setMessages((prev) => [...prev, { role: 'user', content: trimmedInput }]);
    setInput('');
    setLoading(true);
    setError('');
    setStreamingText('');
    setStreamingIndex(0);

    const historyForRequest = messages
      .slice(-6)
      .map((message) => ({ role: message.role, content: message.content }));

    try {
      const response = await fetch(`${apiBaseUrl}/chat`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: trimmedInput, history: historyForRequest }),
      });

      const data = await response.json();
      if (!response.ok) {
        throw new Error(data.detail || 'The request could not be completed.');
      }

      const fullResponse = data.response || 'I could not generate a response right now.';
      setStreamingText(fullResponse);
      setStreamingIndex(0);
    } catch (err) {
      setError(err.message || 'Unable to reach the local server.');
      setLoading(false);
      setStreamingText('');
      setStreamingIndex(0);
    }
  }

  useEffect(() => {
    if (!loading || !streamingText) return;

    if (streamingIndex < streamingText.length) {
      const timer = window.setTimeout(() => {
        setStreamingIndex((prev) => prev + 1);
      }, 18);
      return () => window.clearTimeout(timer);
    }

    if (streamingIndex >= streamingText.length) {
      setMessages((prev) => {
        const lastMessage = prev[prev.length - 1];
        if (lastMessage?.role === 'assistant') {
          return prev.slice(0, -1).concat({ role: 'assistant', content: streamingText });
        }
        return prev.concat({ role: 'assistant', content: streamingText });
      });
      setLoading(false);
      setStreamingText('');
      setStreamingIndex(0);
    }
  }, [loading, streamingIndex, streamingText]);

  function handlePromptClick(prompt) {
    setInput(prompt);
  }

  return (
    <div className="app-shell">
      <div className="chat-card">
        <header className="hero">
          <div>
            <p className="eyebrow">Local demo</p>
            <h1>AWS Docs Assistant</h1>
            <p className="subtitle">Ask practical questions about AWS services and get grounded answers from the bundled documentation.</p>
          </div>
        </header>

        <div className="prompt-row" aria-label="Suggested prompts">
          {starterPrompts.map((prompt) => (
            <button key={prompt} type="button" className="prompt-pill" onClick={() => handlePromptClick(prompt)}>
              {prompt}
            </button>
          ))}
        </div>

        <div className="messages" role="log" aria-live="polite">
          {messages.map((message, index) => (
            <div key={`${message.role}-${index}`} className={`message ${message.role}`}>
              <div className="message-label">{message.role === 'user' ? 'You' : 'Assistant'}</div>
              <p>{message.content}</p>
            </div>
          ))}
          {loading && (
            <div className="message assistant">
              <div className="message-label">Assistant</div>
              <p>{streamingText ? streamingText.slice(0, streamingIndex) : 'Thinking...'}</p>
            </div>
          )}
        </div>

        {error && <div className="error-banner">{error}</div>}

        <form onSubmit={handleSubmit} className="composer">
          <input
            value={input}
            onChange={(event) => setInput(event.target.value)}
            placeholder="Ask about S3, Lambda, IAM, VPC, or Bedrock..."
          />
          <button type="submit" disabled={loading}>
            {loading ? 'Sending...' : 'Send'}
          </button>
        </form>
      </div>
    </div>
  );
}

export default App;
