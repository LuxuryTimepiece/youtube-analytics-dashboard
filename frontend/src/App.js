import React, { useState } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [videoId, setVideoId] = useState('');
  const [result, setResult] = useState(null);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleAnalyze = async () => {
    if (!videoId.trim()) {
      setError('Please enter a valid YouTube video ID');
      return;
    }
    
    setLoading(true);
    setError('');
    setResult(null);
    
    try {
      const response = await axios.get(`http://localhost:5000/analyze/${videoId}`);
      if (response.data.error) {
        setError(response.data.error);
      } else {
        setResult(response.data);
      }
    } catch (err) {
      setError('Failed to connect to the backend—check if it’s running!');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="App">
      <h1>YouTube Analytics Dashboard</h1>
      <div className="input-section">
        <input
          type="text"
          value={videoId}
          onChange={(e) => setVideoId(e.target.value)}
          placeholder="Enter YouTube Video ID (e.g., dQw4w9WgXcQ)"
          disabled={loading}
        />
        <button onClick={handleAnalyze} disabled={loading}>
          {loading ? 'Analyzing...' : 'Analyze'}
        </button>
      </div>
      {error && <p className="error">{error}</p>}
      {result && !result.error && (
        <div className="results">
          <p><strong>Transcript:</strong> {result.transcript}</p>
          <p><strong>Sentiment:</strong> {result.sentiment}</p>
          <p><strong>Top Keywords:</strong> {result.keywords.join(', ')}</p>
        </div>
      )}
    </div>
  );
}

export default App;